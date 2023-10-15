from natsort import humansorted

from demo_updater.pkg import qmode
from demo_updater.pkg.mvdparser import Team


def from_mode_and_players(mode, players) -> str:
    if qmode.is_teamplay(mode):
        participants = [
            t.to_string(strip_fixes=True) for t in Team.from_players(players)
        ]

    else:
        participants = [p.name for p in players]

    delimiter = ", " if mode in ["race", "ffa"] else " vs "
    return delimiter.join(humansorted(participants))
