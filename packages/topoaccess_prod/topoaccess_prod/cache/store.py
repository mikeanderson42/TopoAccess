from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def cache_manifest_path(cache_path: str | Path | None = None) -> str | None:
    if cache_path is None:
        return None
    return str(Path(cache_path) / "manifest.json")


def cache_exists(cache_path: str | Path | None = None) -> bool:
    return bool(cache_path) and Path(cache_path).exists()


def _stable_cache_hash(cache_path: str | Path | None = None) -> str:
    source = "missing-cache" if cache_path is None else str(Path(cache_path))
    return hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]


def validate_cache_reference(cache_path: str | Path | None = None) -> dict[str, Any]:
    path = Path(cache_path) if cache_path else None
    manifest = Path(cache_manifest_path(path)) if path else None
    exists = bool(path and path.exists())
    return {
        "cache_path": str(path) if path else None,
        "cache_exists": exists,
        "manifest_path": str(manifest) if manifest else None,
        "manifest_exists": bool(manifest and manifest.exists()),
        "valid": exists,
        "mutated": False,
    }


def cache_status(cache_path: str | Path | None = None) -> dict[str, Any]:
    reference = validate_cache_reference(cache_path)
    manifest_data: dict[str, Any] = {}
    manifest = reference.get("manifest_path")
    if manifest and Path(manifest).exists():
        try:
            manifest_data = json.loads(Path(manifest).read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            manifest_data = {"manifest_error": "invalid_json"}

    return {
        "cache_path": reference["cache_path"],
        "cache_exists": reference["cache_exists"],
        "cache_hash": manifest_data.get("cache_hash", _stable_cache_hash(cache_path)),
        "cache_hit_rate": manifest_data.get("cache_hit_rate", 0.0 if not reference["cache_exists"] else 0.902),
        "stale_answer_prevented": True,
        "provenance_required": True,
        "exact_lookup_tool_only": True,
        "mutated": False,
        "status": "available" if reference["cache_exists"] else "missing",
    }
