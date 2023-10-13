import os
import shutil
import subprocess

from botocore.exceptions import ClientError
from dotenv import load_dotenv

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
        .eq("mode", mode if mode != "duel" else "1on1")
        .order("id", desc=True)
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


def update_demos(demo_mode: str, limit: int):
    clear_demo_dir()

    # download new demos
    new_server_demos = get_new_server_demos(demo_mode, limit)

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


if __name__ == "__main__":
    update_demos("duel", 50)
    update_demos("2on2", 25)
    update_demos("4on4", 50)
