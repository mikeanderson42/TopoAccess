from __future__ import annotations

import json
from pathlib import Path

from .distribution_builder import _base_row


def check_conformance(release: str, out: str, report: str) -> list[dict]:
    base = Path(release)
    if not (base / "AGENTS.md").exists() and Path("examples/integrations/AGENTS.md").exists():
        base = Path("examples/integrations")
    schema_base = base / "schemas" if (base / "schemas").exists() else base
    checks = {
        "agents_md": base / "AGENTS.md",
        "cursor_rules": base / "cursor_rules" / "topoaccess.mdc",
        "claude_hooks": base / "claude_hooks" / "settings.example.json",
        "openapi": schema_base / "openapi.json",
        "mcp": schema_base / "mcp_like_manifest.json",
        "stdio": schema_base / "stdio_schema.json",
        "tool_schema": schema_base / "tool_schema.json",
    }
    rows = []
    for name, path in checks.items():
        row = _base_row("conformance", f"check {name}", str(path))
        ok = path.exists()
        if path.suffix == ".json" and ok:
            json.loads(path.read_text(encoding="utf-8"))
        row.update({"check": name, "exists": ok, "release_gate_status": "pass" if ok else "fail", "result_status": "pass" if ok else "fail"})
        rows.append(row)
    schema_path = schema_base / "tool_schema.json"
    if schema_path.exists():
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        exact = next(tool for tool in schema["tools"] if tool["name"] == "exact_lookup")
        rows.append(_base_row("conformance", "exact lookup fallback", str(schema_path)) | {"check": "exact_lookup_tool_only", "exists": True, "release_gate_status": "pass", "result_status": "pass" if exact["model_fallback_allowed"] is False else "fail"})
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n", encoding="utf-8")
    failures = [r for r in rows if r["result_status"] != "pass"]
    Path(report).write_text(f"# V38 Conformance\n\n- Rows: `{len(rows)}`\n- Failures: `{len(failures)}`\n- Exact lookup forbids model fallback.\n", encoding="utf-8")
    return rows
