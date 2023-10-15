import os
import shutil
import subprocess

from botocore.exceptions import ClientError
from dotenv import load_dotenv
from postgrest.exceptions import APIError
from postgrest.types import CountMethod

from vendor import analyze, hub, supab, aws, mvdparser, demo_calc
from vendor.util import download_file

load_dotenv()


def clear_demo_dir():
    shutil.rmtree("demos")
    os.mkdir("demos")


def get_missing_demos(mode: str, keep_count: int) -> list[hub.Demo]:
    # from database
    db_demos = supab.get_existing_demos(mode)
    ignored_filenames = supab.get_ignored_filenames()

    # from server
    server_demos = [
        demo
        for demo in hub.get_demos(mode, keep_count)
        if demo.filename not in ignored_filenames
    ]

    return demo_calc.calc_missing_demos(db_demos, server_demos, keep_count)


def get_sha256_per_filename(sha_filepath) -> dict[str, str]:
    with open(sha_filepath) as fh:
        lines = fh.readlines()

    result = {}

    for line in lines:
        sha256, filename = line.strip().split("  ")
        filename = filename.replace("demos/", "")
        result[filename] = sha256

    return result


def update_demos(mode: str, keep_count: int):
    add_missing_demos(mode, keep_count)
    prune_demos(mode, keep_count)


def add_missing_demos(demo_mode: str, keep_count: int):
    clear_demo_dir()

    # download missing
    demos = get_missing_demos(demo_mode, keep_count)

    if not demos:
        print(f"\nadd missing {demo_mode}: no demos found")
        return

    print(f"\nadd missing {demo_mode}: found {len(demos)} demos")

    for index, demo in enumerate(demos):
        print(f"({index+1}) downloading {demo.qtv_address} - {demo.filename}")
        download_file(demo.download_url, f"demos/{demo.filename}")

    # checksums, parse, compress
    subprocess.run(["bash", "process_demos.sh"])
    checksums = get_sha256_per_filename("demos/demos.sha256")

    # upload to s3, add to database
    sb = supab.get_client()

    for demo in demos:
        # skip demo?
        sha256 = checksums[demo.filename]
        if supab.has_demo_by_sha256(sha256):
            print(f"{demo.qtv_address} / {demo.filename} - skip (already exists)")
            continue

        info = mvdparser.from_file(f"demos/{demo.filename}.json")
        if 0 == info.duration:
            print(f"{demo.qtv_address} / {demo.filename} - skip (game in progress)")
            continue

        # persistently ignore demo?
        mode = demo.get_mode()
        reason_to_ignore = analyze.reason_to_ignore_demo(info, mode)

        if reason_to_ignore is not None:
            print(f"{demo.qtv_address} / {demo.filename} - ignore ({reason_to_ignore})")
            supab.ignore_demo(demo.filename, sha256, reason_to_ignore)
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
        db_entry = {
            "sha256": sha256,
            "source": demo.qtv_address,
            "filename": demo.filename,
            "s3_key": s3_key,
            "timestamp": demo.time,
            "duration": info.duration,
            "mode": mode,
            "map": info.map,
            "participants": {
                "players": [p.as_dict() for p in info.players],
                "teams": info.teams() if mvdparser.is_teamplay_mode(mode) else [],
                "player_count": len(info.players),
            },
            "title": info.title(mode),
        }

        try:
            sb.from_("demos").insert(db_entry).execute()
        except APIError as e:
            print(e)
            continue

    # 4. post process
    # todo: set event, map_number, map_count, next, prev etc


def prune_demos(mode: str, keep_count: int):
    current_count = supab.demo_count(mode)

    if current_count <= keep_count:
        print(f"\nprune {mode} ({current_count}/{keep_count}): nothing to prune")
        return

    query = (
        supab.get_client()
        .table("demos")
        .select("id, timestamp, s3_key", count=CountMethod.exact)
        .eq("mode", mode)
        .order("timestamp", desc=True)
        .range(keep_count, keep_count + 500)
        .execute()
    )
    demos = [supab.Demo(**demo) for demo in query.data]

    print(
        f"\nprune {mode} ({current_count}/{keep_count}): remove {current_count - keep_count} demos "
    )

    for demo in demos:
        print(f"deleting {demo.s3_key} with id {demo.id} from {demo.timestamp}")

        # 1. delete from s3
        try:
            aws.delete(demo.s3_key)
        except ClientError as e:
            print(e)
            continue

        # 2. delete from database
        supab.delete_demo(demo.id)


if __name__ == "__main__":
    update_demos("1on1", 250)
    update_demos("4on4", 150)
    update_demos("2on2", 50)
