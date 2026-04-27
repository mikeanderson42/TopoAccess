from src.worker import enqueue


def test_enqueue():
    assert enqueue("sync") == "queued:sync"
