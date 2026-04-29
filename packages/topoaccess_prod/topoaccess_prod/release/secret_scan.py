from __future__ import annotations

import json
import re
from pathlib import Path

from .path_filters import BINARY_EXTENSIONS, iter_files

PATTERNS = [re.compile(r"sk-[A-Za-z0-9]{20,}"), re.compile(r"BEGIN (RSA |OPENSSH )?PRIVATE KEY"), re.compile(r"(?i)(api[_-]?key|secret|token)\s*=\s*['\"][^'\"]{12,}")]


def scan_secrets(paths: list[str], out: str, report: str, exclude_dirs: list[str] | None = None, max_file_bytes: int = 1_000_000) -> list[dict]:
    rows = []
    excludes = ["__pycache__", *(exclude_dirs or [])]
    for path, meta in iter_files(paths, exclude_dirs=excludes):
        if meta["result_status"] == "skipped":
            continue
        if meta["result_status"] == "error":
            rows.append({"phase": "secret_scan", **meta, "hits": [], "result_status": "fail"})
            continue
        size = int(meta.get("bytes", 0))
        if path.suffix.lower() in BINARY_EXTENSIONS:
            rows.append({"phase": "secret_scan", "path": str(path), "hits": [], "skipped_reason": "binary_extension", "result_status": "skipped"})
            continue
        if size > max_file_bytes:
            rows.append({"phase": "secret_scan", "path": str(path), "hits": [], "bytes": size, "skipped_reason": "too_large", "result_status": "skipped"})
            continue
        hits = _scan_file(path)
        rows.append({"phase": "secret_scan", "path": str(path), "hits": hits, "result_status": "fail" if hits else "pass"})
    failures = [row for row in rows if row["result_status"] == "fail"]
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
    with Path(report).open("a", encoding="utf-8") as f:
        f.write(f"\n## Secret Scan\n\n- Files scanned: {len(rows)}\n- Failures: {len(failures)}\n")
    return rows


def _scan_file(path: Path, chunk_size: int = 65536) -> list[str]:
    hits: set[str] = set()
    tail = ""
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as stream:
            while True:
                chunk = stream.read(chunk_size)
                if not chunk:
                    break
                text = tail + chunk
                for pattern in PATTERNS:
                    if pattern.search(text):
                        hits.add(pattern.pattern)
                tail = text[-512:]
    except OSError as exc:
        return [f"scan_error:{type(exc).__name__}"]
    return sorted(hits)
