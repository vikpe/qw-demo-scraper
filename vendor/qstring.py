from os.path import commonprefix
from typing import List

DELIMITERS = '.•:"_-|[]{}() '
MIN_FIX_LENGTH = 2


def strip_fixes(names: List[str]) -> List[str]:
    if len(names) < 2:
        return names

    if any(len(name) < MIN_FIX_LENGTH for name in names):
        return names

    prefix = get_prefix(names)
    if prefix:
        names = [name[len(prefix) :] for name in names]

    suffix = get_suffix(names)
    if suffix:
        names = [name[: -len(suffix)] for name in names]

    return [n.strip() for n in names]


def get_prefix(names: List[str]) -> str:
    prefix = commonprefix(names)

    delimiter_index = _get_last_delimiter_index(prefix, DELIMITERS)
    if delimiter_index == -1:
        return ""

    prefix = prefix[0 : delimiter_index + 1]
    prefix_length = len(prefix)

    if prefix_length < MIN_FIX_LENGTH:
        return ""

    if any([len(name) <= prefix_length for name in names]):
        return ""

    return prefix[: delimiter_index + 1]


def get_suffix(names: List[str]) -> str:
    return get_prefix([name[::-1] for name in names])[::-1]


def _get_last_delimiter_index(value: str, delimiters: str) -> int:
    last_index = -1

    for d in delimiters:
        if d in value:
            last_index = max(last_index, value.rindex(d))

    return last_index
