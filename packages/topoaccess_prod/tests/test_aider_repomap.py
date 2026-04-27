from pathlib import Path

from topoaccess_prod.integrations.aider_repomap import export_repomap


def test_repomap_exports_budgets(tmp_path: Path):
    rows = export_repomap("default", [1000, 2000], str(tmp_path / "map"), str(tmp_path / "report.md"))
    assert len(rows) == 2
    assert (tmp_path / "map" / "repomap_1000.md").exists()

