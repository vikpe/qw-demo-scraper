from typing import List

from natsort import humansorted

from demo_scraper.pkg import qmode
from demo_scraper.services.supab.player import Player
from demo_scraper.services.supab.team import Team


def from_mode_and_players(mode: str, players: List[Player]) -> str:
    if qmode.is_teamplay(mode):
        participants = [
            t.to_string(strip_fixes=True) for t in Team.from_players(players)
        ]

    else:
        participants = [p.name for p in players]

    delimiter = ", " if mode in ["race", "ffa"] else " vs "
    return delimiter.join(humansorted(participants))
