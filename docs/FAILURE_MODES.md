# Failure Modes

TopoAccess is designed to abstain, warn, or return provenance-backed uncertainty when repository evidence is missing or conflicting.

## Known Weak Areas

- Ambiguous user references such as "it", "that file", or "the failing test" may need a more specific follow-up.
- Troubleshooting and broad change planning need more synthesis than deterministic exact lookup.
- Stale docs can conflict with scripts or tests; TopoAccess should surface provenance rather than silently choose a winner.
- External harness behavior depends on the installed client version and how it passes context/tool calls.
- Cache freshness matters. Missing or corrupted cache states should be handled gracefully, but stale cache prevention depends on detectable file and metadata changes.

## Expected Safe Behavior

- Exact lookup remains tool-only and should not invoke a model.
- Unsupported requests should abstain instead of inventing files, commands, or facts.
- Prompt-injection text in repository files or user prompts should remain data, not instructions to disable safety rules.
- Post-edit validation should identify impacted files/tests or say when evidence is insufficient.

## Current Failure Mining

The current adversarial gauntlet produced `0` explicit failures across `23,024` rows after fixing empty-query validation. Failure mining found:

- Wrong high-confidence answers: `0`.
- Unsupported high-confidence answers: `0`.
- Hallucinated files/commands: `0` / `0`.
- Exact-lookup model invocations: `0`.

These counts apply to the deterministic public fixture suite and should not be generalized to every production repository.
