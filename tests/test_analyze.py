from context import analyze, mvdparser

human_player = mvdparser.Player(
    name="XantoM",
    team="red",
    top_color=4,
    bottom_color=3,
    frags=12,
    teamkills=0,
    deaths=2,
    suicides=1,
    ping="16",
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
    ping="10",
)


def describe_reason_to_skip_demo():
    def test_game_in_progress():
        info = analyze.ParseResult(
            filepath="demo1.mvd", date="", duration=0, map="", serverinfo="", players=[]
        )

        assert analyze.reason_to_skip_demo(info) == "game in progress"

    def test_has_bots():
        info = analyze.ParseResult(
            filepath="demo1.mvd",
            date="",
            duration=610,
            map="",
            serverinfo="",
            players=[human_player],
        )

        # no bots
        assert analyze.reason_to_skip_demo(info) is None

        # has bots
        info.players.append(bot_player)
        assert analyze.reason_to_skip_demo(info) == "has bots"
