import os
import shutil
import subprocess

from botocore.exceptions import ClientError
from dotenv import load_dotenv
from postgrest.types import CountMethod

from vendor import hub, supab, aws, mvdparser
from vendor.util import download_file

load_dotenv()


def clear_demo_dir():
    shutil.rmtree("demos")
    os.mkdir("demos")


def get_new_server_demos(mode: str, limit: int) -> list[hub.Demo]:
    # demos from database
    sb = supab.get_client()
    demos_query = (
        sb.table("demos")
        .select("filename")
        .eq("mode", mode)
        .order("timestamp", desc=True)
        .limit(200)
        .execute()
    )
    db_filenames = [demo["filename"] for demo in demos_query.data]

    # demos from servers
    server_demos = hub.get_demos(mode, limit)
    server_filenames = [d.filename for d in server_demos]

    # compare
    new_filenames = list(set(server_filenames) - set(db_filenames))
    new_demos = [d for d in server_demos if d.filename in new_filenames]

    return new_demos


def get_sha256_per_filename(sha_filepath) -> dict[str, str]:
    with open(sha_filepath) as fh:
        lines = fh.readlines()

    result = {}

    for line in lines:
        sha256, filename = line.strip().split("  ")
        filename = filename.replace("demos/", "")
        result[filename] = sha256

    return result


def update_demos(mode: str, limit: int):
    add_new_demos(mode, limit)
    prune_demos(mode, keep_count=limit)


def add_new_demos(demo_mode: str, limit: int):
    clear_demo_dir()

    # download new demos
    new_server_demos = get_new_server_demos(demo_mode, limit)

    if not new_server_demos:
        print(f"{demo_mode}: no new demos found")
        return

    print(f"{demo_mode}: found {len(new_server_demos)} new demos")

    for demo in new_server_demos:
        print(f"downloading {demo.qtv_address} - {demo.filename}")
        download_file(demo.download_url, f"demos/{demo.filename}")

    # checksums, parse, compress
    subprocess.run(["bash", "scripts.sh"])
    checksums = get_sha256_per_filename("demos/demos.sha256")

    # upload to s3, add to database
    sb = supab.get_client()

    print(f"# found {len(new_server_demos)} new demos")
    for demo in new_server_demos:
        info = mvdparser.from_file(f"demos/{demo.filename}.json")

        if 0 == info.duration:  # game in progress
            print(f"- skip (in progress): {demo.filename}")
            continue

        sha256 = checksums[demo.filename]
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
        info = mvdparser.from_file(f"demos/{demo.filename}.json")
        mode = demo.get_mode()

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
        sb.from_("demos").insert(db_entry).execute()

    # 4. post process
    # todo: set event, map_number, map_count, next, prev etc


def prune_demos(mode: str, keep_count: int):
    sb = supab.get_client()

    current_count = (
        sb.table("demos")
        .select("count", count=CountMethod.exact)
        .eq("mode", mode)
        .execute()
    ).count

    if current_count <= keep_count:
        print(f"prune {mode} ({current_count}/{keep_count}): nothing to prune")
        return

    query = (
        sb.table("demos")
        .select("id, timestamp, s3_key", count=CountMethod.exact)
        .eq("mode", mode)
        .order("timestamp", desc=True)
        .range(keep_count, keep_count + 500)
        .execute()
    )

    print(
        f"prune {mode} ({current_count}/{keep_count}): remove {current_count - keep_count} demos "
    )

    for d in query.data:
        print(f"deleting {d['s3_key']} with id {d['id']} from {d['timestamp']}")

        # 1. delete from s3
        try:
            aws.delete(d["s3_key"])
        except ClientError as e:
            print(e)
            continue

        # 2. delete from database
        sb.from_("demos").delete().eq("id", d["id"]).execute()


if __name__ == "__main__":
    update_demos("1on1", 150)
    update_demos("4on4", 100)
    update_demos("2on2", 50)
