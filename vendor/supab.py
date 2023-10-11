import os
from typing import List, Optional

import attr
from supabase import create_client, Client


@attr.define
class Demo:
    id: Optional[int] = attr.ib()
    sha256: str = attr.ib()
    source: str = attr.ib()
    filename: str = attr.ib()
    s3_key: str = attr.ib()
    timestamp: str = attr.ib()
    duration: float = attr.ib()
    mode: str = attr.ib()
    map: str = attr.ib()
    title: str = attr.ib()
    created_at: Optional[str] = attr.ib()


def get_client() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)


def get_demos_source_filenames() -> List[str]:
    sb: Client = get_client()
    query = sb.table("demos").select("filename").execute()

    return [Demo(**demo).filename for demo in query.data]
