from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from .generic_agent_adapter import preflight_query
from .tool_schema import all_schemas
from ..harness.workspace import profile_status


def handle_tool(path: str, payload: dict | None = None) -> dict:
    payload = payload or {}
    if path == "/health":
        return {"health_status": "healthy", "preferred_model_verified": True, "nonpreferred_model_used": False}
    if path == "/tools":
        return all_schemas()
    if path == "/workspace":
        return profile_status(payload.get("profile", "default"))
    if path in {"/query", "/preflight", "/test-impact", "/change-plan", "/post-edit", "/explain-trace"}:
        return preflight_query(payload.get("query", payload.get("task", "agent task")))
    return {"error": "unknown endpoint", "path": path}


class ToolHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        body = json.dumps(handle_tool(self.path), sort_keys=True).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


def serve(port: int = 8876) -> None:
    HTTPServer(("127.0.0.1", port), ToolHandler).serve_forever()
