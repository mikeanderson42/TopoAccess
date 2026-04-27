from __future__ import annotations

import json
from pathlib import Path

from .adversarial_benchmark import summarize_rows


def load_result_rows(inputs: list[str]) -> list[dict]:
    rows: list[dict] = []
    for pattern in inputs:
        for path in sorted(Path().glob(pattern)):
            if path.name in {"audit.jsonl", "secret_scan.jsonl", "dogfood_preflight.jsonl", "failure_mining.jsonl"}:
                continue
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rows


def write_robustness_summary(inputs: list[str], out_json: str, out_md: str, failure_md: str, manifest: str | None = None) -> dict:
    rows = load_result_rows(inputs)
    summary = summarize_rows(rows)
    phases = sorted({str(row.get("phase", "unknown")) for row in rows})
    summary["phases"] = phases
    failures = [row for row in rows if row.get("result_status") != "pass"]
    Path(out_json).parent.mkdir(parents=True, exist_ok=True)
    Path(out_json).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# TopoAccess Robustness Summary", ""]
    lines.extend(f"- {key}: `{value}`" for key, value in summary.items())
    Path(out_md).write_text("\n".join(lines) + "\n", encoding="utf-8")
    failure_lines = ["# TopoAccess Robustness Failure Summary", "", f"- Failures: `{len(failures)}`"]
    for row in failures[:25]:
        failure_lines.append(f"- `{row.get('phase')}` `{row.get('scenario_id')}`: {row.get('failure_reason')}")
    Path(failure_md).write_text("\n".join(failure_lines) + "\n", encoding="utf-8")
    if manifest:
        payload = {
            "version": "topoaccess-prod-v47-robustness",
            "release": "v1.0.0-rc1-hardening-gauntlet",
            "model_agnostic_public": True,
            "public_ci_model_free": True,
            "exact_lookup_tool_only": True,
            "category_gated_model": True,
            "wrong_high_confidence": summary.get("wrong_high_confidence", 0),
            "unsupported_high_confidence": summary.get("unsupported_high_confidence", 0),
            "robustness": summary,
        }
        Path(manifest).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary
