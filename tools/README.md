# Tools

## Purpose

CLI helpers for bootstrapping repos and running the PezzosCode execution workflow.

## Structure / Map

- `tools/bootstrap-into` - Seed a target repo with templates, docs, tools, and skills.
- `tools/pc-prepare-features` - Generate global design/UX/dependency-order artifacts and run feature generation.
- `tools/pc-review-features` - Run Security Expert/Product Manager review over generated feature folders and inject findings.
- `tools/pc-feature` - Run the work item protocol end-to-end.
- `tools/pc-commit` - Enforce commit scope/message policy.
- `tools/offload-proxy/pp` - Offload noisy command output to `.offload/`.

## Workflow

1. Use `bootstrap-into` to initialize a target repo; use `bootstrap-into --reapply` to force-overwrite syncable template-managed files during refresh.
2. Use `pc-prepare-features` to refresh design/UX/order artifacts and generate feature docs (`--include-process-features` is opt-in).
3. Use `pc-review-features` to inject pre-execution security/product findings (`REVIEW_ROLE_MODE=deterministic` for local fallback mode).
4. Use `pc-feature` to execute approved work items.
5. Use `pc-commit` to finalize scoped commits.
6. Use `tools/offload-proxy/pp` for large-output read commands.

## Generated Artifacts

- `pc-prepare-features` writes `docs/03-logs/prepare-features-state.json` (PM gate decisions + runtime state).
- `pc-prepare-features` writes `docs/03-logs/prepare-features-pm-todo.md` (owner-scoped PM feedback lifecycle).
- `pc-prepare-features --snapshot-runs` writes per-run snapshots to `docs/03-logs/prepare-features-runs/<run-id>/`.
- `pc-review-features` writes `docs/03-logs/review-features-report.json` (per-feature findings + totals, including patcher vs human validation routing).

## Related Docs

- `docs/00-context/system-map.md`
- `docs/04-process/ticket-execution-protocol.md`
- `docs/03-logs/decision-log.md`
- `AGENTS.md`
