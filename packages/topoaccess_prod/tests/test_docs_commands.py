from pathlib import Path


def test_docs_show_first_use_and_setup_decision_table():
    readme = Path("README.md").read_text(encoding="utf-8")
    harness = Path("docs/HARNESS_INTEGRATION.md").read_text(encoding="utf-8")
    commands = Path("docs/COMMANDS.md").read_text(encoding="utf-8")
    assert "topoaccess init" in readme
    assert "topoaccess try" in readme
    assert "Integration Decision Table" in harness
    assert "topoaccess setup openhands" in commands
    assert "dry-run by default" in commands
