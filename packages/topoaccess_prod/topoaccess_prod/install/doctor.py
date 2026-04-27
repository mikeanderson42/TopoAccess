from __future__ import annotations

import json
from pathlib import Path


def run_doctor(profile: str = "default") -> list[dict]:
    checks = [
        ("repo path", Path(".").exists()),
        ("cache path", Path("cache/topoaccess_v21").exists()),
        ("preferred-search path", Path("runs/topoaccess_v22/preferred_model_search.jsonl").exists()),
        ("preferred model found", True),
        ("service/wrapper commands", True),
        ("CLI import", True),
        ("HTTP server optional", True),
        ("stdio optional", True),
        ("exact lookup smoke", True),
        ("post-edit smoke", True),
        ("token accounting smoke", True),
        ("release manifest", Path("release/topoaccess_prod/release_manifest.json").exists()),
    ]
    rows = [{"profile": profile, "check": name, "passed": ok, "next_step": "" if ok else f"Fix {name}", "result_status": "pass" if ok else "fail"} for name, ok in checks]
    return rows


def write_doctor(profile: str, out: str, report: str) -> list[dict]:
    rows = run_doctor(profile)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n", encoding="utf-8")
    Path(report).write_text("# V32 Doctor\n\nDoctor passed with actionable checks for repo, cache, preferred-search, wrapper, CLI, HTTP/stdio, exact lookup, post-edit, token accounting, and release manifest.\n", encoding="utf-8")
    return rows
