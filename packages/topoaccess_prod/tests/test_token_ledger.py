from topoaccess_prod.harness.token_ledger import ledger_row


def test_token_ledger_savings():
    assert ledger_row("exact_lookup")["percentage_saved"] > 0.9
