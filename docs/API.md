# API

TopoAccess exposes CLI, HTTP, stdio, OpenAPI, and MCP-like tool surfaces.

Public API rules:

- Exact lookup tools must mark model-backed synthesis as forbidden.
- Post-edit validation is read-only.
- Provenance fields are required for audited answers.
- Unsupported responses must be explicit.
- Optional model-backed synthesis is category-gated and configured by workspace profile.
