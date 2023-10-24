from demo_scraper.services.supab.team import Team, get_majority_color
from demo_scraper.services.supab.player import Player


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
                    name_color="www",
                    team="red",
                    team_color="www",
                    color=(4, 2),
                    frags=7,
                    ping=12,
                ),
                Player(
                    name="beta",
                    name_color="wwww",
                    team="red",
                    team_color="www",
                    color=(4, 2),
                    frags=5,
                    ping=12,
                ),
            ],
        )
        assert team.as_dict()["name"] == "red"

    def test_from_players():
        player_beta = Player(
            name="beta",
            name_color="wwww",
            team="red",
            team_color="www",
        )
        player_alpha = Player(
            name="alpha",
            name_color="wwwww",
            team="red",
            team_color="www",
        )
        player_gamma = Player(
            name="gamma",
            name_color="wwwww",
            team="blue",
            team_color="wwww",
        )
        teams = Team.from_players(
            [
                player_beta,
                player_alpha,
                player_gamma,
            ]
        )
        assert teams[0] == Team(
            name="red",
            name_color="www",
            players=[
                player_beta,
                player_alpha,
            ],
        )

        assert teams[1] == Team(
            name="blue",
            name_color="wwww",
            players=[
                player_gamma,
            ],
        )

    def test_get_color():
        team_red = Team(
            players=[
                Player(color=(4, 2)),
                Player(color=(4, 2)),
                Player(color=(13, 13)),
            ]
        )
        assert team_red.get_color() == (4, 2)

    def test_get_frags():
        teams = Team.from_players([Player(frags=1), Player(frags=2)])
        assert teams[0].get_frags() == 3

    def test_to_string():
        teams = Team.from_players(
            [Player(name="beta..", team="red"), Player(name="alpha..", team="red")]
        )
        assert teams[0].to_string() == "red (alpha.., beta..)"
        assert teams[0].to_string(strip_fixes=True) == "red (alpha, beta)"
