# Harness Token Ledger

V34 adds per-harness token accounting for Codex, Claude Code, OpenClaw, Hermes, generic, HTTP, and stdio.

Run:

```bash
python packages/topoaccess_prod/scripts/topoaccess_harness_token_breakdown.py --profile default --harnesses codex claude-code openclaw hermes generic http stdio --categories exact_lookup test_impact command_lookup report_fact change_planning troubleshooting post_edit_validation unsupported
```

Savings differ by harness because prompt-pack formatting overhead differs. Exact and tool-only categories generally save the most tokens.
