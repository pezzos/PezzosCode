# Human Orchestration Workflow (PO Loop)

> **Canonical PO loop for running PezzosCode with Codex as Developer**
>
> This workflow is deterministic and update-in-place only. It does not create competing docs.

---

## New Project Bootstrap

1. **Create/Update Context (00-context)**
   - Fill `docs/00-context/*.md` as the source of truth.
2. **Update PRD (context-to-product)**
   - Run the skill `context-to-product` to update `docs/01-product/prd.md` in place.
3. **Update Features (prd-to-features)**
   - Run the skill `prd-to-features` to update `docs/02-features/` in place.
   - No duplicate feature folders.
4. **Generate Tickets (feature-tasks-to-tickets)**
   - Run the skill `feature-tasks-to-tickets` to create one ticket per task in the current feature’s `dev-tasks.md`.
5. **Execute Ticket**
   - Follow `docs/04-process/ticket-execution-protocol.md` (TDD + gates + docs + commit).
   - If tester/reviewer raises issues, implementer must iterate and log in the ticket.
6. **Repeat**
   - Go back to step 4 for the next feature.

## Add Features / Existing Project

1. **Context delta only**
   - Update `docs/00-context/*.md` only if assumptions, constraints, users, or system state changed.
2. **Update PRD (context-to-product)**
   - Run the skill `context-to-product` to update `docs/01-product/prd.md` in place.
3. **Incremental Features (prd-to-features)**
   - Run the skill `prd-to-features` in incremental mode (default for existing projects) to add only missing features.
   - The skill uses `docs/03-logs/implementation-log.md` and `docs/03-logs/decision-log.md` to avoid re-adding completed or rejected items.
4. **Generate Tickets**
   - Run the skill `feature-tasks-to-tickets` to create tickets for the current feature’s tasks.
5. **Execute Ticket**
   - Follow the ticket execution protocol in `docs/04-process/ticket-execution-protocol.md`.
   - If tester/reviewer raises issues, implementer must iterate and log in the ticket.
6. **Repeat**
   - Continue from step 4 until P0/P1 items are complete.

## Chain of Truth

Context docs → PRD → Feature folders → Tickets → Worklogs → Implementation/Decision logs

## Update-in-Place Rules (by skill)

- **context-to-product:** update `docs/01-product/prd.md` only; do not create a new PRD file.
- **prd-to-features:** update existing `docs/02-features/` and add only missing folders; do not duplicate.
- **feature-tasks-to-tickets:** create `docs/02-features/<feature>/TASK-###.md` for each task in `dev-tasks.md`.

## Skill Invocation Guide

- **context-to-product**
  - Reads: `docs/00-context/*.md`
  - Writes: `docs/01-product/prd.md` (update in place)
  - Logs: update `docs/03-logs/decision-log.md` when scope/priorities change
- **prd-to-features**
  - Reads: `docs/01-product/prd.md`, `docs/02-features/AGENTS.md`
  - Writes: `docs/02-features/<feature>/` (update in place, add only missing)
  - Logs: update `docs/03-logs/implementation-log.md` when new features are added
- **feature-tasks-to-tickets**
  - Reads: `docs/02-features/`, `docs/04-process/ticket-template.md`, `docs/02-features/<feature>/dev-tasks.md`
  - Writes: `docs/02-features/<feature>/TASK-###.md` (current feature only)
  - Logs: worklog lives in `docs/03-logs/tickets/`

## Definition of Done for a Ticket

- Must meet `docs/04-process/definition-of-done.md`.
- Must pass `make ci`.
- Must have a worklog with Preflight, TDD plan, docs update checklist, gates, and commit message.

## When to Stop and Ask PO Approval

- If risk is HIGH per `docs/04-process/ticket-execution-protocol.md`, stop after Preflight and wait for PO approval.
