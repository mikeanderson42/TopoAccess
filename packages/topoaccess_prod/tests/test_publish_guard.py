from topoaccess_prod.harness.publish_guard import FORBIDDEN


def test_publish_guard_forbidden_patterns_include_model_files():
    assert ".gguf" in FORBIDDEN
