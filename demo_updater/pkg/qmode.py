import re


def is_teamplay(mode: str) -> bool:
    if mode == "1on1":
        return False

    return is_xonx(mode) or mode in ["ctf", "wipeout"]


def is_xonx(mode: str) -> bool:
    regex = r"(?:\d+on){1,}\d+"
    return re.search(regex, mode) is not None
