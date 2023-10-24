from typing import List, Optional

import attr
from natsort import humansorted

from demo_scraper.pkg.mvdparser import Player as MvdPlayer
from demo_scraper.services.supab.player import Player
from demo_scraper.services.supab.team import Team


def is_valid_mvd_player(player: MvdPlayer) -> bool:
    return len(player.name) > 0 and player.distance_moved > 0


def parse_mvd_players(players: List[MvdPlayer]) -> List[Player]:
    valid_mvd_players = [p for p in players if is_valid_mvd_player(p)]
    players = [Player.from_mvdparser_player(p) for p in valid_mvd_players]
    return humansorted(players, lambda p: p.name)


@attr.define
class Participants:
    players: Optional[List[Player]] = attr.ib(default=[])
    teams: Optional[List[Team]] = attr.ib(default=[])
    player_count: Optional[int] = attr.ib(default=0)

    @classmethod
    def from_mvdparser_players(
        cls, mvd_players: List[MvdPlayer], is_teamplay: bool
    ) -> "Participants":
        players = parse_mvd_players(mvd_players)

        return cls(
            players=[] if is_teamplay else players,
            teams=Team.from_players(players) if is_teamplay else [],
            player_count=len(players),
        )
