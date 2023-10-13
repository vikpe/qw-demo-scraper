import os

from context import mvdparser


def get_path(filename: str) -> str:
    test_path = os.path.abspath(os.path.dirname(__file__))
    return f"{test_path}/files/{filename}"


def ztest_is_teamplay_mode():
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
    def test_participants_1on1():
        file_path = get_path(
            "duel_packetlossking_vs_[pikachu][bravado]231013-0406.mvd.json"
        )

        parse_result = mvdparser.from_file(file_path)
        assert parse_result.participants("1on1") == {
            "teams": [],
            "players": [
                {
                    "name": "_pikachu_",
                    "team": "red",
                    "top_color": 4,
                    "bottom_color": 4,
                    "frags": 10,
                    "teamkills": 0,
                    "deaths": 68,
                    "suicides": 3,
                    "ping": 39,
                },
                {
                    "name": "PacketLossKing",
                    "team": "blue",
                    "top_color": 13,
                    "bottom_color": 13,
                    "frags": 63,
                    "teamkills": 0,
                    "deaths": 15,
                    "suicides": 2,
                    "ping": 41,
                },
            ],
            "player_count": 2,
        }


def test_participants_teamplay():
    file_path = get_path("2on2_blue_vs_red[aerowalk]20231012-2359.mvd.json")
    parse_result = mvdparser.from_file(file_path)
    assert parse_result.participants("2on2") == {
        "teams": [
            {
                "name": "blue",
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
                "players": [
                    {
                        "name": "en_karl",
                        "team": "red",
                        "top_color": 4,
                        "bottom_color": 4,
                        "frags": 51,
                        "teamkills": 3,
                        "deaths": 31,
                        "suicides": 2,
                        "ping": 25,
                    },
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
                ],
                "frags": 61,
                "top_color": 4,
                "bottom_color": 4,
            },
        ],
        "players": [],
        "player_count": 4,
    }
