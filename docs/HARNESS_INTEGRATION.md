# Harness Integration

TopoAccess can be used from shell-capable, HTTP-capable, and stdio-capable coding agents.

TopoAccess is model-agnostic by default. Exact lookup never requires a model; local model adapters are configured by workspace profile only for category-gated synthesis/planning tasks.

## Codex

```bash
topoaccess codex-brief \
  --profile default \
  --task "Plan a safe CLI improvement"

topoaccess setup codex --profile demo --dry-run
```

Legacy script paths remain available for harnesses that call fixed files:

```bash
python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief \
  --profile demo \
  --task "What tests should I run after editing README.md?"
```

## Claude Code

Use the hook examples in `examples/integrations/claude_hooks/`. Hooks are read-first and should not auto-run destructive commands.

```bash
topoaccess setup claude --profile demo --dry-run
```

## Cursor

Use `examples/integrations/cursor_rules/topoaccess.mdc` to remind agents to run TopoAccess preflight and post-edit validation.

```bash
topoaccess setup cursor --profile demo --dry-run
```

## Generic HTTP/stdio

Use `examples/integrations/schemas/openapi.json`, `mcp_like_manifest.json`, and `stdio_schema.json` for tool integration. Write/apply tools are absent by default; post-edit validation is read-only.

```bash
topoaccess serve-http --profile demo --port 8876 --smoke
topoaccess stdio --profile demo --help
topoaccess setup generic --profile demo --dry-run
topoaccess setup http --profile demo --dry-run
topoaccess setup stdio --profile demo --dry-run
```

Setup shortcuts are dry-run by default and print snippets. They do not write external harness configs unless a future explicit `--apply` path is added.
