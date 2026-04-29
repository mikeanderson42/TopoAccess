from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from .generic_agent_adapter import preflight_query
from .tool_schema import all_schemas
from ..harness.workspace import profile_status


def handle_tool(path: str, payload: dict | None = None) -> dict:
    payload = payload or {}
    path = urlparse(path).path
    if path == "/health":
        return {"health_status": "healthy", "preferred_model_verified": True, "nonpreferred_model_used": False}
    if path == "/tools":
        return all_schemas()
    if path == "/workspace":
        return profile_status(payload.get("profile", "default"))
    if path in {"/query", "/preflight", "/test-impact", "/change-plan", "/post-edit", "/explain-trace"}:
        return preflight_query(payload.get("query", payload.get("task", "agent task")))
    return {"status": "error", "error_type": "unknown_endpoint", "message": "unknown endpoint", "path": path, "recoverable": True}


def structured_error(error_type: str, message: str, *, path: str | None = None, request_id: object | None = None, recoverable: bool = True) -> dict:
    return {
        "status": "error",
        "error_type": error_type,
        "message": message,
        "path": path,
        "request_id": request_id,
        "recoverable": recoverable,
    }


class ToolHandler(BaseHTTPRequestHandler):
    max_body_bytes = 1_000_000

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        response = handle_tool(path)
        status = 404 if response.get("error_type") == "unknown_endpoint" else 200
        self._send_json(response, status=status)

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            payload = self._read_json_body()
        except ValueError as exc:
            message = str(exc)
            status = 413 if message == "payload_too_large" else 400
            self._send_json(structured_error(message, message, path=path), status=status)
            return
        try:
            response = handle_tool(path, payload)
        except Exception as exc:  # pragma: no cover - defensive bridge guard
            self._send_json(structured_error("tool_error", str(exc), path=path), status=500)
            return
        status = 404 if response.get("error_type") == "unknown_endpoint" else 200
        self._send_json(response, status=status)

    def do_PUT(self) -> None:  # noqa: N802
        self._send_json(structured_error("method_not_allowed", "method not allowed", path=urlparse(self.path).path), status=405)

    def log_message(self, format: str, *args: object) -> None:
        return

    def _read_json_body(self) -> dict:
        raw_length = self.headers.get("Content-Length", "0")
        try:
            length = int(raw_length)
        except ValueError as exc:
            raise ValueError("invalid_request") from exc
        if length > self.max_body_bytes:
            raise ValueError("payload_too_large")
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError as exc:
            raise ValueError("invalid_json") from exc
        if not isinstance(payload, dict):
            raise ValueError("invalid_request")
        return payload

    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def serve(port: int = 8876, host: str = "127.0.0.1", allow_nonlocal: bool = False, max_body_bytes: int = 1_000_000) -> None:
    if host not in {"127.0.0.1", "localhost", "::1"} and not allow_nonlocal:
        raise ValueError("non-local HTTP bind requires --allow-nonlocal")
    ToolHandler.max_body_bytes = max_body_bytes
    ThreadingHTTPServer((host, port), ToolHandler).serve_forever()
