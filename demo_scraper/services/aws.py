import logging
import os

import boto3

logging.getLogger("boto").setLevel(logging.CRITICAL)


def upload(filepath: str, key: str, metadata=None):
    if metadata is None:
        metadata = {}

    s3 = boto3.client("s3")
    bucket = os.getenv("AWS_S3_BUCKET")
    s3.upload_file(
        filepath,
        bucket,
        key,
        ExtraArgs={"Metadata": metadata},
    )


def delete(key):
    s3 = boto3.client("s3")
    bucket = os.getenv("AWS_S3_BUCKET")
    s3.delete_object(
        Bucket=bucket,
        Key=key,
    )
