# Harness Integration

TopoAccess can be used from shell-capable, HTTP-capable, and stdio-capable coding agents.

## Codex

```bash
python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief \
  --profile default \
  --task "Plan a safe CLI improvement"
```

## Claude Code

Use the generated hook examples in `release/topoaccess_prod_v39/claude_hooks/`. Hooks are read-first and should not auto-run destructive commands.

## Cursor

Use the generated rule file in `release/topoaccess_prod_v39/cursor_rules/` to remind agents to run TopoAccess preflight and post-edit validation.

## Generic HTTP/stdio

Use `release/topoaccess_prod_v39/openapi.json`, `mcp_like_manifest.json`, and `stdio_schema.json` for tool integration. Write/apply tools are absent by default; post-edit validation is read-only.
