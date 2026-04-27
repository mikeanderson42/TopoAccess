from __future__ import annotations

import json


def log_event(event: dict) -> str:
    return json.dumps(event, sort_keys=True)
