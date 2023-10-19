import os
import shutil
import subprocess
import time
from typing import List

import attr
import schedule
from botocore.exceptions import ClientError
import colorama
from colorama import Fore
from postgrest.exceptions import APIError

from demo_scraper.pkg import analyze, mvdparser, net, title, qmode
from demo_scraper.pkg import demo_calc
from demo_scraper.pkg.checksum import get_sha256_per_filename
from demo_scraper.services import aws, supab
from demo_scraper.services import hub

colorama.init(autoreset=True)


def delete_demos(demos: List[supab.Demo]):
    if not demos:
        return

    deleted_demo_ids = []

    # 1. delete from s3
    for demo in demos:
        try:
            aws.delete(demo.s3_key)
            deleted_demo_ids.append(demo.id)
        except ClientError as e:
            print(e)
            continue

    # 2. delete from database (for demos where s3 deletion was successful)
    if deleted_demo_ids:
        supab.delete_demos(deleted_demo_ids)


def prune_demos(mode: str, keep_count: int):
    current_count = supab.get_demo_count_by_mode(mode)

    if current_count <= keep_count:
        print(
            f"{Fore.LIGHTMAGENTA_EX}prune {mode} ({current_count}/{keep_count}): nothing to prune"
        )
        return

    print(
        f"{Fore.LIGHTMAGENTA_EX}prune {mode} ({current_count}/{keep_count}): remove {current_count - keep_count} demos "
    )

    demos = supab.get_demos_to_prune(mode, keep_count)
    delete_demos(demos)


def add_missing_demos(mode: str, keep_count: int):
    # download missing
    missing_demos = find_missing_demos(mode, keep_count)

    if not missing_demos:
        print(f"{Fore.LIGHTGREEN_EX}add missing {mode}: no demos found")
        return

    print(f"{Fore.LIGHTGREEN_EX}add missing {mode}: found {len(missing_demos)} demos")
    net.download_files_to_dir_in_parallel(
        [demo.download_url for demo in missing_demos],
        "demos",
    )

    # checksums, parse, compress
    subprocess.run(["bash", "process_demos.sh"])
    checksums = get_sha256_per_filename("demos/demos.sha256")

    # upload to s3, add to database
    for demo in missing_demos:
        # skip demo?
        sha256 = checksums[demo.filename]
        if supab.has_demo_by_sha256(sha256):
            print(
                f"{Fore.BLUE}{demo.qtv_address} / {demo.filename} - skip (already exists)"
            )
            continue

        info = mvdparser.MvdInfo.from_file(f"demos/{demo.filename}.json")
        if 0 == info.duration:
            print(
                f"{Fore.BLUE}{demo.qtv_address} / {demo.filename} - skip (game in progress)"
            )
            continue

        # persistently ignore demo?
        reason_to_ignore = analyze.reason_to_ignore_demo(info)

        if reason_to_ignore is not None:
            print(f"{demo.qtv_address} / {demo.filename} - ignore ({reason_to_ignore})")
            ignored_demo = supab.NewIgnoredDemo(
                sha256=sha256,
                mode=mode,
                filename=demo.filename,
                reason=reason_to_ignore,
            )
            supab.ignore_demo(ignored_demo)
            continue

        zip_filename = f"{demo.filename}.gz"
        s3_key = f"qw/demos/recent/{zip_filename}"

        # 1. upload to s3
        try:
            zip_path = f"demos/{zip_filename}"
            metadata = {
                "sha256": sha256,
                "qtv_address": demo.qtv_address,
                "filename": demo.filename,
            }
            aws.upload(zip_path, s3_key, metadata)
        except ClientError as e:
            print(e)
            continue

        # 2. add to database
        is_teamplay = info.serverinfo.teamplay in [1, 2] or qmode.is_teamplay(mode)

        db_demo = supab.NewDemo(
            sha256=sha256,
            source=demo.qtv_address,
            filename=demo.filename,
            s3_key=s3_key,
            timestamp=demo.time,
            duration=info.duration,
            mode=mode,
            map=info.map,
            matchtag=info.serverinfo.get("matchtag", ""),
            title=title.from_mode_and_players(mode, info.players),
            participants=supab.Participants(
                players=[] if is_teamplay else info.players,
                teams=mvdparser.Team.from_players(info.players) if is_teamplay else [],
                player_count=len(info.players),
            ),
        )

        try:
            supab.add_demo(db_demo)
        except APIError as e:
            print(e)
            continue


def find_missing_demos(mode: str, keep_count: int) -> list[hub.Demo]:
    # from database
    db_demos = supab.get_demos_by_mode(mode)
    ignored_filenames = supab.get_ignored_filenames_by_mode(mode)

    # from server
    server_demos = [
        demo
        for demo in hub.get_demos(mode, keep_count + len(ignored_filenames))
        if demo.filename not in ignored_filenames
    ]

    return demo_calc.calc_missing_demos(db_demos, server_demos, keep_count)


@attr.define
class ModeScraper:
    mode: str = attr.ib()
    keep_count: int = attr.ib()
    demo_dir: str = attr.ib(default="demos")

    def add_demos(self):
        self._clear_demo_dir()
        add_missing_demos(self.mode, self.keep_count)
        print()

    def prune_demos(self):
        prune_demos(self.mode, self.keep_count)
        print()

    def _clear_demo_dir(self):
        shutil.rmtree(self.demo_dir)
        os.mkdir(self.demo_dir)


@attr.define
class ModeSettings:
    name: str = attr.ib()
    keep_count: int = attr.ib()


class ScrapeApp:
    _scrapers: List[ModeScraper]

    def __init__(self, mode_settings: List[ModeSettings]):
        self._scrapers = [
            ModeScraper(mode.name, mode.keep_count) for mode in mode_settings
        ]

    def run_once(self):
        for scraper in self._scrapers:
            scraper.add_demos()
            scraper.prune_demos()

    def run_forever(self, add_interval: int, prune_interval: int):
        self.run_once()

        for scraper in self._scrapers:
            schedule.every(add_interval).minutes.do(scraper.add_demos)
            schedule.every(prune_interval).minutes.do(scraper.prune_demos)

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("exit..")
