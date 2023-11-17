from demo_scraper.pkg import parse


def test_parse_hostport():
    assert parse.hostport("quake.se:28501") == "quake.se:28501"
    assert parse.hostport("QUAKE.SE:28501") == "quake.se:28501"
    assert parse.hostport("dm6.uk:28503 (ANTILAG)") == "dm6.uk:28503"
    assert parse.hostport("QUAKE.SE KTX:28503") == "quake.se:28503"
    assert parse.hostport("de.quake.world:27502 [QW-Group]") == "de.quake.world:27502"
    assert parse.hostport("la.quake.world:28501 NAQW") == "la.quake.world:28501"
