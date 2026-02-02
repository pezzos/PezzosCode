---
name: feature-tasks-to-tickets
description: Generate tickets for the current feature by reading its dev-tasks list and creating one ticket per TASK item. Use when a user wants all planned tasks for a feature turned into executable tickets.
---

# Feature Tasks to Tickets

## Overview

Identify the current feature (lowest-numbered feature folder without tickets),
read its `dev-tasks.md`, and create one ticket per task.

## Inputs

- `docs/02-features/` (feature folders)
- `docs/02-features/AGENTS.md`
- `docs/04-process/ticket-template.md`
- `docs/01-product/prd.md`
- `docs/02-features/<feature>/dev-tasks.md`

## Rules

- Features are ordered by numeric prefix in folder names (e.g., `01-...`, `02-...`).
- A feature is considered ticketed if it contains any `TASK-*.md`.
- Create tickets at `docs/02-features/<feature>/TASK-XXX.md`.
- Only create tickets for the current feature (lowest-numbered un-ticketed feature).
- Each ticket corresponds to one `TASK-###` entry in `dev-tasks.md`.
- Do not use or update `docs/03-logs/implementation-log.md` for this workflow.

## Steps

1. Read `docs/02-features/AGENTS.md` and follow the selection rule for product surfaces.
2. List `docs/02-features/` folders and sort by numeric prefix.
3. For each feature folder, check for any `TASK-*.md` file.
4. Select the first feature without tickets (current feature).
5. Read `docs/01-product/prd.md` and locate the matching feature to capture PRD order and priority.
6. Read `docs/02-features/<feature>/dev-tasks.md` and extract task ids + titles + acceptance criteria blocks (only indented task bullet lines under each TASK).
7. For each task, copy `docs/04-process/ticket-template.md` into the feature folder as `TASK-###.md`.
8. Fill in Title, Type, Context, Scope, Success Criteria, Plan, and the new sections with real content.
   - Include task acceptance criteria and estimate (if present) in Context and Success Criteria.
   - Replace the template header with a ticket-specific header (e.g., `# Ticket: <task title>`).
   - Include references to `feature-spec.md`, `tech-design.md`, and `test-plan.md` in Context.
   - Populate **References** with specific sections to check (Summary, Requirements, Architecture, Test Strategy).
   - Pre-fill Implementer/Tester/Reviewer sections with prompt bullets to guide feedback loops.
   - PRD Traceability (order + link)
   - Change Budget (max files/modules/lines)
   - Docs Updated (pre-populate expected docs)
9. Populate Definition of Done (ticket-specific) using:
   - dev-task acceptance criteria
   - relevant feature spec/test plan references
10. If required info is missing, leave clear TODOs and ask for clarification.

## Output Format

- Feature selected.
- Ticket files created with names and paths.
- PRD order captured for the feature.
- Missing inputs/questions.

## Commands

- `tools/offload-proxy/pp rg --files docs/02-features`
- `tools/offload-proxy/pp rg -n "TASK-" docs/02-features`
- `tools/offload-proxy/pp sed -n '1,200p' docs/04-process/ticket-template.md`
- `tools/offload-proxy/pp sed -n '1,200p' docs/01-product/prd.md`
- `tools/offload-proxy/pp sed -n '1,200p' docs/02-features/<feature>/dev-tasks.md`

## DoD

- Current feature identified by numeric order.
- One `TASK-###.md` created per task in `dev-tasks.md`.
- PRD traceability and change budget filled or called out as missing.
- Ticket fields filled or gaps explicitly called out.
