import context

context.apply()

from vendor import qstring


def test_prefix():
    assert qstring.get_prefix(["• alpha", "• beta"]) == "• "
    assert qstring.get_prefix(["a.alpha", "a.beta"]) == "a."
    assert qstring.get_prefix(["dc•alpha", "dc•beta"]) == "dc•"
    assert qstring.get_prefix(["••••alpha", "••••beta"]) == "••••"
    assert qstring.get_prefix(["••alpha", "••beta"]) == "••"
    assert qstring.get_prefix(["dc•alpha", "dc•alphabet"]) == "dc•"
    assert qstring.get_prefix([".alpha", ".beta"]) == "."
    assert qstring.get_prefix(["::: alpha", ":::    beta"]) == "::: "
    assert qstring.get_prefix(["---a", "---"]) == "---"


def test_suffix():
    assert qstring.get_suffix(["alpha •", "beta •"]) == " •"
    assert qstring.get_suffix(["alpha.a", "beta.a"]) == ".a"
    assert qstring.get_suffix(["alpha•dc", "beta•dc"]) == "•dc"
    assert qstring.get_suffix(["alpha••••", "beta••••"]) == "••••"
    assert qstring.get_suffix(["alpha••", "beta••"]) == "••"
    assert qstring.get_suffix(["alpha•dc", "alphabet•dc"]) == "•dc"
    assert qstring.get_suffix(["alpha.", "beta."]) == "."
    assert qstring.get_suffix(["a---", "---"]) == "---"
    assert qstring.get_suffix(["alpha :::", "beta     :::"]) == " :::"


def describe_strip_fixes():
    def test_prefix():
        assert qstring.strip_fixes(["• alpha", "• beta"]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["a.alpha", "a.beta"]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["dc•alpha", "dc•beta"]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["••••alpha", "••••beta"]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["••alpha", "••beta"]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["dc•alpha", "dc•alphabet"]) == ["alpha", "alphabet"]
        assert qstring.strip_fixes([".alpha", ".beta"]) == [".alpha", ".beta"]
        assert qstring.strip_fixes(["::: alpha", ":::    beta"]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["---a", "---"]) == ["---a", "---"]

    def test_suffix():
        assert qstring.strip_fixes(["alpha •", "beta •"]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["alpha.a", "beta.a"]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["alpha•dc", "beta•dc"]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["alpha••••", "beta••••"]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["alpha••", "beta••"]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["alpha•dc", "alphabet•dc"]) == ["alpha", "alphabet"]
        assert qstring.strip_fixes(["alpha.", "beta."]) == ["alpha.", "beta."]
        assert qstring.strip_fixes(["a---", "---"]) == ["a---", "---"]
        assert qstring.strip_fixes(["alpha :::", "beta     :::"]) == ["alpha", "beta"]

    def test_prefix_and_suffix():
        assert qstring.strip_fixes(["a.alpha.b", "a.beta.b"]) == ["alpha", "beta"]
        assert qstring.strip_fixes([".alpha.", ".beta."]) == [".alpha.", ".beta."]
        assert qstring.strip_fixes(["||alpha--", "||beta--"]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["))alpha((", "))beta(("]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["__alpha..", "__beta.."]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["•••alpha•••", "•••beta•••"]) == ["alpha", "beta"]
        assert qstring.strip_fixes(["•••a•••", "•••"]) == ["•••a•••", "•••"]

    def test_misc():
        # too short
        assert qstring.strip_fixes([".a", ".b"]) == [".a", ".b"]
        assert qstring.strip_fixes(["a", "b"]) == ["a", "b"]

        # mixed prefixes
        assert qstring.strip_fixes(["alpha", "• beta", "• gamma"]) == [
            "alpha",
            "• beta",
            "• gamma",
        ]

        # single value
        assert qstring.strip_fixes(["...alpha"]) == ["...alpha"]
        assert qstring.strip_fixes(["alpha..."]) == ["alpha..."]

        # no delimiter
        assert qstring.strip_fixes(["alpha", "beta"]) == ["alpha", "beta"]
