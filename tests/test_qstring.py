import context

context.apply()

from demo_scraper.pkg.qstring import get_prefix, get_suffix, strip_fixes


def test_prefix():
    assert get_prefix(["• alpha", "• beta"]) == "• "
    assert get_prefix(["a.alpha", "a.beta"]) == "a."
    assert get_prefix(["dc•alpha", "dc•beta"]) == "dc•"
    assert get_prefix(["••••alpha", "••••beta"]) == "••••"
    assert get_prefix(["••alpha", "••beta"]) == "••"
    assert get_prefix(["dc•alpha", "dc•alphabet"]) == "dc•"
    assert get_prefix([".alpha", ".beta"]) == "."
    assert get_prefix(["::: alpha", ":::    beta"]) == "::: "
    assert get_prefix(["---a", "---"]) == "---"


def test_suffix():
    assert get_suffix(["alpha •", "beta •"]) == " •"
    assert get_suffix(["alpha.a", "beta.a"]) == ".a"
    assert get_suffix(["alpha•dc", "beta•dc"]) == "•dc"
    assert get_suffix(["alpha••••", "beta••••"]) == "••••"
    assert get_suffix(["alpha••", "beta••"]) == "••"
    assert get_suffix(["alpha•dc", "alphabet•dc"]) == "•dc"
    assert get_suffix(["alpha.", "beta."]) == "."
    assert get_suffix(["a---", "---"]) == "---"
    assert get_suffix(["alpha :::", "beta     :::"]) == " :::"


def describe_strip_fixes():
    def test_prefix():
        assert strip_fixes(["• alpha", "• beta"]) == ["alpha", "beta"]
        assert strip_fixes(["a.alpha", "a.beta"]) == ["alpha", "beta"]
        assert strip_fixes(["dc•alpha", "dc•beta"]) == ["alpha", "beta"]
        assert strip_fixes(["••••alpha", "••••beta"]) == ["alpha", "beta"]
        assert strip_fixes(["••alpha", "••beta"]) == ["alpha", "beta"]
        assert strip_fixes(["dc•alpha", "dc•alphabet"]) == ["alpha", "alphabet"]
        assert strip_fixes([".alpha", ".beta"]) == [".alpha", ".beta"]
        assert strip_fixes(["::: alpha", ":::    beta"]) == ["alpha", "beta"]
        assert strip_fixes(["---a", "---"]) == ["---a", "---"]

    def test_suffix():
        assert strip_fixes(["alpha •", "beta •"]) == ["alpha", "beta"]
        assert strip_fixes(["alpha.a", "beta.a"]) == ["alpha", "beta"]
        assert strip_fixes(["alpha•dc", "beta•dc"]) == ["alpha", "beta"]
        assert strip_fixes(["alpha••••", "beta••••"]) == ["alpha", "beta"]
        assert strip_fixes(["alpha••", "beta••"]) == ["alpha", "beta"]
        assert strip_fixes(["alpha•dc", "alphabet•dc"]) == ["alpha", "alphabet"]
        assert strip_fixes(["alpha.", "beta."]) == ["alpha.", "beta."]
        assert strip_fixes(["a---", "---"]) == ["a---", "---"]
        assert strip_fixes(["alpha :::", "beta     :::"]) == ["alpha", "beta"]

    def test_prefix_and_suffix():
        assert strip_fixes(["a.alpha.b", "a.beta.b"]) == ["alpha", "beta"]
        assert strip_fixes([".alpha.", ".beta."]) == [".alpha.", ".beta."]
        assert strip_fixes(["||alpha--", "||beta--"]) == ["alpha", "beta"]
        assert strip_fixes(["))alpha((", "))beta(("]) == ["alpha", "beta"]
        assert strip_fixes(["__alpha..", "__beta.."]) == ["alpha", "beta"]
        assert strip_fixes(["•••alpha•••", "•••beta•••"]) == ["alpha", "beta"]
        assert strip_fixes(["•••a•••", "•••"]) == ["•••a•••", "•••"]

    def test_misc():
        # too short
        assert strip_fixes([".a", ".b"]) == [".a", ".b"]
        assert strip_fixes(["a", "b"]) == ["a", "b"]

        # mixed prefixes
        assert strip_fixes(["alpha", "• beta", "• gamma"]) == [
            "alpha",
            "• beta",
            "• gamma",
        ]

        # single value
        assert strip_fixes(["...alpha"]) == ["...alpha"]
        assert strip_fixes(["alpha..."]) == ["alpha..."]

        # no delimiter
        assert strip_fixes(["alpha", "beta"]) == ["alpha", "beta"]
