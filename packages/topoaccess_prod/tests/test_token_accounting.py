from topoaccess_prod.harness.token_accounting import token_row


def test_token_savings_positive():
    assert token_row("exact_lookup")["token_savings"] > 0.9
