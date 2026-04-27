from pathlib import Path

from topoaccess_prod.harness.harness_compat_matrix import build_matrix


def test_harness_compat_matrix_rows(tmp_path: Path):
    rows = build_matrix("default", str(tmp_path / "compat.jsonl"), str(tmp_path / "report.md"))
    targets = {row["integration_target"] for row in rows}
    assert {"Codex", "Claude Code", "Cursor", "Aider", "HTTP", "stdio"}.issubset(targets)
    assert all(row["exact_lookup_tool_only"] for row in rows)

