import boto3

from vendor import hub


def upload_demo(s3: boto3.client, filepath: str, key: str, metadata: dict[str, str]):
    s3.upload_file(
        filepath,
        "quakeworld",
        key,
        ExtraArgs={"Metadata": metadata},
    )


def upload_recent_demo(s3: boto3.client, demo: hub.Demo, sha256: str):
    filename = f"{demo.filename}.gz"
    filepath = f"demos/{filename}"
    key = f"qw/demos/recent/{filename}"
    metadata = {
        "sha256": sha256,
        "qtv_address": demo.qtv_address,
        "filename": demo.filename,
    }
    upload_demo(s3, filepath, key, metadata)
