from demo_scraper.pkg.mvdparser import (
    MvdInfo,
    Player,
    to_int,
)
from demo_scraper.pkg.server_info import ServerInfo


def test_parse_ping_str():
    assert to_int(None) == 0
    assert to_int("0") == 0
    assert to_int("25") == 25
    assert to_int("25.4") == 25
    assert to_int("25.6") == 26


def describe_player():
    def test_as_dict():
        player = Player(
            name="beta",
            name_raw="beta",
            team="red",
            team_raw="red",
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
            "name_raw": "beta",
            "team": "red",
            "team_raw": "red",
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
        file_path = "tests/files/2on2_blue_vs_red[aerowalk]20231012-2359.mvd.json"
        info = MvdInfo.from_file(file_path)

        assert info.filepath == "2on2_blue_vs_red[aerowalk]20231012-2359.mvd"
        assert info.date == "2023-10-13 0:0"
        assert info.duration == 610.158
        assert info.map == "aerowalk"
        assert info.hostname == "quake.se:28501"

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
                name="xaan",
                name_raw="xaan",
                team="blue",
                team_raw="blue",
                top_color=13,
                bottom_color=13,
                frags=27,
                teamkills=2,
                deaths=35,
                suicides=3,
                ping=13,
                distance_moved=100,
            ),
            Player(
                name="ToT_en_karl",
                name_raw="ToT_en_karl",
                team="red",
                team_raw="red",
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
                name="Dadi",
                name_raw="Dadi",
                team="blue",
                team_raw="blue",
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
                name_raw="ToT_Belgarath",
                team="red",
                team_raw="red",
                top_color=4,
                bottom_color=4,
                frags=10,
                teamkills=3,
                deaths=31,
                suicides=5,
                ping=14,
                distance_moved=100,
            ),
        ]
