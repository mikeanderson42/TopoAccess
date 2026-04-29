import io
import json

from topoaccess_prod.integrations.http_tool_server import ToolHandler, handle_tool


def test_http_health_tool():
    assert handle_tool("/health")["preferred_model_verified"] is True


def test_http_unknown_endpoint_is_structured_error():
    result = handle_tool("/missing")
    assert result["status"] == "error"
    assert result["error_type"] == "unknown_endpoint"


def test_http_handler_uses_threading_ready_class():
    assert ToolHandler.max_body_bytes >= 1_000_000


def test_http_read_json_body_rejects_invalid_json():
    handler = object.__new__(ToolHandler)
    handler.headers = {"Content-Length": "8"}
    handler.rfile = io.BytesIO(b"not-json")
    try:
        handler._read_json_body()
    except ValueError as exc:
        assert str(exc) == "invalid_json"
    else:  # pragma: no cover
        raise AssertionError("invalid JSON should fail")


def test_http_read_json_body_accepts_object():
    payload = b'{"query":"x"}'
    handler = object.__new__(ToolHandler)
    handler.headers = {"Content-Length": str(len(payload))}
    handler.rfile = io.BytesIO(payload)
    assert handler._read_json_body() == {"query": "x"}
