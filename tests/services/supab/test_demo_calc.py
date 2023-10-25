from demo_scraper.services.hub import Demo as HubDemo
from demo_scraper.services.supab.demo import Demo as DbDemo
from demo_scraper.services.supab.demo_calc import calc_missing_demos


def describe_calc_missing_demos():
    def test_no_server_demos():
        db_demos = []
        server_demos = []

        assert (
            calc_missing_demos(
                db_demos,
                server_demos,
                keep_count=10,
            )
            == []
        )

    def test_no_demos_in_database():
        db_demos = []
        server_demos = [
            HubDemo(filename="demo3.mvd", time="3"),
            HubDemo(filename="demo2.mvd", time="2"),
            HubDemo(filename="demo1.mvd", time="1"),
        ]

        # not restricted by limit
        assert (
            calc_missing_demos(
                db_demos,
                server_demos,
                keep_count=10,
            )
            == server_demos
        )

        # restricted by limit
        assert calc_missing_demos(
            db_demos,
            server_demos,
            keep_count=1,
        ) == [HubDemo(filename="demo3.mvd", time="3")]

    def test_all_newer():
        db_demos = [
            DbDemo(filename="demo3.mvd", timestamp="3"),
            DbDemo(filename="demo2.mvd", timestamp="2"),
            DbDemo(filename="demo1.mvd", timestamp="1"),
        ]
        server_demos = [
            HubDemo(filename="demo6.mvd", time="6"),
            HubDemo(filename="demo5.mvd", time="5"),
            HubDemo(filename="demo4.mvd", time="4"),
        ]

        assert (
            calc_missing_demos(
                db_demos,
                server_demos,
                keep_count=3,
            )
            == server_demos
        )

    def test_all_older():
        db_demos = [
            DbDemo(filename="demo6.mvd", timestamp="6"),
            DbDemo(filename="demo5.mvd", timestamp="5"),
            DbDemo(filename="demo4.mvd", timestamp="4"),
        ]
        server_demos = [
            HubDemo(filename="demo3.mvd", time="3"),
            HubDemo(filename="demo2.mvd", time="2"),
            HubDemo(filename="demo1.mvd", time="1"),
        ]

        assert (
            calc_missing_demos(
                db_demos,
                server_demos,
                keep_count=3,
            )
            == []
        )

    def test_mixed():
        db_demos = [
            DbDemo(filename="demo10.mvd", timestamp="10"),
            DbDemo(filename="demo09.mvd", timestamp="09"),
            DbDemo(filename="demo08.mvd", timestamp="08"),
            DbDemo(filename="demo06.mvd", timestamp="06"),
            DbDemo(filename="demo05.mvd", timestamp="05"),
            DbDemo(filename="demo04.mvd", timestamp="04"),
            DbDemo(filename="demo01.mvd", timestamp="01"),
        ]
        server_demos = [
            HubDemo(filename="demo12.mvd", time="12"),
            HubDemo(filename="demo11.mvd", time="11"),
            HubDemo(filename="demo09.mvd", time="09"),
            HubDemo(filename="demo08.mvd", time="08"),
            HubDemo(filename="demo07.mvd", time="07"),
            HubDemo(filename="demo03.mvd", time="03"),
            HubDemo(filename="demo02.mvd", time="02"),
            HubDemo(filename="demo01.mvd", time="01"),
        ]

        assert calc_missing_demos(
            db_demos,
            server_demos,
            keep_count=1,
        ) == [
            HubDemo(filename="demo12.mvd", time="12"),
        ]

        assert calc_missing_demos(
            db_demos,
            server_demos,
            keep_count=3,
        ) == [
            HubDemo(filename="demo12.mvd", time="12"),
            HubDemo(filename="demo11.mvd", time="11"),
        ]

        assert calc_missing_demos(
            db_demos,
            server_demos,
            keep_count=999,
        ) == [
            HubDemo(filename="demo12.mvd", time="12"),
            HubDemo(filename="demo11.mvd", time="11"),
            HubDemo(filename="demo07.mvd", time="07"),
            HubDemo(filename="demo03.mvd", time="03"),
            HubDemo(filename="demo02.mvd", time="02"),
        ]
