from src.api import route_status


def test_route_status():
    assert route_status()["status"] == "ok"
