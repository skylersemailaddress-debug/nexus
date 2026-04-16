"""DB reset runner scaffold adapted from NexusV3 donor."""

from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class DbResetRequest:
    db_name: str
    db_user: str
    db_host: str
    db_port: int


def build_reset_report(req: DbResetRequest) -> dict:
    return {
        "db_name": req.db_name,
        "db_user": req.db_user,
        "db_host": req.db_host,
        "db_port": req.db_port,
        "status": "db-reset-scaffold",
    }


def write_report(path: str, report: dict) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
