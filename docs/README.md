# Documentation System

> The source of truth for context, requirements, features, logs, and workflow.

## Purpose

This system keeps product context and execution history in one place so humans
and LLMs can collaborate without guessing. It prioritizes clear scope, minimal
duplication, and chronological logs of what happened.

## Structure / Map

- `docs/00-context/` - Vision, system map, users, assumptions, and boundaries.
- `docs/01-product/` - PRD and success criteria.
- `docs/02-features/` - Per-feature specs, designs, tasks, and tests.
- `docs/03-logs/` - Implementation, decisions, bugs, validation, insights.
- `docs/04-process/` - Execution protocols and quality standards.

## Workflow

1. Start with `docs/00-context/` (especially boundaries and operating model).
2. Define requirements in `docs/01-product/prd.md`.
3. Create features from `docs/02-features/feature-template/`.
4. Follow `docs/04-process/` for ticket execution and definition of done.
5. Update `docs/03-logs/` as work happens.

## Related Docs

- `AGENTS.md`
- `docs/00-context/context-boundaries-operating-model.md`
- `docs/01-product/prd.md`
- `docs/02-features/feature-template/`
- `docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/definition-of-done.md`
