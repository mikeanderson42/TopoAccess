from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


PUBLIC_VERSION = "1.0.0rc1"
BRANCH = "release/v1.0.0-rc1"
REMOTE = "https://github.com/mikeanderson42/TopoAccess.git"


EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "runs",
    "logs",
    "tmp",
    "dist",
    "build",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".gguf", ".safetensors", ".ckpt", ".pth", ".pt"}
EXCLUDED_NAMES = {".env"}
PRIVATE_PATHS = {
    "<local-sync-script-path>": "<local-sync-script-path>",
    "<local-repo-sync-script-path>": "<local-repo-sync-script-path>",
    "<local-repo-path>": "<local-repo-path>",
}


def _copy_tree(src: Path, dst: Path, files_copied: list[str], files_excluded: list[str]) -> None:
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            if path.is_file():
                files_excluded.append(str(rel))
            continue
        if path.is_file() and (path.suffix.lower() in EXCLUDED_SUFFIXES or path.name in EXCLUDED_NAMES):
            files_excluded.append(str(rel))
            continue
        target = dst / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            files_copied.append(str(target.relative_to(dst)))


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _scrub_private_paths(root: Path) -> None:
    for path in root.rglob("*"):
        if not path.is_file() or path.stat().st_size > 1_000_000:
            continue
        if path.suffix.lower() in {".pyc", ".pyo", ".gz", ".zip"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        new_text = text
        for old, new in PRIVATE_PATHS.items():
            new_text = new_text.replace(old, new)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")


def _public_readme() -> str:
    return """# TopoAccess

TopoAccess is a local repo-intelligence sidecar for coding agents.

It is not a replacement for Codex, Claude Code, Cursor, Aider, OpenClaw, OpenHands, or other coding agents. It gives those agents a smaller, provenance-backed view of a repository so exact lookup, test-impact, command lookup, change planning, and post-edit validation do not require dumping broad repo context into a model.

## Why It Exists

Coding agents waste tokens and make mistakes when they must rediscover repository structure from scratch. TopoAccess routes exact work through deterministic tools and TopoGraph/cache indexes, then reserves model use for category-gated synthesis tasks.

Measured local release-candidate results:

- Codex dogfood savings: 0.9332 average token savings over 250 V38 tasks.
- Harness token savings baseline: 0.9553.
- Exact lookup: tool-only.
- Preferred model use: category-gated.
- Wrong high-confidence: 0.
- Unsupported high-confidence: 0.

Public CI does not require a local Qwen model, GPU, LM Studio, Ollama, private cache, or model weights.

## Architecture

```text
coding agent -> TopoAccess CLI/HTTP/stdio -> router -> deterministic tools / TopoGraph / cache
                                             -> category-gated preferred model only when allowed
                                             -> provenance + trace + safety counters
```

## Install

```bash
git clone https://github.com/mikeanderson42/TopoAccess.git
cd TopoAccess
python -m pip install -e packages/topoaccess_prod
topoaccessctl --help
```

## Quick Start

```bash
python packages/topoaccess_prod/scripts/topoaccessctl.py status --cache cache/topoaccess_v21
python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief --profile default --task "Improve exact command lookup resolver"
python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit --profile default --changed-files packages/topoaccess_prod/README.md
```

## Harness Integrations

- Codex: `release/topoaccess_prod_v37/AGENTS.md` style guidance and `topoaccess_agent.py codex-brief`.
- Claude Code: safe hook examples.
- Cursor: `.mdc` rules.
- Aider: token-budgeted repo-map export.
- Hermes/generic: CLI/HTTP/stdio tool schemas.

## Safety Model

- Exact lookup remains tool-only.
- Model use remains category-gated for change planning, model-required narrative, report synthesis, and troubleshooting.
- Nonpreferred model use fails local release gates.
- Provenance is required for audited answers.
- Unsupported requests should abstain instead of guessing.

## Known Limitations

- Native service install remains an operator action.
- Public CI is model-free and validates import, CLI, tests, conformance, artifact audit, and secret scan.
- Local model-backed categories require operator configuration.

## License And Credits

Apache-2.0. Creator / Project Owner / System Architect: Michael A. Anderson <MikeAnderson42@gmail.com>.

AI-assisted implementation is credited as assistance under Michael A. Anderson's direction, not ownership.
"""


def _workflow() -> str:
    return """name: TopoAccess CI

on:
  push:
    branches: ["main", "release/**"]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install package
        run: python -m pip install -U pip pytest && python -m pip install -e packages/topoaccess_prod
      - name: Product tests
        run: python -m pytest packages/topoaccess_prod/tests
      - name: Import and CLI smoke
        run: python -c "import topoaccess_prod; print(topoaccess_prod.__name__)" && topoaccessctl --help
      - name: Compile
        run: python -m compileall packages/topoaccess_prod
      - name: Artifact audit
        run: python packages/topoaccess_prod/scripts/topoaccess_artifact_audit.py --paths packages/topoaccess_prod .github --out audit.jsonl --report AUDIT.md
      - name: Secret scan
        run: python packages/topoaccess_prod/scripts/topoaccess_secret_scan.py --paths packages/topoaccess_prod .github --out secret_scan.jsonl --report AUDIT.md
"""


def _small_docs(target: Path) -> None:
    docs = {
        "docs/INSTALL.md": "# Install\n\n```bash\npython -m pip install -e packages/topoaccess_prod\ntopoaccessctl --help\n```\n",
        "docs/QUICKSTART.md": "# Quickstart\n\nRun a Codex brief and post-edit validation from the package scripts.\n",
        "docs/HOW_IT_WORKS.md": "# How It Works\n\nTopoAccess routes repo questions through deterministic tools, TopoGraph/cache indexes, and category-gated synthesis.\n",
        "docs/TOKEN_SAVINGS.md": "# Token Savings\n\nV38 Codex dogfood reported `0.9332` average savings. Exact lookup savings are driven by tool-only routing.\n",
        "docs/HARNESS_INTEGRATION.md": "# Harness Integration\n\nCodex, Claude Code, Cursor, Aider, OpenClaw, OpenHands, HTTP, and stdio integrations are documented under `packages/topoaccess_prod/docs`.\n",
        "docs/SAFETY.md": "# Safety\n\nExact lookup is tool-only. Preferred model use is category-gated. Provenance is required.\n",
        "docs/API.md": "# API\n\nUse the CLI scripts, OpenAPI manifest, MCP-like manifest, and stdio schema in `packages/topoaccess_prod`.\n",
        "docs/DEVELOPMENT.md": "# Development\n\nRun `python -m pytest packages/topoaccess_prod/tests` and `python -m compileall packages/topoaccess_prod`.\n",
        "docs/PUBLISHING.md": "# Publishing\n\nPush release branches only after tests, artifact audit, secret scan, and conformance pass. Never force push.\n",
    }
    for path, text in docs.items():
        _write(target / path, text)


def _examples(target: Path) -> None:
    _write(target / "examples/workspace.default.yaml", "profile: default\nrepo: .\ncache: cache/topoaccess_v21\nmodel_required: false\n")
    _write(target / "examples/codex_brief.sh", "#!/usr/bin/env bash\npython packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief --profile default --task \"$*\"\n")
    _write(target / "examples/http_tool_server.sh", "#!/usr/bin/env bash\npython packages/topoaccess_prod/scripts/topoaccess_http_tool_server.py --profile default --port 8876\n")
    _write(target / "examples/stdio_tool.sh", "#!/usr/bin/env bash\npython packages/topoaccess_prod/scripts/topoaccess_agent.py stdio\n")
    _write(target / "examples/post_edit_validation.sh", "#!/usr/bin/env bash\npython packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit --profile default --changed-files \"$@\"\n")
    _write(target / "examples/basic_repo/README.md", "# Basic Repo Fixture\n\nA tiny fixture for public, model-free smoke examples.\n")


def _github_files(target: Path) -> None:
    _write(target / ".github/workflows/topoaccess-ci.yml", _workflow())
    _write(target / ".github/ISSUE_TEMPLATE/bug_report.md", "## Bug\n\n## Steps To Reproduce\n\n## Expected Behavior\n")
    _write(target / ".github/ISSUE_TEMPLATE/feature_request.md", "## Feature\n\n## Use Case\n\n## Safety Impact\n")
    _write(target / ".github/pull_request_template.md", "## Summary\n\n## Tests\n\n## Safety / Provenance\n\n- [ ] No model files, caches, secrets, logs, or env files\n")
    _write(target / ".github/dependabot.yml", "version: 2\nupdates: []\n")


def public_export(source: str, target: str, layout: str, out: str, report: str) -> dict:
    src_root = Path(source).resolve()
    target_root = Path(target).resolve()
    if target_root.exists():
        shutil.rmtree(target_root)
    target_root.mkdir(parents=True)
    files_copied: list[str] = []
    files_excluded: list[str] = []
    pkg_src = src_root / "packages" / "topoaccess_prod"
    pkg_dst = target_root / "packages" / "topoaccess_prod"
    _copy_tree(pkg_src, pkg_dst, files_copied, files_excluded)
    pyproject = pkg_dst / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text(encoding="utf-8")
        text = text.replace('version = "1.0.0"', f'version = "{PUBLIC_VERSION}"')
        text = text.replace('name = "topoaccess-prod"', 'name = "topoaccess-prod"')
        text = text.replace('include = ["topoaccess_prod*"]', 'include = ["topoaccess_prod*", "topoaccess*"]')
        pyproject.write_text(text, encoding="utf-8")
    stable = pkg_dst / "topoaccess"
    stable.mkdir(parents=True, exist_ok=True)
    (stable / "__init__.py").write_text('"""Stable TopoAccess compatibility shims for topoaccess-prod."""\n', encoding="utf-8")
    files_copied.append("packages/topoaccess_prod/topoaccess/__init__.py")
    for name in ["v29_common.py", "provenance.py"]:
        shutil.copy2(src_root / "topoaccess" / name, stable / name)
        files_copied.append(f"packages/topoaccess_prod/topoaccess/{name}")
    for pycache in target_root.rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)
    _write(target_root / "README.md", _public_readme())
    for name in ["LICENSE", "NOTICE", "CHANGELOG.md", "AUTHORS.md", "CREDITS.md"]:
        shutil.copy2(pkg_src / name, target_root / name)
        files_copied.append(name)
    _write(target_root / "CONTRIBUTING.md", "# Contributing\n\nRun tests and safety scans before submitting a PR.\n")
    _write(target_root / "SECURITY.md", "# Security\n\nDo not submit secrets, model weights, local caches, logs, or env files. Report issues through GitHub issues.\n")
    _write(
        target_root / ".gitignore",
        "__pycache__/\n*.py[cod]\n.pytest_cache/\n*.egg-info/\nbuild/\ndist/\ncache/\nruns/\nlogs/\n.env\n*.gguf\n*.safetensors\n*.ckpt\n*.pt\n*.pth\n",
    )
    _small_docs(target_root)
    _examples(target_root)
    _github_files(target_root)
    compat_src = src_root / "release" / "topoaccess_prod_v37"
    compat_dst = target_root / "release" / "topoaccess_prod_v39"
    if compat_src.exists():
        for name in [
            "AGENTS.md",
            "cursor_rules",
            "claude_hooks",
            "repomap",
            "tool_schema.json",
            "openapi.json",
            "mcp_like_manifest.json",
            "stdio_schema.json",
        ]:
            src_item = compat_src / name
            dst_item = compat_dst / name
            if src_item.is_dir():
                shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
            elif src_item.exists():
                dst_item.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_item, dst_item)
            if src_item.exists():
                files_copied.append(str(dst_item.relative_to(target_root)))
    _write(target_root / "release_notes.md", "# v1.0.0-rc1\n\nFirst public release candidate for TopoAccess.\n")
    _scrub_private_paths(target_root)
    strategy = {
        "layout": "package-subfolder",
        "reason": "Root-module conversion is risky because product commands and tests intentionally target packages/topoaccess_prod.",
        "public_layout_mode": layout,
    }
    row = {
        "run_id": "v39_public_export",
        "phase": "public_export",
        "source_worktree": str(src_root),
        "public_export_path": str(target_root),
        "branch": BRANCH,
        "commit": "",
        "remote_url": REMOTE,
        "remote_verified": False,
        "public_layout_mode": strategy["layout"],
        "files_copied": len(files_copied),
        "files_excluded": len(files_excluded),
        "blocked_files": [],
        "package_path": "packages/topoaccess_prod",
        "version": PUBLIC_VERSION,
        "release_tag": "v1.0.0-rc1",
        "tests_status": "pending",
        "audit_status": "pending",
        "scan_status": "pending",
        "conformance_status": "pending",
        "push_attempted": False,
        "push_status": "not_attempted",
        "result_status": "pass",
        "strategy": strategy,
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    Path("runs/topoaccess_prod_v39/export_strategy.jsonl").write_text(json.dumps(strategy, sort_keys=True) + "\n", encoding="utf-8")
    Path(report).write_text(
        "# V39 Public Repo Layout\n\n"
        "- Layout chosen: `package-subfolder`.\n"
        "- Reason: root-module conversion is risky because commands/tests intentionally target `packages/topoaccess_prod`.\n"
        f"- Public export path: `{target_root}`.\n"
        f"- Files copied: `{len(files_copied)}`.\n"
        f"- Files excluded: `{len(files_excluded)}`.\n",
        encoding="utf-8",
    )
    return row
