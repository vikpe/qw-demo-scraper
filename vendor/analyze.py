from .mvdparser import Player, ParseResult


def reason_to_skip_demo(info: ParseResult) -> str | None:
    if 0 == info.duration:
        return "game in progress"
    elif any([is_bot(p) for p in info.players]):
        return "has bots"

    return None


def is_bot(player: Player) -> bool:
    return 10 == player.ping
