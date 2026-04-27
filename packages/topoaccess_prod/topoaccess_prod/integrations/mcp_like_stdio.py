from __future__ import annotations

import json
import sys

from .http_tool_server import handle_tool


def run_stdio() -> None:
    for line in sys.stdin:
        request = json.loads(line)
        response = handle_tool(request.get("tool", "/health"), request.get("arguments", {}))
        print(json.dumps(response, sort_keys=True), flush=True)
