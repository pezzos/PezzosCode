---
name: next-feature-ticket
description: Find the next feature without a ticket by scanning docs/02-features in numeric order and create a ticket file using docs/04-process/ticket-template.md. Use when a user wants the next un-ticketed feature queued with a TASK ticket.
---

# Next Feature Ticket

## Overview
Identify the next feature folder without a ticket and create a ticket file based on the standard template.

## Inputs
- `docs/02-features/` (feature folders)
- `docs/02-features/AGENTS.md`
- `docs/04-process/ticket-template.md`

## Rules
- Features are ordered by numeric prefix in folder names (e.g., `01-...`, `02-...`).
- A feature is considered ticketed if it contains `ticket-TASK-XXX.md`.
- Create tickets at `docs/02-features/<feature>/ticket-TASK-XXX.md`.
- Do not use or update `docs/03-logs/implementation-log.md` for this workflow.

## Steps
1) Read `docs/02-features/AGENTS.md` for current conventions.
2) List `docs/02-features/` folders and sort by numeric prefix.
3) For each feature folder, check for any `ticket-TASK-*.md` file.
4) Select the first feature without a ticket.
5) Copy `docs/04-process/ticket-template.md` into the feature folder as `ticket-TASK-XXX.md`.
6) Fill in Title, Type, Context, Scope, Success Criteria, and Plan using feature docs.
7) If required info is missing, leave clear TODOs and ask for clarification.

## Output Format
- Feature selected.
- Ticket file created with name and path.
- Missing inputs/questions.

## Commands
- `rg --files docs/02-features`
- `rg -n "ticket-TASK-" docs/02-features`
- `cat docs/04-process/ticket-template.md`

## DoD
- Next un-ticketed feature identified by numeric order.
- `ticket-TASK-XXX.md` created in the feature folder.
- Ticket fields filled or gaps explicitly called out.
