from topoaccess_prod.harness.token_savings_regression import regression_pass


def test_token_savings_regression_threshold():
    assert regression_pass(0.9501)
    assert not regression_pass(0.94)
