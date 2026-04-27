from __future__ import annotations


def estimate_roi(tasks_per_day: int, tokens_per_task: int, savings: float, price_per_million_tokens: float = 0.0) -> dict:
    """Estimate token and optional cost savings without assuming any vendor price."""
    daily_baseline = tasks_per_day * tokens_per_task
    daily_saved = int(round(daily_baseline * savings))
    monthly_saved = daily_saved * 30
    annual_saved = daily_saved * 365
    return {
        "tasks_per_day": tasks_per_day,
        "tokens_per_task": tokens_per_task,
        "savings_rate": savings,
        "daily_baseline_tokens": daily_baseline,
        "daily_tokens_saved": daily_saved,
        "monthly_tokens_saved": monthly_saved,
        "annual_tokens_saved": annual_saved,
        "price_per_million_tokens": price_per_million_tokens,
        "daily_cost_saved": _cost(daily_saved, price_per_million_tokens),
        "monthly_cost_saved": _cost(monthly_saved, price_per_million_tokens),
        "annual_cost_saved": _cost(annual_saved, price_per_million_tokens),
    }


def scenario_table(tokens_per_task: int = 20_000, price_per_million_tokens: float = 0.0) -> list[dict]:
    rows = []
    for tasks in [25, 50, 100, 250]:
        for label, savings in [("conservative", 0.80), ("v45_average", 0.9307), ("v45_median", 0.9397), ("v45_high", 0.9664)]:
            row = estimate_roi(tasks, tokens_per_task, savings, price_per_million_tokens)
            row["case"] = label
            rows.append(row)
    return rows


def _cost(tokens: int, price_per_million_tokens: float) -> float:
    return round(tokens / 1_000_000 * price_per_million_tokens, 6)
