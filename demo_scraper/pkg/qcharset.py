color_white = "w"
color_brown = "b"
color_gold = "g"

gold_codes = [
    16,
    16 + 128,
    17,
    17 + 128,  # braces
    5 + 128,
    14 + 128,
    15 + 128,
    28 + 128,  # dots
]

charset_top_rows = [
    "•",
    "",
    "",
    "",
    "",
    "•",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "•",
    "•",
    "[",
    "]",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "•",
    "",
    "",
    "",
]


def raw_to_utf8(raw: str) -> str:
    result = ""

    for code in map(ord, raw):
        result += to_plain_string(code)

    return result


def raw_to_color_codes(raw: str) -> str:
    result = ""

    for code in map(ord, raw):
        result += to_color_code(code)

    return result


def remove_color(code: int) -> int:
    return code & 0x7F


def to_plain_string(code: int) -> str:
    plain_code = remove_color(code)

    if plain_code == 127:  # weird left arrow at end of charset
        return ""
    elif plain_code < len(charset_top_rows):
        return charset_top_rows[plain_code]
    else:
        return chr(plain_code)


def to_color_code(code: int) -> str:
    if is_brown_char(code):
        return color_brown
    elif is_gold_char(code):
        return color_gold
    else:
        return color_white


def is_brown_char(code: int) -> bool:
    row_in_charset = code / 16
    return row_in_charset > 9 or 18 <= remove_color(code) <= 27


def is_gold_char(code: int) -> bool:
    return code in gold_codes
