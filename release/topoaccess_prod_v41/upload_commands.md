# TopoAccess v1.0.0-rc1 Upload Commands

Run these commands after this release-candidate polish PR is merged and checks are green on `main`.

```bash
gh release create v1.0.0-rc1 \
  --repo mikeanderson42/TopoAccess \
  --target main \
  --title "TopoAccess v1.0.0-rc1" \
  --notes-file release/topoaccess_prod_v41/release_notes.md \
  --prerelease
```

```bash
gh release upload v1.0.0-rc1 \
  --repo mikeanderson42/TopoAccess \
  release/topoaccess_prod_v41/dist/topoaccess_prod_v41-source-fallback.tar.gz \
  release/topoaccess_prod_v41/archive/topoaccess_prod_v41-release.tar.gz \
  release/topoaccess_prod_v41/checksums.txt \
  release/topoaccess_prod_v41/release_manifest.json
```

Do not upload caches, model files, GGUF files, `.env` files, secrets, or local logs.
