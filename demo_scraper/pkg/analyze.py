from demo_scraper.pkg.mvdparser import Player, MvdInfo


def reason_to_ignore_demo(info: MvdInfo, mode: str) -> str | None:
    bot_names = get_bot_names(info.players)
    if bot_names:
        return f"has bots ({', '.join(bot_names)})"

    if info.duration < min_duration_per_mode(mode):
        return f"probably aborted ({format_duration(info.duration)})"

    if info.serverinfo.deathmatch == 4:
        return f"dmm4"

    return None


def format_duration(seconds: float) -> str:
    minutes = int(seconds / 60)
    seconds = int(seconds % 60)

    if minutes < 1:
        return f"{seconds} seconds"

    return f"{minutes} minutes, {seconds} seconds"


def min_duration_per_mode(mode: str) -> int:
    min_minutes_per_mode = {
        "wipeout": 1,
        "ffa": 5,
        "ctf": 5,
        "1on1": 10,
        "2on2": 10,
        "4on4": 20,
    }
    default = 10

    return min_minutes_per_mode.get(mode, default) * 60


def get_bot_names(players: list[Player]) -> list[str]:
    return [p.name for p in players if is_bot(p)]


def is_bot(player: Player) -> bool:
    return 10 == player.ping
