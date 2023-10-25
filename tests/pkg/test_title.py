from demo_scraper.pkg import title
from demo_scraper.services.supab.player import Player
from demo_scraper.services.supab.team import Team


def test_from_mode_and_teams():
    teams = [
        Team(
            name="red",
            players=[
                Player(name="alpha"),
                Player(name="beta"),
            ],
        ),
        Team(
            name="tot",
            players=[
                Player(name="tot_gamma"),
                Player(name="tot_delta"),
            ],
        ),
    ]

    assert title.from_teams(teams) == "red (alpha, beta) vs tot (delta, gamma)"


def describe_from_mode_and_players():
    players = [
        Player(name="alpha"),
        Player(name="beta"),
        Player(name="tot_gamma"),
        Player(name="tot_delta"),
    ]

    def test_ffa():
        assert (
            title.from_mode_and_players("ffa", players)
            == "alpha, beta, tot_delta, tot_gamma"
        )

    def test_1on1():
        assert title.from_mode_and_players("1on1", players[0:2]) == "alpha vs beta"

    def test_race():
        assert title.from_mode_and_players("race", players[0:1]) == "alpha"
        assert (
            title.from_mode_and_players("race", players)
            == "alpha, beta, tot_delta, tot_gamma"
        )
