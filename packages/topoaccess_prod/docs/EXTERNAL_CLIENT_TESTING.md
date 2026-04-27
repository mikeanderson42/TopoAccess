# External Client Testing

TopoAccess supports Codex, Claude Code, OpenClaw, Hermes/generic shell agents, HTTP, and stdio integration modes.

V34 probes local client availability without requiring those clients to be installed. If a client is absent, the result is `not installed` and integration remains simulated through the generated schema and shell snippets.

Run:

```bash
python packages/topoaccess_prod/scripts/topoaccess_probe_external_clients.py
```

External absence is not a failure. Claiming a real-client pass when no client is installed is a failure.
