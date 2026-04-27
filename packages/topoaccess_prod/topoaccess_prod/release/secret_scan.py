from __future__ import annotations

import json
import re
from pathlib import Path

PATTERNS = [re.compile(r"sk-[A-Za-z0-9]{20,}"), re.compile(r"BEGIN (RSA |OPENSSH )?PRIVATE KEY"), re.compile(r"(?i)(api[_-]?key|secret|token)\s*=\s*['\"][^'\"]{12,}")]


def scan_secrets(paths: list[str], out: str, report: str) -> list[dict]:
    rows = []
    for root in paths:
        for path in Path(root).rglob("*"):
            if not path.is_file() or path.stat().st_size > 1_000_000 or "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            hits = [pattern.pattern for pattern in PATTERNS if pattern.search(text)]
            rows.append({"phase": "secret_scan", "path": str(path), "hits": hits, "result_status": "fail" if hits else "pass"})
    failures = [row for row in rows if row["result_status"] == "fail"]
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
    with Path(report).open("a", encoding="utf-8") as f:
        f.write(f"\n## Secret Scan\n\n- Files scanned: {len(rows)}\n- Failures: {len(failures)}\n")
    return rows
