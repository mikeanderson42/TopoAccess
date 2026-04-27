from pathlib import Path


def test_docs_show_30_second_quickstart_and_legacy_fallback():
    readme = Path("README.md").read_text(encoding="utf-8")
    quickstart = Path("docs/QUICKSTART.md").read_text(encoding="utf-8")
    commands = Path("docs/COMMANDS.md").read_text(encoding="utf-8")
    assert "topoaccess init" in readme
    assert "topoaccess try" in readme
    assert "topoaccess setup codex" in commands
    assert "python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief" in quickstart
