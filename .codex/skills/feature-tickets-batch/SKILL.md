---
name: feature-tickets-batch
description: Generate tickets for all un-ticketed feature folders by scanning docs/02-features in numeric order and creating ticket files using docs/04-process/ticket-template.md. Use when a user wants a one-time batch of tickets for the current feature scope.
---

# Feature Tickets (Batch)

## Overview

Identify all feature folders without tickets and create ticket files based on the standard template.

## Inputs

- `docs/02-features/` (feature folders)
- `docs/02-features/AGENTS.md`
- `docs/04-process/ticket-template.md`
- `docs/01-product/prd.md`

## Rules

- Features are ordered by numeric prefix in folder names (e.g., `01-...`, `02-...`).
- A feature is considered ticketed if it contains any `TASK-*.md`.
- Create tickets at `docs/02-features/<feature>/TASK-XXX.md`.
- Only create tickets for P0/P1 features unless explicitly requested to include P2.
- Do not use or update `docs/03-logs/implementation-log.md` for this workflow.

## Steps

1. Read `docs/02-features/AGENTS.md` and follow the selection rule for product surfaces.
2. List `docs/02-features/` folders and sort by numeric prefix.
3. For each feature folder, check for any `TASK-*.md` file.
4. Select all features without tickets (batch).
5. Read `docs/01-product/prd.md` and locate matching features in the prioritized list to capture PRD order and priority.
6. For each selected P0/P1 feature, copy `docs/04-process/ticket-template.md` into the feature folder as `TASK-XXX.md`.
7. Fill in Title, Type, Context, Scope, Success Criteria, Plan, and the new sections:
   - PRD Traceability (order + link)
   - Change Budget (max files/modules/lines)
   - Docs Updated (pre-populate expected docs)
8. If required info is missing, leave clear TODOs and ask for clarification.

## Output Format

- Features selected (batch).
- Ticket files created with names and paths.
- PRD order captured for each feature.
- Missing inputs/questions.

## Commands

- `tools/offload-proxy/pp rg --files docs/02-features`
- `tools/offload-proxy/pp rg -n "TASK-" docs/02-features`
- `tools/offload-proxy/pp sed -n '1,200p' docs/04-process/ticket-template.md`
- `tools/offload-proxy/pp sed -n '1,200p' docs/01-product/prd.md`

## DoD

- All un-ticketed features identified by numeric order.
- `TASK-XXX.md` created in each un-ticketed P0/P1 feature folder.
- PRD traceability and change budget filled or called out as missing.
- Ticket fields filled or gaps explicitly called out.
