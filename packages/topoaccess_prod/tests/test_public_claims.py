from topoaccess_prod.harness.benchmark_marathon import generate_row
from topoaccess_prod.harness.benchmark_stats import summarize_rows
from topoaccess_prod.harness.public_claims import claims_are_safe, public_claims


def test_public_claims_are_safe_for_zero_high_confidence_failures():
    summary = summarize_rows([generate_row(i, "demo", 11, ["topoaccess_tool_only"], ["exact_lookup"]) for i in range(10)])
    claims = public_claims(summary)
    assert claims
    assert claims_are_safe(summary)
