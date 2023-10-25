from typing import List, Optional

import attr
from natsort import humansorted

from demo_scraper.pkg.mvdparser import Player as MvdPlayer
from demo_scraper.pkg import qcharset
from demo_scraper.services.supab.player import Player
from demo_scraper.services.supab.team import Team


@attr.define
class Participants:
    players: Optional[List[Player]] = attr.ib(default=[])
    teams: Optional[List[Team]] = attr.ib(default=[])
    player_count: Optional[int] = attr.ib(default=0)

    def as_dict(self) -> dict:
        return {
            "players": [p.as_dict() for p in self.players],
            "teams": [t.as_dict() for t in self.teams],
            "player_count": self.player_count,
        }

    @classmethod
    def from_mvdparser_players(
        cls, mvd_players: List[MvdPlayer], is_teamplay: bool
    ) -> "Participants":
        valid_players = [p for p in mvd_players if is_valid_mvd_player(p)]
        player_count = len(valid_players)

        if is_teamplay:
            return cls(
                players=[],
                teams=teams_from_mvdplayers(valid_players),
                player_count=player_count,
            )
        else:
            return cls(
                players=mvd_players_to_db_players(valid_players),
                teams=[],
                player_count=player_count,
            )


def is_valid_mvd_player(player: MvdPlayer) -> bool:
    return len(player.name) > 0 and player.distance_moved > 0


def mvd_players_to_db_players(mvd_players: List[MvdPlayer]) -> List[Player]:
    players = [Player.from_mvdparser_player(p) for p in mvd_players]
    return humansorted(players, lambda p: p.name)


def teams_from_mvdplayers(mvd_players: List[MvdPlayer]) -> List[Team]:
    players_per_team: dict[str, List[MvdPlayer]] = {}
    for player in mvd_players:
        players_per_team.setdefault(player.team_raw, []).append(player)

    teams = []
    for team_name, players in players_per_team.items():
        team = Team(
            name=qcharset.raw_to_utf8(players[0].team_raw),
            name_color=qcharset.raw_to_color_codes(players[0].team_raw),
            players=mvd_players_to_db_players(players),
        )
        teams.append(team)

    return teams
