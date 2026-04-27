# Safe Publish

V36 replaces the old sync workflow with a safe publish dry-run.

The safe publish tool:

- stages only an allowlist,
- blocks model files, GGUFs, caches, logs, secrets, and env files,
- requires Apache-2.0 license metadata,
- requires release artifacts,
- refuses push when no remote is configured,
- never force pushes.

The old `sync_repository.sh` is not used for publishing.

