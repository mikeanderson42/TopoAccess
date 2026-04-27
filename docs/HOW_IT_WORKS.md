# How It Works

TopoAccess sits beside a coding agent and answers repo-intelligence questions through deterministic tools, cache metadata, TopoGraph-style indexes, and compact prompt packs.

```text
agent -> CLI/HTTP/stdio -> workspace profile -> tools/cache/router -> provenance/trace
```

For audited answers, TopoAccess can attach structured span provenance. A span-hash entry records the source URI, cited line span, byte offsets, byte length, line count, full-content hash, exact cited-span hash, and a bounded excerpt. Agent-facing outputs do not include full raw audited span text by default.

Verification tries the original byte offset first. If the file changed and the original offset no longer matches, TopoAccess scans live source candidates with the same byte length and line count. Zero matches return `fail_missing_force_reaudit`. One match returns `pass_relocated_unique`. Multiple matches are scored with prefix hash, suffix hash, section-anchor hash, occurrence index, line proximity, and byte proximity; the result only passes when the top score is at least `0.85`, the score gap is at least `0.20`, and at least one context anchor matches. Otherwise TopoAccess returns `fail_ambiguous_force_reaudit`.

Post-call validation uses a field-mask posture for payload-style checks: expected fields may change, but changes outside the allowed mask are unauthorized. Raw JSON equality is not treated as the authority for scoped validation.

Exact repo facts stay tool-only and never require a model. Optional model-backed synthesis is only allowed for category-gated synthesis/planning tasks:

- `change_planning`
- `model_required_narrative`
- `report_synthesis`
- `troubleshooting`

This keeps exact lookup, command lookup, artifact lookup, and report facts from becoming broad model-context prompts. Public CI exercises this deterministic surface without requiring private model files, LM Studio, Ollama, GPU access, or private caches.

The current public benchmark shows the largest token savings on exact lookup, unsupported request handling, command lookup, symbol lookup, and artifact lookup. Change planning and troubleshooting still save tokens, but they are the weakest categories because they need richer context and may use optional category-gated synthesis in local deployments.
