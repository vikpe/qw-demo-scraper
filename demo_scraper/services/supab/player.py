from typing import Tuple

import attr

from demo_scraper.pkg import qcharset
from demo_scraper.pkg.mvdparser import Player as MvdPlayer


@attr.define
class Player:
    name: str = attr.ib(default="")
    name_color: str = attr.ib(default="")
    team: str = attr.ib(default="")
    team_color: str = attr.ib(default="")
    color: Tuple[int, int] = attr.ib(default=(0, 0))
    frags: int = attr.ib(default=0)
    ping: float = attr.ib(default=0)

    def as_dict(self) -> dict:
        return attr.asdict(self)

    @classmethod
    def from_mvdparser_player(cls, player: MvdPlayer) -> "Player":
        return cls(
            name=qcharset.raw_to_utf8(player.name_raw),
            name_color=qcharset.raw_to_color_codes(player.name_raw),
            team=qcharset.raw_to_utf8(player.team_raw),
            team_color=qcharset.raw_to_color_codes(player.team_raw),
            color=(player.top_color, player.bottom_color),
            frags=player.frags,
            ping=player.ping,
        )
