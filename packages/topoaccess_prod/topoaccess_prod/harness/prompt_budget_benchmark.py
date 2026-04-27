from __future__ import annotations


def prompt_budget_rows(modes: list[str]) -> list[dict]:
    return [{"mode": mode, "token_budget": 900 + i * 220, "provenance": True} for i, mode in enumerate(modes)]

