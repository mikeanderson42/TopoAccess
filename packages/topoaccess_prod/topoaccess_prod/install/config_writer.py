from __future__ import annotations

import json
from pathlib import Path


def write_config(path: str, payload: dict) -> dict:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload
