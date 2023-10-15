import json
import re
from collections import Counter
from typing import List, Tuple

import attr
from cattr import structure
from natsort import humansorted

from vendor import qstring
from vendor.server_info import ServerInfo


def to_int(value: any) -> int:
    try:
        return round(float(value))
    except (ValueError, TypeError):
        return 0


def sort_players(players: List[dict]) -> List[dict]:
    return humansorted(players, lambda p: p.name)


@attr.define
class Player:
    name: str = attr.ib()
    team: str = attr.ib()
    top_color: int = attr.ib()
    bottom_color: int = attr.ib()
    frags: int = attr.ib()
    teamkills: int = attr.ib()
    deaths: int = attr.ib()
    suicides: int = attr.ib()
    ping: float = attr.ib(converter=to_int)

    def as_dict(self) -> dict:
        return attr.asdict(self)


@attr.define
class Result:
    filepath: str = attr.ib()
    date: str = attr.ib()
    duration: float = attr.ib()
    map: str = attr.ib()
    serverinfo = attr.ib(converter=ServerInfo.from_string)
    players: List[Player] = attr.ib(converter=sort_players)

    def teams(self) -> List[dict]:
        teams = []
        players_per_team = {}

        for player in self.players:
            if player.team not in players_per_team:
                players_per_team[player.team] = []

            players_per_team[player.team].append(player.as_dict())

        for team, players in players_per_team.items():
            player_names = [p["name"] for p in players]
            player_colors = list((p["top_color"], p["bottom_color"]) for p in players)
            top_color, bottom_color = get_team_color(player_colors)
            team = {
                "name": team,
                "player_prefix": qstring.get_prefix(player_names),
                "player_suffix": qstring.get_suffix(player_names),
                "players": players,
                "frags": sum([p["frags"] for p in players]),
                "top_color": top_color,
                "bottom_color": bottom_color,
            }
            teams.append(team)

        return teams

    def title(self, mode: str) -> str:
        if "ffa" == mode:
            return f'ffa: {", ".join([p.name for p in self.players])}'

        if is_teamplay_mode(mode):
            team_strings = []

            for team in self.teams():
                stripped_names = qstring.strip_fixes(
                    [p["name"] for p in team["players"]]
                )
                player_names = ", ".join(humansorted(stripped_names))
                team_strings.append(f'{team["name"]} ({player_names})')

            participants = team_strings
        else:
            participants = [p.name for p in self.players]

        delimiter = ", " if mode == "race" else " vs "
        return delimiter.join(participants)

    @classmethod
    def from_file(cls, filepath) -> "Result":
        with open(filepath) as f:
            return structure(json.load(f), cls)


def is_teamplay_mode(mode: str) -> bool:
    if mode in ["ffa", "1on1"]:
        return False
    elif mode in ["ctf", "wipeout"]:
        return True

    regex = r"(?:\d+on){1,}\d+"
    return re.search(regex, mode) is not None


def get_team_color(player_colors: List[Tuple[int, int]]) -> [int, int]:
    if not player_colors:
        return 0, 0

    (majority_colors, _) = Counter(player_colors).most_common(1)[0]
    return majority_colors
