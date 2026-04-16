"""Registry capability scaffold adapted from NexusV3 donor."""

from __future__ import annotations

import json
from pathlib import Path


def registry_capabilities(seed_path: Path) -> list[dict]:
    if not seed_path.exists():
        return []

    data = json.loads(seed_path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []
