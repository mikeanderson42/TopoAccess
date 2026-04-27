# TopoAccess v1.0.0-rc1 Upload Commands

Run these commands only after the V40 release-assets PR is merged and checks remain green on `main`.

```bash
gh release create v1.0.0-rc1 \
  --repo mikeanderson42/TopoAccess \
  --target main \
  --title "TopoAccess v1.0.0-rc1" \
  --notes-file release/topoaccess_prod_v40/release_notes.md \
  --prerelease
```

```bash
gh release upload v1.0.0-rc1 \
  --repo mikeanderson42/TopoAccess \
  release/topoaccess_prod_v40/checksums.txt \
  release/topoaccess_prod_v40/dist/topoaccess-prod-v38-source-fallback.tar.gz \
  release/topoaccess_prod_v40/archive/topoaccess-prod-v38-release.tar.gz
```

Do not upload caches, model files, GGUF files, logs, `.env` files, or secrets.
