import json
from pathlib import Path

from topoaccess_prod.release.conformance import check_conformance


def test_conformance_detects_required_assets(tmp_path: Path):
    rel = tmp_path / "release"
    (rel / "cursor_rules").mkdir(parents=True)
    (rel / "claude_hooks").mkdir()
    (rel / "AGENTS.md").write_text("exact lookup is tool-only", encoding="utf-8")
    (rel / "cursor_rules" / "topoaccess.mdc").write_text("rules", encoding="utf-8")
    (rel / "claude_hooks" / "settings.example.json").write_text("{}", encoding="utf-8")
    (rel / "openapi.json").write_text("{}", encoding="utf-8")
    (rel / "mcp_like_manifest.json").write_text("{}", encoding="utf-8")
    (rel / "stdio_schema.json").write_text("{}", encoding="utf-8")
    (rel / "tool_schema.json").write_text(json.dumps({"tools": [{"name": "exact_lookup", "model_fallback_allowed": False}]}), encoding="utf-8")
    rows = check_conformance(str(rel), str(tmp_path / "out.jsonl"), str(tmp_path / "report.md"))
    assert all(row["result_status"] == "pass" for row in rows)

