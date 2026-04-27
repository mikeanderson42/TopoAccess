from __future__ import annotations

from .tool_schema import all_schemas


def manifest() -> dict:
    return {"server": "topoaccess_http_tool_server", "schema": all_schemas(), "stdio": True, "http": True}
