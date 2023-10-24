from collections import Counter
from typing import List, Tuple

import attr
from natsort import humansorted

from demo_scraper.pkg import fixes
from demo_scraper.services.supab.player import Player


def get_majority_color(colors: List[Tuple[int, int]]) -> [int, int]:
    if not colors:
        return 0, 0

    (majority_colors, _) = Counter(colors).most_common(1)[0]
    return majority_colors


@attr.define
class Team:
    name: str = attr.ib(default="")
    name_color: str = attr.ib(default="")
    players: List[Player] = attr.ib(default=[])

    @classmethod
    def from_players(cls, players: List[Player]) -> List["Team"]:
        players_per_team = {}

        for player in players:
            players_per_team.setdefault(player.team, []).append(player)

        return [
            cls(
                name=players[0].team,
                name_color=players[0].team_color,
                players=players,
            )
            for players in players_per_team.values()
        ]

    def to_string(self, strip_fixes=False):
        names = [p.name for p in self.players]

        if strip_fixes:
            names = fixes.strip_fixes(names)

        name_list = ", ".join(humansorted(names))
        return f"{self.name} ({name_list})"

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "name_color": self.name_color,
            "color": self.get_color(),
            "frags": self.get_frags(),
            "players": [p.as_dict() for p in self.players],
        }

    def get_frags(self) -> int:
        return sum([p.frags for p in self.players])

    def get_color(self) -> Tuple[int, int]:
        player_colors = [p.color for p in self.players]
        return get_majority_color(player_colors)
