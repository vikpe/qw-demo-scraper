import os
from typing import Optional

import attr
from supabase import create_client, Client


@attr.define
class Demo:
    id: Optional[int] = attr.ib(default=0)
    sha256: Optional[str] = attr.ib(default="")
    source: Optional[str] = attr.ib(default="")
    filename: Optional[str] = attr.ib(default="")
    s3_key: Optional[str] = attr.ib(default="")
    timestamp: Optional[str] = attr.ib(default="")
    duration: Optional[float] = attr.ib(default=0.0)
    mode: Optional[str] = attr.ib(default="")
    map: Optional[str] = attr.ib(default="")
    title: Optional[str] = attr.ib(default="")
    participants: Optional[dict] = attr.ib(default={})
    fts: Optional[str] = attr.ib(default="")
    created_at: Optional[str] = attr.ib(default="")


def get_client() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)
