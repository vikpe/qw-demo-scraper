import boto3


def upload(filepath: str, key: str, metadata=None):
    if metadata is None:
        metadata = {}

    bucket = "quakeworld"
    s3 = boto3.client("s3")
    s3.upload_file(
        filepath,
        bucket,
        key,
        ExtraArgs={"Metadata": metadata},
    )
