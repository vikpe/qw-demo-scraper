import context

context.apply()

from demo_scraper.pkg import qcharset


def test_to_plain_code():
    assert qcharset.to_plain_string(127) == ""


def test_raw_to_utf8():
    assert qcharset.raw_to_utf8(r"XantoM") == "XantoM"
    assert qcharset.raw_to_utf8(r" ParadokS") == "• ParadokS"
    assert qcharset.raw_to_utf8(r"ÆÕ/Anza") == "FU/Anza"
    assert qcharset.raw_to_utf8(r"maÃÌer") == "maCLer"
    assert qcharset.raw_to_utf8(r"áðbogo") == "[ap]•bogo"


def test_raw_to_color_codes():
    assert qcharset.raw_to_color_codes(r"XantoM") == "wwwwww"
    assert qcharset.raw_to_color_codes(r" ParadokS") == "wwwwwwwwww"
    assert qcharset.raw_to_color_codes(r"ÆÕ/Anza") == "bbwwwww"
    assert qcharset.raw_to_color_codes(r"maÃÌer") == "wwbbww"
    assert qcharset.raw_to_color_codes(r"áðbogo") == "gbbgbwwww"
