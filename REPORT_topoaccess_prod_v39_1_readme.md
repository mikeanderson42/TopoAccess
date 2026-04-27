# TopoAccess V39.1 README

The root README was rewritten for a public audience.

## Improvements

- Defines TopoAccess as a local repo-intelligence sidecar, not a coding-agent replacement.
- Explains token savings, exact lookup, provenance, test-impact, command lookup, and unsupported handling.
- Adds an architecture flow from agent to workspace profile, TopoGraph/cache/tools, category router, and provenance/trace output.
- Documents measured results: Codex dogfood savings `0.9332`, harness savings about `0.9553`, exact lookup tool-only, wrong high-confidence `0`, unsupported high-confidence `0`.
- Clarifies that public CI does not require the local preferred model, GPU, LM Studio, Ollama, or private cache.
- Adds quickstart commands for install, workspace init, doctor, Codex brief, and post-edit validation.

Docs polished:

- `docs/QUICKSTART.md`
- `docs/HOW_IT_WORKS.md`
- `docs/TOKEN_SAVINGS.md`
- `docs/HARNESS_INTEGRATION.md`
