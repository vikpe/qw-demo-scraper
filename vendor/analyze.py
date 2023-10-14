from .mvdparser import Player, ParseResult


def reason_to_ignore_demo(info: ParseResult) -> str | None:
    bot_names = get_bot_names(info.players)

    if bot_names:
        return f"has bots ({', '.join(bot_names)})"

    return None


def get_bot_names(players: list[Player]) -> list[str]:
    return [p.name for p in players if is_bot(p)]


def is_bot(player: Player) -> bool:
    return 10 == player.ping
