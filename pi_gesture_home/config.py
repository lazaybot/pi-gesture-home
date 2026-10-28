"""Load configuration while keeping credentials outside the repository."""

from __future__ import annotations

import json
from pathlib import Path


ALLOWED_DOMAINS = {"light", "fan", "media_player"}


def load_config(path: str | Path) -> dict:
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {"gestures", "mqtt", "safety"}
    missing = required - config.keys()
    if missing:
        raise ValueError(f"configuration missing: {', '.join(sorted(missing))}")
    mappings = config["gestures"]
    for command, mapping in mappings.items():
        entity = mapping.get("entity_id", "")
        domain = entity.split(".", 1)[0]
        if domain not in ALLOWED_DOMAINS:
            raise ValueError(
                f"unsafe or unsupported entity domain '{domain}' for command '{command}'"
            )
    return config
