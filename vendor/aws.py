import boto3

from vendor import hub


def upload_recent_demo(s3: boto3.client, demo: hub.Demo, sha256: str):
    bucket = "quakeworld"
    filename = f"{demo.filename}.gz"
    filepath = f"demos/{filename}"
    key = f"qw/demos/recent/{filename}"
    metadata = {
        "sha256": sha256,
        "qtv_address": demo.qtv_address,
        "filename": demo.filename,
    }

    s3.upload_file(
        filepath,
        bucket,
        key,
        ExtraArgs={"Metadata": metadata},
    )
