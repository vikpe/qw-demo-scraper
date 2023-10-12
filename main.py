import os
import shutil
import subprocess

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from vendor import hub, supab, aws
from vendor.util import download_file

load_dotenv()

LIMIT = 1


def clear_demo_dir():
    shutil.rmtree("demos")
    os.mkdir("demos")


def get_new_server_demos(limit: int) -> list[hub.Demo]:
    # demos from database
    # todo: optimize db call
    db_filenames = supab.get_demos_source_filenames()

    # demos from servers
    server_demos = hub.get_demos(limit)
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


def main():
    clear_demo_dir()

    # demos from database
    new_server_demos = get_new_server_demos(LIMIT)

    # download
    for demo in new_server_demos:
        print(f"downloading {demo.qtv_address} - {demo.filename}")
        download_file(demo.download_url, f"demos/{demo.filename}")

    # checksums, parse, compress
    subprocess.run(["bash", "scripts.sh"])
    checksums = get_sha256_per_filename("demos/demos.sha256")

    # upload to s3, add to database
    sb = supab.get_client()

    for demo in new_server_demos:
        # 1. upload to s3
        try:
            aws.upload_recent_demo(s3, demo, checksums[demo.filename])
        except ClientError as e:
            print(e)
            continue

        # 2. add to database
        info = mvdparser.from_file(f"demos/{demo.filename}.json")
        mode = demo.get_mode()

        db_entry = {
            "sha256": sha256,
            "source": demo.qtv_address,
            "filename": demo.filename,  # 2023-10-12T11:44:00Z
            "s3_key": s3_key,
            "timestamp": demo.time,
            "duration": info.duration,
            "mode": mode,
            "map": info.map,
            "players": [p.as_dict() for p in info.players],
            "title": info.participants(mode),
        }
        sb.from_("demos").insert(db_entry).execute()

    # 4. post process
    # todo: set event, map_number, map_count, next, prev etc


if __name__ == "__main__":
    main()
