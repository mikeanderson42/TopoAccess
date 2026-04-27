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
- Provenance fields are required for audited answers. Audit-grade provenance can include span-hash entries with `source_uri`, line span, byte offsets, `span_byte_length`, `span_line_count`, `content_hash`, `span_hash`, and a bounded excerpt.
- Agent-facing provenance does not emit full raw audited span text by default. Bounded excerpts are display aids, not a second source of truth.
- A `source_uri` or path by itself is not immutable evidence; audit-required verification should fail if a cited source has no span hash or if the cited span no longer matches.
- If a cited span moves within the same source, verification can pass by scanning candidate spans with the same byte length, line count, and hash.
- Multiple matching candidate spans are scored by prefix, suffix, section-anchor, occurrence, line-proximity, and byte-proximity signals. Relocation only passes when the top score is at least `0.85`, the score gap is at least `0.20`, and at least one context anchor matches.
- Verification results include calibration fields: `winning_tier`, `confidence`, `score_gap`, `candidate_count`, `sampled_reaudit`, `sampled_reaudit_result`, and `calibration_status`.
- Sampled re-audit uses deterministic hashing of `source_uri`, `span_hash`, and `content_hash` at a default `0.02` rate. Sampled failures fail closed.
- Post-call validation should prefer field-mask scoped diffs over raw JSON equality, so allowed response fields can change without approving unrelated mutations.
- Unsupported responses must be explicit.
- Optional model-backed synthesis is category-gated and configured by workspace profile.

First-use API smoke:

```bash
topoaccess try
topoaccess verify-provenance --path README.md --start-line 1 --end-line 5
topoaccess setup http --profile demo --dry-run
topoaccess setup stdio --profile demo --dry-run
```
