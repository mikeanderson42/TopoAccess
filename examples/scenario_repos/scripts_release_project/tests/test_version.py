from release_tool.version import VERSION


def test_version_shape():
    assert VERSION.count(".") == 2
