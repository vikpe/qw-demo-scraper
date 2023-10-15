from natsort import humansorted
import re

from demo_updater.pkg import qstring
from demo_updater.pkg.mvdparser import Team


def title(self) -> str:
    if "ffa" == self.serverinfo.mode:
        return f'ffa: {", ".join([p.name for p in self.players])}'

    if is_teamplay_mode(self.serverinfo.mode):
        team_strings = []

        for team in Team.from_players(self.players):
            stripped_names = qstring.strip_fixes([p.name for p in team.players])
            player_names = ", ".join(humansorted(stripped_names))
            team_strings.append(f"{team.name} ({player_names})")

        participants = team_strings
    else:
        participants = [p.name for p in self.players]

    delimiter = ", " if self.serverinfo.mode == "race" else " vs "
    return delimiter.join(participants)


def is_teamplay_mode(mode: str) -> bool:
    if mode in ["ffa", "1on1"]:
        return False
    elif mode in ["ctf", "wipeout"]:
        return True

    regex = r"(?:\d+on){1,}\d+"
    return re.search(regex, mode) is not None
