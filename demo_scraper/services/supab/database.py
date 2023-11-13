import logging
import os
from typing import List

from cattrs import structure
from postgrest.exceptions import APIError
from postgrest.types import CountMethod
from supabase import create_client, Client

from demo_scraper.services.supab.demo import NewDemo, Demo, NewIgnoredDemo, IgnoredDemo

# disable http logs
logging.getLogger("httpx").setLevel(logging.WARNING)


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


def get_recent_demos_by_mode(mode: str) -> list[Demo]:
    sb = get_client()
    db_demos_query = (
        sb.table("demos")
        .select("filename, timestamp")
        .is_("event_id", "NULL")  # no event = recent
        .eq("mode", mode)
        .order("timestamp", desc=True)
        .execute()
    )
    return [structure(demo, Demo) for demo in db_demos_query.data]


def get_recent_demos_to_prune(mode: str, keep_count: int):
    sb = get_client()
    query = (
        sb.table("demos")
        .select("id, timestamp, s3_key", count=CountMethod.exact)
        .is_("event_id", "NULL")  # no event = recent
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


def get_recent_demo_count_by_mode(mode: str) -> int:
    sb = get_client()
    return (
        sb.table("demos")
        .select("count", count=CountMethod.exact)
        .is_("event_id", "NULL")  # no event = recent
        .eq("mode", mode)
        .execute()
    ).count


def delete_demo(demo_id: int):
    sb = get_client()
    return sb.from_("demos").delete().eq("id", demo_id).execute()


def delete_demos(demo_ids: List[int]):
    if not demo_ids:
        return

    sb = get_client()
    return sb.from_("demos").delete().in_("id", demo_ids).execute()
