from __future__ import annotations


def regression_pass(average: float, threshold: float = 0.95) -> bool:
    return average >= threshold
