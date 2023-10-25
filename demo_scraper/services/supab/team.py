from collections import Counter
from typing import List, Tuple

import attr
from natsort import humansorted

from demo_scraper.pkg import fixes
from demo_scraper.services.supab.player import Player


@attr.define
class Team:
    name: str = attr.ib(default="")
    name_color: str = attr.ib(default="")
    players: List[Player] = attr.ib(default=[])

    def to_string(self, strip_fixes=False):
        names = [p.name for p in self.players]

        if strip_fixes:
            names = fixes.strip_fixes(names)

        name_list = ", ".join(humansorted(names))
        return f"{self.name} ({name_list})"

    def as_dict(self) -> dict:
        result = {
            "name": self.name,
            "name_color": self.name_color,
            "colors": list(self.get_colors()),
            "frags": self.get_frags(),
            "players": [p.as_dict() for p in self.players],
        }

        return result

    def get_frags(self) -> int:
        return sum([p.frags for p in self.players])

    def get_colors(self) -> Tuple[int, int]:
        player_colors = [p.colors for p in self.players]
        return get_majority_color(player_colors)


def get_majority_color(colors: List[Tuple[int, int]]) -> [int, int]:
    if not colors:
        return 0, 0

    (majority_colors, _) = Counter(colors).most_common(1)[0]
    return majority_colors
