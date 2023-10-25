from demo_scraper.pkg import title
from demo_scraper.services.supab.player import Player


def describe_from_mode_and_players():
    players = [
        Player(name="alpha", team="red"),
        Player(name="beta", team="red"),
        Player(name="tot_gamma", team="blue"),
        Player(name="tot_delta", team="blue"),
    ]

    def test_ffa():
        assert (
            title.from_mode_and_players("ffa", players)
            == "alpha, beta, tot_delta, tot_gamma"
        )

    def test_xonx():
        assert (
            title.from_mode_and_players("2on2", players)
            == "blue (delta, gamma) vs red (alpha, beta)"
        )
        assert (
            title.from_mode_and_players("4on4", players)
            == "blue (delta, gamma) vs red (alpha, beta)"
        )
        assert (
            title.from_mode_and_players("2on2", players[0:3])
            == "blue (tot_gamma) vs red (alpha, beta)"
        )

    def test_1on1():
        assert title.from_mode_and_players("1on1", players[0:2]) == "alpha vs beta"

    def test_race():
        assert title.from_mode_and_players("race", players[0:1]) == "alpha"
        assert (
            title.from_mode_and_players("race", players)
            == "alpha, beta, tot_delta, tot_gamma"
        )
