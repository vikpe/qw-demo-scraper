from demo_scraper.pkg.mvdparser import Player

from services.supab.participants import (
    is_valid_mvd_player,
    parse_mvd_players,
)


def test_is_valid_player():
    assert not is_valid_mvd_player(Player(name=""))
    assert not is_valid_mvd_player(Player(name="dough", frags=5, distance_moved=0))
    assert is_valid_mvd_player(Player(name="XantoM", frags=0, distance_moved=100))


def test_parse_players():
    players = [
        Player(name="", name_raw=""),
        Player(name="XantoM", name_raw="XantoM", distance_moved=100),
    ]
    parsed_players = parse_mvd_players(players)
    assert len(parsed_players) == 1
    assert parsed_players[0].name == "XantoM"
