from __future__ import annotations

import json
from pathlib import Path


def print_json(data: object) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def write_jsonl(path: str | Path, rows: list[dict]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def status_from_result(result: dict | list[dict] | None) -> int:
    if result is None:
        return 0
    if isinstance(result, list):
        return 0 if all(row.get("result_status", "pass") == "pass" for row in result) else 1
    return 0 if result.get("status", result.get("result_status", "pass")) == "pass" else 1
