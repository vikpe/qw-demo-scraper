from typing import Optional

import attr

from demo_scraper.services.supab.participants import Participants


# disable http logs


@attr.define
class Demo:
    id: Optional[int] = attr.ib(default=0)
    sha256: Optional[str] = attr.ib(default="")
    source: Optional[str] = attr.ib(default="")
    filename: Optional[str] = attr.ib(default="")
    s3_key: Optional[str] = attr.ib(default="")
    timestamp: Optional[str] = attr.ib(default="")
    duration: Optional[float] = attr.ib(default=0.0)
    mode: Optional[str] = attr.ib(default="")
    map: Optional[str] = attr.ib(default="")
    title: Optional[str] = attr.ib(default="")
    participants: Optional[Participants] = attr.ib(default=Participants())


@attr.define
class NewDemo:
    sha256: str = attr.ib()
    source: str = attr.ib()
    filename: str = attr.ib()
    s3_key: str = attr.ib()
    timestamp: str = attr.ib()
    duration: float = attr.ib()
    mode: str = attr.ib()
    map: str = attr.ib()
    matchtag: str = attr.ib()
    title: str = attr.ib()
    participants: Participants = attr.ib()

    def as_dict(self) -> dict:
        return {
            "sha256": self.sha256,
            "source": self.source,
            "filename": self.filename,
            "s3_key": self.s3_key,
            "timestamp": self.timestamp,
            "duration": self.duration,
            "mode": self.mode,
            "map": self.map,
            "matchtag": self.matchtag,
            "title": self.title,
            "participants": self.participants.as_dict(),
        }


@attr.define
class IgnoredDemo:
    id: Optional[int] = attr.ib(default=0)
    sha256: Optional[str] = attr.ib(default="")
    mode: Optional[str] = attr.ib(default="")
    filename: Optional[str] = attr.ib(default="")
    reason: Optional[str] = attr.ib(default="")
    timestamp: Optional[str] = attr.ib(default="")


@attr.define
class NewIgnoredDemo:
    sha256: str = attr.ib()
    mode: str = attr.ib()
    filename: str = attr.ib()
    reason: str = attr.ib()
    timestamp: str = attr.ib()

    def as_dict(self) -> dict:
        return attr.asdict(self)
