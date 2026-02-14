---
name: feature-status-audit
description: Audit TASK-*.md tickets for one feature folder under docs/02-features and update frontmatter status fields using deterministic evidence rules. Use when the user asks to reconcile task progress, correct stale ticket statuses, or run a status audit before reporting.
---

# Feature Status Audit

## Overview

Audit all `TASK-###.md` files for one feature folder, summarize what looks done,
and update ticket frontmatter `status` fields automatically.

## Inputs

- `docs/02-features/` (feature folders)
- `docs/02-features/<feature>/TASK-*.md`
- `docs/02-features/<feature>/dev-tasks.md`
- `docs/03-logs/implementation-log.md` (optional context)

## Rules

- Operate on **one feature at a time** (lowest-numbered feature folder by default).
- Do not edit files outside the selected feature folder.
- Update frontmatter `status` using deterministic rules:
  - **Done** if all items in **Definition of Done (Ticket-Specific)** are checked.
  - **Done** if Evidence Hints are satisfied.
  - **Ongoing** if any checkbox in the ticket is checked OR Tests/Report fields are filled.
  - **To Do** otherwise.
- Preserve existing `status: "Done"` if already set.
- If status is set to **Done**, mark all DoD checkboxes as checked.
- Update `status_reason` with the evidence or rule used.

## Steps

1. Select the current feature folder (lowest-numbered with `TASK-*.md`).
2. For each task ticket:
   - Parse the ticket sections.
   - Evaluate status using the rules above.
   - Update frontmatter `status`.
3. Produce a summary:
   - Tasks marked Done / Ongoing / To Do
   - Checklist of tasks to confirm manually

## Deterministic Helper

Use the bundled wrapper to run the audit consistently and optionally emit JSON:

- `python3 .codex/skills/feature-status-audit/scripts/run_audit.py`
- `python3 .codex/skills/feature-status-audit/scripts/run_audit.py --feature 01 --json`

## Output Format

- Feature audited.
- Status summary per task.
- Checklist of tasks to confirm.

## Commands

- `tools/offload-proxy/pp rg -n "TASK-" docs/02-features/<feature>`
- `tools/offload-proxy/pp sed -n '1,200p' docs/02-features/<feature>/TASK-*.md`
- `tools/feature-status-audit [F=01]`

## DoD

- Task statuses updated in frontmatter for the selected feature.
- Summary + checklist provided.
