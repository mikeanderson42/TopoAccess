from __future__ import annotations

import json
import re
from pathlib import Path


RISKY_PATTERNS = [
    (re.compile(r"\bguarantee[sd]?\b", re.I), "avoid guaranteed outcomes"),
    (re.compile(r"\balways\b", re.I), "avoid universal claims"),
    (re.compile(r"\bnever\b", re.I), "allow only for exact lookup/model-free invariants"),
    (re.compile(r"\bproduction[- ]proven\b", re.I), "benchmark is fixture-based, not universal production proof"),
    (re.compile(r"\brequires? (Qwen|LM Studio|Ollama|GPU|model weights?)\b", re.I), "public package must remain model-free"),
]

SUPPORTED_EXCEPTIONS = [
    "exact lookup never requires a model",
    "exact lookup remains tool-only",
    "never require a model",
    "never force push",
    "does public ci require",
    "does not require",
    "do not require",
    "not guarantee",
    "not guarantees",
    "not a universal",
    "not universal production guarantees",
    "no hidden writes",
]


def audit_claims(paths: list[str | Path]) -> list[dict]:
    rows: list[dict] = []
    for path in _iter_markdown(paths):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for pattern, guidance in RISKY_PATTERNS:
                if not pattern.search(line):
                    continue
                status = "pass" if _is_supported_exception(line) else "review"
                rows.append(
                    {
                        "path": str(path),
                        "line": line_number,
                        "claim": line.strip(),
                        "guidance": guidance,
                        "evidence": _evidence_for(line),
                        "result_status": status,
                    }
                )
    if not rows:
        rows.append(
            {
                "path": "",
                "line": 0,
                "claim": "No risky absolute public claims detected.",
                "guidance": "No action required.",
                "evidence": "claims_audit",
                "result_status": "pass",
            }
        )
    return rows


def write_claims_audit(paths: list[str | Path], out: str | Path, report: str | Path) -> list[dict]:
    rows = audit_claims(paths)
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    review_rows = [row for row in rows if row["result_status"] != "pass"]
    lines = [
        "# TopoAccess Claims Audit",
        "",
        f"- Claims reviewed: `{len(rows)}`",
        f"- Unsupported absolute claims: `{len(review_rows)}`",
        "",
        "Public claims must stay scoped to public benchmarks, conformance checks, and documented limitations.",
    ]
    for row in review_rows[:25]:
        lines.append(f"- `{row['path']}:{row['line']}` {row['guidance']}: {row['claim']}")
    Path(report).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return rows


def claims_gate_passed(rows: list[dict]) -> bool:
    return all(row["result_status"] == "pass" for row in rows)


def _iter_markdown(paths: list[str | Path]) -> list[Path]:
    files: list[Path] = []
    for item in paths:
        path = Path(item)
        if path.is_file() and path.suffix.lower() in {".md", ".markdown"}:
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(p for p in path.rglob("*.md") if ".git" not in p.parts))
    return files


def _is_supported_exception(line: str) -> bool:
    lowered = line.lower()
    return any(exception in lowered for exception in SUPPORTED_EXCEPTIONS)


def _evidence_for(line: str) -> str:
    lowered = line.lower()
    if "token" in lowered or "benchmark" in lowered:
        return "docs/BENCHMARKS.md and release/topoaccess_prod_v45/scenario_summary.json"
    if "exact lookup" in lowered or "model" in lowered:
        return "conformance and model-agnostic docs"
    return "documentation limitation or support statement"
