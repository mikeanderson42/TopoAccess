# TopoAccess V39.1 Branch Rules

The branch-protection rule should require the actual check name:

```text
TopoAccess CI / test
```

It should not require the workflow filename:

```text
.github/workflows/topoaccess-prod-ci.yml
```

Recommended solo-maintainer settings:

- Keep force-push protection enabled.
- Keep branch deletion protection enabled.
- Keep pull-request-before-merge enabled.
- Keep required status checks enabled.
- Set required approvals to `0` if allowed, use admin bypass after green CI, or add another reviewer.
- Do not bypass failing CI.

PR #1 remains on `release/v1.0.0-rc1-public`; do not push directly to `main`.
