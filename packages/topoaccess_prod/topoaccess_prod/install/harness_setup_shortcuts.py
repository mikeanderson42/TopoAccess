from __future__ import annotations

from .harness_installer import install_target


TARGET_ALIASES = {
    "claude": "claude-code",
    "cursor": "cursor",
    "aider": "aider",
    "codex": "codex",
    "openclaw": "openclaw",
    "openhands": "openhands",
    "hermes": "hermes",
    "generic": "generic",
    "http": "http",
    "stdio": "stdio",
}

TARGET_NOTES = {
    "codex": "Use codex-brief before edits and post-edit after changes.",
    "claude-code": "Use hook examples in examples/integrations/claude_hooks/.",
    "cursor": "Use examples/integrations/cursor_rules/topoaccess.mdc.",
    "aider": "Use repo-map exports and call topoaccess before broad-context prompts.",
    "openclaw": "Use CLI/HTTP snippets when the OpenClaw client is installed.",
    "openhands": "Use CLI/HTTP snippets when the OpenHands client is installed.",
    "hermes": "Use generic CLI/stdio/HTTP integration snippets.",
    "generic": "Use CLI, HTTP, stdio, or schema files from examples/integrations/.",
    "http": "Run topoaccess serve-http --smoke before connecting a client.",
    "stdio": "Run topoaccess stdio interactively from a harness process.",
}


def run_setup_shortcut(target: str, profile: str = "demo", dry_run: bool = True, apply: bool = False) -> dict:
    canonical = TARGET_ALIASES.get(target, target)
    if apply:
        return {
            "command": f"topoaccess setup {target}",
            "target": target,
            "canonical_target": canonical,
            "dry_run": False,
            "result_status": "fail",
            "error": "--apply is reserved for future explicit external-config writers; dry-run snippets are safe today.",
        }
    payload = install_target(canonical, profile=profile, dry_run=True, release_dir=".topoaccess/setup")
    return {
        "command": f"topoaccess setup {target}",
        "target": target,
        "canonical_target": canonical,
        "profile": profile,
        "dry_run": dry_run,
        "apply": apply,
        "snippet": payload["snippet"],
        "test_command": f"topoaccess install-harness --target {canonical} --profile {profile} --dry-run",
        "integration_note": TARGET_NOTES.get(canonical, "Use TopoAccess as a model-free repo-intelligence sidecar."),
        "target_installed_check": "not_checked",
        "external_configs_modified": False,
        "result_status": "pass",
    }
