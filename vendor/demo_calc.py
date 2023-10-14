from typing import List

from . import hub, supab


def calc_missing_demos(
    db_demos: List[supab.Demo], server_demos: List[hub.Demo], keep_count: int
):
    if not db_demos:
        return server_demos

    db_filenames = [demo.filename for demo in db_demos]

    demos_to_keep = [
        {"timestamp": d.timestamp, "filename": d.filename} for d in db_demos
    ] + [
        {"timestamp": d.time, "filename": d.filename}
        for d in server_demos
        if d.filename not in db_filenames
    ]
    demos_to_keep.sort(key=lambda x: x["timestamp"], reverse=True)
    demos_to_keep = demos_to_keep[:keep_count]

    filenames_to_keep = [d["filename"] for d in demos_to_keep]
    missing_demos = [
        d
        for d in server_demos
        if d.filename in filenames_to_keep and d.filename not in db_filenames
    ]

    return missing_demos
