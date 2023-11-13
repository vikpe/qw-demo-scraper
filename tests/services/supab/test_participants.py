from demo_scraper.pkg.mvdparser import Player as MvdPlayer
from demo_scraper.services.supab.participants import (
    is_valid_mvd_player,
    mvd_players_to_db_players,
    teams_from_mvdplayers,
)
from demo_scraper.services.supab.player import Player as DbPlayer
from demo_scraper.services.supab.team import Team as DbTeam


def test_is_valid_player():
    assert not is_valid_mvd_player(MvdPlayer(name=""))
    assert not is_valid_mvd_player(MvdPlayer(name="dough", frags=5, distance_moved=0))
    assert is_valid_mvd_player(MvdPlayer(name="XantoM", frags=0, distance_moved=100))


def test_mvd_players_to_db_players():
    players = [
        MvdPlayer(name="_XantoM", name_raw=" XantoM", distance_moved=100),
        MvdPlayer(name="_ ParadokS", name_raw=" ParadokS", distance_moved=100),
    ]
    assert mvd_players_to_db_players(players) == [
        DbPlayer(
            name="• ParadokS", name_color="wwwwwwwwww", colors=(0, 0), frags=0, ping=0
        ),
        DbPlayer(
            name="• XantoM", name_color="wwwwwwww", colors=(0, 0), frags=0, ping=0
        ),
    ]


def test_teams_from_mvdplayers():
    players = [
        MvdPlayer(name="beta", name_raw="beta", team="red", team_raw="red"),
        MvdPlayer(name="gamma", name_raw="gamma", team="blue", team_raw="blue"),
        MvdPlayer(name="delta", name_raw="delta", team="blue", team_raw="blue"),
        MvdPlayer(name="alpha", name_raw="alpha", team="red", team_raw="red"),
    ]
    assert teams_from_mvdplayers(players) == [
        DbTeam(
            name="blue",
            name_color="wwww",
            players=[
                DbPlayer(
                    name="delta",
                    name_color="wwwww",
                    colors=(0, 0),
                    frags=0,
                    ping=0,
                ),
                DbPlayer(
                    name="gamma",
                    name_color="wwwww",
                    colors=(0, 0),
                    frags=0,
                    ping=0,
                ),
            ],
        ),
        DbTeam(
            name="red",
            name_color="www",
            players=[
                DbPlayer(
                    name="alpha",
                    name_color="wwwww",
                    colors=(0, 0),
                    frags=0,
                    ping=0,
                ),
                DbPlayer(
                    name="beta",
                    name_color="wwww",
                    colors=(0, 0),
                    frags=0,
                    ping=0,
                ),
            ],
        ),
    ]
