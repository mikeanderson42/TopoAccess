import json
from pathlib import Path

from topoaccess_prod.integrations.claude_hooks import generate_claude_hooks


def test_claude_hooks_generate_settings(tmp_path: Path):
    out = tmp_path / "hooks"
    row = generate_claude_hooks("default", str(out), str(tmp_path / "report.md"))
    payload = json.loads((out / "settings.example.json").read_text(encoding="utf-8"))
    assert "hooks" in payload
    assert row["result_status"] == "pass"

