# Human Orchestration Workflow (PO Loop)

> **Canonical PO loop for running PezzosCode with Codex as Developer**
>
> This workflow is deterministic and update-in-place only. It does not create competing docs.

---

## New Project Bootstrap

1. **Create/Update Context (00-context)**
   - Fill `docs/00-context/*.md` as the source of truth.
2. **Context Clarity Gate (`make context-check`)**
   - Validate required context files, unresolved open-question checkboxes, and expected-feature completeness before PRD generation.
   - Writes `docs/03-logs/context-clarity-report.json` and blocks PRD refresh on failures.
3. **Write/Refresh PRD (`make write-prd`)**
   - Runs Product Manager prompt review over context + process docs and existing PRD.
   - Applies focused updates only (no unnecessary rewording of unchanged sections).
   - Writes `docs/03-logs/write-prd-report.json` and `docs/03-logs/write-prd-state.json`.
4. **Prepare Features (`make prepare-features`)**
   - Runs `Architect → UX → Security → dependency planner baseline → Orderer → Product Manager gate → feature generation`.
   - Generates/updates `docs/01-product/design.md`, `docs/01-product/ux-ui.md`, and `docs/01-product/security.md`.
   - Architect/UX/Security/Orderer role outputs are prompt-driven (`prompts/architect-prepare.md`, `prompts/ux-prepare.md`, `prompts/security-prepare.md`, `prompts/orderer-prepare.md`) and must return structured JSON artifacts.
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
5. **Review Features (`make review-features`)**
   - Runs `Security Expert → Product Manager` over generated feature folders.
   - Review role outputs are prompt-driven (`prompts/security-review-features.md`, `prompts/product-manager-review-features.md`) and run in dedicated profile sessions by default.
   - Skips features already marked `Status: Done` by default (use `INCLUDE_COMPLETED=1` only for explicit audit runs).
   - Writes actionable checklist tasks only in `dev-tasks.md` (`Action` + `Acceptance`); `feature-spec.md` receives constraint summaries only.
   - Persists aggregated findings to `docs/03-logs/review-features-report.json`.
6. **Audit Feature Status (feature-status-audit)**
   - Run the skill `feature-status-audit` to update task statuses for the current feature.
7. **Execute Work Item**
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
8. **Release Readiness Check (`make release-readiness`)**
   - Runs Product Manager role only (no additional specialist profiles in this command).
   - Writes `docs/03-logs/release-readiness-report.json`.
   - Updates a machine-managed release-readiness block in `docs/00-context/expected-features.md`.
   - If actionable follow-up features are added, loop back to step 2 (`make write-prd`) then step 3.
9. **Repeat**
   - Continue step 6 execution until target scope is complete, then run step 8.

## Add Features / Existing Project

1. **Context delta only**
   - Update `docs/00-context/*.md` only if assumptions, constraints, users, or system state changed.
2. **Context Clarity Gate (`make context-check`)**
   - Validate required context docs + expected-feature completeness before PRD refresh.
   - Writes `docs/03-logs/context-clarity-report.json` and blocks when unresolved context issues remain.
3. **Write/Refresh PRD (`make write-prd`)**
   - Runs Product Manager prompt review over context + process docs and existing PRD.
   - Applies focused updates only (no unnecessary rewording of unchanged sections).
   - Writes `docs/03-logs/write-prd-report.json` and `docs/03-logs/write-prd-state.json`.
4. **Prepare Features (`make prepare-features`)**
   - Refreshes `design.md`, `ux-ui.md`, `security.md`, dependency order plan, and incremental feature generation from the updated PRD.
   - PM approval is semantic, not only structural: block when artifacts are generic/tooling-centric instead of project-specific.
   - Refreshes `docs/03-logs/prepare-features-state.json` with PM gate/runtime status.
   - Refreshes `docs/03-logs/prepare-features-pm-todo.md` with PM loop feedback tasks and ownership.
   - Use `INCLUDE_PROCESS_FEATURES=1` only when process features should become executable feature folders.
   - Do not delete existing features.
   - Skip any feature whose `dev-tasks.md` shows `Status: Done`.
   - Keep each feature small enough to execute as a single work item; split oversized features here, not during execution.
5. **Review Features (`make review-features`)**
   - Runs Security Expert + Product Manager findings pass on generated features and writes actionable fixes to feature docs.
   - Defaults to open/in-progress features; pass `INCLUDE_COMPLETED=1` only for explicit audits.
   - Refreshes `docs/03-logs/review-features-report.json` with per-feature findings/totals.
6. **Audit Feature Status**
   - Run the skill `feature-status-audit` to update task statuses for the current feature.
7. **Execute Work Item**
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
8. **Release Readiness Check (`make release-readiness`)**
   - Runs Product Manager role only (no additional specialist profiles in this command).
   - Writes `docs/03-logs/release-readiness-report.json`.
   - Updates a machine-managed release-readiness block in `docs/00-context/expected-features.md`.
   - If actionable follow-up features are added, loop back to step 2 (`make write-prd`) then step 3.
9. **Repeat**
   - Continue from step 6 until P0/P1 items are complete, then run step 8.

## Chain of Truth

Context docs + expected features → context-clarity report → write-prd report/state + PRD → design/ux/security blueprints + dependency order plan → feature folders → review findings in feature docs + review report artifact → dev-tasks execution logs → release-readiness report + expected-features follow-ups → PRD refresh loop

## Update-in-Place Rules (by skill)

- **make context-check:** validate context completeness/clarity and write `docs/03-logs/context-clarity-report.json`.
- **make write-prd:** update `docs/01-product/prd.md` in place with focused changes only.
- **make write-prd:** write `docs/03-logs/write-prd-report.json` and `docs/03-logs/write-prd-state.json`.
- **make prepare-features:** update `docs/01-product/design.md`, `docs/01-product/ux-ui.md`, `docs/01-product/security.md`, and `docs/02-features/feature-order.{json,md}` before running generation.
- **make prepare-features:** persist PM loop/runtime state to `docs/03-logs/prepare-features-state.json`.
- **make prepare-features:** persist PM feedback TODO tracking to `docs/03-logs/prepare-features-pm-todo.md`.
- **make prepare-features:** `tools/prd-to-features` consumes `feature-order.json`, updates existing `docs/02-features/` in place, and adds only missing folders.
- **make prepare-features:** never delete feature folders; skip features marked `Status: Done` in `dev-tasks.md`.
- **make review-features:** update machine-managed findings sections in `feature-spec.md` and `dev-tasks.md` only.
- **make review-features:** write aggregated findings report to `docs/03-logs/review-features-report.json`.
- **Feature status source of truth:** `dev-tasks.md` (`Status: Not Started | In Progress | Done`); do not track feature status in `feature-spec.md`.
- **make release-readiness:** write `docs/03-logs/release-readiness-report.json`.
- **make release-readiness:** update only the machine-managed release-readiness block inside `docs/00-context/expected-features.md`.
- **feature-status-audit:** update task `status` fields for the current feature.

## Skill Invocation Guide

- **make context-check / tools/pc-context-check**
  - Reads: `docs/00-context/*.md`
  - Writes: `docs/03-logs/context-clarity-report.json`
  - Blocks when required context files are missing/empty, open-question checkboxes are unresolved, or expected features are incomplete.
- **make write-prd / tools/pc-write-prd**
  - Reads: `docs/00-context/*.md`, `docs/04-process/*.md`, `docs/00-context/expected-features.md`, existing `docs/01-product/prd.md`
  - Reads prompts: `prompts/product-manager-write-prd.md`
  - Writes: `docs/01-product/prd.md`, `docs/03-logs/write-prd-report.json`, `docs/03-logs/write-prd-state.json`
  - Logs: update `docs/03-logs/decision-log.md` when priorities/scope materially change
- **make prepare-features / tools/pc-prepare-features**
  - Reads: `docs/01-product/prd.md`, `docs/00-context/context-boundaries-operating-model.md`, `docs/02-features/AGENTS.md`
  - Reads prompts: `prompts/architect-prepare.md`, `prompts/ux-prepare.md`, `prompts/security-prepare.md`, `prompts/orderer-prepare.md`, `prompts/product-manager-prepare-gate.md`
  - Writes: `docs/01-product/design.md`, `docs/01-product/ux-ui.md`, `docs/01-product/security.md`, `docs/02-features/feature-order.{json,md}`, `docs/03-logs/prepare-features-state.json`, `docs/03-logs/prepare-features-pm-todo.md`, and incremental feature folder updates via `tools/prd-to-features`
  - Logs: update `docs/03-logs/implementation-log.md` when preparation updates artifacts/features
- **make review-features / tools/pc-review-features**
  - Reads: generated `docs/02-features/<feature>/feature-spec.md` + `dev-tasks.md`, plus `docs/01-product/ux-ui.md`
  - Reads prompts: `prompts/security-review-features.md`, `prompts/product-manager-review-features.md`
  - Writes: actionable review tasks in `dev-tasks.md`, constraint summaries in `feature-spec.md`, plus `docs/03-logs/review-features-report.json`
  - Logs: update `docs/03-logs/validation-log.md` when review pass completes
- **make release-readiness / tools/pc-release-readiness**
  - Reads: `docs/01-product/{prd.md,design.md,ux-ui.md,security.md}`, `docs/02-features/*/{feature-spec.md,dev-tasks.md}`, `docs/00-context/expected-features.md`
  - Reads prompts: `prompts/product-manager-release-readiness.md`
  - Writes: `docs/03-logs/release-readiness-report.json`, machine-managed release-readiness block in `docs/00-context/expected-features.md`
  - Logs: update `docs/03-logs/validation-log.md` when release-readiness pass completes
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
