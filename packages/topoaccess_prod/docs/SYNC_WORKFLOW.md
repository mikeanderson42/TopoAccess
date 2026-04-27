# Sync Workflow

V35 inspected `<local-sync-script-path>`.

The script stages the full worktree, commits, and pushes. It has `--help`, but no dry-run mode. It must not be run automatically for TopoAccess publication.

Use it only after:

- License is confirmed.
- Remote is configured.
- Artifact audit passes.
- Secret scan passes.
- Operator reviews staged files.

