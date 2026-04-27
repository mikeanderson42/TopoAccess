from topoaccess_prod.integrations.http_tool_server import handle_tool


def test_http_health_tool():
    assert handle_tool("/health")["preferred_model_verified"] is True
