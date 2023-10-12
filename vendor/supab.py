import os
from typing import Optional, List

import attr
from supabase import create_client, Client


@attr.define
class Demo:
    sha256: str = attr.ib()
    source: str = attr.ib()
    filename: str = attr.ib()
    s3_key: str = attr.ib()
    timestamp: str = attr.ib()
    duration: float = attr.ib()
    mode: str = attr.ib()
    map: str = attr.ib()
    title: str = attr.ib()
    players: List[dict] = attr.ib()
    id: Optional[int] = attr.ib(default=0)
    created_at: Optional[str] = attr.ib(default=None)


def get_client() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)
