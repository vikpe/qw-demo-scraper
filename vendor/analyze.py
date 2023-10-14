from .mvdparser import Player, ParseResult


def reason_to_ignore_demo(info: ParseResult, mode: str) -> str | None:
    bot_names = get_bot_names(info.players)

    if bot_names:
        return f"has bots ({', '.join(bot_names)})"

    if info.duration < min_duration_per_mode(mode):
        return f"probably aborted ({format_duration(info.duration)})"

    return None


def format_duration(seconds: float) -> str:
    minutes = int(seconds / 60)
    seconds = int(seconds % 60)

    if minutes < 1:
        return f"{seconds} seconds"

    return f"{minutes} minutes, {seconds} seconds"


def min_duration_per_mode(mode: str) -> int:
    min_minutes_per_mode = {
        "ffa": 5,
        "1on1": 3,
        "2on2": 5,
        "4on4": 10,
    }
    default = 10

    return min_minutes_per_mode.get(mode, default) * 60


def get_bot_names(players: list[Player]) -> list[str]:
    return [p.name for p in players if is_bot(p)]


def is_bot(player: Player) -> bool:
    return 10 == player.ping
