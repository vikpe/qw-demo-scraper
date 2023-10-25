from demo_scraper.services.supab.player import Player
from demo_scraper.services.supab.team import Team, get_majority_color


def test_get_majority_color():
    assert get_majority_color([]) == (0, 0)
    assert get_majority_color([(1, 2), (3, 4)]) == (1, 2)
    assert get_majority_color([(1, 2), (3, 4), (5, 6)]) == (1, 2)
    assert get_majority_color([(1, 2), (3, 4), (1, 2)]) == (1, 2)


def describe_team():
    def test_as_dict():
        team = Team(
            name="red",
            name_color="www",
            players=[
                Player(
                    name="alpha",
                    name_color="wwwww",
                    color=(4, 2),
                    frags=7,
                    ping=12,
                ),
                Player(
                    name="beta",
                    name_color="wwww",
                    color=(4, 2),
                    frags=5,
                    ping=25,
                ),
            ],
        )

        team_dict = team.as_dict()
        assert team_dict["name"] == "red"
        assert team_dict["name_color"] == "www"
        assert team_dict["color"] == [4, 2]
        assert team_dict["frags"] == 12
        assert len(team_dict["players"]) == 2
        assert team_dict["players"][0] == {
            "name": "alpha",
            "name_color": "wwwww",
            "frags": 7,
            "ping": 12,
        }

    def test_get_color():
        team = Team(
            players=[
                Player(color=(4, 2)),
                Player(color=(4, 2)),
                Player(color=(13, 13)),
            ]
        )
        assert team.get_color() == (4, 2)

    def test_get_frags():
        team = Team(players=[Player(frags=1), Player(frags=2)])
        assert team.get_frags() == 3

    def test_to_string():
        team = Team(
            name="red",
            players=[
                Player(name="beta___"),
                Player(name="alpha___"),
            ],
        )
        assert team.to_string() == "red (alpha___, beta___)"
        assert team.to_string(strip_fixes=True) == "red (alpha, beta)"
