def hostport(value: str) -> str:
    result = value.lower().strip()

    needles = [" ktx"]

    for needle in needles:
        result = result.replace(needle, "")

    if " " in result:
        result, _ = result.split(" ", 1)

    return result
