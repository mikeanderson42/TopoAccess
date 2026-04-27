from topoaccess_prod.release.safe_publish import BLOCKED


def test_safe_publish_blocks_model_extensions():
    assert ".gguf" in BLOCKED

