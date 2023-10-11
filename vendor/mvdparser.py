import json
from typing import List

import attr
from cattr import structure


@attr.define
class Player:
    name: str = attr.ib()
    team: str = attr.ib()
    top_color: int = attr.ib()
    bottom_color: int = attr.ib()
    frags: int = attr.ib()
    teamkills: int = attr.ib()
    deaths: int = attr.ib()
    suicides: int = attr.ib()
    avg_ping: float = attr.ib()


@attr.define
class ParseResult:
    filepath: str = attr.ib()
    date: str = attr.ib()
    duration: float = attr.ib()
    map: str = attr.ib()
    serverinfo: str = attr.ib()
    players: List[Player] = attr.ib()


def from_file(filepath) -> ParseResult:
    with open(filepath) as f:
        return structure(json.load(f), ParseResult)
