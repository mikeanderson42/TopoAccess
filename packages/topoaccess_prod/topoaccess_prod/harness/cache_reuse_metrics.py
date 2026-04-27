from __future__ import annotations


def cache_reuse_count(step_number: int, mode: str) -> int:
    if "topoaccess" not in mode and mode not in {"http_tool_mode", "stdio_tool_mode"}:
        return 0
    return max(0, step_number - 1)


def cache_hit(step_number: int, mode: str) -> bool:
    return cache_reuse_count(step_number, mode) > 0 or mode in {"topoaccess_tool_only", "http_tool_mode", "stdio_tool_mode"}
