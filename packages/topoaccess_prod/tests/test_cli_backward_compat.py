import subprocess
import sys


def test_legacy_scripts_help_still_work():
    commands = [
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccessctl.py", "--help"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_agent.py", "--help"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_workspace.py", "--help"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_doctor.py", "--help"],
    ]
    for command in commands:
        result = subprocess.run(command, text=True, capture_output=True)
        assert result.returncode == 0, result.stderr
