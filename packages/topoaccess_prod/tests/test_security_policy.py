from topoaccess_prod.harness.security_policy import validate_policy


def test_security_policy_passes():
    assert validate_policy()["result_status"] == "pass"

