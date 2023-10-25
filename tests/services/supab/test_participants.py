from demo_scraper.pkg.mvdparser import Player as MvdPlayer
from demo_scraper.services.supab.participants import (
    is_valid_mvd_player,
    mvd_players_to_db_players,
)
from demo_scraper.services.supab.player import Player as DbPlayer


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
