"""Registry capability scaffold adapted from NexusV3 donor."""

from __future__ import annotations

import json
from pathlib import Path


def registry_capabilities(seed_path: Path) -> list[dict]:
    if not seed_path.exists():
        return []

    data = json.loads(seed_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        return []

    capabilities: list[dict] = []
    for item in data:
        if isinstance(item, dict) and item.get("id"):
            capabilities.append(item)
    return capabilities
