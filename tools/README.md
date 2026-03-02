# Tools

## Purpose

CLI helpers for bootstrapping repos and running the PezzosCode execution workflow.

## Structure / Map

- `tools/bootstrap-into` - Seed a target repo with templates, docs, and tools.
- `tools/pc-context-check` - Validate context clarity and expected-feature completeness before PRD generation.
- `tools/pc-write-prd` - Refresh PRD in place from context/process docs through Product Manager review.
- `tools/pc-prepare-features` - Generate global design/UX/security/dependency-order artifacts and run feature generation.
- `tools/pc-review-features` - Run Security Expert/Product Manager review over feature folders and inject canonical findings.
- `tools/pc-release-readiness` - Run PM release-readiness review and map actionable follow-ups to expected-features.
- `tools/pc-feature` - Run the work item protocol end-to-end.
- `tools/pc-commit` - Enforce commit scope/message policy.
- `tools/offload-proxy/pp` - Offload noisy command output to `.offload/`.

## Workflow

1. Use `bootstrap-into` to initialize a target repo; use `bootstrap-into --reapply` to force-overwrite syncable template-managed files during refresh.
2. Use `pc-context-check` to validate context clarity before PRD refresh (`make write-prd` also runs this preflight by default).
3. Use `pc-write-prd` to update `docs/01-product/prd.md` in place (`WRITE_PRD_ROLE_MODE=deterministic` for local fallback mode).
4. Use `pc-prepare-features` to refresh design/UX/security/order artifacts and generate feature docs (`--include-process-features` is opt-in).
5. Use `pc-review-features` to inject pre-execution security/product findings (`REVIEW_ROLE_MODE=deterministic` for local fallback mode; `INCLUDE_COMPLETED=1` for explicit completed-feature audits).
6. Use `pc-feature` to execute approved work items.
7. Use `pc-release-readiness` for PM go/no-go and expected-feature follow-up planning (`RELEASE_READINESS_ROLE_MODE=deterministic` for local fallback mode).
8. Use `pc-commit` to finalize scoped commits.
9. Use `tools/offload-proxy/pp` for large-output read commands.

## Generated Artifacts

- `pc-context-check` writes `docs/03-logs/context-clarity-report.json` (required context quality gate status before PRD updates).
- `pc-write-prd` writes `docs/03-logs/write-prd-report.json` (PRD update decision + changed sections).
- `pc-write-prd` writes `docs/03-logs/write-prd-state.json` (idempotency cache for unchanged source/PRD hashes).
- `pc-prepare-features` writes `docs/03-logs/prepare-features-state.json` (PM gate decisions + runtime state).
- `pc-prepare-features` writes `docs/03-logs/prepare-features-pm-todo.md` (owner-scoped PM feedback lifecycle).
- `pc-prepare-features` writes `docs/01-product/security.md` (project-scoped security baseline for implementation/review).
- `pc-prepare-features --snapshot-runs` writes per-run snapshots to `docs/03-logs/prepare-features-runs/<run-id>/`.
- `pc-review-features` writes `docs/03-logs/review-features-report.json` (per-feature canonical findings + totals; features with `Status: Done` are skipped by default).
- `pc-release-readiness` writes `docs/03-logs/release-readiness-report.json` (PM release-go/no-go + follow-up tasks).
- `pc-release-readiness` updates a machine-managed block in `docs/00-context/expected-features.md` for actionable follow-up features.

## Related Docs

- `docs/00-context/system-map.md`
- `docs/04-process/ticket-execution-protocol.md`
- `docs/03-logs/decision-log.md`
- `AGENTS.md`
