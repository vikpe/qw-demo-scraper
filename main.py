import os
import shutil
import subprocess

from botocore.exceptions import ClientError
from dotenv import load_dotenv
from postgrest.exceptions import APIError

from demo_updater.pkg import analyze, mvdparser, net, title, qmode, demo_calc
from demo_updater.pkg.checksum import get_sha256_per_filename
from demo_updater.services import aws, hub, supab


def clear_demo_dir():
    shutil.rmtree("demos")
    os.mkdir("demos")


def update_demos(mode: str, keep_count: int):
    add_missing_demos(mode, keep_count)
    prune_demos(mode, keep_count)


def get_missing_demos(mode: str, keep_count: int) -> list[hub.Demo]:
    # from database
    db_demos = supab.get_demos_by_mode(mode)
    ignored_filenames = supab.get_ignored_filenames_by_mode(mode)

    # from server
    server_demos = [
        demo
        for demo in hub.get_demos(mode, keep_count)
        if demo.filename not in ignored_filenames
    ]

    return demo_calc.calc_missing_demos(db_demos, server_demos, keep_count)


def add_missing_demos(demo_mode: str, keep_count: int):
    clear_demo_dir()

    # download missing
    demos = get_missing_demos(demo_mode, keep_count)

    if not demos:
        print(f"\nadd missing {demo_mode}: no demos found")
        return

    print(f"\nadd missing {demo_mode}: found {len(demos)} demos")
    net.download_files_to_dir_in_parallel(
        [demo.download_url for demo in demos],
        "demos",
    )

    # checksums, parse, compress
    subprocess.run(["bash", "process_demos.sh"])
    checksums = get_sha256_per_filename("demos/demos.sha256")

    # upload to s3, add to database
    for demo in demos:
        # skip demo?
        sha256 = checksums[demo.filename]
        if supab.has_demo_by_sha256(sha256):
            print(f"{demo.qtv_address} / {demo.filename} - skip (already exists)")
            continue

        info = mvdparser.MvdInfo.from_file(f"demos/{demo.filename}.json")
        if 0 == info.duration:
            print(f"{demo.qtv_address} / {demo.filename} - skip (game in progress)")
            continue

        # persistently ignore demo?
        reason_to_ignore = analyze.reason_to_ignore_demo(info)

        if reason_to_ignore is not None:
            print(f"{demo.qtv_address} / {demo.filename} - ignore ({reason_to_ignore})")
            ignored_demo = supab.NewIgnoredDemo(
                sha256=sha256,
                mode=demo.get_mode(),
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
        mode = demo.get_mode()
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


def prune_demos(mode: str, keep_count: int):
    current_count = supab.get_demo_count_by_mode(mode)

    if current_count <= keep_count:
        print(f"\nprune {mode} ({current_count}/{keep_count}): nothing to prune")
        return

    print(
        f"\nprune {mode} ({current_count}/{keep_count}): remove {current_count - keep_count} demos "
    )

    for demo in supab.get_demos_to_prune(mode, keep_count):
        print(f"deleting {demo.s3_key} with id {demo.id} from {demo.timestamp}")
        delete_demo(demo.id, demo.s3_key)


def delete_demo(demo_id: int, demo_s3_key: str):
    # 1. delete from s3
    try:
        aws.delete(demo_s3_key)
    except ClientError as e:
        print(e)
        return

    # 2. delete from database (if s3 deletion is successful)
    supab.delete_demo(demo_id)


def main():
    load_dotenv()

    update_demos("1on1", 250)
    update_demos("4on4", 150)
    update_demos("2on2", 50)


if __name__ == "__main__":
    main()
