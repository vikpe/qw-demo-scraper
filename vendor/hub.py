from typing import List, Optional

import attr
import requests


@attr.define
class Demo:
    qtv_address: Optional[str] = attr.ib(default="")
    time: Optional[str] = attr.ib(default="")
    filename: Optional[str] = attr.ib(default="")
    download_url: Optional[str] = attr.ib(default="")
    qtvplay_url: Optional[str] = attr.ib(default="")

    def get_mode(self) -> str:
        if self.filename.startswith("duel_"):
            return "1on1"

        known_modes = [
            "2on2",
            "ffa",
            "4on4",
        ]

        for mode in known_modes:
            if self.filename.startswith(f"{mode}_"):
                return mode

        return "unknown"


def get_demos(mode: str, limit: int) -> List[Demo]:
    mode_ = "duel" if mode == "1on1" else mode
    url = f"https://hubapi.quakeworld.nu/v2/demos?mode={mode_}&limit={limit}"
    res = requests.get(url).json()

    return [Demo(**demo) for demo in res]
