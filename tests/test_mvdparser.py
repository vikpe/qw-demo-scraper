import context
from context import get_testfile_path
from demo_scraper.pkg.server_info import ServerInfo

context.apply()

from demo_scraper.pkg.mvdparser import (
    MvdInfo,
    Player,
    Team,
    get_majority_color,
    is_valid_player,
    parse_players,
    to_int,
)


def test_parse_ping_str():
    assert to_int(None) == 0
    assert to_int("0") == 0
    assert to_int("25") == 25
    assert to_int("25.4") == 25
    assert to_int("25.6") == 26


def test_get_team_color():
    assert get_majority_color([]) == (0, 0)
    assert get_majority_color([(1, 2), (3, 4)]) == (1, 2)
    assert get_majority_color([(1, 2), (3, 4), (5, 6)]) == (1, 2)
    assert get_majority_color([(1, 2), (3, 4), (1, 2)]) == (1, 2)


def test_is_valid_player():
    assert not is_valid_player(Player(name=""))
    assert not is_valid_player(Player(name="dough", frags=5, distance_moved=0))
    assert is_valid_player(Player(name="XantoM", frags=0, distance_moved=100))


def describe_parse_players():
    players = [Player(name=""), Player(name="XantoM", distance_moved=100)]
    converted_players = parse_players(players)
    assert len(converted_players) == 1
    assert converted_players[0].name == "XantoM"


def describe_team():
    def test_as_dict():
        team = Team(
            name="red",
            players=[
                Player(
                    name="alpha",
                    team="red",
                    top_color=4,
                    bottom_color=2,
                    frags=7,
                    distance_moved=100,
                ),
                Player(
                    name="beta",
                    team="red",
                    top_color=4,
                    bottom_color=2,
                    frags=5,
                    distance_moved=50,
                ),
            ],
        )
        assert team.as_dict() == {
            "name": "red",
            "top_color": 4,
            "bottom_color": 2,
            "frags": 12,
            "players": [
                {
                    "name": "alpha",
                    "team": "red",
                    "top_color": 4,
                    "bottom_color": 2,
                    "frags": 7,
                    "deaths": 0,
                    "suicides": 0,
                    "teamkills": 0,
                    "ping": 0,
                    "distance_moved": 100,
                },
                {
                    "name": "beta",
                    "team": "red",
                    "top_color": 4,
                    "bottom_color": 2,
                    "frags": 5,
                    "deaths": 0,
                    "suicides": 0,
                    "teamkills": 0,
                    "ping": 0,
                    "distance_moved": 50,
                },
            ],
        }

    def test_from_players():
        teams = Team.from_players(
            [
                Player(name="beta", team="red"),
                Player(name="alpha", team="red"),
                Player(name="gamma", team="blue"),
            ]
        )
        assert teams[0] == Team(
            name="red",
            players=[
                Player(name="beta", team="red"),
                Player(name="alpha", team="red"),
            ],
        )
        assert teams[1] == Team(
            name="blue",
            players=[
                Player(name="gamma", team="blue"),
            ],
        )

    def test_get_color():
        teams = Team.from_players(
            [
                Player(top_color=4, bottom_color=2),
                Player(top_color=4, bottom_color=2),
                Player(top_color=13, bottom_color=13),
            ]
        )
        assert teams[0].get_color() == (4, 2)

    def test_get_frags():
        teams = Team.from_players([Player(frags=1), Player(frags=2)])
        assert teams[0].get_frags() == 3

    def test_to_string():
        teams = Team.from_players(
            [Player(name="beta..", team="red"), Player(name="alpha..", team="red")]
        )
        assert teams[0].to_string() == "red (alpha.., beta..)"
        assert teams[0].to_string(strip_fixes=True) == "red (alpha, beta)"


def describe_player():
    def test_as_dict():
        player = Player(
            name="beta",
            team="red",
            top_color=4,
            bottom_color=2,
            frags=1,
            teamkills=2,
            deaths=3,
            suicides=4,
            ping=5,
            distance_moved=100,
        )
        assert player.as_dict() == {
            "name": "beta",
            "team": "red",
            "top_color": 4,
            "bottom_color": 2,
            "frags": 1,
            "teamkills": 2,
            "deaths": 3,
            "suicides": 4,
            "ping": 5,
            "distance_moved": 100,
        }


def describe_mvd_info():
    def test_from_file():
        file_path = get_testfile_path(
            "2on2_blue_vs_red[aerowalk]20231012-2359.mvd.json"
        )
        info = MvdInfo.from_file(file_path)

        assert info.filepath == "2on2_blue_vs_red[aerowalk]20231012-2359.mvd"
        assert info.date == "2023-10-13 0:0"
        assert info.duration == 610.158
        assert info.map == "aerowalk"

        assert (
            info.serverinfo.as_dict()
            == ServerInfo(
                admin="suom1 <suom1@irc.ax>",
                deathmatch=3,
                gamedir="qw",
                ktxver="1.42",
                map="aerowalk",
                maxclients=4,
                maxfps=77,
                maxspectators=6,
                mode="2on2",
                pm_ktjump=1,
                progs="so",
                qvm="so",
                sv_antilag=2,
                teamplay=2,
                timelimit=10,
                version="MVDSV 0.36",
                z_ext="511",
            ).as_dict()
        )
        assert info.players == [
            Player(
                name="Dadi",
                team="blue",
                top_color=12,
                bottom_color=13,
                frags=15,
                teamkills=0,
                deaths=46,
                suicides=1,
                ping=12,
                distance_moved=100,
            ),
            Player(
                name="ToT_Belgarath",
                team="red",
                top_color=4,
                bottom_color=4,
                frags=10,
                teamkills=3,
                deaths=31,
                suicides=5,
                ping=14,
                distance_moved=100,
            ),
            Player(
                name="ToT_en_karl",
                team="red",
                top_color=4,
                bottom_color=4,
                frags=51,
                teamkills=3,
                deaths=31,
                suicides=2,
                ping=25,
                distance_moved=100,
            ),
            Player(
                name="xaan",
                team="blue",
                top_color=13,
                bottom_color=13,
                frags=27,
                teamkills=2,
                deaths=35,
                suicides=3,
                ping=13,
                distance_moved=100,
            ),
        ]
