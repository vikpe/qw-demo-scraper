from typing import List

import attr
import requests


@attr.define
class Demo:
    qtv_address: str = attr.ib()
    time: str = attr.ib()
    filename: str = attr.ib()
    download_url: str = attr.ib()
    qtvplay_url: str = attr.ib()

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
    url = f"http://hubapi.quakeworld.nu/v2/demos?mode={mode}&limit={limit}"
    res = requests.get(url).json()

    return [Demo(**demo) for demo in res]
