from src.version import VERSION


def test_version_is_rc():
    assert VERSION.endswith("rc1")
