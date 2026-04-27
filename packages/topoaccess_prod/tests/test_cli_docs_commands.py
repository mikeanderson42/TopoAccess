from pathlib import Path


def test_docs_prefer_topoaccess_command_for_quickstart():
    readme = Path("README.md").read_text(encoding="utf-8")
    quickstart = Path("docs/QUICKSTART.md").read_text(encoding="utf-8")
    assert "topoaccess workspace init" in readme
    assert "topoaccess codex-brief" in quickstart
    assert "python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief" in quickstart
