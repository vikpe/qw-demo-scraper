import context

context.apply()
from demo_scraper.pkg import analyze, mvdparser

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
        info = analyze.MvdInfo(
            filepath="demo1.mvd",
            date="",
            duration=610,
            map="",
            serverinfo=r"\mode\1on1",
            players=[human_player],
        )

        assert analyze.reason_to_ignore_demo(info) is None

        info.players.append(bot_player)
        assert analyze.reason_to_ignore_demo(info) == "has bots (: Timber)"

    def test_probably_aborted():
        info = analyze.MvdInfo(
            filepath="demo1.mvd",
            date="",
            duration=620,
            map="",
            serverinfo=r"\mode\1on1",
            players=[human_player],
        )

        assert analyze.reason_to_ignore_demo(info) is None

        info.duration = 72
        assert (
            analyze.reason_to_ignore_demo(info)
            == "probably aborted (1 minutes, 12 seconds)"
        )

        info.duration = 12
        assert analyze.reason_to_ignore_demo(info) == "probably aborted (12 seconds)"

    def test_dmm4():
        info = analyze.MvdInfo(
            filepath="demo1.mvd",
            date="",
            duration=620,
            map="",
            serverinfo=r"\mode\1on1\deathmatch\4",
            players=[human_player],
        )
        assert analyze.reason_to_ignore_demo(info) == "dmm4"
