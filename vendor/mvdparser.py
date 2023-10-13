import json
import re
from collections import Counter
from typing import List, Tuple

import attr
from cattr import structure
from natsort import humansorted


def parse_ping_str(value) -> int:
    try:
        return round(float(value))
    except ValueError:
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
    ping: str = attr.ib(converter=parse_ping_str)

    def as_dict(self) -> dict:
        return attr.asdict(self)


@attr.define
class ParseResult:
    filepath: str = attr.ib()
    date: str = attr.ib()
    duration: float = attr.ib()
    map: str = attr.ib()
    serverinfo: str = attr.ib()
    players: List[Player] = attr.ib(converter=sort_players)

    def participants(self, mode) -> dict:
        result = {
            "teams": [],
            "players": [],
            "player_count": len(self.players),
        }

        if is_teamplay_mode(mode):
            players_per_team = {}

            for player in self.players:
                if player.team not in players_per_team:
                    players_per_team[player.team] = []

                players_per_team[player.team].append(player.as_dict())

            for team, players in players_per_team.items():
                top_color, bottom_color = get_team_color(
                    list((p["top_color"], p["bottom_color"]) for p in players)
                )
                team = {
                    "name": team,
                    "players": players,
                    "frags": sum([p["frags"] for p in players]),
                    "top_color": top_color,
                    "bottom_color": bottom_color,
                }
                result["teams"].append(team)

        else:
            result["players"] = [p.as_dict() for p in self.players]

        return result


def from_file(filepath) -> ParseResult:
    with open(filepath) as f:
        return structure(json.load(f), ParseResult)


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
