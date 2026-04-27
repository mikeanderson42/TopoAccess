# API

TopoAccess exposes CLI, HTTP, stdio, OpenAPI, and MCP-like tool surfaces.

Preferred local commands:

```bash
topoaccess --help
topoaccess init
topoaccess try
topoaccess serve-http --profile demo --port 8876 --smoke
topoaccess stdio --profile demo --help
topoaccess conformance --release examples/integrations
```

Public API rules:

- Exact lookup tools must mark model-backed synthesis as forbidden.
- Post-edit validation is read-only.
- Provenance fields are required for audited answers.
- Unsupported responses must be explicit.
- Optional model-backed synthesis is category-gated and configured by workspace profile.

First-use API smoke:

```bash
topoaccess try
topoaccess setup http --profile demo --dry-run
topoaccess setup stdio --profile demo --dry-run
```
