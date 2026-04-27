from topoaccess_prod.cli.command_registry import command_names, command_table


def test_command_registry_has_primary_commands():
    names = set(command_names())
    assert {"version", "commands", "workspace", "doctor", "codex-brief", "post-edit", "benchmark", "audit", "secret-scan"} <= names
    assert all(row["model_free_default"] for row in command_table())
