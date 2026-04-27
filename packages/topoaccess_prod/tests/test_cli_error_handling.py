import subprocess
import sys


def test_cli_unknown_command_returns_nonzero():
    result = subprocess.run(
        [sys.executable, "-c", "from topoaccess_prod.cli.main import main; raise SystemExit(main(['not-a-command']))"],
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "invalid choice" in result.stderr


def test_cli_empty_query_returns_nonzero():
    result = subprocess.run(
        [sys.executable, "-c", "from topoaccess_prod.cli.main import main; raise SystemExit(main(['query', '--query', '']))"],
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "query must be a non-empty string" in result.stdout
