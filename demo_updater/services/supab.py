import os
from typing import Optional

import attr
from postgrest.exceptions import APIError
from postgrest.types import CountMethod
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

    def as_dict(self) -> dict:
        return attr.asdict(self)


@attr.define
class IgnoredDemo:
    id: Optional[int] = attr.ib(default=0)
    sha256: Optional[str] = attr.ib(default="")
    filename: Optional[str] = attr.ib(default="")
    reason: Optional[str] = attr.ib(default="")
    created_at: Optional[str] = attr.ib(default="")


def get_client() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)


def has_demo_by_sha256(sha256: str) -> bool:
    sb = get_client()
    return (
        sb.table("demos")
        .select("count", count=CountMethod.exact)
        .eq("sha256", sha256)
        .execute()
    ).count > 0


def ignore_demo(mode: str, filename: str, sha256: str, reason: str):
    try:
        sb = get_client()
        return (
            sb.table("ignored_demos")
            .insert(
                {"mode": mode, "filename": filename, "sha256": sha256, "reason": reason}
            )
            .execute()
        )
    except APIError as e:
        print(e)


def get_existing_demos_by_mode(mode: str) -> list[Demo]:
    sb = get_client()
    db_demos_query = (
        sb.table("demos")
        .select("filename, timestamp")
        .eq("mode", mode)
        .order("timestamp", desc=True)
        .execute()
    )
    return [Demo(**demo) for demo in db_demos_query.data]


def get_ignored_filenames_by_mode(mode: str) -> list[str]:
    sb = get_client()
    query = sb.table("ignored_demos").select("filename").eq("mode", mode).execute()
    return [IgnoredDemo(**demo).filename for demo in query.data]


def demo_count_by_mode(mode: str) -> int:
    sb = get_client()
    return (
        sb.table("demos")
        .select("count", count=CountMethod.exact)
        .eq("mode", mode)
        .execute()
    ).count


def delete_demo(demo_id: int):
    sb = get_client()
    return sb.from_("demos").delete().eq("id", demo_id).execute()
