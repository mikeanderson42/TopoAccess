# How It Works

TopoAccess sits beside a coding agent and answers repo-intelligence questions through deterministic tools, cache metadata, TopoGraph-style indexes, and compact prompt packs.

```text
agent -> CLI/HTTP/stdio -> workspace profile -> tools/cache/router -> provenance/trace
```

Exact repo facts stay tool-only and never require a model. Optional model-backed synthesis is only allowed for category-gated synthesis/planning tasks:

- `change_planning`
- `model_required_narrative`
- `report_synthesis`
- `troubleshooting`

This keeps exact lookup, command lookup, artifact lookup, and report facts from becoming broad model-context prompts. Public CI exercises this deterministic surface without requiring private model files, LM Studio, Ollama, GPU access, or private caches.
