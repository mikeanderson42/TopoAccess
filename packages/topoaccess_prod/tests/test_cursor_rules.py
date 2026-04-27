from pathlib import Path

from topoaccess_prod.integrations.cursor_rules import generate_cursor_rules


def test_cursor_rules_generate(tmp_path: Path):
    out = tmp_path / "cursor"
    report = tmp_path / "report.md"
    row = generate_cursor_rules("default", str(out), str(report))
    assert (out / "topoaccess.mdc").exists()
    assert row["exact_lookup_tool_only"] is True

