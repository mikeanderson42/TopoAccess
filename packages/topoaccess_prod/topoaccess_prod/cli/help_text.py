from __future__ import annotations

DESCRIPTION = """TopoAccess unified CLI.

TopoAccess is model-agnostic by default. Exact lookup remains tool-only, and
optional model-backed synthesis is workspace-configured and category-gated.
"""

EPILOG = """Examples:
  topoaccess workspace init --profile demo --repo . --cache .topoaccess/cache
  topoaccess doctor --profile demo
  topoaccess codex-brief --profile demo --task "What tests should I run after editing README.md?"
  topoaccess post-edit --profile demo --changed-files README.md
  topoaccess benchmark smoke --profile demo
"""
