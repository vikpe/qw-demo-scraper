import json
from typing import List
from typing import Optional

import attr
from cattrs import structure

from demo_scraper.pkg.server_info import ServerInfo


def to_int(value: any) -> int:
    try:
        return round(float(value))
    except (ValueError, TypeError):
        return 0


def path_to_filename(path: str) -> str:
    return path.split("/")[-1]


@attr.define
class Player:
    name: Optional[str] = attr.ib(default="")
    name_raw: Optional[str] = attr.ib(default="")
    team: Optional[str] = attr.ib(default="")
    team_raw: Optional[str] = attr.ib(default="")
    top_color: Optional[int] = attr.ib(default=0)
    bottom_color: Optional[int] = attr.ib(default=0)
    frags: Optional[int] = attr.ib(default=0)
    teamkills: Optional[int] = attr.ib(default=0)
    deaths: Optional[int] = attr.ib(default=0)
    suicides: Optional[int] = attr.ib(default=0)
    ping: Optional[float] = attr.ib(converter=to_int, default=0)
    distance_moved: Optional[float] = attr.ib(converter=to_int, default=0)

    def as_dict(self) -> dict:
        return attr.asdict(self)


@attr.define
class MvdInfo:
    filepath: str = attr.ib(converter=path_to_filename)
    date: str = attr.ib()
    duration: float = attr.ib()
    map: str = attr.ib()
    hostname: str = attr.ib()
    serverinfo = attr.ib(converter=ServerInfo.from_string)
    players: List[Player] = attr.ib()

    @classmethod
    def from_file(cls, filepath) -> "MvdInfo":
        with open(filepath) as f:
            return structure(json.load(f), cls)
