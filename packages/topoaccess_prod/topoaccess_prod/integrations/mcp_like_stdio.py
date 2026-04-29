from __future__ import annotations

import json
import sys

from .http_tool_server import handle_tool


def structured_stdio_error(error_type: str, message: str, request_id: object | None = None) -> dict:
    return {
        "status": "error",
        "error_type": error_type,
        "message": message,
        "request_id": request_id,
        "recoverable": True,
    }


def parse_stdio_request(line: str) -> tuple[str | None, dict | None, dict | None]:
    if not line.strip():
        return None, None, structured_stdio_error("empty_request", "empty stdio request")
    try:
        request = json.loads(line)
    except json.JSONDecodeError as exc:
        return None, None, structured_stdio_error("invalid_json", f"invalid JSON: {exc.msg}")
    if not isinstance(request, dict):
        return None, None, structured_stdio_error("invalid_request", "stdio request must be a JSON object")
    request_id = request.get("request_id")
    tool = request.get("tool", "/health")
    arguments = request.get("arguments", {})
    if not isinstance(tool, str):
        return None, None, structured_stdio_error("invalid_request", "tool must be a string", request_id)
    if not isinstance(arguments, dict):
        return None, None, structured_stdio_error("invalid_arguments", "arguments must be a JSON object", request_id)
    return tool, arguments, None


def run_stdio() -> None:
    for line in sys.stdin:
        tool, arguments, error = parse_stdio_request(line)
        if error is not None:
            print(json.dumps(error, sort_keys=True), flush=True)
            continue
        try:
            response = handle_tool(tool or "/health", arguments or {})
        except Exception as exc:  # pragma: no cover - defensive bridge guard
            response = structured_stdio_error("tool_error", str(exc))
        print(json.dumps(response, sort_keys=True), flush=True)
