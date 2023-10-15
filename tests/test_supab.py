import context

context.apply()

from pkg.mvdparser import Player
from services import supab


def zdescribe_participants():
    def ztest_as_dict():
        participants = supab.Participants(
            players=[Player(name="foo"), Player(name="bar")],
            teams=[],
            player_count=2,
        )
        assert participants.as_dict() == {
            "players": [{"name": "foo"}, {"name": "bar"}],
            "teams": [],
            "player_count": 2,
        }
