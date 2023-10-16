import context

context.apply()

from demo_updater.pkg.qmode import is_xonx, is_teamplay


def test_is_teamplay():
    assert is_teamplay("2on2")
    assert is_teamplay("2on2on2")
    assert is_teamplay("4on4")
    assert is_teamplay("ctf")
    assert is_teamplay("wipeout")
    assert not is_teamplay("1on1")
    assert not is_teamplay("duel")
    assert not is_teamplay("ffa")
    assert not is_teamplay("race")


def test_is_xonx():
    assert is_xonx("1on1")
    assert is_xonx("2on2")
    assert not is_xonx("ffa")
