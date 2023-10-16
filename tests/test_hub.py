import responses
from responses import matchers

import context

context.apply()

from demo_scraper.services import hub


def test_mode():
    assert hub.Demo(filename="alpha.mvd.json").get_mode() == "unknown"
    assert hub.Demo(filename="duel_20211012-2359.mvd.json").get_mode() == "1on1"
    assert hub.Demo(filename="2on2_20211012-2359.mvd.json").get_mode() == "2on2"
    assert hub.Demo(filename="4on4_20211012-2359.mvd.json").get_mode() == "4on4"
    assert hub.Demo(filename="ffa_20211012-2359.mvd.json").get_mode() == "ffa"
    assert hub.Demo(filename="race_20211012-2359.mvd.json").get_mode() == "race"
    assert hub.Demo(filename="10on10_20211012-2359.mvd.json").get_mode() == "10on10"
    assert hub.Demo(filename="2on2on2_20211012-2359.mvd.json").get_mode() == "2on2on2"


def describe_get_demos():
    @responses.activate
    def test_error():
        responses.get(
            url="https://hubapi.quakeworld.nu/v2/demos",
            match=[matchers.query_param_matcher({"mode": "duel", "limit": 2})],
            json="error",
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
