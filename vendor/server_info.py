from typing import Optional

import attr


def to_int(value: any) -> int | None:
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


@attr.define
class ServerInfo:
    admin: Optional[str | None] = attr.ib(default=None)
    deathmatch: Optional[int | None] = attr.ib(default=None, converter=to_int)
    gamedir: Optional[str | None] = attr.ib(default=None)
    ktxver: Optional[str | None] = attr.ib(default=None)
    map: Optional[str | None] = attr.ib(default=None)
    maxclients: Optional[int | None] = attr.ib(default=None, converter=to_int)
    maxfps: Optional[int | None] = attr.ib(default=None, converter=to_int)
    maxspectators: Optional[int | None] = attr.ib(default=None, converter=to_int)
    mode: Optional[str | None] = attr.ib(default=None)
    needpass: Optional[int | None] = attr.ib(default=None, converter=to_int)
    pm_ktjump: Optional[int | None] = attr.ib(default=None, converter=to_int)
    progs: Optional[str | None] = attr.ib(default=None)
    qvm: Optional[str | None] = attr.ib(default=None)
    sv_antilag: Optional[int | None] = attr.ib(default=None, converter=to_int)
    teamplay: Optional[int | None] = attr.ib(default=None, converter=to_int)
    timelimit: Optional[int | None] = attr.ib(default=None, converter=to_int)
    version: Optional[str | None] = attr.ib(default=None)
    z_ext: Optional[str | None] = attr.ib(default=None)

    def as_dict(self) -> dict:
        return attr.asdict(self)

    @classmethod
    def from_string(cls, serverinfo: str) -> "ServerInfo":
        parts = serverinfo.lstrip("\\").split("\\")
        keys = [k.lstrip("*") for k in parts[0::2]]
        values = parts[1::2]
        info = dict(zip(keys, values))

        return ServerInfo(
            admin=info.get("admin", None),
            deathmatch=info.get("deathmatch", None),
            gamedir=info.get("gamedir", None),
            ktxver=info.get("ktxver", None),
            map=info.get("map", None),
            maxclients=info.get("maxclients", None),
            maxfps=info.get("maxfps", None),
            maxspectators=info.get("maxspectators", None),
            mode=info.get("mode", None),
            needpass=info.get("needpass", None),
            pm_ktjump=info.get("pm_ktjump", None),
            progs=info.get("progs", None),
            qvm=info.get("qvm", None),
            sv_antilag=info.get("sv_antilag", None),
            teamplay=info.get("teamplay", None),
            timelimit=info.get("timelimit", None),
            version=info.get("version", None),
            z_ext=info.get("z_ext", None),
        )
