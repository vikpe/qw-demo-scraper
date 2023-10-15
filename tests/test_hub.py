import responses
from responses import matchers

import context

context.apply()

from vendor import hub
from vendor.hub import Demo


def test_mode():
    assert Demo(filename="alpha.mvd.json").get_mode() == "unknown"
    assert Demo(filename="duel_20211012-2359.mvd.json").get_mode() == "1on1"
    assert Demo(filename="2on2_20211012-2359.mvd.json").get_mode() == "2on2"
    assert Demo(filename="4on4_20211012-2359.mvd.json").get_mode() == "4on4"
    assert Demo(filename="ffa_20211012-2359.mvd.json").get_mode() == "ffa"
    assert Demo(filename="race_20211012-2359.mvd.json").get_mode() == "race"
    assert Demo(filename="10on10_20211012-2359.mvd.json").get_mode() == "10on10"
    assert Demo(filename="2on2on2_20211012-2359.mvd.json").get_mode() == "2on2on2"


def describe_get_demos():
    @responses.activate
    def test_error():
        responses.get(
            url="https://hubapi.quakeworld.nu/v2/demos",
            match=[matchers.query_param_matcher({"mode": "duel", "limit": 2})],
            json=["error"],
        )
        assert hub.get_demos("1on1", 2) == []

    @responses.activate
    def test_success():
        responses.get(
            url="https://hubapi.quakeworld.nu/v2/demos",
            match=[matchers.query_param_matcher({"mode": "duel", "limit": 2})],
            json=[{"filename": "duel_20211012-2359.mvd.json"}],
        )
        demos = hub.get_demos("1on1", 2)
        assert demos[0].filename == "duel_20211012-2359.mvd.json"
