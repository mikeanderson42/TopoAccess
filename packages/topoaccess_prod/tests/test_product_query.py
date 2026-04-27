from topoaccess_prod.cli.topoaccessctl import run_command


def test_product_query_route():
    result = run_command("query", query="What tests should I run?")
    assert result["route"] == "tool_only"
