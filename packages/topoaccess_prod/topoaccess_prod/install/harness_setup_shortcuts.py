from __future__ import annotations

from .harness_installer import install_target


TARGET_ALIASES = {
    "claude": "claude-code",
    "cursor": "cursor",
    "aider": "aider",
    "codex": "codex",
    "generic": "generic",
    "http": "http",
    "stdio": "stdio",
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
        "external_configs_modified": False,
        "result_status": "pass",
    }
