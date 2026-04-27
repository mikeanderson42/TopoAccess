from pathlib import Path

from topoaccess_prod.release.status_badges import generate_status_badges


def test_status_badges_write_json(tmp_path: Path):
    status = generate_status_badges(str(tmp_path / "release"), str(tmp_path / "out.jsonl"), str(tmp_path / "report.md"))
    assert status["exact_lookup_tool_only"] is True
    assert (tmp_path / "release" / "status.json").exists()

