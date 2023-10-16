import json
from collections import Counter
from typing import List, Tuple
from typing import Optional

import attr
from cattrs import structure
from natsort import humansorted

from demo_scraper.pkg import qstring
from demo_scraper.pkg.server_info import ServerInfo


def to_int(value: any) -> int:
    try:
        return round(float(value))
    except (ValueError, TypeError):
        return 0


def path_to_filename(path: str) -> str:
    return path.split("/")[-1]


def sort_players(players: List[dict]) -> List[dict]:
    return humansorted(players, lambda p: p.name)


@attr.define
class Player:
    name: Optional[str] = attr.ib(default="")
    team: Optional[str] = attr.ib(default="")
    top_color: Optional[int] = attr.ib(default=0)
    bottom_color: Optional[int] = attr.ib(default=0)
    frags: Optional[int] = attr.ib(default=0)
    teamkills: Optional[int] = attr.ib(default=0)
    deaths: Optional[int] = attr.ib(default=0)
    suicides: Optional[int] = attr.ib(default=0)
    ping: Optional[float] = attr.ib(converter=to_int, default=0)

    def as_dict(self) -> dict:
        return attr.asdict(self)


@attr.define
class Team:
    name: str = attr.ib()
    players: List[Player] = attr.ib()

    @classmethod
    def from_players(cls, players: List[Player]) -> List["Team"]:
        players_per_team = {}

        for player in players:
            players_per_team.setdefault(player.team, []).append(player)

        return [
            cls(
                name=players[0].team,
                players=players,
            )
            for players in players_per_team.values()
        ]

    def to_string(self, strip_fixes=False):
        names = [p.name for p in self.players]

        if strip_fixes:
            names = qstring.strip_fixes(names)

        name_list = ", ".join(humansorted(names))
        return f"{self.name} ({name_list})"

    def as_dict(self) -> dict:
        (top_color, bottom_color) = self.get_color()
        return {
            "name": self.name,
            "top_color": top_color,
            "bottom_color": bottom_color,
            "frags": self.get_frags(),
            "players": [p.as_dict() for p in self.players],
        }

    def get_frags(self) -> int:
        return sum([p.frags for p in self.players])

    def get_color(self) -> Tuple[int, int]:
        player_colors = list((p.top_color, p.bottom_color) for p in self.players)
        return get_majority_color(player_colors)


@attr.define
class MvdInfo:
    filepath: str = attr.ib(converter=path_to_filename)
    date: str = attr.ib()
    duration: float = attr.ib()
    map: str = attr.ib()
    serverinfo = attr.ib(converter=ServerInfo.from_string)
    players: List[Player] = attr.ib(converter=sort_players)

    @classmethod
    def from_file(cls, filepath) -> "MvdInfo":
        with open(filepath) as f:
            return structure(json.load(f), cls)


def get_majority_color(colors: List[Tuple[int, int]]) -> [int, int]:
    if not colors:
        return 0, 0

    (majority_colors, _) = Counter(colors).most_common(1)[0]
    return majority_colors
