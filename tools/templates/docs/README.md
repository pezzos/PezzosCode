# Docs

## Purpose

- Capture project context and execution memory for human + AI collaboration.
- Keep `docs/00-context/` and `docs/03-logs/` as the factual anchors for project statements.
- Provide feature-level specs/tasks/tests and the process rules used to execute them.

## Structure / Map

- `docs/00-context/` - Vision, users, assumptions, system map, boundaries, expected features.
- `docs/01-product/` - PRD plus global architecture (`design.md`), UX (`ux-ui.md`), and security (`security.md`) blueprints.
- `docs/02-features/` - Dependency-ordered feature plan plus per-feature spec, technical design, tasks, and test plan.
- `docs/03-logs/` - Implementation, decisions, bugs, validation outcomes, and insights.
- `docs/04-process/` - Execution protocol, orchestration workflow, and quality standards.

## Workflow

1. Start from `docs/00-context/` before changing product or feature docs.
2. Run `make write-prd` to update `docs/01-product/prd.md` in place from context/process inputs and write `docs/03-logs/write-prd-report.json` plus `docs/03-logs/write-prd-state.json`.
3. Run `make prepare-features` before feature generation to refresh design/UX/security/order artifacts and write `docs/03-logs/prepare-features-state.json` plus `docs/03-logs/prepare-features-pm-todo.md` (use `INCLUDE_PROCESS_FEATURES=1` only when process features should be generated; use `SNAPSHOT_RUNS=1` for per-run snapshots).
4. Run `make review-features` after generation to inject Security Expert/Product Manager findings for open/in-progress features (use `INCLUDE_COMPLETED=1` only for explicit audits); actionable tasks are written in `dev-tasks.md`, summary constraints in `feature-spec.md`, and the run report in `docs/03-logs/review-features-report.json`.
5. Follow `Plan -> Patch -> Test -> Report` for each work item via `make feature`.
6. Run `make release-readiness` when you want a PM go/no-go and follow-up plan; it writes `docs/03-logs/release-readiness-report.json` and updates the machine-managed release-readiness block in `docs/00-context/expected-features.md`.
7. Record meaningful changes, decisions, bugs, validations, and insights in `docs/03-logs/`.

## Related Docs

- `docs/00-context/context-boundaries-operating-model.md`
- `docs/03-logs/AGENTS.md`
- `docs/04-process/human-orchestration-workflow.md`
- `docs/04-process/ticket-execution-protocol.md`
