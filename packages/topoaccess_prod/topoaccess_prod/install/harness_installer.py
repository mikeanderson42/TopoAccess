from __future__ import annotations

import json
from pathlib import Path

from .shell_snippets import snippet
from ..integrations.tool_schema import all_schemas


def install_target(target: str, profile: str = "default", dry_run: bool = True, release_dir: str = "release/topoaccess_prod_v33") -> dict:
    safe = target.replace("-", "_")
    out_dir = Path(release_dir) / "installers"
    out_dir.mkdir(parents=True, exist_ok=True)
    md = out_dir / ("hermes_generic.md" if target in {"hermes", "generic"} else f"{safe}.md")
    payload = {
        "target": target,
        "profile": profile,
        "dry_run": dry_run,
        "snippet": snippet(target, profile),
        "tool_schema": str(out_dir / "tool_schema.json"),
        "result_status": "pass",
    }
    md.write_text(
        f"""# {target} TopoAccess install

Dry-run only by default. No external harness config is modified unless an explicit future `--apply` mode is used.

## Exact command

```bash
python packages/topoaccess_prod/scripts/topoaccess_agent_install.py --target {target} --profile {profile} --dry-run
```

## Shell snippet

```bash
{payload['snippet']}
```

## Config snippet

```json
{{"tool_server": "topoaccess", "profile": "{profile}", "schema": "tool_schema.json", "read_only_default": true}}
```

## Safety note

Exact lookup remains tool-only. Preferred model fallback is category-gated. Nonpreferred model use fails release gates.

## Test

```bash
python packages/topoaccess_prod/scripts/topoaccess_adapter_smoke.py --profile {profile} --targets {target} --out runs/topoaccess_prod_v33/installer_smoke.jsonl --report REPORT_topoaccess_prod_v33_docs.md
```

## Remove

Delete the shell alias/snippet or remove the generated tool entry from your harness config. This dry-run installer does not write external config files.
""",
        encoding="utf-8",
    )
    (out_dir / "tool_schema.json").write_text(json.dumps(all_schemas(), indent=2, sort_keys=True), encoding="utf-8")
    return payload


def write_installers(targets: list[str], profile: str, dry_run: bool, out: str) -> list[dict]:
    release_dir = "release/topoaccess_prod_v33" if "topoaccess_prod_v33" in out else "release/topoaccess_prod_v32"
    rows = [install_target(target, profile, dry_run, release_dir) for target in targets]
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with Path(out).open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")
    return rows
