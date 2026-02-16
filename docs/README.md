# Docs

## Purpose

- Capture project context and execution memory for human + AI collaboration.
- Keep `docs/00-context/` and `docs/03-logs/` as the factual anchors for project statements.
- Provide feature-level specs/tasks/tests and the process rules used to execute them.

## Structure / Map

- `docs/00-context/` - Vision, users, assumptions, system map, boundaries, expected features.
- `docs/01-product/` - PRD plus global architecture (`design.md`) and UX (`ux-ui.md`) blueprints.
- `docs/02-features/` - Dependency-ordered feature plan plus per-feature spec, technical design, tasks, and test plan.
- `docs/03-logs/` - Implementation, decisions, bugs, validation outcomes, and insights.
- `docs/04-process/` - Execution protocol, orchestration workflow, and quality standards.

## Workflow

1. Start from `docs/00-context/` before changing product or feature docs.
2. Run `make prepare-features` before feature generation to refresh design/UX/order artifacts and write `docs/03-logs/prepare-features-state.json`.
3. Run `make review-features` after generation to inject security/product findings and write `docs/03-logs/review-features-report.json`.
4. Follow `Plan -> Patch -> Test -> Report` for each work item via `make feature`.
5. Record meaningful changes, decisions, bugs, validations, and insights in `docs/03-logs/`.

## Related Docs

- `docs/00-context/context-boundaries-operating-model.md`
- `docs/03-logs/AGENTS.md`
- `docs/04-process/human-orchestration-workflow.md`
- `docs/04-process/ticket-execution-protocol.md`
