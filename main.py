import subprocess

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from vendor import hub, supab, aws
from vendor.util import download_file

load_dotenv()

LIMIT = 1


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


def get_sha256_per_filename() -> dict[str, str]:
    with open("demos/demos.sha256") as fh:
        lines = fh.readlines()

    result = {}

    for line in lines:
        sha256, filename = line.strip().split("  ")
        filename = filename.replace("demos/", "")
        result[filename] = sha256

    return result


def main():
    # demos from database
    new_server_demos = get_new_server_demos(LIMIT)

    # download
    for demo in new_server_demos:
        print(f"downloading {demo.qtv_address} - {demo.filename}")
        download_file(demo.download_url, f"demos/{demo.filename}")

    # checksums, parse, compress
    subprocess.run(["bash", "scripts.sh"])
    checksums = get_sha256_per_filename()

    # upload to s3
    # todo: s3 manager download/delete
    s3 = boto3.client("s3")

    for demo in new_server_demos:
        # upload to s3
        try:
            aws.upload_recent_demo(s3, demo, checksums[demo.filename])
        except ClientError as e:
            print(e)
            continue

        # insert into database
        # combine info
        # todo: info = mvdparser.from_file(info_path)

    # post process
    # todo: set event, map_number, map_count, next, prev etc


if __name__ == "__main__":
    main()
