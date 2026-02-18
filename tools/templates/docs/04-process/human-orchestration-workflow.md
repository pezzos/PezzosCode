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
3. **Prepare Features (`make prepare-features`)**
   - Runs `Architect → UX → dependency planner baseline → Orderer → Product Manager gate → feature generation`.
   - Generates/updates `docs/01-product/design.md` and `docs/01-product/ux-ui.md`.
   - Architect/UX/Orderer role outputs are prompt-driven (`prompts/architect-prepare.md`, `prompts/ux-prepare.md`, `prompts/orderer-prepare.md`) and must return structured JSON artifacts.
   - Product Manager gate (`prompts/product-manager-prepare-gate.md`) approves only when semantic quality criteria pass: feature-specific architecture and project-specific user journeys.
   - Generates `docs/02-features/feature-order.json` + `docs/02-features/feature-order.md`.
   - Persists loop/runtime state to `docs/03-logs/prepare-features-state.json`.
   - Persists PM feedback TODO tracker to `docs/03-logs/prepare-features-pm-todo.md` (project-scoped, issue-complete open/carry/done tasks with owner assignment).
   - Resolves dependency ambiguity/cycles with numbered CLI choices (2-4 options + risk notes).
   - Process feature entries in `## Process Features` are excluded by default; pass `INCLUDE_PROCESS_FEATURES=1` to include them in generation.
   - `tools/prd-to-features` consumes the ordered plan and updates `docs/02-features/` in dependency order.
   - No duplicate feature folders.
   - Never delete existing feature folders.
   - Never re-add features whose `dev-tasks.md` has `Status: Done`.
   - Keep each feature small enough to execute as a single work item; split oversized features here, not during execution.
4. **Review Features (`make review-features`)**
   - Runs `Security Reviewer → Product Manager` over generated feature folders.
   - Injects actionable findings into `feature-spec.md` and `dev-tasks.md` before execution starts.
   - Persists aggregated findings to `docs/03-logs/review-features-report.json`.
5. **Audit Feature Status (feature-status-audit)**
   - Run the skill `feature-status-audit` to update task statuses for the current feature.
6. **Execute Work Item**
   - Use `docs/02-features/<feature>/dev-tasks.md` as the source of truth.
   - Follow `docs/04-process/ticket-execution-protocol.md` (TDD + gates + docs + commit).
   - Enforce role-scoped logs (`planner-log.md`, `plan-reviewer-log.md`, `reporter-log.md`, `validation-log.md`).
   - Plan Reviewer validates the plan (no code edits) before patching.
   - Use `prompts/<role>.md` and task variants like `prompts/<role>-<task>.md` (ex: `plan-reviewer-gate`, `patcher-apply`, `planner-update_from_feedback`) for role-specific instructions.
   - If a prompt file is missing, restore it under `prompts/` and rerun the step (prompt loading is file-based only). In template-enabled repos, copy from `tools/templates/prompts/`; in living-only bootstrap repos, re-run bootstrap from the source tooling repo.
   - The PO loop now routes offload violations through docs/03-logs/decision-log.md so the enforced workflow is recorded before progressing.
   - The orchestrator logs each gate handoff in docs/03-logs/decision-log.md and docs/03-logs/validation-log.md before the PO loop continues.
   - Preflight `files_to_change` is patcher-scope only; role/global-log targets are retained as reporter/orchestrator handoff notes instead of patcher plan edits.
   - If tester/reporter raises issues, planner and patcher must iterate and log in the execution log entry.
   - On resume after tester `FAIL`, planner revises the existing `Plan` from feedback; do not regenerate a fresh plan when the plan section is already complete.
   - Plan policy checks treat backticked `tools/pc-feature` references as file-path prose unless explicit command intent (run/execute/args) is present.
   - Runtime control flow is strict: `Orchestrator → Planner → Plan Reviewer → Patcher → Tester → Reporter → Orchestrator`.
   - Restart rules: reviewer `BLOCK` returns to Planner; tester `FAIL` returns to Planner; reporter `FAIL` returns to Planner; only reporter `PASS` advances to final orchestrator gates/commit.
   - If any role has no work on a restart pass, record a no-op note in the iteration log and continue to the next role.
   - During the run, roles can propose improvements in feedback fields; after the run completes or stops, the orchestrator writes a clarified, deduplicated collection to `docs/possible-improvements.md`.
7. **Repeat**
   - Go back to step 5 for the next feature.

## Add Features / Existing Project

1. **Context delta only**
   - Update `docs/00-context/*.md` only if assumptions, constraints, users, or system state changed.
2. **Update PRD (context-to-product)**
   - Run the skill `context-to-product` to update `docs/01-product/prd.md` in place.
3. **Prepare Features (`make prepare-features`)**
   - Refreshes `design.md`, `ux-ui.md`, dependency order plan, and incremental feature generation from the updated PRD.
   - PM approval is semantic, not only structural: block when artifacts are generic/tooling-centric instead of project-specific.
   - Refreshes `docs/03-logs/prepare-features-state.json` with PM gate/runtime status.
   - Refreshes `docs/03-logs/prepare-features-pm-todo.md` with PM loop feedback tasks and ownership.
   - Use `INCLUDE_PROCESS_FEATURES=1` only when process features should become executable feature folders.
   - Do not delete existing features.
   - Skip any feature whose `dev-tasks.md` shows `Status: Done`.
   - Keep each feature small enough to execute as a single work item; split oversized features here, not during execution.
4. **Review Features (`make review-features`)**
   - Runs security/product findings pass on generated features and writes actionable fixes to feature docs.
   - Refreshes `docs/03-logs/review-features-report.json` with per-feature findings/totals.
5. **Audit Feature Status**
   - Run the skill `feature-status-audit` to update task statuses for the current feature.
6. **Execute Work Item**
   - Use `docs/02-features/<feature>/dev-tasks.md` as the source of truth.
   - Follow the execution protocol in `docs/04-process/ticket-execution-protocol.md`.
   - Enforce role-scoped logs (`planner-log.md`, `plan-reviewer-log.md`, `reporter-log.md`, `validation-log.md`).
   - Plan Reviewer validates the plan (no code edits) before patching.
   - Use `prompts/<role>.md` and task variants like `prompts/<role>-<task>.md` (ex: `plan-reviewer-gate`, `patcher-apply`, `planner-update_from_feedback`) for role-specific instructions.
   - If a prompt file is missing, restore it under `prompts/` and rerun the step (prompt loading is file-based only). In template-enabled repos, copy from `tools/templates/prompts/`; in living-only bootstrap repos, re-run bootstrap from the source tooling repo.
   - The orchestrator logs each gate handoff in docs/03-logs/decision-log.md and docs/03-logs/validation-log.md before the PO loop continues.
   - Preflight `files_to_change` is patcher-scope only; role/global-log targets are retained as reporter/orchestrator handoff notes instead of patcher plan edits.
   - If tester/reporter raises issues, planner and patcher must iterate and log in the execution log entry.
   - On resume after tester `FAIL`, planner revises the existing `Plan` from feedback; do not regenerate a fresh plan when the plan section is already complete.
   - Plan policy checks treat backticked `tools/pc-feature` references as file-path prose unless explicit command intent (run/execute/args) is present.
   - Runtime control flow is strict: `Orchestrator → Planner → Plan Reviewer → Patcher → Tester → Reporter → Orchestrator`.
   - Restart rules: reviewer `BLOCK` returns to Planner; tester `FAIL` returns to Planner; reporter `FAIL` returns to Planner; only reporter `PASS` advances to final orchestrator gates/commit.
   - If any role has no work on a restart pass, record a no-op note in the iteration log and continue to the next role.
   - During the run, roles can propose improvements in feedback fields; after the run completes or stops, the orchestrator writes a clarified, deduplicated collection to `docs/possible-improvements.md`.
7. **Repeat**
   - Continue from step 5 until P0/P1 items are complete.

## Chain of Truth

Context docs → PRD → design/ux blueprints → dependency order plan + prepare state artifact → feature folders → review findings in feature docs + review report artifact → dev-tasks execution logs → Implementation/Decision logs

## Update-in-Place Rules (by skill)

- **context-to-product:** update `docs/01-product/prd.md` only; do not create a new PRD file.
- **make prepare-features:** update `docs/01-product/design.md`, `docs/01-product/ux-ui.md`, and `docs/02-features/feature-order.{json,md}` before running generation.
- **make prepare-features:** persist PM loop/runtime state to `docs/03-logs/prepare-features-state.json`.
- **make prepare-features:** persist PM feedback TODO tracking to `docs/03-logs/prepare-features-pm-todo.md`.
- **make prepare-features:** `tools/prd-to-features` consumes `feature-order.json`, updates existing `docs/02-features/` in place, and adds only missing folders.
- **make prepare-features:** never delete feature folders; skip features marked `Status: Done` in `dev-tasks.md`.
- **make review-features:** update machine-managed findings sections in `feature-spec.md` and `dev-tasks.md` only.
- **make review-features:** write aggregated findings report to `docs/03-logs/review-features-report.json`.
- **feature-status-audit:** update task `status` fields for the current feature.

## Skill Invocation Guide

- **context-to-product**
  - Reads: `docs/00-context/*.md`
  - Writes: `docs/01-product/prd.md` (update in place)
  - Logs: update `docs/03-logs/decision-log.md` when scope/priorities change
- **make prepare-features / tools/pc-prepare-features**
  - Reads: `docs/01-product/prd.md`, `docs/00-context/context-boundaries-operating-model.md`, `docs/02-features/AGENTS.md`
  - Reads prompts: `prompts/architect-prepare.md`, `prompts/ux-prepare.md`, `prompts/orderer-prepare.md`, `prompts/product-manager-prepare-gate.md`
  - Writes: `docs/01-product/design.md`, `docs/01-product/ux-ui.md`, `docs/02-features/feature-order.{json,md}`, `docs/03-logs/prepare-features-state.json`, `docs/03-logs/prepare-features-pm-todo.md`, and incremental feature folder updates via `tools/prd-to-features`
  - Logs: update `docs/03-logs/implementation-log.md` when preparation updates artifacts/features
- **make review-features / tools/pc-review-features**
  - Reads: generated `docs/02-features/<feature>/feature-spec.md` + `dev-tasks.md`, plus `docs/01-product/ux-ui.md`
  - Writes: machine-managed review findings into `feature-spec.md` and `dev-tasks.md`, plus `docs/03-logs/review-features-report.json`
  - Logs: update `docs/03-logs/validation-log.md` when review pass completes
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
