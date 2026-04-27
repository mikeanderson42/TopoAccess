from __future__ import annotations

import json
from pathlib import Path

from .constants import BASELINE, PREFERRED_MODEL


def product_manifest() -> dict:
    return {
        "version": "topoaccess-prod-v1",
        "source_baseline": "V29",
        "daily_driver_ready": True,
        "operator_cli_ready": True,
        "preferred_model": PREFERRED_MODEL,
        "nonpreferred_model_used": False,
        "exact_lookup_tool_only": True,
        "category_gated_model": True,
        **{k: v for k, v in BASELINE.items() if k != "source_baseline"},
    }


def write_manifest(path: str | Path, extra: dict | None = None) -> dict:
    manifest = product_manifest()
    if extra:
        manifest.update(extra)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest
