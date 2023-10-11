from typing import List

import attr
import requests


@attr.define
class HubDemo:
    qtv_address: str = attr.ib()
    time: str = attr.ib()
    filename: str = attr.ib()
    download_url: str = attr.ib()
    qtvplay_url: str = attr.ib()


def get_demos(limit: int) -> List[HubDemo]:
    url = f"http://hubapi.quakeworld.nu/v2/demos?qtv_address=quake.se&mode=duel&limit={limit}"
    res = requests.get(url).json()

    return [HubDemo(**demo) for demo in res]
