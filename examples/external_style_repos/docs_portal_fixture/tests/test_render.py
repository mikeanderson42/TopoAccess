from src.render import title


def test_title():
    assert title("Install") == "# Install"
