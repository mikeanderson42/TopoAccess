from topoaccess_prod.cli.main import main


def test_model_free_codex_brief_and_post_edit(capsys):
    assert main(["codex-brief", "--profile", "demo", "--task", "What tests should I run after editing README.md?"]) == 0
    assert "README.md" in capsys.readouterr().out
    assert main(["post-edit", "--profile", "demo", "--changed-files", "README.md"]) == 0
    assert "result_status" in capsys.readouterr().out
