# Publish Checklist

Before pushing or tagging:

- Product tests pass.
- Targeted regressions pass.
- Adapter smoke passes.
- License gate is confirmed for public release.
- Publish guard reports no model files, GGUFs, caches, logs, secrets, or env files.
- Remote is configured and verified.

Run:

```bash
python packages/topoaccess_prod/scripts/topoaccess_publish_guard.py --branch topoaccess-prod-v33-publish --release release/topoaccess_prod_v33
```

Do not force push.
