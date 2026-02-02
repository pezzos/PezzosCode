---
name: feature-status-audit
description: Audit task tickets for a single feature and update ticket frontmatter status fields based on checklist completion and evidence in the ticket. Use when you want to reconcile task status with actual work in an existing repo.
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
