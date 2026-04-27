from __future__ import annotations

from typing import Any

MISSING = object()


def flatten_json_paths(obj: Any) -> dict:
    paths: dict[str, Any] = {}

    def visit(value: Any, path: str) -> None:
        if isinstance(value, dict):
            if not value and path:
                paths[path] = value
            for key, child in value.items():
                child_path = f"{path}.{key}" if path else str(key)
                visit(child, child_path)
            return
        if isinstance(value, list):
            if not value and path:
                paths[path] = value
            for index, child in enumerate(value):
                child_path = f"{path}.{index}" if path else str(index)
                visit(child, child_path)
            return
        paths[path] = value

    visit(obj, "")
    return paths


def field_mask_diff(before: dict, after: dict, allowed_paths: list[str]) -> dict:
    before_flat = flatten_json_paths(before)
    after_flat = flatten_json_paths(after)
    normalized_allowed = [_normalize_path(path) for path in allowed_paths]
    allowed_changes = []
    unauthorized_changes = []
    unchanged_count = 0
    all_paths = sorted(set(before_flat) | set(after_flat))

    for path in all_paths:
        before_value = before_flat.get(path, MISSING)
        after_value = after_flat.get(path, MISSING)
        if before_value == after_value:
            unchanged_count += 1
            continue
        change = {
            "path": path,
            "before": None if before_value is MISSING else before_value,
            "after": None if after_value is MISSING else after_value,
        }
        if _path_allowed(path, normalized_allowed):
            allowed_changes.append(change)
        else:
            unauthorized_changes.append(change)

    return {
        "result_status": "fail" if unauthorized_changes else "pass",
        "allowed_changes": allowed_changes,
        "unauthorized_changes": unauthorized_changes,
        "unchanged_count": unchanged_count,
        "allowed_paths": normalized_allowed,
    }


def _normalize_path(path: str) -> str:
    path = str(path).strip()
    if path.startswith("/"):
        return ".".join(part for part in path.split("/") if part)
    return path.strip(".")


def _path_allowed(path: str, allowed_paths: list[str]) -> bool:
    for allowed in allowed_paths:
        if not allowed:
            continue
        if path == allowed or path.startswith(f"{allowed}."):
            return True
    return False
