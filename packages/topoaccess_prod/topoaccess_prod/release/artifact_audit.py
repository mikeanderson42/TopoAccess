from __future__ import annotations

import json
from pathlib import Path

FORBIDDEN_EXTS = {".gguf", ".safetensors", ".ckpt", ".pth", ".pt"}
FORBIDDEN_NAMES = {".env"}


def audit_artifacts(paths: list[str], out: str, report: str) -> list[dict]:
    rows = []
    for root in paths:
        for path in Path(root).rglob("*"):
            if not path.is_file():
                continue
            rel = str(path)
            parts = set(path.parts)
            if "__pycache__" in parts:
                continue
            runtime_cache = path.parts[0] == "cache" if path.parts else False
            fail = path.suffix.lower() in FORBIDDEN_EXTS or path.name in FORBIDDEN_NAMES or "logs" in parts or runtime_cache
            rows.append({"phase": "artifact_audit", "path": rel, "bytes": path.stat().st_size, "result_status": "fail" if fail else "pass"})
    failures = [row for row in rows if row["result_status"] == "fail"]
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
    Path(report).write_text(f"# V35 Security Audit\n\n## Artifact Audit\n\n- Files scanned: {len(rows)}\n- Failures: {len(failures)}\n", encoding="utf-8")
    return rows
