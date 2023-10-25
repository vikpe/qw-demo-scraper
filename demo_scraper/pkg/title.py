from typing import List

from natsort import humansorted

from demo_scraper.services.supab.player import Player
from demo_scraper.services.supab.team import Team


def from_mode_and_players(mode: str, players: List[Player]) -> str:
    names = [p.name for p in players]
    delimiter = ", " if mode in ["race", "ffa"] else " vs "
    return delimiter.join(humansorted(names))


def from_teams(teams: List[Team]) -> str:
    team_strings = [t.to_string(strip_fixes=True) for t in teams]
    return " vs ".join(humansorted(team_strings))
