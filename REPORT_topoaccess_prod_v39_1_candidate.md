# TopoAccess V39.1 Candidate

V39.1 repairs PR #1 public CI, restores the public cache package surface, polishes README/docs, adds release asset and branch-protection guidance, and pushes a follow-up commit to `release/v1.0.0-rc1-public` after tests/audits pass.

Initial observed blocker: GitHub Actions `TopoAccess CI / test` fails because `topoaccess_prod.cache.store` is missing from the public export.

## Current V39.1 Status

- CI failure fixed locally: yes.
- `topoaccess_prod.cache` restored: yes.
- Product tests: passed, 67 tests.
- Public CI-ready checks: passed locally.
- README improved: yes.
- Release asset instructions generated: yes.
- Branch protection guidance generated: yes.
- Follow-up commit pushed to PR #1: pending final push step.

## Branch Protection Setting

Require the actual GitHub status check:

```text
TopoAccess CI / test
```

Do not require the workflow filename `.github/workflows/topoaccess-prod-ci.yml`.
