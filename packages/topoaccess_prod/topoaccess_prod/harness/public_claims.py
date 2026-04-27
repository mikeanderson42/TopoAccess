from __future__ import annotations


def public_claims(summary: dict) -> list[str]:
    return [
        f"In the public model-free benchmark, TopoAccess-assisted modes averaged {summary['average_token_savings']:.4f} token savings vs the broad-context baseline.",
        f"Median assisted token savings was {summary['median_token_savings']:.4f}.",
        f"p50/p95 latency across all modes was {summary['p50_latency_ms']:.1f} ms / {summary['p95_latency_ms']:.1f} ms.",
        "Exact lookup remained tool-only; public CI and public benchmark paths do not require local model weights.",
        f"Wrong high-confidence and unsupported high-confidence counts were {summary['wrong_high_confidence']} and {summary['unsupported_high_confidence']}.",
    ]


def claims_are_safe(summary: dict) -> bool:
    return summary["wrong_high_confidence"] == 0 and summary["unsupported_high_confidence"] == 0 and summary["average_token_savings"] >= 0
