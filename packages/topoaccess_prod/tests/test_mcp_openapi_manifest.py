from topoaccess_prod.harness.tool_schema_conformance import validate_tool_schema
from topoaccess_prod.integrations.mcp_manifest import mcp_manifest, stdio_schema
from topoaccess_prod.integrations.openapi_manifest import openapi_manifest


def test_manifest_policies():
    assert openapi_manifest()["paths"]["/exact-lookup"]["post"]["x-model-fallback"] is False
    assert any(tool["name"] == "exact_lookup" and tool["model_fallback_allowed"] is False for tool in mcp_manifest()["tools"])
    assert stdio_schema()["transport"] == "stdio"
    assert validate_tool_schema()["exact_lookup_tool_only"] is True

