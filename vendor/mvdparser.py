import json
from typing import List

import attr
from cattr import structure
from natsort import natsorted


def parse_ping_str(value) -> int:
    try:
        return round(float(value))
    except ValueError:
        return 0


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
    ping: str = attr.ib(converter=parse_ping_str)

    def as_dict(self) -> dict:
        return attr.asdict(self)


@attr.define
class ParseResult:
    filepath: str = attr.ib()
    date: str = attr.ib()
    duration: float = attr.ib()
    map: str = attr.ib()
    serverinfo: str = attr.ib()
    players: List[Player] = attr.ib()

    def participants(self, mode) -> str:
        if "ffa" == mode:
            return str(len(self.players))

        if "1on1" == mode:
            participants = [p.name for p in self.players]
        else:
            teams = {}

            for player in self.players:
                teams.setdefault(player.team, []).append(player.name)

            for team in teams:
                natsorted(teams[team])

            participants = [f'{team} ({", ".join(teams[team])})' for team in teams]

        natsorted(participants)
        return " vs ".join(participants)


def from_file(filepath) -> ParseResult:
    with open(filepath) as f:
        return structure(json.load(f), ParseResult)
