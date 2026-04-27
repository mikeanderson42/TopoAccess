from topoaccess_prod.install.first_run import run_first_init
from topoaccess_prod.install.try_demo import run_try_demo


def test_first_use_paths_do_not_require_or_invoke_models(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    init = run_first_init()
    demo = run_try_demo()
    assert init["model_required"] is False
    assert demo["model_required"] is False
    assert demo["model_invoked"] is False
    assert demo["exact_lookup_tool_only"] is True
