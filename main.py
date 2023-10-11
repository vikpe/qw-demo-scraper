import os
import subprocess

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

import database
import hub
from util import download_file
from glob import glob

load_dotenv()  # take environment variables from .env.

LIMIT = 1


def get_new_server_demos(limit: int) -> list[hub.HubDemo]:
    # demos from database
    # todo: optimize db call
    db_filenames = [d.filename for d in database.get_demos()]

    # demos from servers
    server_demos = hub.get_demos(limit)
    server_filenames = [d.filename for d in server_demos]

    # compare
    new_filenames = list(set(server_filenames) - set(db_filenames))
    new_demos = [d for d in server_demos if d.filename in new_filenames]

    return new_demos


def main():
    # demos from database
    new_server_demos = get_new_server_demos(LIMIT)

    # download
    for demo in new_server_demos:
        print(f"downloading {demo.filename} to demos/")
        download_file(demo.download_url, os.path.join("demos", demo.filename))

    # parse, compress
    subprocess.run(["bash", "scripts.sh"])

    # combine info
    # for demo in new_server_demos:
    #     pass
    #
    # # insert into database
    # for info_path in glob("demos/*/*.mvd.json"):
    #     info = mvdparser.from_file(info_path)
    #
    #     print(info.filepath, info.duration, type(info.players[0].frags))

    # upload to s3
    s3 = boto3.client("s3")

    for zip_file_path in glob("demos/*/*.mvd.gz"):
        try:
            s3.upload_file(zip_file_path, "quakeworld", zip_file_path)
        except ClientError as e:
            print(e)


if __name__ == "__main__":
    main()
