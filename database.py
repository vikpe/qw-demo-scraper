import os
from typing import List, Optional

import attr
from supabase import create_client, Client


@attr.define
class DbDemo:
    id: Optional[int] = attr.ib()
    filename: str = attr.ib()
    info: str = attr.ib()
    created_at: Optional[str] = attr.ib()


def get_demos() -> List[DbDemo]:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    query = supabase.table("demos").select("*").execute()

    return [DbDemo(**demo) for demo in query.data]
