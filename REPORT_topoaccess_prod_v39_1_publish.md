# TopoAccess V39.1 Publish

Target PR: https://github.com/mikeanderson42/TopoAccess/pull/1

Target branch: `release/v1.0.0-rc1-public`

## Planned Commit

```bash
git commit -m "Fix public CI and polish TopoAccess rc1"
git push origin release/v1.0.0-rc1-public
```

## Release Assets

Release asset instructions were added in:

- `docs/RELEASE_ASSETS.md`
- `release/topoaccess_prod_v39_1/release_upload_commands.md`
- `release/topoaccess_prod_v39_1/release_assets.json`

No GitHub Release was created or uploaded. That should happen only after PR merge and green CI.

## Branch Protection

The required status check should be:

```text
TopoAccess CI / test
```

It should not be the workflow file path:

```text
.github/workflows/topoaccess-prod-ci.yml
```

Solo-maintainer options are documented in `docs/BRANCH_PROTECTION.md`.
