from topoaccess_prod.integrations.mcp_like_stdio import parse_stdio_request


def test_stdio_invalid_json_returns_structured_error():
    _tool, _args, error = parse_stdio_request("not-json\n")
    assert error["error_type"] == "invalid_json"
    assert error["recoverable"] is True


def test_stdio_non_object_returns_structured_error():
    _tool, _args, error = parse_stdio_request("[]\n")
    assert error["error_type"] == "invalid_request"


def test_stdio_bad_arguments_returns_structured_error():
    _tool, _args, error = parse_stdio_request('{"tool":"/health","arguments":[]}\n')
    assert error["error_type"] == "invalid_arguments"


def test_stdio_valid_request_parses():
    tool, args, error = parse_stdio_request('{"tool":"/health","arguments":{}}\n')
    assert error is None
    assert tool == "/health"
    assert args == {}
