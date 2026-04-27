from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class CommandInfo:
    name: str
    summary: str
    category: str
    model_free_default: bool = True
    legacy_equivalent: str = ""


COMMANDS: dict[str, CommandInfo] = {
    "init": CommandInfo("init", "Create a demo workspace and local cache for first use.", "workspace", legacy_equivalent="topoaccess workspace init"),
    "try": CommandInfo("try", "Run a self-contained model-free demo.", "workspace"),
    "setup": CommandInfo("setup", "Generate dry-run harness setup snippets with short target names.", "integration", legacy_equivalent="topoaccess install-harness"),
    "version": CommandInfo("version", "Print package version and public runtime posture.", "release"),
    "commands": CommandInfo("commands", "List supported topoaccess subcommands.", "help"),
    "workspace": CommandInfo("workspace", "Initialize, inspect, list, or validate workspace profiles.", "workspace", legacy_equivalent="topoaccess_workspace.py"),
    "doctor": CommandInfo("doctor", "Run model-free workspace and package health checks.", "workspace", legacy_equivalent="topoaccess_doctor.py"),
    "query": CommandInfo("query", "Run a model-free/product query through topoaccessctl.", "lookup", legacy_equivalent="topoaccessctl.py query"),
    "preflight": CommandInfo("preflight", "Generate a generic-agent preflight recommendation.", "agent", legacy_equivalent="topoaccess_agent.py preflight"),
    "codex-brief": CommandInfo("codex-brief", "Generate a compact Codex-oriented repo brief.", "agent", legacy_equivalent="topoaccess_agent.py codex-brief"),
    "post-edit": CommandInfo("post-edit", "Validate changed files after an edit.", "agent", legacy_equivalent="topoaccess_agent.py post-edit"),
    "benchmark": CommandInfo("benchmark", "Run model-free smoke, row, or scenario benchmarks.", "benchmark"),
    "serve-http": CommandInfo("serve-http", "Start or smoke-test the HTTP tool server.", "integration", legacy_equivalent="topoaccess_http_tool_server.py"),
    "stdio": CommandInfo("stdio", "Run the stdio tool bridge.", "integration", legacy_equivalent="topoaccess_agent.py stdio"),
    "install-harness": CommandInfo("install-harness", "Generate dry-run harness install snippets.", "integration", legacy_equivalent="topoaccess_agent_install.py"),
    "conformance": CommandInfo("conformance", "Run integration artifact conformance checks.", "validation", legacy_equivalent="topoaccess_conformance_check.py"),
    "audit": CommandInfo("audit", "Run artifact audit checks.", "validation", legacy_equivalent="topoaccess_artifact_audit.py"),
    "secret-scan": CommandInfo("secret-scan", "Run secret scan checks.", "validation", legacy_equivalent="topoaccess_secret_scan.py"),
    "self-check": CommandInfo("self-check", "Run package self-check through topoaccessctl.", "validation", legacy_equivalent="topoaccessctl.py self-check"),
    "verify-provenance": CommandInfo("verify-provenance", "Create and verify a span-hash provenance entry for a file span.", "validation"),
}


def command_names() -> list[str]:
    return sorted(COMMANDS)


def command_table() -> list[dict]:
    return [
        {
            "name": info.name,
            "summary": info.summary,
            "category": info.category,
            "model_free_default": info.model_free_default,
            "legacy_equivalent": info.legacy_equivalent,
        }
        for info in sorted(COMMANDS.values(), key=lambda item: item.name)
    ]


Handler = Callable[[object], int]
