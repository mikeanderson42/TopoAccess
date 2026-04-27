from src.service import get_user, health


def test_health():
    assert health()["ok"] is True


def test_get_user():
    assert get_user("42")["id"] == "42"
