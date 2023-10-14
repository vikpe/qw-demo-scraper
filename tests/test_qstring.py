from context import qstring

sf = qstring.strip_fixes


def describe_strip_fixes():
    def test_prefix():
        assert sf(["• alpha", "• beta"]) == ["alpha", "beta"]
        assert sf(["a.alpha", "a.beta"]) == ["alpha", "beta"]
        assert sf(["dc•alpha", "dc•beta"]) == ["alpha", "beta"]
        assert sf(["••••alpha", "••••beta"]) == ["alpha", "beta"]
        assert sf(["••alpha", "••beta"]) == ["alpha", "beta"]
        assert sf(["dc•alpha", "dc•alphabet"]) == ["alpha", "alphabet"]
        assert sf([".alpha", ".beta"]) == [".alpha", ".beta"]
        assert sf(["::: alpha", ":::    beta"]) == ["alpha", "beta"]
        assert sf(["---a", "---"]) == ["---a", "---"]

    def test_suffix():
        assert sf(["alpha •", "beta •"]) == ["alpha", "beta"]
        assert sf(["alpha.a", "beta.a"]) == ["alpha", "beta"]
        assert sf(["alpha•dc", "beta•dc"]) == ["alpha", "beta"]
        assert sf(["alpha••••", "beta••••"]) == ["alpha", "beta"]
        assert sf(["alpha••", "beta••"]) == ["alpha", "beta"]
        assert sf(["alpha•dc", "alphabet•dc"]) == ["alpha", "alphabet"]
        assert sf(["alpha.", "beta."]) == ["alpha.", "beta."]
        assert sf(["a---", "---"]) == ["a---", "---"]
        assert sf(["alpha :::", "beta     :::"]) == ["alpha", "beta"]

    def test_prefix_and_suffix():
        assert sf(["a.alpha.b", "a.beta.b"]) == ["alpha", "beta"]
        assert sf([".alpha.", ".beta."]) == [".alpha.", ".beta."]
        assert sf(["||alpha--", "||beta--"]) == ["alpha", "beta"]
        assert sf(["))alpha((", "))beta(("]) == ["alpha", "beta"]
        assert sf(["__alpha..", "__beta.."]) == ["alpha", "beta"]
        assert sf(["•••alpha•••", "•••beta•••"]) == ["alpha", "beta"]
        assert sf(["•••a•••", "•••"]) == ["•••a•••", "•••"]

    def test_misc():
        # too short
        assert sf([".a", ".b"]) == [".a", ".b"]
        assert sf(["a", "b"]) == ["a", "b"]

        # mixed prefixes
        assert sf(["alpha", "• beta", "• gamma"]) == ["alpha", "• beta", "• gamma"]

        # single value
        assert sf(["...alpha"]) == ["...alpha"]
        assert sf(["alpha..."]) == ["alpha..."]

        # no delimiter
        assert sf(["alpha", "beta"]) == ["alpha", "beta"]
