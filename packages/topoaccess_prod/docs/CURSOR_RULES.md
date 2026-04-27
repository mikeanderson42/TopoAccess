# Cursor Rules

TopoAccess can emit a Cursor `.mdc` rule file scoped to `packages/topoaccess_prod/**`.

The rules are dry-run by default and remind Cursor to run preflight before edits, post-edit validation afterward, keep exact lookup tool-only, and avoid committing local artifacts.

Generate:

```bash
python packages/topoaccess_prod/scripts/topoaccess_generate_cursor_rules.py --profile default --dry-run --out release/topoaccess_prod_v37/cursor_rules
```

