import os
from typing import Optional, List

import attr
from cattrs import structure
from postgrest.exceptions import APIError
from postgrest.types import CountMethod
from supabase import create_client, Client

from demo_scraper.pkg.mvdparser import Player, Team


@attr.define
class Participants:
    players: Optional[List[Player]] = attr.ib(default=[])
    teams: Optional[List[Team]] = attr.ib(default=[])
    player_count: Optional[int] = attr.ib(default=0)


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
    participants: Optional[Participants] = attr.ib(default=Participants())


@attr.define
class NewDemo:
    sha256: str = attr.ib()
    source: str = attr.ib()
    filename: str = attr.ib()
    s3_key: str = attr.ib()
    timestamp: str = attr.ib()
    duration: float = attr.ib()
    mode: str = attr.ib()
    map: str = attr.ib()
    matchtag: str = attr.ib()
    title: str = attr.ib()
    participants: Participants = attr.ib()

    def as_dict(self) -> dict:
        return attr.asdict(self)


@attr.define
class IgnoredDemo:
    id: Optional[int] = attr.ib(default=0)
    sha256: Optional[str] = attr.ib(default="")
    mode: Optional[str] = attr.ib(default="")
    filename: Optional[str] = attr.ib(default="")
    reason: Optional[str] = attr.ib(default="")
    created_at: Optional[str] = attr.ib(default="")


@attr.define
class NewIgnoredDemo:
    sha256: str = attr.ib()
    mode: str = attr.ib()
    filename: str = attr.ib()
    reason: str = attr.ib()

    def as_dict(self) -> dict:
        return attr.asdict(self)


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


def add_demo(demo: NewDemo):
    sb = get_client()
    return sb.table("demos").insert(demo.as_dict()).execute()


def ignore_demo(demo: NewIgnoredDemo):
    try:
        sb = get_client()
        return sb.table("ignored_demos").insert(demo.as_dict()).execute()
    except APIError as e:
        print(e)


def get_demos_by_mode(mode: str) -> list[Demo]:
    sb = get_client()
    db_demos_query = (
        sb.table("demos")
        .select("filename, timestamp")
        .eq("mode", mode)
        .order("timestamp", desc=True)
        .execute()
    )
    return [structure(demo, Demo) for demo in db_demos_query.data]


def get_demos_to_prune(mode: str, keep_count: int):
    sb = get_client()
    query = (
        sb.table("demos")
        .select("id, timestamp, s3_key", count=CountMethod.exact)
        .eq("mode", mode)
        .order("timestamp", desc=True)
        .range(keep_count, keep_count + 500)
        .execute()
    )
    return [structure(demo, Demo) for demo in query.data]


def get_ignored_filenames_by_mode(mode: str) -> list[str]:
    sb = get_client()
    query = sb.table("ignored_demos").select("filename").eq("mode", mode).execute()
    return [structure(demo, IgnoredDemo).filename for demo in query.data]


def get_demo_count_by_mode(mode: str) -> int:
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
