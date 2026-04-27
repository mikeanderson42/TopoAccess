# Claude Code Hooks

TopoAccess emits safe example Claude Code hooks for workspace status, preflight reminders, post-edit validation, and pytest/git command enrichment.

The generated settings are examples only. They do not auto-run destructive commands and do not bypass preferred-model or exact-tool policy.

Generate:

```bash
python packages/topoaccess_prod/scripts/topoaccess_generate_claude_hooks.py --profile default --dry-run --out release/topoaccess_prod_v37/claude_hooks
```

