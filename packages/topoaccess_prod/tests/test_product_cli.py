from topoaccess_prod.cli.topoaccessctl import run_command


def test_product_cli_status():
    assert run_command("status")["status"] == "pass"
