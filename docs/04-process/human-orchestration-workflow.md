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
   - Never delete existing feature folders.
   - Never re-add features whose `dev-tasks.md` has `Status: Done`.
   - Keep each feature small enough to execute as a single work item; split oversized features here, not during execution.
4. **Audit Feature Status (feature-status-audit)**
   - Run the skill `feature-status-audit` to update task statuses for the current feature.
5. **Execute Work Item**
   - Use `docs/02-features/<feature>/dev-tasks.md` as the source of truth.
   - Follow `docs/04-process/ticket-execution-protocol.md` (TDD + gates + docs + commit).
   - Enforce role-scoped logs (`planner-log.md`, `plan-reviewer-log.md`, `reporter-log.md`, `validation-log.md`).
   - Plan Reviewer validates the plan (no code edits) before patching.
   - Use `prompts/<role>.md` and task variants like `prompts/<role>-<task>.md` for role-specific instructions.
   - If a prompt file is missing, copy it from `tools/templates/prompts/` and rerun the step.
   - The PO loop now routes offload violations through docs/03-logs/decision-log.md so the enforced workflow is recorded before progressing.
   - The orchestrator logs each gate handoff in docs/03-logs/decision-log.md and docs/03-logs/validation-log.md before the PO loop continues.
   - If tester/reporter raises issues, planner and patcher must iterate and log in the execution log entry.
   - After the run completes or stops, propose improvements (patch not auto-applied) and record in `docs/possible-improvements.md`.
6. **Repeat**
   - Go back to step 4 for the next feature.

## Add Features / Existing Project

1. **Context delta only**
   - Update `docs/00-context/*.md` only if assumptions, constraints, users, or system state changed.
2. **Update PRD (context-to-product)**
   - Run the skill `context-to-product` to update `docs/01-product/prd.md` in place.
3. **Incremental Features (prd-to-features)**
   - Run the skill `prd-to-features` in incremental mode (default for existing projects) to add only missing features.
   - Do not delete existing features.
   - Skip any feature whose `dev-tasks.md` shows `Status: Done`.
   - Keep each feature small enough to execute as a single work item; split oversized features here, not during execution.
4. **Audit Feature Status**
   - Run the skill `feature-status-audit` to update task statuses for the current feature.
5. **Execute Work Item**
   - Use `docs/02-features/<feature>/dev-tasks.md` as the source of truth.
   - Follow the execution protocol in `docs/04-process/ticket-execution-protocol.md`.
   - Enforce role-scoped logs (`planner-log.md`, `plan-reviewer-log.md`, `reporter-log.md`, `validation-log.md`).
   - Plan Reviewer validates the plan (no code edits) before patching.
   - Use `prompts/<role>.md` and task variants like `prompts/<role>-<task>.md` for role-specific instructions.
   - If a prompt file is missing, copy it from `tools/templates/prompts/` and rerun the step.
   - The orchestrator logs each gate handoff in docs/03-logs/decision-log.md and docs/03-logs/validation-log.md before the PO loop continues.
   - If tester/reporter raises issues, planner and patcher must iterate and log in the execution log entry.
   - After the run completes or stops, propose improvements (patch not auto-applied) and record in `docs/possible-improvements.md`.
6. **Repeat**
   - Continue from step 4 until P0/P1 items are complete.

## Chain of Truth

Context docs → PRD → Feature folders → dev-tasks → execution logs → Implementation/Decision logs

## Update-in-Place Rules (by skill)

- **context-to-product:** update `docs/01-product/prd.md` only; do not create a new PRD file.
- **prd-to-features:** update existing `docs/02-features/` and add only missing folders; do not duplicate.
- **prd-to-features:** never delete feature folders; skip features marked `Status: Done` in `dev-tasks.md`.
- **feature-status-audit:** update task `status` fields for the current feature.

## Skill Invocation Guide

- **context-to-product**
  - Reads: `docs/00-context/*.md`
  - Writes: `docs/01-product/prd.md` (update in place)
  - Logs: update `docs/03-logs/decision-log.md` when scope/priorities change
- **prd-to-features**
  - Reads: `docs/01-product/prd.md`, `docs/02-features/AGENTS.md`
  - Writes: `docs/02-features/<feature>/` (update in place, add only missing)
  - Logs: update `docs/03-logs/implementation-log.md` when new features are added
- **feature-status-audit**
  - Reads: `docs/02-features/<feature>/dev-tasks.md`
  - Writes: updates task `status` in dev-tasks
  - Logs: update `docs/03-logs/implementation-log.md` when status backfill is run

## Definition of Done for a Work Item

- Must meet `docs/04-process/definition-of-done.md`.
- Must pass `make ci`.
- Must have a worklog or dev-tasks execution log with Preflight, TDD plan, docs update checklist, gates, and commit message.

## When to Stop and Ask PO Approval

- If risk is HIGH per `docs/04-process/ticket-execution-protocol.md` and approval is not granted, stop after Preflight and wait for PO approval. If approval is granted, continue.
