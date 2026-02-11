# Tools

## Purpose

CLI helpers for bootstrapping repos and running the PezzosCode execution workflow.

## Structure / Map

- `tools/bootstrap-into` - Seed a target repo with templates, docs, tools, and skills.
- `tools/pc-feature` - Run the work item protocol end-to-end.
- `tools/pc-commit` - Enforce commit scope/message policy.
- `tools/offload-proxy/pp` - Offload noisy command output to `.offload/`.

## Workflow

1. Use `bootstrap-into` to initialize or refresh a target repo.
2. Use `pc-feature` to execute approved work items.
3. Use `pc-commit` to finalize scoped commits.
4. Use `tools/offload-proxy/pp` for large-output read commands.

## Related Docs

- `docs/00-context/system-map.md`
- `docs/04-process/ticket-execution-protocol.md`
- `docs/03-logs/decision-log.md`
- `AGENTS.md`
