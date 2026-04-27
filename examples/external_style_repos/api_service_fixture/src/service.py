def health() -> dict:
    return {"ok": True}


def get_user(user_id: str) -> dict:
    return {"id": user_id, "kind": "demo"}
