import context

context.apply()
from vendor import analyze, mvdparser

human_player = mvdparser.Player(
    name="XantoM",
    team="red",
    top_color=4,
    bottom_color=3,
    frags=12,
    teamkills=0,
    deaths=2,
    suicides=1,
    ping=16,
)

bot_player = mvdparser.Player(
    name=": Timber",
    team="blue",
    top_color=0,
    bottom_color=0,
    frags=5,
    teamkills=0,
    deaths=1,
    suicides=2,
    ping=10,
)


def describe_reason_to_ignore_demo():
    def test_has_bots():
        info = analyze.Result(
            filepath="demo1.mvd",
            date="",
            duration=610,
            map="",
            serverinfo="",
            players=[human_player],
        )

        assert analyze.reason_to_ignore_demo(info, "1on1") is None

        info.players.append(bot_player)
        assert analyze.reason_to_ignore_demo(info, "1on1") == "has bots (: Timber)"

    def test_probably_aborted():
        info = analyze.Result(
            filepath="demo1.mvd",
            date="",
            duration=620,
            map="",
            serverinfo="",
            players=[human_player],
        )

        assert analyze.reason_to_ignore_demo(info, "1on1") is None

        info.duration = 72
        assert (
            analyze.reason_to_ignore_demo(info, "1on1")
            == "probably aborted (1 minutes, 12 seconds)"
        )

        info.duration = 12
        assert (
            analyze.reason_to_ignore_demo(info, "1on1")
            == "probably aborted (12 seconds)"
        )
