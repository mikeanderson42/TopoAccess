# Safe Sync

The user sync script pattern can stage with `git add -A` and push. V38 does not run it directly.

The safe wrapper stages only an allowlist after tests, release gates, artifact audit, secret scan, branch check, and remote check. It never force pushes.

```bash
python packages/topoaccess_prod/scripts/topoaccess_safe_sync.py --branch topoaccess-prod-v38-distribution --release release/topoaccess_prod_v38 --dry-run
```

