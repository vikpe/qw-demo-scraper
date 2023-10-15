import os

import context

context.apply()

from vendor import mvdparser


def get_path(filename: str) -> str:
    test_path = os.path.abspath(os.path.dirname(__file__))
    return f"{test_path}/files/{filename}"


def test_parse_ping_str():
    assert mvdparser.to_int(None) == 0
    assert mvdparser.to_int("0") == 0
    assert mvdparser.to_int("25") == 25
    assert mvdparser.to_int("25.4") == 25
    assert mvdparser.to_int("25.6") == 26


def test_is_teamplay_mode():
    assert mvdparser.is_teamplay_mode("10on10")
    assert mvdparser.is_teamplay_mode("2on2")
    assert mvdparser.is_teamplay_mode("2on2on2")
    assert mvdparser.is_teamplay_mode("4on4")
    assert mvdparser.is_teamplay_mode("ctf")
    assert mvdparser.is_teamplay_mode("wipeout")
    assert not mvdparser.is_teamplay_mode("1on1")
    assert not mvdparser.is_teamplay_mode("ffa")


def test_get_team_color():
    assert mvdparser.get_team_color([]) == (0, 0)
    assert mvdparser.get_team_color([(1, 2), (3, 4)]) == (1, 2)
    assert mvdparser.get_team_color([(1, 2), (3, 4), (5, 6)]) == (1, 2)
    assert mvdparser.get_team_color([(1, 2), (3, 4), (1, 2)]) == (1, 2)


def describe_parse_result():
    def test_teams():
        file_path = get_path("2on2_blue_vs_red[aerowalk]20231012-2359.mvd.json")
        parse_result = mvdparser.Result.from_file(file_path)
        assert parse_result.teams() == [
            {
                "name": "blue",
                "player_prefix": "",
                "player_suffix": "",
                "players": [
                    {
                        "name": "Dadi",
                        "team": "blue",
                        "top_color": 12,
                        "bottom_color": 13,
                        "frags": 15,
                        "teamkills": 0,
                        "deaths": 46,
                        "suicides": 1,
                        "ping": 12,
                    },
                    {
                        "name": "xaan",
                        "team": "blue",
                        "top_color": 13,
                        "bottom_color": 13,
                        "frags": 27,
                        "teamkills": 2,
                        "deaths": 35,
                        "suicides": 3,
                        "ping": 13,
                    },
                ],
                "frags": 42,
                "top_color": 12,
                "bottom_color": 13,
            },
            {
                "name": "red",
                "player_prefix": "ToT_",
                "player_suffix": "",
                "players": [
                    {
                        "name": "ToT_Belgarath",
                        "team": "red",
                        "top_color": 4,
                        "bottom_color": 4,
                        "frags": 10,
                        "teamkills": 3,
                        "deaths": 31,
                        "suicides": 5,
                        "ping": 14,
                    },
                    {
                        "name": "ToT_en_karl",
                        "team": "red",
                        "top_color": 4,
                        "bottom_color": 4,
                        "frags": 51,
                        "teamkills": 3,
                        "deaths": 31,
                        "suicides": 2,
                        "ping": 25,
                    },
                ],
                "frags": 61,
                "top_color": 4,
                "bottom_color": 4,
            },
        ]

    def describe_to_title():
        def test_ffa():
            file_path = get_path("2on2_blue_vs_red[aerowalk]20231012-2359.mvd.json")
            info = mvdparser.Result.from_file(file_path)
            info.serverinfo.mode = "ffa"
            assert info.title() == "ffa: Dadi, ToT_Belgarath, ToT_en_karl, xaan"

        def test_xonx():
            file_path = get_path("2on2_blue_vs_red[aerowalk]20231012-2359.mvd.json")
            info = mvdparser.Result.from_file(file_path)
            info.serverinfo.mode = "2on2"
            assert info.title() == "blue (Dadi, xaan) vs red (Belgarath, en_karl)"

        def test_1on1():
            file_path = get_path(
                "duel_packetlossking_vs_[pikachu][bravado]231013-0406.mvd.json"
            )
            info = mvdparser.Result.from_file(file_path)
            info.serverinfo.mode = "1on1"
            assert info.title() == "_pikachu_ vs PacketLossKing"

        def test_race():
            file_path = get_path("2on2_blue_vs_red[aerowalk]20231012-2359.mvd.json")
            info = mvdparser.Result.from_file(file_path)
            info.serverinfo.mode = "race"
            assert info.title() == "Dadi, ToT_Belgarath, ToT_en_karl, xaan"
