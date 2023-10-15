from typing import List, Optional

import attr
import requests
from cattrs import structure


@attr.define
class Demo:
    qtv_address: Optional[str] = attr.ib(default="")
    time: Optional[str] = attr.ib(default="")
    filename: Optional[str] = attr.ib(default="")
    download_url: Optional[str] = attr.ib(default="")
    qtvplay_url: Optional[str] = attr.ib(default="")

    def get_mode(self) -> str:
        if "_" not in self.filename:
            return "unknown"
        elif self.filename.startswith("duel_"):
            return "1on1"
        else:
            return self.filename.split("_")[0]


def get_demos(mode: str, limit: int) -> List[Demo]:
    try:
        mode_ = "duel" if mode == "1on1" else mode
        url = f"https://hubapi.quakeworld.nu/v2/demos?mode={mode_}&limit={limit}"
        res = requests.get(url).json()
        return [structure(demo, Demo) for demo in res] if isinstance(res, list) else []
    except Exception as e:
        print(e)
        return []
