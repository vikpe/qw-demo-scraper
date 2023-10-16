from os.path import commonprefix
from typing import List

DELIMITERS = '.•:"_-|[]{}() '
MIN_FIX_LENGTH = 2


def strip_fixes(names: List[str]) -> List[str]:
    if len(names) < 2:
        return names

    name_lengths = [len(name) for name in names]
    if any(len_ < MIN_FIX_LENGTH for len_ in name_lengths):
        return names

    prefix = get_prefix(names)
    prefix_len = len(prefix)
    if prefix_len >= MIN_FIX_LENGTH and not any(
        [plen <= prefix_len for plen in name_lengths]
    ):
        names = [name[prefix_len:] for name in names]

    suffix = get_suffix(names)
    suffix_len = len(suffix)
    if suffix_len >= MIN_FIX_LENGTH and not any(
        [slen <= suffix_len for slen in name_lengths]
    ):
        names = [name[:-suffix_len] for name in names]

    return [n.strip() for n in names]


def get_prefix(names: List[str]) -> str:
    prefix = commonprefix(names)

    delimiter_index = _get_last_delimiter_index(prefix, DELIMITERS)
    if delimiter_index == -1:
        return ""

    return prefix[0 : delimiter_index + 1]


def get_suffix(names: List[str]) -> str:
    return get_prefix([name[::-1] for name in names])[::-1]


def _get_last_delimiter_index(value: str, delimiters: str) -> int:
    last_index = -1

    for d in delimiters:
        if d in value:
            last_index = max(last_index, value.rindex(d))

    return last_index
