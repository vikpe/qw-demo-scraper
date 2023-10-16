import context

context.apply()

from demo_scraper.services import supab, hub
from demo_scraper.pkg import demo_calc

calc_missing = demo_calc.calc_missing_demos


def describe_calc_missing_demos():
    def test_no_server_demos():
        db_demos = []
        server_demos = []

        assert (
            calc_missing(
                db_demos,
                server_demos,
                keep_count=10,
            )
            == []
        )

    def test_no_demos_in_database():
        db_demos = []
        server_demos = [
            hub.Demo(filename="demo3.mvd", time="3"),
            hub.Demo(filename="demo2.mvd", time="2"),
            hub.Demo(filename="demo1.mvd", time="1"),
        ]

        # not restricted by limit
        assert (
            calc_missing(
                db_demos,
                server_demos,
                keep_count=10,
            )
            == server_demos
        )

        # restricted by limit
        assert calc_missing(
            db_demos,
            server_demos,
            keep_count=1,
        ) == [hub.Demo(filename="demo3.mvd", time="3")]

    def test_all_newer():
        db_demos = [
            supab.Demo(filename="demo3.mvd", timestamp="3"),
            supab.Demo(filename="demo2.mvd", timestamp="2"),
            supab.Demo(filename="demo1.mvd", timestamp="1"),
        ]
        server_demos = [
            hub.Demo(filename="demo6.mvd", time="6"),
            hub.Demo(filename="demo5.mvd", time="5"),
            hub.Demo(filename="demo4.mvd", time="4"),
        ]

        assert (
            calc_missing(
                db_demos,
                server_demos,
                keep_count=3,
            )
            == server_demos
        )

    def test_all_older():
        db_demos = [
            supab.Demo(filename="demo6.mvd", timestamp="6"),
            supab.Demo(filename="demo5.mvd", timestamp="5"),
            supab.Demo(filename="demo4.mvd", timestamp="4"),
        ]
        server_demos = [
            hub.Demo(filename="demo3.mvd", time="3"),
            hub.Demo(filename="demo2.mvd", time="2"),
            hub.Demo(filename="demo1.mvd", time="1"),
        ]

        assert (
            calc_missing(
                db_demos,
                server_demos,
                keep_count=3,
            )
            == []
        )

    def test_mixed():
        db_demos = [
            supab.Demo(filename="demo10.mvd", timestamp="10"),
            supab.Demo(filename="demo09.mvd", timestamp="09"),
            supab.Demo(filename="demo08.mvd", timestamp="08"),
            supab.Demo(filename="demo06.mvd", timestamp="06"),
            supab.Demo(filename="demo05.mvd", timestamp="05"),
            supab.Demo(filename="demo04.mvd", timestamp="04"),
            supab.Demo(filename="demo01.mvd", timestamp="01"),
        ]
        server_demos = [
            hub.Demo(filename="demo12.mvd", time="12"),
            hub.Demo(filename="demo11.mvd", time="11"),
            hub.Demo(filename="demo09.mvd", time="09"),
            hub.Demo(filename="demo08.mvd", time="08"),
            hub.Demo(filename="demo07.mvd", time="07"),
            hub.Demo(filename="demo03.mvd", time="03"),
            hub.Demo(filename="demo02.mvd", time="02"),
            hub.Demo(filename="demo01.mvd", time="01"),
        ]

        assert calc_missing(
            db_demos,
            server_demos,
            keep_count=1,
        ) == [
            hub.Demo(filename="demo12.mvd", time="12"),
        ]

        assert calc_missing(
            db_demos,
            server_demos,
            keep_count=3,
        ) == [
            hub.Demo(filename="demo12.mvd", time="12"),
            hub.Demo(filename="demo11.mvd", time="11"),
        ]

        assert calc_missing(
            db_demos,
            server_demos,
            keep_count=999,
        ) == [
            hub.Demo(filename="demo12.mvd", time="12"),
            hub.Demo(filename="demo11.mvd", time="11"),
            hub.Demo(filename="demo07.mvd", time="07"),
            hub.Demo(filename="demo03.mvd", time="03"),
            hub.Demo(filename="demo02.mvd", time="02"),
        ]
