# Implementation Log

> **What changed in code & why**
>
> A chronological record of all code changes, technical decisions made during implementation, and the reasoning behind them. This is the MEMORY that most teams miss.

---

## Purpose

This log captures:

- **What** code was changed
- **Why** the change was made
- **How** it was implemented
- **Trade-offs** considered
- **Lessons learned**

This helps with:

- Understanding the evolution of the codebase
- Debugging when things break
- Onboarding new team members
- Avoiding repeating mistakes

---

## Log Entries

### 2026-02-19 - Batch A review-features hardening (scope, canonical tasks, simplified task contract)

**Feature/Bug:** Review findings were too broad/noisy, duplicated actionable details across docs, and continued to generate tasks for already completed features.

**Changed Files:**

- `tools/pc-review-features`
- `tests/test_pc_review_features.py`
- `prompts/security-review-features.md`
- `prompts/product-manager-review-features.md`
- `tools/templates/prompts/security-review-features.md`
- `tools/templates/prompts/product-manager-review-features.md`
- `Makefile`
- `tools/templates/root/Makefile`
- `docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `docs/README.md`
- `tools/templates/docs/README.md`
- `tools/README.md`

**What Changed:**

- Added completed-feature scope control in review runtime:
  - `pc-review-features` now skips features marked `Done/Complete/Completed/Shipped` by default.
  - New opt-in flag `--include-completed` to review completed features explicitly.
  - Added Makefile passthrough `INCLUDE_COMPLETED=1`.
- Switched role prompt contract from free-form findings to canonical key selection:
  - review roles now return `selected_keys` + per-key verbatim evidence snippets.
  - runtime validates evidence exists in feature docs before accepting role-selected findings.
- Made finding titles/actions deterministic by mapping canonical keys to fixed templates in `pc-review-features`.
- Simplified review rendering contract:
  - `dev-tasks.md` now contains actionable tasks with only `Action` + `Acceptance`.
  - `feature-spec.md` now contains constraint summaries only (`spec_guidance`) to avoid checklist duplication.
- Reduced report metadata shape:
  - removed reviewer/owner/phase fields from finding payloads.
  - retained deterministic ids + `severity` + `blocking` and moved report schema to `version: 3`.

**Why:**

- Prior output created high finding volume on completed work and mixed global hardening guidance with feature-local execution tasks.
- Actionable checklist duplication between feature docs reduced clarity of source of truth.
- Deterministic canonical findings reduce drift and duplicate/noisy phrasing across reruns.

### 2026-02-18 - Role-driven `review-features` with Security Expert + PM routing

**Feature/Bug:** Upgrade `make review-features` to use dedicated Security Expert and Product Manager sessions (matching prepare-features role model) and route findings to patcher vs human validation.

**Changed Files:**

- `tools/pc-review-features`
- `tests/test_pc_review_features.py`
- `prompts/security-review-features.md`
- `prompts/product-manager-review-features.md`
- `tools/templates/prompts/security-review-features.md`
- `tools/templates/prompts/product-manager-review-features.md`
- `.codex.toml`
- `tools/templates/root/.codex.toml`
- `Makefile`
- `tools/templates/root/Makefile`
- `docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `docs/README.md`
- `tools/templates/docs/README.md`
- `tools/README.md`

**What Changed:**

- Refactored `pc-review-features` to support:
  - role mode selection (`codex` default, `deterministic` fallback),
  - dedicated role sessions in sequence: `Security Expert -> Product Manager`,
  - profile defaults: `SecurityExpert` (`REVIEW_SECURITY_PROFILE`) and `ProductManager` (`REVIEW_PM_PROFILE`).
- Added prompt-driven review contracts for both review roles (live + template prompt files).
- Extended findings model to include routing metadata:
  - `owner` (`patcher` or `human`),
  - `phase` (`patch`, `automated-test`, `human-validation`),
  - `blocking` boolean.
- Updated machine-managed insertion blocks:
  - `feature-spec.md`: role-labeled findings table with routing metadata.
  - `dev-tasks.md`: explicit `Patcher Tasks` and `Human Validation Requests`.
- Upgraded `review-features-report.json` to `version: 2` with aggregate owner-route totals (`patcher_findings`, `human_findings`) and role mode.
- Added Makefile passthrough `REVIEW_ROLE_MODE=<codex|deterministic>` for both live and template make targets.
- Updated workflow/docs references to the new review prompts and role labels.
- Added regression tests for deterministic run output, idempotent marker behavior, and default profile routing.

**Why:**

- The previous review pass was deterministic-only and did not leverage dedicated role prompts/profiles like prepare-features.
- Patcher vs human validation ownership needed to be explicit in review outputs so downstream execution can route findings correctly.

### 2026-02-18 - PM TODO reconciliation now tracks all unresolved PM findings

**Feature/Bug:** PM TODO artifact only reflected coarse owner-level todo updates, not the full unresolved PM finding set.

**Changed Files:**

- `tools/pc-prepare-features`
- `tests/test_pc_prepare_features.py`
- `prompts/product-manager-prepare-gate.md`
- `tools/templates/prompts/product-manager-prepare-gate.md`
- `docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`

**What Changed:**

- Updated `apply_pm_todo_updates` reconciliation behavior:
  - always reconcile TODOs against the full `review_issues` set when PM gate is blocked,
  - keep every unresolved PM issue tracked as an open/carry TODO,
  - mark stale open/carry TODOs as `done` when their issue is resolved, even if the loop is still blocked on other issues,
  - reopen previously done TODOs when matching PM issues reappear.
- Added tests for:
  - closing resolved TODOs during blocked loops,
  - tracking full review-issue coverage even when PM role emits sparse owner-level `todo_updates`.
- Updated PM gate prompt contract and workflow docs to state issue-complete PM TODO tracking expectations (project-scoped with owner assignment).

**Why:**

- Deterministic idempotent prepare runs require PM TODO state to be complete and stable at project/version scope, not just owner-bucket summaries.
- Full issue tracking prevents silent gap loss between PM findings output and persisted TODO artifacts.

### 2026-02-18 - Prepare prompt minimal-diff contract + PM actionable routing hardening

**Feature/Bug:** Reduce unnecessary artifact rewrites in prepare retries and make PM BLOCK feedback deterministic and owner-actionable.

**Changed Files:**

- `prompts/architect-prepare.md`
- `prompts/ux-prepare.md`
- `prompts/product-manager-prepare-gate.md`
- `tools/templates/prompts/architect-prepare.md`
- `tools/templates/prompts/ux-prepare.md`
- `tools/templates/prompts/product-manager-prepare-gate.md`
- `tools/pc-prepare-features`
- `tests/test_pc_prepare_features.py`

**What Changed:**

- Updated Architect/UX prompt contracts to require retry-loop minimal diff behavior:
  - avoid style-only rewrites when no actionable owner-scoped PM work exists,
  - emit `changed_sections` and `change_rationale` metadata on updates.
- Updated PM gate prompt contract to require owner-actionable issues with:
  - target artifact,
  - target section/heading,
  - explicit acceptance condition,
    and owner-scoped `todo_updates` on BLOCK.
- Added runtime guardrails in `pc-prepare-features`:
  - role change-contract validation for Architect/UX retries (no-op when no actionable inputs; metadata required on changes),
  - PM issue actionability validation,
  - PM BLOCK todo update coverage checks,
  - criterion failure mapping to owner-specific actionable issues (`feature_specificity` -> architect, `journey_specificity` -> ux, `dependency_alignment` -> dependency-planner).
- Added regression tests covering:
  - Architect retry rewrite rejection without actionable inputs,
  - Architect change-metadata requirements when actionable tasks exist,
  - PM criterion-to-owner mapping,
  - PM BLOCK missing-todo validation,
  - PM issue ambiguity validation.

**Why:**

- Retry loops were producing noisy wording edits that increased review cost without resolving PM blockers.
- PM criterion-level feedback could remain ambiguous and slow deterministic convergence across owner roles.

### 2026-02-18 - Prepare retry-persistence, PM guardrails, and optional per-run snapshots

**Feature/Bug:** Make PM feedback evolution inspectable during retries and add deterministic snapshot history for prepare runs.

**Changed Files:**

- `tools/pc-prepare-features`
- `Makefile`
- `tools/templates/root/Makefile`
- `docs/README.md`
- `tools/README.md`
- `tools/templates/docs/README.md`
- `tests/test_pc_prepare_features.py`
- `tests/test_docs_logs.py`

**What Changed:**

- Added retry-time persistence in `pc-prepare-features` so blocked PM iterations write both:
  - `docs/03-logs/prepare-features-state.json`
  - `docs/03-logs/prepare-features-pm-todo.md`
    before entering the next loop iteration.
- Added legacy-state warning at run start when existing prepare state is `version < 2` or missing `pm_todos`.
- Added optional per-run snapshots:
  - new CLI flag `--snapshot-runs`
  - snapshots written to `docs/03-logs/prepare-features-runs/<run-id>/`
  - includes `index.json` plus paired state/PM-TODO snapshot files per persistence point.
- Wired `SNAPSHOT_RUNS=1` in live/template `Makefile` prepare target.
- Updated live/template docs to include PM TODO artifact and snapshot toggle guidance.
- Extended tests to cover:
  - retry path persisting artifacts before next iteration,
  - per-run snapshot artifact generation,
  - docs contract mentions for PM TODO artifact and snapshot option.

**Why:**

- PM issue counts can change across loops, but prior behavior only persisted artifacts after the loop exited, making mid-loop evolution difficult to inspect.
- Snapshotable run history provides deterministic diagnostics across concurrent/multi-repo prepare runs.

### 2026-02-18 - PM feedback TODO persistence + retry-context wiring in prepare-features

**Feature/Bug:** Make Product Manager feedback inspectable and owner-routable across prepare loops.

**Changed Files:**

- `tools/pc-prepare-features`
- `prompts/architect-prepare.md`
- `prompts/ux-prepare.md`
- `prompts/product-manager-prepare-gate.md`
- `tools/templates/prompts/architect-prepare.md`
- `tools/templates/prompts/ux-prepare.md`
- `tools/templates/prompts/product-manager-prepare-gate.md`
- `tests/test_pc_prepare_features.py`
- `docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`

**What Changed:**

- Added PM TODO persistence in prepare runtime:
  - new artifact `docs/03-logs/prepare-features-pm-todo.md`,
  - extended `prepare-features-state.json` with `pm_todos` payload (`version: 2`).
- Implemented PM TODO lifecycle helpers (owner/status normalization, update application, fallback auto-create/carry/done behavior).
- Added PM feedback snapshots to each PM gate history entry (`pm_feedback` with criteria/raw issues/review issues/todo updates + loop change summary).
- Added loop diff summary generation for design/UX artifacts and fed summaries into role prompts.
- Extended Architect/UX prompts to consume owner-scoped PM TODO inputs.
- Extended PM prompt contract to return structured `todo_updates`.
- Updated workflow docs to include PM TODO artifact in prepare outputs/contracts.
- Added/updated tests to cover:
  - PM TODO artifact creation in skip-generation flow,
  - prompt payload fields for TODO context,
  - PM TODO auto-create and auto-done fallback behavior.

**Why:**

- PM feedback existed mostly in transient terminal output and partial loop state, making investigation and accountability difficult.
- Explicit owner-scoped TODO tracking enables deterministic retries and clear closure across Architect/UX/PM loops.

### 2026-02-18 - Dedicated Codex profiles for prepare-features roles

**Feature/Bug:** Add role-specific Codex profile defaults for Architect, UX/UI, and Product Manager prepare steps.

**Changed Files:**

- `.codex.toml`
- `tools/templates/root/.codex.toml`
- `tools/pc-prepare-features`
- `tests/test_pc_prepare_features.py`

**What Changed:**

- Added profile definitions in live/template Codex configs:
  - `Architect`
  - `UXUI`
  - `ProductManager`
- Updated `pc-prepare-features` codex role defaults:
  - `PREPARE_ARCHITECT_PROFILE` default -> `Architect`
  - `PREPARE_UX_PROFILE` default -> `UXUI`
  - `PREPARE_PM_PROFILE` default -> `ProductManager`
- Added regression tests validating that Architect/UX/PM role execution uses the new default profile names when env overrides are not set.

**Why:**

- Prepare roles were previously multiplexed through Planner/PlanReviewer defaults, which obscured role intent and reduced configurability.
- Dedicated profile names align prepare execution with the repository’s explicit role model and enable future per-role tuning.

### 2026-02-18 - Prepare retry-loop context carry-forward for Architect/UX

**Feature/Bug:** Make PM-block retries revise prior Architect/UX artifacts with explicit PM feedback instead of behaving like blank-slate reruns.

**Changed Files:**

- `tools/pc-prepare-features`
- `prompts/architect-prepare.md`
- `prompts/ux-prepare.md`
- `tools/templates/prompts/architect-prepare.md`
- `tools/templates/prompts/ux-prepare.md`
- `tests/test_pc_prepare_features.py`

**What Changed:**

- Extended prompt rendering payload with retry context fields:
  - `prepare_iteration`
  - `previous_design_markdown`
  - `previous_ux_markdown`
  - `pm_feedback_json`
- Wired PM retry loop state in `run_prepare(...)` so `retry` persists prior design/UX outputs and last PM findings, then feeds them into the next Architect/UX/PM role run.
- Updated Architect/UX prompt instructions (live + template) to explicitly revise prior drafts and address relevant PM feedback on iterations `> 1`.
- Added tests that validate retry-context payload generation and prompt rendering with prior-draft/PM-feedback markers.

**Why:**

- PM feedback loops previously reran roles with only PRD/context/order data, which often felt like “start from scratch” and slowed convergence.
- Carry-forward context makes retries incremental and improves consistency between loop iterations.

### 2026-02-18 - Fix codex prepare prompt rendering for literal issue schema

**Feature/Bug:** Prevent `make prepare-features` from failing when prepare prompts include literal issue schema text.

**Changed Files:**

- `prompts/architect-prepare.md`
- `prompts/ux-prepare.md`
- `prompts/product-manager-prepare-gate.md`
- `tools/templates/prompts/architect-prepare.md`
- `tools/templates/prompts/ux-prepare.md`
- `tools/templates/prompts/product-manager-prepare-gate.md`
- `tests/test_pc_prepare_features.py`

**What Changed:**

- Escaped literal issue-schema braces in all Architect/UX/PM prepare prompts (live + template copies) so strict `format_map` rendering treats them as literal text.
- Added regression test coverage that renders all six codex-mode prompt templates and asserts the literal `{step, summary, risk, remediation}` schema remains in rendered prompts.

**Why:**

- `pc-prepare-features` uses fail-closed template rendering; unescaped literal braces caused a hard stop before design/ux/order artifacts could be generated.
- Prompt rendering for both source and template copies must stay aligned to avoid consumer repo drift and repeated prepare failures.

### 2026-02-18 - Prepare-features role execution hardening and process-feature opt-in

**Feature/Bug:** Fix generic prepare artifacts by enforcing prompt-driven Architect/UX/PM roles with semantic PM gating, and prevent implicit process-feature generation.

**Changed Files:**

- `tools/pc-prepare-features`
- `tools/prd-to-features`
- `Makefile`
- `tools/templates/root/Makefile`
- `prompts/architect-prepare.md`
- `prompts/ux-prepare.md`
- `prompts/product-manager-prepare-gate.md`
- `tools/templates/prompts/architect-prepare.md`
- `tools/templates/prompts/ux-prepare.md`
- `tools/templates/prompts/product-manager-prepare-gate.md`
- `docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `docs/README.md`
- `tools/templates/docs/README.md`
- `tools/README.md`
- `tests/test_pc_prepare_features.py`
- `tests/test_prd_to_features.py`
- `tests/test_docs_logs.py`

**What Changed:**

- Added prompt-driven role execution to `pc-prepare-features` for Architect, UX, and Product Manager with dedicated prompt files under `prompts/`.
- Added structured JSON parsing for role outputs and fail-closed PM semantic checks (generic-marker detection, feature-specific semantic token checks, PM decision/issue consistency).
- Kept deterministic fallback mode (`--role-mode=deterministic`) for controlled/local validation scenarios.
- Added explicit `--include-process-features` support in both `pc-prepare-features` and `prd-to-features`; default now excludes `## Process Features` unless explicitly enabled.
- Wired `INCLUDE_PROCESS_FEATURES=1` through live/template Makefile `prepare-features` targets.
- Updated workflow/docs contracts to state semantic PM criteria and process-feature opt-in behavior.
- Added tests for semantic PM gate behavior and process-feature opt-in behavior.

**Why:**

- Previous prepare outputs could pass structural checks while remaining generic and tooling-centric.
- PM gate needed semantic criteria enforcement to block non-project-specific architecture/UX artifacts.
- Process/governance checklist entries should not become executable feature folders unless explicitly requested.

### 2026-02-16 - Plan-reviewer conflict remediation output and env-prefixed Allowed Tests normalization

**Feature/Bug:** Improve `pc-feature` conflict remediation clarity and deterministic Plan/Allowed Tests policy alignment when commands include env prefixes.

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Updated `normalize_allowed_test` to canonicalize leading env assignments (for example `PYTHONHASHSEED=0`) before evaluating supported unittest/pytest commands.
- Kept `tools/offload-proxy/pp` canonicalization and added env-prefix handling after offload wrapper stripping.
- Tightened Plan/Allowed Tests mismatch text with explicit remediation wording.
- Added `format_plan_reviewer_conflict_message(...)` and switched the `Decision: Conflict` failure path to emit:
  - parsed `Required changes` lines from reviewer feedback,
  - direct pointer to `plan-reviewer-log.md`.
- Added/updated regression coverage for:
  - env-prefixed normalization behavior,
  - env-prefixed plan-command alignment checks,
  - conflict stderr remediation content and log pointer.

**Why:**

- Existing conflict failures stopped safely but surfaced only generic CLI guidance, forcing users to manually inspect role logs for actionable next steps.
- Env-prefixed commands were ignored during normalization, which could cause deterministic alignment checks to miss real Plan vs Allowed Tests contradictions.

### 2026-02-16 - Phase 5/6 docs and contract hardening for prepare/review artifacts

**Feature/Bug:** Align live/template workflow docs and documentation tests with new prepare/review state/report artifacts.

**Changed Files:**

- `docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `docs/README.md`
- `tools/templates/docs/README.md`
- `tools/README.md`
- `tests/test_docs_logs.py`

**What Changed:**

- Updated human orchestration workflow docs (live + template) to explicitly document:
  - `docs/03-logs/prepare-features-state.json` output from `make prepare-features`,
  - `docs/03-logs/review-features-report.json` output from `make review-features`.
- Extended chain-of-truth and update-in-place sections to include these artifacts.
- Updated docs readme workflow text to mention both artifacts as expected outputs.
- Added `tools/README.md` generated-artifacts section for `pc-prepare-features` and `pc-review-features`.
- Added/extended docs contract tests to fail closed if artifact references are removed from workflow/docs/template docs.

**Why:**

- Phase 3/4 introduced runtime artifacts; phase 5/6 closes documentation drift risk by making artifact contracts explicit and test-enforced.
- Keeping live and template docs synchronized prevents bootstrap repos from missing updated workflow expectations.

### 2026-02-16 - Phase 3/4 hardening for prepare/review orchestration artifacts

**Feature/Bug:** Add deterministic state/report artifacts for `make prepare-features` and `make review-features` loops.

**Changed Files:**

- `tools/pc-prepare-features`
- `tools/pc-review-features`
- `tests/test_pc_prepare_features.py`
- `tests/test_pc_review_features.py`

**What Changed:**

- `tools/pc-prepare-features` now persists loop/runtime state to `docs/03-logs/prepare-features-state.json`:
  - dependency decisions,
  - Product Manager gate history/decision trace,
  - execution stage status (`feature_generation_status`, `schema_check_status`).
- Added prefix-alias override support for interactive decisions (for example `PREPARE_DECISIONS=PM-BLOCK:2` applies to `PM-BLOCK-001`, `PM-BLOCK-002`, ...).
- Added deterministic state writes on PM abort/max-block and during generation/schema progression.
- `tools/pc-review-features` now emits a structured global report to `docs/03-logs/review-features-report.json` with per-feature findings and aggregate totals.
- Extended regression tests to assert:
  - prepare state artifact creation/content,
  - override alias behavior,
  - review report artifact creation/content.

**Why:**

- Phase 3/4 needed the same traceability and rerun diagnostics discipline used in mature `make feature` loops.
- Structured artifacts reduce ambiguity after failures and let humans inspect gate outcomes without re-reading terminal output.

### 2026-02-16 - Add prepare/review feature workflow with dependency ordering and global blueprints

**Feature/Bug:** Extend pre-generation and post-generation workflow without changing `make feature` runtime behavior.

**Changed Files:**

- `tools/pc-prepare-features`
- `tools/pc-review-features`
- `tools/prd-to-features`
- `.codex/skills/prd-to-features/SKILL.md`
- `.codex/skills/prd-to-features/scripts/plan_feature_folders.py`
- `.codex/skills/prd-to-features/references/selection-and-update-rules.md`
- `Makefile`
- `tools/templates/root/Makefile`
- `docs/01-product/design.md`
- `docs/01-product/ux-ui.md`
- `docs/02-features/feature-order.json`
- `docs/02-features/feature-order.md`
- `docs/04-process/human-orchestration-workflow.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tests/test_pc_prepare_features.py`
- `tests/test_pc_review_features.py`
- `tests/test_prd_to_features.py`
- `tests/test_docs_logs.py`

**What Changed:**

- Added `tools/pc-prepare-features` to run:
  - Architect design doc generation (`docs/01-product/design.md`)
  - UX blueprint generation (`docs/01-product/ux-ui.md`)
  - dependency graph resolution + topological ordering
  - Product Manager gate loop
  - handoff to `tools/prd-to-features`.
- Added interactive dependency ambiguity/cycle resolution with 2-4 numbered options and risk explanations, plus deterministic override support via `PREPARE_DECISIONS`.
- Added machine-readable order artifacts:
  - `docs/02-features/feature-order.json`
  - `docs/02-features/feature-order.md`
- Updated `tools/prd-to-features` to consume `feature-order.json` when present and reindex generation order accordingly while preserving non-destructive behavior for existing folders.
- Added `tools/pc-review-features` for post-generation `Security Reviewer -> Product Manager` checks; findings are written idempotently into machine-managed sections in `feature-spec.md` and `dev-tasks.md`.
- Added `make prepare-features` and `make review-features` targets (live + template Makefiles).
- Updated workflow/docs/contracts to include new prepare/review stages while keeping `make feature` protocol/order unchanged.
- Added/extended tests covering ordered-plan consumption, prepare workflow dependency decisions, review findings injection, and docs references.

**Why:**

- Move architecture/UX/dependency alignment earlier in the lifecycle and inject security/product findings before feature execution starts.
- Preserve existing `make feature` runtime guarantees and avoid regressions in the established role/gate flow.

### 2026-02-16 - Enforce required feature-template dev-tasks pair in template sync and improve coherence remediation

**Feature/Bug:** Consumer repos can fail `devtasks-schema-check` when `tools/templates/docs/02-features/feature-template/dev-tasks.md` is missing, while migration tooling is a no-op.

**Changed Files:**

- `tools/pc-template-sync`
- `tools/pc-devtasks-schema-check`
- `tests/test_pc_template_sync.py`
- `tests/test_pc_devtasks_schema_check.py`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`
- `docs/03-logs/decision-log.md`

**What Changed:**

- Added a required template/living pair contract in `tools/pc-template-sync` for:
  - `docs/02-features/feature-template/dev-tasks.md`
  - `tools/templates/docs/02-features/feature-template/dev-tasks.md`
- Updated sync behavior so required one-sided-missing drift is deterministic:
  - with `--apply`, copy existing side to missing side and stage when requested;
  - without `--apply`, fail with explicit copy action guidance.
- Kept fail-closed behavior when both sides of a required pair are missing.
- Added targeted coherence remediation in `tools/pc-devtasks-schema-check` when template source copy is missing:
  - explicit restore path for the missing template-source file,
  - explicit note that `tools/pc-devtasks-migrate-legacy` cannot create missing `tools/templates` files.
- Added regression tests for:
  - missing template-source coherence remediation quality,
  - required-pair missing-side recovery and no-`--apply` guidance.

**Why:**

- `pc-devtasks-migrate-legacy` migrates existing feature entries only; it cannot heal missing template-source files.
- Required pair enforcement in `pc-template-sync` prevents this drift from escaping detection and gives deterministic recovery.

### 2026-02-16 - Add schema/tooling coherence guard for tester-feedback outcome invariant

**Feature/Bug:** Prevent partial sync drift where `devtasks-schema-check` enforces tester-feedback outcomes but runtime/template artifacts lag behind.

**Changed Files:**

- `tools/pc-devtasks-schema-check`
- `tools/pc-feature`
- `docs/02-features/feature-template/dev-tasks.md`
- `tools/templates/docs/02-features/feature-template/dev-tasks.md`
- `tests/test_pc_devtasks_schema_check.py`
- `tests/test_pc_feature.py`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`
- `docs/03-logs/decision-log.md`

**What Changed:**

- Added a deterministic compatibility marker contract (`feedback-outcome-v1`) across:
  - `tools/pc-feature` (`DEVTASKS_SCHEMA_COMPAT_MARKER`),
  - live feature template `dev-tasks.md`,
  - template source copy `dev-tasks.md`.
- Added a fail-fast tooling/template coherence guard in `tools/pc-devtasks-schema-check` that runs before semantic work-item checks and blocks on:
  - missing marker/mismatched marker,
  - missing template copy/live template files in tooling-managed contexts,
  - missing `Outcome:` fields in `Tester Feedback` / `Reporter Feedback` template sections.
- Added explicit remediation output directing users to sync tooling/template artifacts and run `tools/pc-devtasks-migrate-legacy`.
- Added regression coverage for:
  - marker mismatch guard failures,
  - missing feedback outcome field guard failures,
  - matching-coherence pass path.
- Added a focused `pc-feature` regression asserting runtime entry scaffolding still contains tester/reporter `Outcome` placeholders and the compat marker constant.

**Why:**

- Consumer repositories can drift into deterministic pre-commit failures when only schema checks are updated.
- The new guard fails early with actionable remediation instead of allowing late semantic failures from mismatched artifacts.

### 2026-02-16 - Quiet scoped pre-commit output and autofix retry normalization

**Feature/Bug:** `make feature` flows still emitted noisy per-hook status lines and surfaced transient `Failed` states for auto-fixed hooks.

**Changed Files:**

- `tools/pc-hooks-run`
- `tools/pc-feature`
- `tests/test_pc_hooks_run.py`
- `tests/test_pc_feature.py`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Added `--retry-on-autofix` to `tools/pc-hooks-run`:
  - detects modified-file hook failures (`files were modified by this hook`),
  - reruns pre-commit once on that condition,
  - remains silent when the retry succeeds,
  - writes combined first-run/retry diagnostics to offload only when retry still fails.
- Updated `tools/pc-feature` pre-commit execution paths to prefer `tools/pc-hooks-run --hook-stage pre-commit --retry-on-autofix --files ...` for:
  - role-scoped formatting before role commits,
  - scoped autofix during CI retry flow.
- Kept deterministic fallback to direct `pre-commit` (offloaded via `pp`) when `tools/pc-hooks-run` is unavailable.
- Updated scoped autofix reporting labels and adjusted regression tests to validate the new runner contract.

**Why:**

- Align `make feature` behavior with quiet-green / concise-failure policy.
- Remove non-actionable `Passed/Skipped` noise and suppress transient auto-fix `Failed` output when rerun validation passes.

### 2026-02-14 - Context refresh for post-MVP optimization phase

**Feature/Bug:** Context alignment after MVP completion

**Changed Files:**

- `docs/00-context/vision.md`
- `docs/00-context/system-map.md`
- `docs/00-context/context-boundaries-operating-model.md`
- `docs/00-context/users.md`
- `docs/00-context/assumptions.md`
- `docs/00-context/expected-features.md`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Updated context docs to reflect confirmed product reality:
  - single-user/personal workflow scope,
  - MVP status achieved and in use across projects,
  - post-MVP focus on error reduction, token efficiency, and removing unused complexity.
- Replaced stale/placeholder content in `users.md` (edge users now explicitly none).
- Rebased expected feature candidates to the post-MVP hardening backlog.
- Added a decision entry documenting the post-MVP scope constraint.

**Why:**

- Keep source-of-truth context aligned with the current product phase and prevent future scope drift toward generic or high-toil workflows.

### 2026-02-14 - Batch B/C skill hardening: deterministic resources, progressive disclosure, and CI metadata guardrail

**Feature/Bug:** Codex skills robustness and policy hardening (Batch B + C)

**Changed Files:**

- `.codex/skills/feature-status-audit/SKILL.md`
- `.codex/skills/feature-status-audit/scripts/run_audit.py`
- `.codex/skills/update-docs/SKILL.md`
- `.codex/skills/update-docs/scripts/new_log_entry.py`
- `.codex/skills/prd-to-features/SKILL.md`
- `.codex/skills/prd-to-features/scripts/plan_feature_folders.py`
- `.codex/skills/prd-to-features/references/selection-and-update-rules.md`
- `.codex/skills/investigate/SKILL.md`
- `.codex/skills/investigate/references/investigation-rubric.md`
- `.codex/skills/readme-sync/SKILL.md`
- `.codex/skills/readme-sync/references/readme-rules.md`
- `.codex/skills/sync-root-from-context/SKILL.md`
- `.codex/skills/sync-root-from-context/references/root-file-checklist.md`
- `.codex/skills/*/agents/openai.yaml` (dependency/policy updates on selected skills)
- `tools/pc-skills-metadata-check`
- `tests/test_pc_skills_metadata_check.py`
- `Makefile`
- `tools/templates/root/Makefile`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/bug-log.md`
- `docs/03-logs/validation-log.md`
- `docs/03-logs/insights.md`

**What Changed:**

- Added deterministic helper scripts for repeated skill workflows:
  - feature status audits (`run_audit.py`),
  - docs log entry scaffolding (`new_log_entry.py`),
  - PRD-to-feature planning preview (`plan_feature_folders.py`).
- Refactored long skill bodies into progressive-disclosure references for `investigate`, `prd-to-features`, `readme-sync`, and `sync-root-from-context`.
- Added `dependencies.tools` metadata (Serena MCP) to edit-heavy skills and disabled implicit invocation for high-impact mutating skills.
- Added new repository guardrail `tools/pc-skills-metadata-check` and wired it into `make test`/`make ci` through `skills-metadata-check` in both live and template Makefiles.
- Added unit coverage for the new metadata checker.

**Why:**

- Reduce execution variance for repetitive workflows, keep skills concise under context pressure, and enforce metadata quality in CI to prevent trigger/prompt drift and portability regressions.

### 2026-02-14 - Batch A skill metadata hardening and portability cleanup

**Feature/Bug:** Codex skill activation quality and interface consistency

**Changed Files:**

- `.codex/skills/*/SKILL.md` (15 skills)
- `.codex/skills/*/agents/openai.yaml` (15 skills)
- `docs/03-logs/decision-log.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/insights.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Rewrote frontmatter `description` text across all local skills so each description clearly states task scope plus trigger conditions.
- Standardized `agents/openai.yaml` for all skills with consistent `display_name`, `short_description`, and `default_prompt`.
- Ensured every `default_prompt` explicitly references its skill token (for example, `$implement-plan-safe`) for explicit invocation clarity.
- Removed hardcoded user-specific absolute paths from skill metadata/instructions and replaced with portable repo-relative or environment-based paths.
- Resolved validator-incompatible metadata patterns (angle brackets in descriptions) discovered during validation.

**Why:**

- Improve auto-trigger precision, reduce invocation ambiguity, and keep skill metadata portable across machines/worktrees.
- Keep interface metadata aligned with current Codex Skills conventions and avoid stale or inconsistent UI prompts.

### 2026-02-13 - PRD context/process reconciliation via context-to-product

**Feature/Bug:** PRD alignment with current context + workflow policy

**Changed Files:**

- `docs/01-product/prd.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Updated PRD metadata/version and refreshed feature-priority mapping to reflect current expected features from `docs/00-context/expected-features.md`.
- Strengthened workflow/process requirements to match canonical protocol details:
  - command authority for `make feature` / `pc-feature`,
  - mandatory preflight + deterministic risk classification,
  - HIGH-risk approval behavior with `Awaiting PO Approval`,
  - reviewer/tester/reporter feedback-loop restart behavior,
  - fail-closed commit gate + `tools/pc-commit` commit format enforcement.
- Added explicit anti-hardcode testing requirements (fixture count, seed strategy, invariants, contract boundaries) to functional/process sections.
- Cleaned PRD scope section labels to remove remaining template markers and clarified future-scope wording for UI/TUI separation.

**Why:**

- Keep `docs/01-product/prd.md` synchronized with source-of-truth context/process docs and prevent drift between product intent and execution policy.
- Ensure required gating, testing, and documentation constraints are discoverable from the PRD without relying on implicit knowledge.

### 2026-02-13 - Accept documented Codex skill directory layout in skills-check

**Feature/Bug:** False CI failures from strict skill layout gate

**Changed Files:**

- `Makefile`
- `tools/templates/root/Makefile`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Updated `skills-check` to allow documented optional skill subdirectories: `agents`, `scripts`, `references`, and `assets`.
- Added strict validation for `agents/`:
  - `agents/openai.yaml` must exist when `agents/` exists,
  - no extra files in `agents/`,
  - no nested subdirectories in `agents/`.
- Kept fail-closed behavior for unexpected top-level skill files/subdirectories.
- Applied the same logic to `tools/templates/root/Makefile` to preserve live/template parity.

**Why:**

- Codex Skills documentation explicitly allows `agents/openai.yaml`, and current skill scaffolding creates it.
- Existing strict checks caused deterministic `make ci` failure in valid skill states.

### 2026-02-13 - New skill: implement-plan-safe

**Feature/Bug:** Prompt simplification for approved plan execution

**Changed Files:**

- `.codex/skills/implement-plan-safe/SKILL.md`
- `.codex/skills/implement-plan-safe/agents/openai.yaml`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Created new chat-only skill `implement-plan-safe`.
- Defined trigger scope for short user commands (`Implement`, `Please implement this plan`, etc.) tied to existing approved plan context.
- Added explicit no-side-effect guardrails, including explicit-approval requirements for `make feature` / `pc-feature`.
- Added fallback behavior: ask one focused question and stop when no clear plan exists.
- Added interface metadata for skill list/chip behavior.

**Why:**

- Reduce user command verbosity while preserving deterministic execution and safety constraints.

### 2026-02-12 - Dedicated Plan Reviewer Codex profile

**Feature/Bug:** Orchestrator role profile isolation

**Changed Files:**

- `.codex.toml`
- `tools/templates/root/.codex.toml`
- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Added a dedicated `PlanReviewer` profile to both live and template Codex config files.
- Matched the profile tuning to planner-grade review depth (`high` reasoning, `medium` verbosity).
- Routed the plan-reviewer gate in `tools/pc-feature` to execute with `profile="PlanReviewer"` instead of `Planner`.
- Added a regression test that captures `codex_exec` arguments and asserts the Plan Reviewer prompt uses the `PlanReviewer` profile.

**Why:**

- Make role-to-profile mapping explicit for all first-class workflow roles.
- Avoid accidental coupling between Planner tuning and Plan Reviewer behavior.
- Keep bootstrap/template defaults aligned with the live repo config.

### 2026-02-12 - Precommit template-sync autofix policy update

**Feature/Bug:** Deterministic template/living sync in precommit

**Changed Files:**

- `.pre-commit-config.yaml`
- `tools/pc-template-sync`
- `tools/pc-precommit`
- `tests/test_pc_template_sync.py`

**What Changed:**

- Updated precommit hook entry so `template-sync` runs in autofix mode (`--apply --stage`).
- Extended `pc-template-sync` behavior:
  - one-side-changed mismatch: copy changed side into unchanged paired file and optionally stage target,
  - neither-side-changed mismatch (unexpected drift): copy live file to template deterministically,
  - both-sides-changed mismatch: fail with explicit Codex-assisted merge guidance (no automatic overwrite).
- Added staging support in `pc-template-sync` so synced targets are immediately staged.
- Updated `pc-precommit` to refresh staged-file scope between runs and rerun hooks when hook execution changes the staged file set.
- Added dedicated unit tests for the new `pc-template-sync` behavior matrix.

**Why:**

- Remove noisy manual failures for simple copy-sync cases.
- Keep strict safety for conflicting dual-edits that require semantic merge.
- Ensure subsequent hooks validate newly staged template files in the same precommit run.

### 2026-02-12 - Feature 17 closure on `main` (final worktree merge + completed status)

**Feature/Bug:** F-17 closeout and documentation finalization

**Changed Files:**

- `docs/02-features/17-resume-in-progress-tickets/feature-spec.md`
- `docs/02-features/17-resume-in-progress-tickets/tech-design.md`
- `docs/02-features/17-resume-in-progress-tickets/test-plan.md`
- `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md`

**What Changed:**

- Merged the remaining `feature-17-resume-in-progress-tickets-patcher` branch commits into `main` (merge commit `9614166`).
- Updated F-17 documentation status headers from draft/incomplete state to `Completed`.
- Updated F-17 `Last Updated` metadata to `2026-02-12` across the core feature docs.

**Why:**

- Finalize feature 17 on `main` so continued work and review happen from a single, up-to-date branch state.
- Make feature-level documentation reflect the completed delivery state.

**How:**

- Used a non-fast-forward git merge from the feature worktree branch into `main`.
- Applied focused doc-header edits only (status + date) to avoid rewriting execution history.

### 2026-02-12 - Resume contradiction auto-repair for pending execution sections

**Feature/Bug:** F-17 resume auto-repair (contradictory resume state remediation)

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added startup policy parsing for contradiction handling (`repair|block|rewind`) and a dry-run switch for repair simulation.
- Implemented role-artifact parsing helpers to read the latest WI entry from `validation-log.md` / `reporter-log.md`.
- Added deterministic startup reconciliation that backfills pending `Patch`, `Test Results`, and `Reporter Review` sections when artifacts prove those phases already ran.
- Updated resume-route detection to fall back to role artifact outcomes when feedback sections are blank, preserving correct planner restart on tester failures.
- Preserved fail-closed behavior when candidate repair still leaves contradictions.
- Added unit coverage for policy parsing, artifact-outcome fallback routing, reporter-skip handling, and reconciliation behavior.

**Why:**

- Prevent restart failures where role artifacts exist but `dev-tasks.md` sections are still pending, while keeping resume safety deterministic and auditable.

**How:**

- Added in-memory repair planning + route validation before writing `dev-tasks.md`.
- Wrote only when repair unblocks routing (unless dry-run is enabled).
- Extended `TestPcFeature` unit scenarios to lock the new safety and routing invariants.

### 2026-02-11 - Sync docs templates with updated live process/docs files

**Feature/Bug:** Template/living parity (docs template sync)

**Changed Files:**

- `tools/templates/docs/README.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`

**What Changed:**

- Synced template docs to match the already-updated live docs for README and workflow control-flow/restart guidance.
- Removed drift causing `pc-template-sync` manual-resolution errors for unchanged pairs.

**Why:**

- Keep bootstrapped docs consistent with current live docs and restore deterministic template/living parity checks.

**How:**

- Copied live docs into their template counterparts and validated parity with `tools/pc-template-sync`.

### 2026-02-11 - Root config sync from context (non-template root files)

**Feature/Bug:** Root workflow alignment (context-driven sync)

**Changed Files:**

- `AGENTS.md`
- `.gitignore`
- `LICENSE`
- `pp.yml`
- `.serena/project.yml`
- `.serena/.gitignore`

**What Changed:**

- Updated AGENTS test/lint guidance to point to current `make lint`, `make test`, and `make ci` commands.
- Added local runtime cache ignores (`.pytest_cache/`, `.ruff_cache/`) and Serena memory ignore (`.serena/.gitignore`).
- Replaced MIT license placeholder owner/year with project-specific values.
- Expanded offload defaults in `pp.yml` for large-output command families used by this repo (`sed`, unittest invocations, `make test/ci`, `pre-commit run`).
- Refined Serena project initial prompt to reference context/log sources and current orchestration/process docs.

**Why:**

- Keep live root files aligned with the documented operating model (CLI-first, offload-first, deterministic workflow) while preserving template files untouched.

**How:**

- Reconciled root file content against `docs/00-context/` and `docs/01-product/prd.md`, then applied minimal edits only where drift or placeholders were present.

### 2026-02-11 - README sync and deduplication

**Feature/Bug:** Documentation hygiene (README consolidation)

**Changed Files:**

- `README.md`
- `docs/README.md`
- `tools/README.md`
- `tools/serena/solidlsp_override/README.md`
- `tools/serena/solidlsp_override/solidlsp/language_servers/elixir_tools/README.md`

**What Changed:**

- Reduced overlap between root/docs/tools READMEs and kept each file focused on its audience.
- Replaced long repeated explanations with concise structure/workflow pointers.
- Aligned Serena override READMEs with the documented LSP override decision reference (`DEC-002`).

**Why:**

- Keep README content accurate, compact, and easier to maintain without duplicating process/context narratives.

**How:**

- Reconciled README statements against `docs/00-context/` and `docs/03-logs/`, then rewrote each in-scope README to a minimal Purpose/Map/Workflow/Related Docs structure.

### 2026-02-11 - Workflow role-loop audit contract and retry guidance

**Feature/Bug:** Workflow control-flow hardening (role orchestration docs/prompts)

**Changed Files:**

- `docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/human-orchestration-workflow.md`
- `prompts/planner.md`
- `prompts/plan-reviewer-gate.md`
- `prompts/patcher-apply.md`
- `prompts/tester.md`
- `tests/test_orchestrator_workflow_docs.py`

**What Changed:**

- Added an explicit execution-order and restart contract to the ticket execution protocol.
- Synced the human orchestration workflow with strict routing and no-op logging requirements.
- Strengthened role prompts with retry/restart and actionable failure-context guidance.
- Added doc-level regression tests that assert ordering and restart rules are documented.

**Why:**

- Ensure every role can restart cleanly after failure, propagate actionable context, and preserve deterministic workflow ordering.

**How:**

- Updated canonical process docs and role prompts, then added focused tests to prevent documentation regressions.

### 2026-02-10 - Log compaction freshness + dedupe hardening with LLM compact outputs

**Feature/Bug:** F-15 follow-up hardening (offload audit + useful compaction)

**Changed Files:**

- `tools/log-compaction`
- `lib/log_compaction.py`
- `tests/test_log_compaction.py`
- `docs/04-process/output-offload.md`
- `docs/03-logs/compacted/decision-log-compact.json`
- `docs/03-logs/compacted/implementation-log-compact.json`
- `docs/03-logs/compacted/validation-log-compact.json`
- `docs/03-logs/compacted/decision-log-compact.llm.json`
- `docs/03-logs/compacted/implementation-log-compact.llm.json`
- `docs/03-logs/compacted/validation-log-compact.llm.json`
- `docs/03-logs/compacted/compaction-report.json`
- `docs/03-logs/compacted/semantic-map.json`

**What Changed:**

- Reworked `tools/log-compaction` to:
  - parse mixed heading styles by log type,
  - sort entries by parsed date descending before truncation,
  - dedupe entries deterministically with merge logic for evidence/work-item context,
  - support optional semantic-map canonicalization, and
  - emit a token-optimized LLM artifact (`*.llm.json`) in addition to the full compact output.
- Added metrics reporting via `docs/03-logs/compacted/compaction-report.json` with dedupe ratio, freshness lag, and token estimates.
- Added reusable path helpers in `lib/log_compaction.py` for LLM outputs, report, and semantic map.
- Expanded `tests/test_log_compaction.py` to cover mixed heading parsing, freshness lag, DEC-id dedupe, LLM output contract, and new path helpers.
- Updated process docs with explicit compaction commands and report interpretation guidance.

**Why:**

- Keep compact outputs current and trustworthy while minimizing prompt-token usage in repeated LLM calls.

**How:**

- Implemented deterministic parse/sort/dedupe pipeline in compaction tooling, then regenerated derived compact artifacts from canonical logs.

### 2026-02-08 - Precommit autofix scope hardening and deterministic fallback

**Feature/Bug:** Process/Tooling - precommit autofix guardrails

**Changed Files:**

- `.pre-commit-config.yaml`
- `tools/templates/root/.pre-commit-config.yaml`
- `tools/pc-autofix`
- `tools/pc-precommit`
- `tools/pc-template-sync`
- `tools/markdown-lint`
- `tests/test_pc_autofix.py`
- `docs/04-process/git-workflow.md`
- `tools/templates/docs/04-process/git-workflow.md`
- `docs/04-process/ci-autofix-prompt.md`
- `tools/templates/docs/04-process/ci-autofix-prompt.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Hardened precommit autofix scope by passing staged allowlists into `pc-autofix` and blocking out-of-scope edits after Codex runs.
- Updated `pc-precommit` to run hooks on staged files (`pre-commit run --files ...`), restage only modified staged paths, and print re-staged files.
- Moved template sync hook behavior to deterministic check-only in pre-commit path (no Codex execution).
- Updated markdown lint hook behavior to process passed markdown filenames in pre-commit for faster runs.
- Added targeted regression tests for `pc-autofix` prompt/scope behavior.
- Synced living/template process docs with deterministic-first autofix + scoped Codex fallback policy.

**Why:**

- Prevent precommit Codex runs from editing unrelated files (especially `docs/03-logs/*` and feature logs) and reduce pre-commit latency/scope creep.

**How:**

- Replaced broad Codex precommit prompting with explicit allowlist + forbidden-path constraints and post-run git-status scope verification.
- Reworked hook wiring to favor deterministic format/lint passes before any AI fallback and to keep all edits within staged scope.

### 2026-02-08 - Sync resume policy block into ticket execution protocol template

**Feature/Bug:** Template sync (no feature id)

**Changed Files:**

- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Restored the resume startup policy block (RESUME_MODE options and guards) in the template.

**Why:**

- Keep the template aligned with the living execution protocol guidance.

**How:**

- Copied the missing resume policy bullets from `docs/04-process/ticket-execution-protocol.md`.

### 2026-02-08 - Rebaseline feature docs for F-12 incremental PRD-to-features

**Feature/Bug:** Documentation alignment (F-12)

**Changed Files:**

- `docs/02-features/12-incremental-prd-to-features/feature-spec.md`
- `docs/02-features/12-incremental-prd-to-features/tech-design.md`
- `docs/02-features/12-incremental-prd-to-features/dev-tasks.md`
- `docs/02-features/12-incremental-prd-to-features/test-plan.md`

**What Changed:**

- Rewrote F-12 docs to match current incremental policy:
  - add missing features only,
  - never delete existing folders,
  - skip `Status: Done` feature folders,
  - update existing non-done folders in place without destructive overwrite.
- Replaced placeholder related-doc links with concrete repository paths.
- Added explicit task/test coverage for idempotency, duplicate prevention, and no-delete guarantees.

**Why:**

- The original F-12 docs were too generic and did not reflect the current process contract, which made implementation attempts ambiguous.

**How:**

- Audited current PRD/workflow/skill rules and rewrote the feature docs in place.

**Trade-offs / Notes:**

- This is a documentation rebaseline only; feature execution status remains unchanged.

### 2026-02-08 - Template sync for ticket execution protocol (plan policy check)

**Feature/Bug:** Template sync (no feature id)

**Changed Files:**

- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Restored the deterministic plan policy check bullet in the template's Plan step.

**Why:**

- Keep the template aligned with the living execution protocol's Plan requirements.

**How:**

- Added the missing bullet to match `docs/04-process/ticket-execution-protocol.md`.

### 2026-02-08 - Rebaseline backlog feature docs for F-13 to F-16

**Feature/Bug:** Documentation alignment (F-13/F-14/F-15/F-16)

**Changed Files:**

- `docs/02-features/13-role-prompts-plan-reviewer/feature-spec.md`
- `docs/02-features/13-role-prompts-plan-reviewer/tech-design.md`
- `docs/02-features/13-role-prompts-plan-reviewer/dev-tasks.md`
- `docs/02-features/13-role-prompts-plan-reviewer/test-plan.md`
- `docs/02-features/14-learning-loop-improvement-proposals/feature-spec.md`
- `docs/02-features/14-learning-loop-improvement-proposals/tech-design.md`
- `docs/02-features/14-learning-loop-improvement-proposals/dev-tasks.md`
- `docs/02-features/14-learning-loop-improvement-proposals/test-plan.md`
- `docs/02-features/15-offload-audit-and-log-compaction/feature-spec.md`
- `docs/02-features/15-offload-audit-and-log-compaction/tech-design.md`
- `docs/02-features/15-offload-audit-and-log-compaction/dev-tasks.md`
- `docs/02-features/15-offload-audit-and-log-compaction/test-plan.md`
- `docs/02-features/16-feature-gating-and-skill-mining/feature-spec.md`
- `docs/02-features/16-feature-gating-and-skill-mining/tech-design.md`
- `docs/02-features/16-feature-gating-and-skill-mining/dev-tasks.md`
- `docs/02-features/16-feature-gating-and-skill-mining/test-plan.md`

**What Changed:**

- Rewrote feature specs/designs/tasks/test plans for features 13-16 to match the current prompt/process architecture.
- Reframed F-13 from initial prompt creation to prompt-contract maintenance and Plan Reviewer gate validation.
- Added explicit implementation targets for:
  - fail/stall proposal capture and dedup in F-14,
  - offload index/list/get/purge and compaction scope in F-15,
  - soft precommit sequencing warnings plus skill-mining proposals in F-16.
- Replaced placeholder related-document links with concrete repository paths and refreshed metadata dates.

**Why:**

- The original feature docs were generated before recent prompt/workflow hardening and no longer represented the current implementation context.

**How:**

- Audited `prompts/*`, workflow/process docs, and existing logs; then updated each feature document set in place.

**Trade-offs / Notes:**

- Feature `Status` values remain draft/not-started; this change updates scope/requirements, not execution completion.

### 2026-02-08 - Template sync for ticket execution protocol

**Feature/Bug:** Template sync (no feature id)

**Changed Files:**

- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Restored runtime artifact handling and step-routing rules in the template.
- Aligned log location wording with the living protocol doc.

**Why:**

- Keep the template in lockstep with the updated execution protocol.

**How:**

- Applied the corresponding bullet updates from `docs/04-process/ticket-execution-protocol.md`.

### 2026-02-07 - Template sync for workflow docs

**Feature/Bug:** Template sync (no feature id)

**Changed Files:**

- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/dev-workflow.md`

**What Changed:**

- Restated the HIGH-risk approval stop/continue clause in the template.
- Restored the single-worktree-by-default guidance in the parallel-mode template section.

**Why:**

- Keep templates aligned with the living workflow docs and orchestration policy.

**How:**

- Updated the specific lines in the templates to match the corresponding docs.

### 2026-02-07 - Workflow doc sync (orchestration + dev workflow)

**Feature/Bug:** Doc sync (no feature id)

**Changed Files:**

- `docs/04-process/human-orchestration-workflow.md`
- `docs/04-process/dev-workflow.md`

**What Changed:**

- Clarified that HIGH-risk items stop after Preflight and wait for PO approval.
- Updated parallel-mode guidance to require separate sessions/worktrees when parallelizing.

**Why:**

- Align living workflow docs with the intended orchestration and parallel execution policy.

**How:**

- Applied the updated lines in the living docs and verified templates already matched.

### 2026-02-06 - Interactive high-risk approval gate in pc-feature

**Feature/Bug:** F-10 workflow usability (high-risk gate)

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Added `APPROVE_HIGH_RISK` override parsing (`1/true/yes` approve, `0/false/no` deny).
- Added interactive high-risk gate helper that:
  - prints detected risk triggers,
  - prompts `approve high-risk work item and continue? [y/N]` when interactive,
  - defaults to deny in non-interactive mode unless `APPROVE_HIGH_RISK=1`.
- Replaced unconditional high-risk stop with the new approval check.
- Added focused regression tests for:
  - interactive approve continues execution,
  - interactive deny keeps `Awaiting PO Approval` stop,
  - non-interactive deny without override.
- Synced protocol docs/template to document interactive approval + non-interactive override behavior.

**Why:**

- Allow continuing high-risk work in the same `make feature` run while keeping safe default behavior for unattended runs.

**How:**

- Introduced explicit approval helper functions and integrated them in preflight HIGH-risk handling.

### 2026-02-06 - Step 16 docs/template sync + end-to-end validation pass

**Feature/Bug:** Workflow hardening (Step 16)

**Changed Files:**

- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Verified `ticket-execution-protocol.md` and template are synchronized.
- Verified `human-orchestration-workflow.md` and template are synchronized.
- Ran focused orchestration suites and one final `make ci` run.
- Recorded final validation outcomes in global logs.

**Why:**

- Step 16 requires final consistency and one end-to-end validation pass after workflow hardening changes.

**How:**

- Executed diff checks between docs/templates, then ran focused tests and final CI command.

### 2026-02-06 - pc-feature Step 15: autofix scope lockdown

**Feature/Bug:** Workflow hardening (Step 15)

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Replaced autofix `pre-commit --all-files` path with staged-scope-only autofix flow.
- Added helpers:
  - `get_staged_paths(...)`
  - `run_scoped_autofix(...)`
- New autofix behavior:
  - capture/stage scoped paths before autofix
  - run `tools/offload-proxy/pp pre-commit run --files <scoped paths>`
  - fail if any out-of-scope files are touched
  - re-stage only the same scoped file list
- Added test coverage for:
  - out-of-scope touch detection in scoped autofix
  - CI retry autofix using `--files` scoped list (no `--all-files`)
- Updated protocol docs/template with scoped-autofix requirements.

**Why:**

- Prevent autofix from expanding commit scope or mutating unrelated files.

**How:**

- Integrated scoped staging + autofix checks in the CI retry gate and validated behavior with focused unit tests.

### 2026-02-06 - pc-feature Step 14: escalation broker + worktree-first ordering

**Feature/Bug:** Workflow hardening (Step 14)

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Added orchestrator-side escalation broker utilities in `pc-feature`:
  - structured escalation request parsing (`parse_escalation_request`)
  - command normalization/allowlist enforcement
  - broker decision + command dispatch (`process_escalation_request`)
  - broker result formatting + escalation loop handling in `codex_exec`
- Added escalation logging via runner logs (`logs/<WI>/escalation.log`) for request approval, decision, and completion.
- Updated `codex_exec` usage sites to pass runner metadata/root so broker actions are logged.
- Moved patcher worktree preparation/cleaning before the first mutable workflow writes to avoid pre-create root-write drift.
- Added focused tests for:
  - escalation request parsing
  - denied escalation path (allowlist rejection)
  - approved escalation dispatch
  - worktree preparation ordering before first `dev-tasks.md` write
- Synced protocol docs/template with orchestrator-mediated escalation policy.

**Why:**

- Keep escalation execution under orchestrator control and prevent state drift caused by mutable writes before worktree setup.

**How:**

- Refactored `codex_exec` into a one-shot runner + escalation-aware wrapper, introduced broker helpers, and reordered early main-flow setup.

### 2026-02-06 - pc-feature Step 13: deterministic risk path triggers from planned + actual paths

**Feature/Bug:** Workflow hardening (Step 13)

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Added explicit protocol path triggers in risk classification for:
  - `sanitizer/`
  - `detectors/`
  - `restore/`
  - `git_ops/`
  - `metadata/`
- Risk classifier now evaluates both:
  - planned `files_to_change` from preflight JSON
  - actual changed paths from existing patcher worktree status (when available)
- Added helper normalization/dedup logic so trigger output remains deterministic and concise.
- Expanded unit tests to cover each trigger path, actual-path evaluation, and deduped mixed scenarios.
- Updated protocol docs/template wording to match planned+actual path evaluation.

**Why:**

- Align risk classification with protocol-defined path triggers and avoid missing HIGH-risk paths during resume/in-progress work.

**How:**

- Refactored `classify_risk(...)` with path-trigger helpers and wired preflight to include existing worktree changed paths.

### 2026-02-06 - pc-feature Step 12: strict Allowed Tests enforcement and checker parsing

**Feature/Bug:** Workflow hardening (Step 12)

**Changed Files:**

- `tools/pc-feature`
- `tools/pc-allowed-tests-check`
- `tests/test_pc_feature.py`
- `tests/test_pc_allowed_tests_check.py`
- `prompts/planner-update-allowed-tests.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Removed placeholder smoke fallback from `pc-feature`; invalid/missing Allowed Tests now fail immediately after planner remediation attempts with explicit remediation guidance.
- Kept `make ci` forbidden in Allowed Tests and expanded remediation text.
- Hardened `pc-allowed-tests-check` parsing:
  - Proper `python -m unittest discover ...` option/positional parsing (`-s`, `-p`, `-t`).
  - Validation for discover start/top directories and test-pattern matches.
  - Improved unittest target checks for module/path targets.
  - Stronger pytest target validation.
  - Explicit rejection for `make ci`.
- Updated planner Allowed Tests prompt to request meaningful unittest/pytest commands (no placeholders/narrative).
- Synced protocol docs/template with strict failure behavior for invalid Allowed Tests.

**Why:**

- Prevent false-positive workflow progress with placeholder smoke commands and make Allowed Tests validation meaningful and deterministic.

**How:**

- Refactored Allowed Tests handling in `pc-feature`, enhanced checker parsing logic, added focused regressions, and updated process documentation.

### 2026-02-06 - pc-feature Step 11: use tools/pc-commit for final commit

**Feature/Bug:** Workflow hardening (Step 11)

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Replaced direct final `git commit -m ...` in `pc-feature` with `tools/pc-commit`.
- Final commit now passes:
  - `--yes` for non-interactive execution
  - `--message <commit_message>` from the workflow commit section
  - repeated `--allow <path>` values from scoped staged files
- Added regression assertions ensuring:
  - no direct `git commit` call is made
  - `tools/pc-commit` is invoked during final commit path

**Why:**

- Align final commit flow with protocol requirements and keep commit checks centralized in `tools/pc-commit`.

**How:**

- Updated final commit block in `pc-feature` and extended existing final-staging test coverage.

### 2026-02-06 - pc-feature Step 10: reduce final-gate CI attempts

**Feature/Bug:** Workflow hardening (Step 10)

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Replaced multi-attempt CI loop with a strict final gate cadence:
  - Run `make ci` once.
  - If it fails, run one autofix attempt.
  - Run `make ci` one final retry (max 2 total CI runs).
- Updated failure message to report the explicit max-attempt policy.
- Added regression tests for:
  - first-pass CI success uses one CI run
  - failing CI retries exactly once with one autofix call
- Updated protocol docs and template to match the new cadence.

**Why:**

- Reduce costly full-CI runs while keeping a deterministic recovery path.

**How:**

- Modified final gate logic in `pc-feature`, added focused tests, and synced process docs/templates.

### 2026-02-06 - pc-feature Step 09: enforce replanning/repaching after feedback failures

**Feature/Bug:** Workflow hardening (Step 09)

**Changed Files:**

- `tools/pc-feature`
- `prompts/planner-update_from_feedback.md`
- `prompts/patcher-update_from_feedback.md`
- `tests/test_pc_feature.py`

**What Changed:**

- Added a deterministic failure loop in `pc-feature` that, on tester/reporter failure, aggregates feedback, invokes planner feedback review, optionally revises the Plan section, then invokes a dedicated patcher feedback task before retest.
- Added parser helpers for planner feedback decision/rationale/revised-plan extraction.
- Appended Iteration Log rationale notes for each failure cycle.
- Added regression coverage for planner feedback decision parsing and fail-loop planner/patcher enforcement.

**Why:**

- Ensure the workflow cannot skip planner re-evaluation and targeted repatching after failed validation/review cycles.

**How:**

- Extended the main loop failure branch in `tools/pc-feature`, added task-specific prompt templates, and validated with focused unit tests.

### 2026-02-06 - F-09 completion: add tests/ci structured logs in pc-feature

**Feature/Bug:** F-09 Runner library + structured logs

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/02-features/09-runner-structured-logs/dev-tasks.md`
- `docs/02-features/09-runner-structured-logs/validation-log.md`
- `docs/02-features/09-runner-structured-logs/reporter-log.md`

**What Changed:**

- Added `run_command_with_step_log(...)` to centralize command execution logging in `pc-feature`.
- Instrumented Allowed Tests execution with structured `tests` step logs.
- Instrumented CI gate execution with structured `ci` step logs.
- Added focused unit test verifying step-level structured log writes.
- Marked F-09 `dev-tasks.md` status as Done and completed execution report fields.

**Why:**

- F-09 acceptance criteria required logs for CI/tests/precommit/feature runs; tests/ci logging was the remaining gap.

**How:**

- Updated command execution paths in `pc-feature`, then validated with focused unit test suites.

**Trade-offs / Notes:**

- Full `make ci` is currently blocked by a pre-commit permission issue on `.codex/skills/*`, unrelated to this feature logic.

### 2026-02-06 - F-09 log hygiene + per-feature work item IDs

**Feature/Bug:** F-09 Runner library + structured logs (workflow hardening)

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `prompts/reporter.md`
- `tools/templates/prompts/reporter.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `docs/02-features/feature-template/dev-tasks.md`
- `tools/templates/docs/02-features/feature-template/dev-tasks.md`
- `docs/02-features/09-runner-structured-logs/dev-tasks.md`
- `docs/02-features/09-runner-structured-logs/validation-log.md`
- `docs/02-features/09-runner-structured-logs/reporter-log.md`

**What Changed:**

- Work item ID generation now increments per feature (sequence continues across dates).
- Reporter/tester log updates upsert per WI to prevent duplicate entries.
- Reporter prompt clarifies global log timing and avoids contradictory statements.
- Templates/docs updated to reflect the per-feature WI sequence.
- Reconciled F-09 execution/validation/reporter logs and reran Allowed Tests.

**Why:**

- Fix current log inconsistencies and prevent repeat issues.

**How:**

- Updated `pc-feature` logic, added a unit test, and refreshed prompts/templates.

**Trade-offs / Notes:**

- Global logs remain deferred until feature completion per DEC-016.

### 2026-02-05 - Sync ticket execution protocol template/doc

**Feature/Bug:** Docs maintenance (template-sync pre-commit fix)

**Changed Files:**

- `docs/04-process/ticket-execution-protocol.md`

**Summary:**

- Removed a duplicated bullet line so `docs/04-process/ticket-execution-protocol.md` matches its template.

### 2026-02-05 - Context/PRD/process updates for observability and workflow hardening

**Feature/Bug:** Documentation updates (P0/P1/P2 backlog additions)

**Changed Files:**

- `docs/00-context/*`
- `docs/01-product/prd.md`
- `docs/04-process/*`
- `docs/02-features/09-runner-structured-logs/*`
- `docs/02-features/10-unified-autofix-precommit/*`
- `docs/02-features/11-simplify-worktree-tracking/*`
- `docs/02-features/12-incremental-prd-to-features/*`
- `docs/02-features/13-role-prompts-plan-reviewer/*`
- `docs/02-features/14-learning-loop-improvement-proposals/*`
- `docs/02-features/15-offload-audit-and-log-compaction/*`
- `docs/02-features/16-feature-gating-and-skill-mining/*`
- `prompts/*`
- `docs/possible-improvements.md`
- `.codex/skills/prd-to-features/SKILL.md`
- `tools/templates/docs/04-process/*`
- `tools/templates/root/AGENTS.md`

**What Changed:**

- Added observability, runner, precommit, plan review, and learning-loop requirements to context/process docs.
- Added role-specific prompts and possible-improvements log.
- Created backlog feature folders for P0/P1/P2 improvements.

**Why:**

- Make the documentation the source of truth for the requested workflow improvements.

**How:**

- Updated context/PRD/process docs and generated new feature skeletons from templates.

**Trade-offs / Notes:**

- Tooling changes are captured as backlog features and not implemented yet.

### 2026-02-05 - F-08 anti-cheat testing strategy docs/tooling enforcement

**Feature/Bug:** F-08 Anti-cheat testing strategy

**Changed Files:**

- `docs/04-process/testing-strategy.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/testing-strategy.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `tools/pc-feature`
- `tools/pc-allowed-tests-check`
- `tools/pc-ticket`
- `docs/02-features/08-anti-cheat-testing-strategy/dev-tasks.md`

**What Changed:**

- Documented anti-hardcode requirements, workflow enforcement rules, and log sync rules in process docs and templates.
- Hardened pc-feature Allowed Tests handling with smoke-only guardrails and process-doc logging placeholders.
- Restored a deprecated `pc-ticket` stub with an anti-hardcode reminder for bootstrap compatibility.

**Why:**

- Ensure anti-cheat testing requirements are explicit and enforced in the CLI workflow.

**How:**

- Updated process docs/templates and added lightweight tooling checks for Allowed Tests.

**Trade-offs / Notes:**

- Placeholder smoke tests require follow-up to set a real smoke command.

### 2026-02-05 - Add smoke test normalization and auto-log placeholders for process docs

**Feature/Bug:** Process/Tooling - pc-feature workflow resilience

**Changed Files:**

- `tools/pc-feature`

**What Changed:**

- Treated `make ci` as forbidden in Allowed Tests and auto-inserted a smoke placeholder when missing.
- Added a pre-patch smoke run that records results without aborting.
- Detected process doc changes and auto-appended placeholder global log entries after gates if missing.
- Updated reporter prompt to avoid failing solely on missing global logs when auto-appending is queued.

**Why:**

- Prevent loop exhaustion from missing logs or heavy test commands in Allowed Tests.

**How:**

- Added process-doc diff detection and post-gate fallback logging; moved Allowed Tests fixes earlier.

**Trade-offs / Notes:**

- Placeholder smoke commands require follow-up to set real smoke tests.

### 2026-02-05 - Restore pc-ticket stub and align execution protocol log sync wording

**Feature/Bug:** Process/Tooling - docs + bootstrap

**Changed Files:**

- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `tools/pc-ticket`

**What Changed:**

- Added the missing log sync/offload strings to the execution protocol doc and its template.
- Restored a stub `tools/pc-ticket` so bootstrap tests can copy the tool.

**Why:**

- Keep doc expectations aligned with test assertions and ensure bootstrap tooling includes required files.

**How:**

- Inserted the exact required sentences and added a deprecation stub script.

**Trade-offs / Notes:**

- `pc-ticket` remains deprecated; the stub exits with guidance.

### 2026-02-05 - Move Allowed Tests fixes to Planner and validate test existence

**Feature/Bug:** Process/Tooling - pc-feature Allowed Tests

**Changed Files:**

- `tools/pc-feature`
- `tools/pc-allowed-tests-check`

**What Changed:**

- Allowed Tests auto-fix now runs only in the Planner step and is committed there.
- Added a pre-Tester reset for dirty `dev-tasks.md`.
- Added a small script to verify that Allowed Tests reference existing test targets.

**Why:**

- Prevent tester scope failures caused by mid-run dev-tasks edits and missing tests.

**How:**

- Introduced a helper script that validates unittest/pytest targets and integrated it into Planner validation.

**Trade-offs / Notes:**

- Unknown command formats are treated as unverified and may still pass validation.

### 2026-02-05 - Prevent global log edits during patch/test steps

**Feature/Bug:** Process/Tooling - pc-feature global log guard

**Changed Files:**

- `tools/pc-feature`

**What Changed:**

- Updated the patcher prompt to forbid editing `docs/03-logs`.
- Auto-reset global logs to HEAD after patcher/tester steps to avoid pre-gate violations.

**Why:**

- Stop runs from failing when patch/test steps accidentally touch global logs before gates pass.

**How:**

- Added a global log reset helper and wired it into patcher/tester flows.

**Trade-offs / Notes:**

- Global log edits during these steps are discarded to keep the workflow moving.

### 2026-02-05 - Harden pc-feature worktree hygiene and global log enforcement

**Feature/Bug:** Process/Tooling - pc-feature worktree hygiene

**Changed Files:**

- `tools/pc-feature`

**What Changed:**

- Auto-recreate dirty worktrees instead of prompting.
- Added preflight cleanup for global logs and enforced them as read-only until gates pass.
- Added post-role cleanliness checkpoints that recreate the worktree if it is dirty after role commits.

**Why:**

- Prevent role-scope failures caused by leftover worktree dirt from interrupted runs.

**How:**

- Introduced global log tracking/cleanup helpers and a clean-worktree checkpoint utility.
- Updated role-scope enforcement to block global log edits before gates.

**Trade-offs / Notes:**

- Recreate-on-dirty assumes role commits already captured intended changes.

### 2026-02-05 - Sync ticket-execution-protocol template to living guidance

**Feature/Bug:** Process/Tooling - template sync

**Changed Files:**

- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Updated the template to match the living protocol on Allowed Tests ownership, feedback loop logging, docs sync guidance, and commit prerequisites.

**Why:**

- Keep the template aligned with the current process guidance in `docs/04-process/ticket-execution-protocol.md`.

**How:**

- Applied targeted text replacements to the template file.

**Trade-offs / Notes:**

- None.

### 2026-02-05 - Move global log writes to post-completion reporter summary

**Feature/Bug:** Process/Tooling - pc-feature global log timing

**Changed Files:**

- `tools/pc-feature`
- `docs/04-process/ticket-execution-protocol.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/decision-log.md`

**What Changed:**

- Global logs (decision/implementation/validation) are now written only after gates pass using reporter-provided summaries.
- dev-tasks execution log is treated as planner-owned in the workflow docs.

**Why:**

- Avoid premature global logging and keep role outputs scoped to feature logs until completion.

**How:**

- Added a post-gate reporter summary step to feed global log lines and updated the protocol guidance.

**Trade-offs / Notes:**

- Global logs now contain single-line summaries generated by the reporter at completion.

### 2026-02-05 - Keep dev-tasks planner-only and move tester/reporter output to role logs

**Feature/Bug:** Process/Tooling - pc-feature role log boundaries

**Changed Files:**

- `tools/pc-feature`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/decision-log.md`

**What Changed:**

- Removed tester/reporter writes to `dev-tasks.md`, disallowed patcher edits to `dev-tasks.md`, and relied on role logs for tester/reporter output.

**Why:**

- Prevent role-scope violations and keep `dev-tasks.md` as planner-owned task source of truth.

**How:**

- Updated role scope rules to allow `dev-tasks.md` only for the planner and removed dev-tasks updates from tester/reporter paths.

**Trade-offs / Notes:**

- Test results and reporter feedback are recorded in role logs only; `dev-tasks.md` no longer mirrors those sections.

### 2026-02-05 - Harden pc-feature allowed tests parsing

**Feature/Bug:** Process/Tooling - pc-feature allowed tests validation

**Changed Files:**

- `tools/pc-feature`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/bug-log.md`

**What Changed:**

- Added normalization and validation for Allowed Tests entries to ignore narrative text, strip wrapper prefixes, and only accept runnable commands.

**Why:**

- Prevent `pp` from attempting to execute non-command text (e.g., “Totally ...”) when an LLM returns prose in the Allowed Tests section.

**How:**

- Filter Allowed Tests lines through `normalize_allowed_test`, which rejects backticks and non-command starters and strips `tools/offload-proxy/pp` when present.

**Trade-offs / Notes:**

- Commands that don’t resolve to a known executable or standard prefix are ignored and treated as missing tests.

### 2026-02-05 - Fix pc-feature prompt string escaping for lint

**Feature/Bug:** Process/Tooling - pc-feature lint reliability

**Changed Files:**

- `tools/pc-feature`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Removed the stray escape sequence in the worktree prompt f-string so ruff/black can parse the file.

**Status:** Completed

**Testing:**

- `tools/offload-proxy/pp ruff check tools/pc-feature` (PASS)
- `tools/offload-proxy/pp black --check tools/pc-feature` (PASS)

**Author:** Codex

### 2026-02-05 - Remove unused patch_text variable in pc-feature

**Feature/Bug:** Process/Tooling - pc-feature lint cleanup

**Changed Files:**

- `tools/pc-feature`
- `docs/03-logs/implementation-log.md`

**What Changed:**

- Removed the unused `patch_text` assignment while preserving the `codex_exec` call.

**Why:**

- Resolve ruff `F841` unused variable failure in pre-commit.

**How:**

- Dropped the assignment and executed `codex_exec(...)` directly.

**Status:** Completed

**Testing:**

- `ruff check tools/pc-feature` (PASS)

**Author:** Codex

### 2026-02-05 - Reset worktrees that are ahead of main

**Feature/Bug:** Process/Tooling - pc-feature worktree hygiene

**Changed Files:**

- `tools/pc-feature`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Added a guard to delete/recreate worktrees that are clean but still ahead of `main`.

**Status:** Completed

**Testing:**

- Not run (no test command specified)

**Author:** Codex

### 2026-02-05 - Harden preflight JSON parsing for pc-feature

**Feature/Bug:** Process/Tooling - pc-feature preflight

**Changed Files:**

- `tools/pc-feature`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Tightened the preflight prompt to require JSON-only output.
- Added JSON payload extraction to strip non-JSON prefixes/suffixes before parsing.

**Status:** Completed

**Testing:**

- Not run (no test command specified)

**Author:** Codex

### 2026-02-05 - Add allowed test allowlist and forbid recursive feature runs

**Feature/Bug:** Process/Tooling - pc-feature test execution

**Changed Files:**

- `tools/pc-feature`
- `docs/02-features/feature-template/dev-tasks.md`
- `docs/02-features/08-anti-cheat-testing-strategy/dev-tasks.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/02-features/feature-template/dev-tasks.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Added an Allowed Tests section to dev-tasks and enforced it in `pc-feature`.
- Blocked recursive `make feature`/`pc-feature` tests and required Planner/Patcher to specify scoped tests.
- Ran role-scoped testing only from allowlisted commands.

**Status:** Completed

**Testing:**

- Not run (no test command specified)

**Author:** Codex

### 2026-02-05 - Harden pc-feature role isolation and worktree hygiene

**Feature/Bug:** Process/Tooling - pc-feature role enforcement

**Changed Files:**

- `tools/pc-feature`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Added patcher guardrails, role-log reset, and role-scoped formatting to prevent cross-role edits.
- Added dirty worktree detection with user-approved auto-recreate behavior.
- Added resume cleanup to discard dirty role log files before execution.

**Status:** Completed

**Testing:**

- Not run (no test command specified)

**Author:** Codex

### 2026-02-05 - Disable Serena dashboard auto-open for this repo

**Feature/Bug:** Process/Tooling - Serena configuration

**Changed Files:**

- `.serena/project.yml`

**What Changed:**

- Set `web_dashboard_open_on_launch: false` in the repo's Serena project config to prevent auto-opening the dashboard.

**Status:** Completed

**Testing:**

- Not run (config-only change)

**Author:** Codex

### 2026-02-05 - Create feature 08 and close feature 07

**Feature/Bug:** Process/Tooling - feature docs maintenance

**Changed Files:**

- `docs/02-features/08-anti-cheat-testing-strategy/feature-spec.md`
- `docs/02-features/08-anti-cheat-testing-strategy/tech-design.md`
- `docs/02-features/08-anti-cheat-testing-strategy/dev-tasks.md`
- `docs/02-features/08-anti-cheat-testing-strategy/test-plan.md`
- `docs/02-features/07-anti-cheat-testing-strategy/feature-spec.md`
- `docs/02-features/07-anti-cheat-testing-strategy/tech-design.md`
- `docs/02-features/07-anti-cheat-testing-strategy/dev-tasks.md`
- `docs/02-features/07-anti-cheat-testing-strategy/test-plan.md`
- `docs/03-logs/implementation-log.md`

**What Changed:**

- Added feature 08 docs mirroring feature 07 goals with a fresh, empty execution log.
- Marked feature 07 as superseded and completed for archival clarity.

**Status:** Completed

**Testing:**

- Not run (docs-only change)

**Author:** Codex

### 2026-02-04 - Prevent role-scope failures in shared worktree runs

**Feature/Bug:** Process/Tooling - pc-feature role log handling

**Changed Files:**

- `tools/pc-feature`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/bug-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Deferred creating role log files in the patcher worktree until the role actually writes to them, avoiding out-of-scope enforcement errors on resume.

**Status:** Completed

**Testing:**

- Not run (no test command specified)

**Author:** Codex

### 2026-02-04 - Align ticket execution protocol template

**Feature/Bug:** Process/Tooling - template sync follow-up

**Changed Files:**

- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Synced the template copy of the ticket execution protocol to match the living doc so template-sync passes in pre-commit.

**Status:** Completed

**Testing:**

- `tools/offload-proxy/pp tools/pc-template-sync` (PASS)

**Author:** Codex

### 2026-02-04 - Sync ticket execution protocol template

**Feature/Bug:** Process/Tooling - template sync

**Changed Files:**

- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `docs/03-logs/implementation-log.md`

**What Changed:**

- Aligned the template workflow bullets with the current living `ticket-execution-protocol.md`, including the role scope and worktree tracking notes.

**Status:** Completed

**Testing:**

- Not run (docs-only change)

**Author:** Codex

### 2026-02-04 - Codex exec uses repo-local CODEX_HOME and profiles

**Feature/Bug:** Process/Tooling - codex exec configuration

**Changed Files:**

- `tools/pc-autofix`
- `tools/pc-template-sync`
- `tools/pc-feature`
- `.codex.toml`
- `tools/templates/root/.codex.toml`
- `tools/README.md`
- `.gitignore`
- `tools/templates/root/.gitignore`
- `docs/02-features/07-anti-cheat-testing-strategy/dev-tasks.md`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Set `CODEX_HOME` to the repo-local `.codex` directory for script-driven Codex exec.
- Invoked Codex with project `-C` and role profile selection (Default by default).
- Routed `pc-feature` sub-agent runs to the Planner/Patcher/Tester/Reporter profiles.
- Tuned the Planner profile for higher reasoning and added AI-oriented tooling notes.
- Updated Codex session storage to `.codex_subagent` and copied auth.json when missing.
- Added warnings for missing auth.json and stripped OPENAI_API_KEY from scripted Codex runs.
- Resolved ambiguous `main` ref by preferring `refs/heads/main` when creating worktrees.
- Fixed Python typing syntax in hook scripts for older Python runtimes.
- Ignored temporary `.tmp/`, `.offload/`, and `.codex_subagent/` paths in role scope checks.
- Staged only filtered change paths to avoid git add failures from `.tmp/` worktrees.
- Bypassed git hooks for role commits and surfaced commit stderr to avoid hidden pre-commit failures.
- Added `.codex_subagent/config.toml` (repo + template), tightened `.gitignore`, and passed explicit Codex overrides including Serena MCP.
- Added profiles and Serena MCP defaults to the root template `.codex.toml`.

**Status:** Completed

**Testing:**

- Not run (no test command specified)

**Author:** Codex

### 2026-02-04 - Sync templates to match the living docs

**Feature/Bug:** Process/Tooling - template-sync maintenance

**Changed Files:**

- `tools/templates/docs/README.md`
- `tools/templates/docs/04-process/git-workflow.md`
- `tools/templates/docs/04-process/output-offload.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/dev-workflow.md`
- `tools/templates/docs/04-process/testing-strategy.md`
- `tools/templates/docs/04-process/definition-of-done.md`
- `docs/03-logs/implementation-log.md`

**What Changed:**

- Replaced the templates for the listed docs with the current living versions so the template-sync pre-commit gate no longer reports out-of-sync pairs.

**Status:** Completed

**Testing:**

- Not run (docs-only change)

**Author:** Codex

### 2026-02-04 - Enforce template/living sync in pre-commit

**Feature/Bug:** Process/Tooling - template sync gate

**Changed Files:**

- `tools/pc-feature`
- `tools/pc-template-sync`
- `.pre-commit-config.yaml`
- `tools/templates/root/.pre-commit-config.yaml`
- `docs/02-features/07-anti-cheat-testing-strategy/dev-tasks.md`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Normalized `pc-feature` branch detection to accept `heads/main`.
- Added a pre-commit hook that diffs templates vs living files and runs Codex autofix when exactly one side changed.
- Synced the pre-commit hook definition in the template root config.

**Status:** Completed

**Testing:**

- Not run (no test command specified)

**Author:** Codex

### 2026-02-04 - Worktree policy enforcement and collector automation

**Feature/Bug:** Process/Tooling - worktree role scope + collector

**Changed Files:**

- `tools/pc-feature`
- `docs/02-features/AGENTS.md`
- `docs/02-features/feature-template/dev-tasks.md`
- `docs/02-features/feature-template/planner-log.md`
- `docs/02-features/feature-template/reporter-log.md`
- `docs/02-features/feature-template/validation-log.md`
- `docs/02-features/06-worktree-policy-naming-convention/dev-tasks.md`
- `docs/02-features/06-worktree-policy-naming-convention/planner-log.md`
- `docs/02-features/06-worktree-policy-naming-convention/reporter-log.md`
- `docs/02-features/06-worktree-policy-naming-convention/validation-log.md`
- `docs/02-features/07-anti-cheat-testing-strategy/dev-tasks.md`
- `docs/02-features/07-anti-cheat-testing-strategy/planner-log.md`
- `docs/02-features/07-anti-cheat-testing-strategy/reporter-log.md`
- `docs/02-features/07-anti-cheat-testing-strategy/validation-log.md`
- `docs/04-process/dev-workflow.md`
- `docs/04-process/git-workflow.md`
- `docs/04-process/human-orchestration-workflow.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/02-features/AGENTS.md`
- `tools/templates/docs/02-features/feature-template/dev-tasks.md`
- `tools/templates/docs/02-features/feature-template/planner-log.md`
- `tools/templates/docs/02-features/feature-template/reporter-log.md`
- `tools/templates/docs/02-features/feature-template/validation-log.md`
- `tools/templates/docs/04-process/dev-workflow.md`
- `tools/templates/docs/04-process/git-workflow.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `tools/templates/root/AGENTS.md`

**What Changed:**

- Added role-scoped log templates and updated docs to reference them.
- Updated `pc-feature` to create role branches/worktrees, enforce file scopes, write a worktree manifest, auto-collect role changes into `main`, and clean up worktrees.

**Status:** Completed

**Testing:**

- `tools/offload-proxy/pp make ci` (FAIL: end-of-file-fixer PermissionError on `.codex/skills/readme-sync/SKILL.md`)

**Author:** Codex

### 2026-02-04 - Fix pc-feature work item header parsing

**Feature/Bug:** Tooling - pc-feature work item id parsing

**Changed Files:**

- `tools/pc-feature`

**What Changed:**

- Filtered execution log headers to only accept concrete `WI-YYYYMMDD-XX` ids, ignoring the template placeholder so `make feature` no longer fails on a fresh `dev-tasks.md`.

**Status:** Completed

**Testing:**

- Not run (user reported failure; no test command defined)

**Author:** Codex

### 2026-02-04 - Process update - dev-tasks execution loop

**Feature/Bug:** Process - dev-tasks execution source of truth

**Changed Files:**

- `docs/02-features/AGENTS.md`
- `docs/02-features/feature-template/dev-tasks.md`
- `docs/04-process/dev-workflow.md`
- `docs/04-process/human-orchestration-workflow.md`
- `docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/definition-of-done.md`
- `docs/00-context/system-map.md`
- `docs/03-logs/decision-log.md`

**What Changed:**

- Documented dev-tasks as the execution source of truth with role ownership and an execution log.
- Updated workflow docs to use Planner/Patcher/Tester/Reporter loop and optional ticket wrappers.
- Refreshed context and DoD language to reflect work-item execution terminology.

**Status:** Completed

**Testing:**

- Not run (docs-only changes)

**Author:** Alexandre Pezzotta

### 2026-02-04 - Process update - split oversized features before execution

**Feature/Bug:** Process - feature sizing for uniform execution

**Changed Files:**

- `docs/04-process/dev-workflow.md`
- `docs/04-process/human-orchestration-workflow.md`
- `docs/03-logs/decision-log.md`

**What Changed:**

- Defined that oversized work is split into smaller features before execution to keep the workflow uniform.

**Status:** Completed

**Testing:**

- Not run (docs-only changes)

**Author:** Alexandre Pezzotta

### 2026-02-04 - Process update - remove ticket wrappers

**Feature/Bug:** Process - dev-tasks-only execution

**Changed Files:**

- `docs/02-features/AGENTS.md`
- `docs/02-features/feature-template/dev-tasks.md`
- `docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/human-orchestration-workflow.md`
- `docs/00-context/system-map.md`
- `docs/03-logs/decision-log.md`

**What Changed:**

- Removed ticket-wrapper references and documented dev-tasks-only execution with `make feature`.

**Status:** Completed

**Testing:**

- Not run (docs-only changes)

**Author:** Alexandre Pezzotta

### 2026-02-04 - Process update - remove feature-tasks-to-tickets skill

**Feature/Bug:** Process - dev-tasks-only workflow cleanup

**Changed Files:**

- `.codex/skills/feature-tasks-to-tickets/` (removed)
- `tools/templates/docs/02-features/AGENTS.md`
- `tools/templates/docs/02-features/feature-template/dev-tasks.md`
- `tools/templates/docs/04-process/dev-workflow.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/definition-of-done.md`
- `tools/templates/docs/AGENTS.md`
- `tools/templates/docs/04-process/AGENTS.md`
- `tools/templates/docs/04-process/llm-prompts.md`
- `tools/templates/docs/04-process/ci-autofix-prompt.md`
- `tools/templates/docs/04-process/ticket-template.md`

**What Changed:**

- Removed the deprecated skill and aligned templates with the dev-tasks-only workflow.

**Status:** Completed

**Testing:**

- Not run (docs-only changes)

**Author:** Alexandre Pezzotta

### 2026-02-04 - Tooling update - pc-feature orchestration + remove ticket tooling

**Feature/Bug:** Process - work item execution tooling

**Changed Files:**

- `tools/pc-feature`
- `Makefile`
- `tools/templates/root/Makefile`
- `tools/README.md`
- `tools/pc-ticket` (removed)
- `tools/ticket-bootstrap` (removed)
- `tests/test_pc_feature.py`
- `tests/test_pc_ticket.py` (removed)
- `tests/test_bootstrap_into.py`
- `tests/test_docs_logs.py`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/validation-log.md`
- `docs/02-features/feature-template/dev-tasks.md`
- `tools/templates/docs/02-features/feature-template/dev-tasks.md`

**What Changed:**

- Replaced the pc-feature ticket wrapper with a dev-tasks execution-log orchestrator and removed ticket tooling.
- Updated Make targets and tests to match the work-item execution flow.

**Status:** Completed

**Testing:**

- Not run (tooling + docs updates)

**Author:** Alexandre Pezzotta

### 2026-02-04 - Tooling update - pc-feature scoped workflow implementation

**Feature/Bug:** Process - work item execution tooling

**Changed Files:**

- `tools/pc-feature`
- `Makefile`
- `tools/templates/root/Makefile`
- `tests/test_pc_feature.py`
- `tests/test_pc_ticket.py` (removed)
- `tests/test_bootstrap_into.py`
- `tests/test_docs_logs.py`
- `docs/02-features/feature-template/dev-tasks.md`
- `tools/templates/docs/02-features/feature-template/dev-tasks.md`
- `docs/04-process/AGENTS.md`
- `tools/templates/docs/04-process/AGENTS.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Implemented the scoped work-item orchestration loop in `pc-feature` (plan/patch/test/report, make ci, autofix, commit message only) and aligned tests/docs/templates to the updated workflow.

**Status:** Completed

**Testing:**

- Not run (tooling + docs updates)

**Author:** Alexandre Pezzotta

### 2026-02-04 - Docs update - add execution log to remaining features

**Feature/Bug:** Process - dev-tasks execution readiness

**Changed Files:**

- `docs/02-features/06-worktree-policy-naming-convention/dev-tasks.md`
- `docs/02-features/07-anti-cheat-testing-strategy/dev-tasks.md`

**What Changed:**

- Added Ownership/Execution Log sections so `pc-feature` can run on features 06 and 07.

**Status:** Completed

**Testing:**

- Not run (docs-only changes)

**Author:** Alexandre Pezzotta

### 2026-02-04 - Fix lint failure in pc-feature execution log tooling

**Feature/Bug:** Tooling - lint compliance

**Changed Files:**

- `tools/pc-feature`

**What Changed:**

- Removed the unused `lines` assignment in `entry_outcome()` so the script passes `ruff`'s F841 check without altering behavior.

**Status:** Completed

**Testing:**

- Not run (lint-only change)

**Author:** Alexandre Pezzotta

### 2026-02-04 - Tooling update - shared patcher worktree for review roles

**Feature/Bug:** Tooling - pc-feature orchestration

**Changed Files:**

- `tools/pc-feature`
- `docs/04-process/ticket-execution-protocol.md`
- `tests/test_docs_logs.py`

**What Changed:**

- Ran Planner/Tester/Reporter on the patcher worktree so review roles see shared content while keeping role-scoped log enforcement.
- Documented the shared worktree behavior in the execution protocol and added a doc regression test.

**Status:** Blocked (gates failed)

**Testing:**

- `tools/offload-proxy/pp make feature F=07` (FAIL: codex exec network/model refresh errors and Serena MCP startup failure)
- `tools/offload-proxy/pp make ci` (FAIL: end-of-file-fixer PermissionError on `.codex/skills/readme-sync/SKILL.md`)

**Author:** Codex

### 2026-02-04 - Ticket 401 - Add or update tests

**Feature/Bug:** P1 - Orchestrator + sub-agent roles

**Changed Files:**

- `tests/test_orchestrator_role_gates.py`

**What Changed:**

- Added regression coverage that asserts each workflow gate test in the orchestrator/sub-agent test plan includes the artifact, gate, and audit language required for the primary CLI path.

**Status:** Tests passing

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p test_orchestrator_role_gates.py` (PASS)

**Author:** Alexandre Pezzotta

### 2026-02-03 - Ticket 401 - Add or update tests

**Feature/Bug:** P0 - Output offload enforcement

**What Changed:**

- Added doc regression tests (`tests/test_output_offload_enforcement_docs.py`) so TC-D002/TC-D003 demand mention of offload artifacts and gating phrases.
- Logged the ticket progress across the worklog, implementation log, and validation log while baselining the final `make ci` pass.

**Status:** Completed

**Author:** pc-ticket

### 2026-02-03 - Ticket 102 - Implement or update tooling/scripts

**Feature/Bug:** P0 - Output offload enforcement

**What Changed:**

- Docs/logs updates initiated via `pc-ticket` automation.

**Status:** In progress

**Author:** pc-ticket

### 2026-02-03 - Ticket 102 - Implement or update tooling/scripts (tests-first doc regression)

**Feature/Bug:** P1 - Orchestrator + sub-agent roles

**Changed Files:**

- `tests/test_orchestrator_workflow_docs.py`

**What Changed:**

- Added regression coverage that asserts TC-WF001, TC-WF002, and TC-WF003 are documented in the orchestrator/sub-agent test plan so the new tooling enforcement tests block until the workflow gate descriptions are present.

**Status:** Tests passing

**Testing:**

- `python -m unittest tests/test_orchestrator_workflow_docs.py` (FAIL: module not found unless using discovery)
- `python -m unittest discover -s tests -p test_orchestrator_workflow_docs.py` (PASS)

**Author:** Alexandre Pezzotta

### 2026-02-03 - Ticket 102 - Expand offload proxy regression coverage

**Feature/Bug:** P0 - Output offload enforcement

**Changed Files:**

- `tests/test_offload_proxy.py`

**What Changed:**

- Added regression tests that assert `tools/offload-proxy/pp` offloads large outputs, surfaces the pointer id string, and atomically records the stored artifact under `.offload/`.
- Covered the `always_offload` configuration path so even short commands emit pointer ids, enabling downstream gates to reference the recorded output.

**Status:** Tests passing

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p test_offload_proxy.py` (PASS)

**Author:** Alexandre Pezzotta

### 2026-02-03 - Ticket 101 - Define workflow behavior

**Feature/Bug:** P0 - Output offload enforcement

**What Changed:**

- Docs/logs updates initiated via `pc-ticket` automation.

**Status:** In progress

**Author:** pc-ticket

### 2026-02-03 - Ticket 101 - Define workflow behavior (tests-first docs gating)

**Feature/Bug:** P0 - Output offload enforcement

**Changed Files:**

- `tests/test_output_offload_enforcement_docs.py`

**What Changed:**

- Added a regression suite that asserts the feature docs describe the required workflow steps, approval gates, and noisy-command outputs (offload ids/references) for the output offload enforcement workflow.
- Executed the new tests so the docs updates stay blocked until they can satisfy the gating expectations.

**Status:** Tests failing (expected)

**Testing:**

- `python -m unittest discover -s tests -p test_output_offload_enforcement_docs.py` (FAIL: docs still lack the workflow/gate/offload phrases that the tests now require)

**Author:** Alexandre Pezzotta

### 2026-02-03 - Ticket 101 - Document gating definitions for output offload enforcement

**Feature/Bug:** P0 - Output offload enforcement

**Changed Files:**

- `docs/02-features/04-output-offload-enforcement/feature-spec.md`
- `docs/02-features/04-output-offload-enforcement/tech-design.md`
- `docs/02-features/04-output-offload-enforcement/test-plan.md`
- `docs/02-features/04-output-offload-enforcement/dev-tasks.md`
- `docs/03-logs/tickets/04-101--define-workflow-behavior.md`

**What Changed:**

- Documented the required workflow steps, approval gate, and noisy command handling gate artifacts so the doc regression tests can find their phrases.
- Captured the current dev-task status and worklog notes to show this doc work is underway.

**Status:** Done

**Testing:**

- `tools/offload-proxy/pp make test` (PASS)

**Author:** Alexandre Pezzotta

### 2026-02-03 - Ticket 101 - Define workflow behavior (orchestrator/sub-agent roles)

**Feature/Bug:** P1 - Orchestrator + sub-agent roles

**Changed Files:**

- `docs/02-features/05-orchestrator-sub-agent-roles/feature-spec.md`
- `docs/02-features/05-orchestrator-sub-agent-roles/tech-design.md`
- `docs/02-features/05-orchestrator-sub-agent-roles/dev-tasks.md`
- `docs/02-features/05-orchestrator-sub-agent-roles/test-plan.md`
- `docs/03-logs/tickets/05-101--define-workflow-behavior.md`

**What Changed:**

- Embedded the orchestrator/sub-agent responsibilities summary and the orchestrator Plan gate description in the feature spec so the workflow doc tests can find the required phrases.
- Enumerated the gate outputs per role in the technical design and noted the gate handoffs.
- Updated the dev-task metadata (status, last updated, change log) and noted the gating test plan entries to reflect the tests-first docs requirement.

**Status:** Tests passing

**Testing:**

- `python -m unittest discover -s tests -p test_orchestrator_workflow_docs.py` (PASS)
- `make ci` (PASS)

**Author:** Alexandre Pezzotta

### 2026-02-03 - Automate ticket log entry creation for pc-ticket

**Feature/Bug:** Ticket execution automation

**Changed Files:**

- `tools/pc-ticket`
- `tests/test_update_reapply_templates_docs.py`
- `docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/ticket-template.md`

**What Changed:**

- `pc-ticket` now auto-adds a stub implementation log entry with the ticket ID and PRD feature name.
- The regression test now checks for the ticket ID and feature name instead of a brittle hardcoded phrase.
- Process docs clarify that log entries are automation-generated and must use a stable ticket/feature format.

**Why:**

- Remove manual steps from ticket execution and prevent blocked runs caused by missing literal phrases.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (doc + tooling change only).

**Author:** Alexandre Pezzotta

### 2026-02-03 - Record documentation/test-plan alignment for CLI gating docs

**Feature/Bug:** Update/reapply templates workflow docs

**Changed Files:**

- `docs/02-features/03-update-reapply-templates/test-plan.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/tickets/03-501--update-docs-logs.md`

**What Changed:**

- Added the TC-D001 documentation test case so the CLI gating workflow's docs/logs are explicitly verified before any further changes land.
- Added the plain `tc-d001: docs/logs accurately describe the cli gating workflow` text to the documentation tests section so the regression detection can find the exact phrase.
- Noted the doc/log alignment work in both the implementation log and the ticket worklog to keep the audit trail complete.

**Why:**

- The failing regression now requires every doc/update log change to mention the gating workflow; documenting it prevents the regression from resurfacing after future edits.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp make test` (PASS)

**Author:** Alexandre Pezzotta

### 2026-02-03 - add docs/log regression tests before doc updates

**Feature/Bug:** Update/reapply templates workflow docs

**Changed Files:**

- `tests/test_update_reapply_templates_docs.py`
- `docs/03-logs/tickets/03-501--update-docs-logs.md`

**What Changed:**

- Added two failing regressions that pin the ticket test plan to a new `TC-D001` doc/log validation case and require the implementation log to mention `docs/logs updates for ticket 501`.
- Captured the TDD plan in the ticket worklog so the upcoming doc changes are gated by these tests before any implementation work starts.

**Why:**

- The ticket explicitly demands tests-first coverage for docs/log updates; recording these expectations in tests and the worklog locks down the upcoming doc work and keeps the reasoning transparent.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- `python -m unittest tests/test_update_reapply_templates_docs.py` (FAIL: ModuleNotFoundError because `tests` is not a package)
- `python -m unittest discover -s tests -p test_update_reapply_templates_docs.py` (FAIL: assertions target `tc-d001` doc-case and the `docs/logs updates for ticket 501` phrase that are not yet added)

**Author:** Alexandre Pezzotta

### 2026-02-03 - Normalize scope fields in pc-ticket preflight

**Feature/Bug:** Ticket preflight workflow

**Changed Files:**

- `tools/pc-ticket`

**What Changed:**

- Added `normalize_scope` to coerce `scope_in`/`scope_out` values into strings, joining list responses from the Codex preflight JSON before gating.

**Why:**

- Codex sometimes returns scope fields as arrays; handling lists prevents `AttributeError` when `.strip()` is called and keeps scope validation consistent.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (manual change only).

**Author:** Alexandre Pezzotta

### 2026-02-03 - Gate-focused reapply tests land before CLI updates

**Feature/Bug:** Update/reapply templates CLI tooling

**Changed Files:**

- `tests/test_bootstrap_into.py`

**What Changed:**

- Added a TDD-first regression that exercises a reapply run with a locally modified file and asserts that the CLI prints the preflight validation gate, template diff review gate, and conflict summary output whenever it prompts for overwrite/merge/skip choices.

**Why:**

- The ticket requires writing tests before altering the CLI behavior; capturing the desired gate phrases as failing assertions ensures the future implementation reuses these expectations to keep reapply workflow outputs predictable and safe.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p test_bootstrap_into.py` (FAIL: the gating phrases are not yet emitted)

**Author:** Alexandre Pezzotta

### 2026-02-03 - Capture reapply exit/log expectations with tests

**Feature/Bug:** Update/reapply templates CLI tooling

**Changed Files:**

- `tests/test_bootstrap_into.py`

**What Changed:**

- Renamed the reapply gate regression to `test_update_reapply_primary_flow_reports_gates` and added `test_update_reapply_exit_code_and_log_outputs` so the tests now assert the CLI emits the documented gate/conflict phrases, exits cleanly, and keeps bootstrap markers intact when the user skips reapply updates.

**Why:**

- The ticket's test plan calls for regression coverage that proves the CLI outputs, exit codes, and logs behave as expected before any production changes land, so these tests capture that barrier.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p test_bootstrap_into.py` (PASS)

**Author:** Alexandre Pezzotta

### 2026-02-03 - Report pre-commit install failures without aborting bootstrap

**Feature/Bug:** Update/reapply templates CLI tooling

**Changed Files:**

- `tools/bootstrap-into`

**What Changed:**

- Wrapped the `pre-commit install` invocation in a check that only prints a warning when the install fails so `bootstrap-into` can finish even if hook installation returns a non-zero status.

**Why:**

- The failing test surfaced that a stubbed `pre-commit` command (returning 2) caused bootstrap to exit early, so continuing gracefully while warning maintains the documented CLI workflow.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp make test` (PASS)

**Author:** Alexandre Pezzotta

### 2026-02-03 - Print gates during reapply prompts

**Feature/Bug:** Update/reapply templates CLI tooling

**Changed Files:**

- `tools/bootstrap-into`

**What Changed:**

- Emit the preflight validation gate, template diff review gate, and conflict summary output any time a syncable file already exists before prompting for overwrite/merge/skip, matching the regression expectations.

**Why:**

- The new regression in `tests/test_bootstrap_into.py` asserts the CLI prints the gate phrases during reapply runs so the workflow outputs stay predictable and surface every checkpoint before user decisions.

**Impact:**

- **Breaking changes:** No
- **Performance:** Slightly more verbose, gated to local edits only
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp make test` (PASS)

**Author:** Alexandre Pezzotta

### 2026-02-03 - Add docs workflow regression tests before doc updates

**Feature/Bug:** Update/reapply templates workflow docs

**Changed Files:**

- `tests/test_update_reapply_templates_docs.py`

**What Changed:**

- Added TDD-first regression tests that assert the feature-spec and tech-design docs mention the workflow behavior steps, gates, and outputs so the future documentation work is guided by failing tests rather than direct edits.

**Why:**

- The ticket explicitly required writing tests before touching production docs; encoding the behavior requirements as failing tests keeps the upcoming doc updates scoped and verifiable.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p test_update_reapply_templates_docs.py` (FAIL: key phrases are not yet present in the docs)

**Author:** Alexandre Pezzotta

### 2026-02-03 - Remove inline frontmatter comments from ticket templates

**Feature/Bug:** Ticket tooling templates

**Changed Files:**

- `docs/04-process/ticket-template.md`
- `tools/templates/docs/04-process/ticket-template.md`
- `.codex/skills/feature-tasks-to-tickets/SKILL.md`

**What Changed:**

- Removed inline comments from `status` and `complexity` frontmatter fields and moved guidance into HTML comments below the frontmatter block.
- Documented the “no inline comments in frontmatter values” rule in the feature-tasks-to-tickets skill.

**Why:**

- Inline comments in frontmatter values break `ticket-bootstrap` parsing, causing `make ticket` failures.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (template/skill docs change).

### 2026-02-03 - Auto-restage lint fixes during pc-commit checks

**Feature/Bug:** Commit tooling

**Changed Files:**

- `tools/pc-commit`

**What Changed:**

- When `make check` fails, `pc-commit` now detects whether the only unstaged files are already in the staged set, auto-restages those linted files, and re-runs `make lint` then `make test`.
- If any unstaged file is not already staged (or there are untracked files), the commit still fails with a clear error.

**Why:**

- Ticket work is required to start from a clean worktree, so post-lint unstaged changes should only be auto-fix updates to already-staged files. This prevents false failures while preserving safety.

**Impact:**

- **Breaking changes:** No
- **Performance:** Slightly more work only when lint auto-fixes are applied.
- **Dependencies:** None

**Testing:**

- Not run (workflow script change).

### 2026-02-03 - Guard pre-commit stash pop to avoid staging unrelated changes

**Feature/Bug:** Pre-commit automation

**Changed Files:**

- `tools/pc-precommit`

**What Changed:**

- Only stash when unstaged or untracked changes exist, and only pop the stash if a new stash entry was actually created.

**Why:**

- Prevent the hook from popping a previously existing user stash (or restoring unrelated changes) when there were no unstaged changes to preserve.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (hook script change only).

### 2026-02-03 - Record Execute work item workflow gating summary

**Feature/Bug:** Ticket execution workflow

**Changed Files:**

- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`
- `docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Documented the Execute work item workflow gating summary and its required log sync language so the implementation log mirrors the protocol instructions.

**Why:**

- Keep the log/reporting guardrails aligned with the Execute work item workflow and capture the gating narrative alongside the protocol update.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change).

### 2026-02-03 - Capture Prettier-driven ticket T-102 log update

**Feature/Bug:** Ticket execution workflow

**Changed Files:**

- `docs/03-logs/tickets/102--implement-or-update-tooling-scripts.md`

**What Changed:**

- Documented the Prettier-driven rewrite of T-102's preflight section so the scope, non-goals, doc/test checklist, and systematic-review notes align with the Execute Ticket Workflow expectations for feature F-02.
- Explained that the adjustment merely captures formatting changes generated by the hook once CI was rerun.

**Why:**

- Because the Prettier hook modified the ticket worklog, this entry preserves the reasoning and details behind that alteration and the subsequent rerun of `make ci`.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- `make ci`

**Author:** Alexandre Pezzotta

### 2026-02-03 - Lock systematic-review logging in pc-ticket tests

**Feature/Bug:** Ticket execution workflow

**Changed Files:**

- `tests/test_pc_ticket.py`

**What Changed:**

- Added `test_systematic_review_logs_commands` to ensure the `Systematic review` line emitted by `build_preflight_block` preserves the joined review items, keeping the canonical command summary before production code changes.

**Why:**

- Guarding this line keeps the instruction “log the commands you ran” from regressing as tooling updates are applied, aligning with the Execute Ticket Workflow requirement to record the systematic review.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- `python -m unittest tests/test_pc_ticket.py` _(fails: ModuleNotFoundError because `tests` is not a package)_
- `python -m unittest discover -s tests`
- `tools/offload-proxy/pp make ci`

**Author:** Alexandre Pezzotta

### 2026-02-03 - Auto-update ticket status on completion

**Feature/Bug:** Ticket execution workflow

**Changed Files:**

- `tools/pc-ticket`
- `docs/04-process/ticket-template.md`

**What Changed:**

- Added automatic status updates (with `status_timestamp`) when ticket execution completes, ensuring `make ticket` can detect completed tickets.

### 2026-02-03 - Fix pc-commit on macOS bash 3.2

**Feature/Bug:** Commit tooling

**Changed Files:**

- `tools/pc-commit`

**What Changed:**

- Replaced `mapfile` usage with a fallback read loop when `mapfile` is unavailable, so `pc-commit` works on macOS default Bash.

### 2026-02-03 - Avoid skipping commit when worklog is out of sync

**Feature/Bug:** Ticket execution workflow

**Changed Files:**

- `tools/pc-ticket`

**What Changed:**

- Only skip the commit step when the recorded commit message is found in git history, preventing false “commit already recorded” skips after failed commits.

### 2026-02-03 - Normalize malformed worklog headers before section checks

**Feature/Bug:** Ticket execution workflow

**Changed Files:**

- `tools/pc-ticket`

**What Changed:**

- Added a normalization pass that fixes bullet-prefixed worklog headers (for example `-##`) before parsing sections, preventing false “missing section” errors.

### 2026-02-03 - Add feature-level wrapper for ticket generation + execution

**Feature/Bug:** Ticket execution workflow

**Changed Files:**

- `tools/pc-feature`
- `Makefile`
- `tools/templates/root/Makefile`

**What Changed:**

- Added `pc-feature` to generate tickets from `dev-tasks.md` for a feature id and run `make ticket` across them in order.
- Added a `make feature F=<id>` target to invoke the wrapper with optional manual mode passthrough.

### 2026-02-03 - Auto-complete ticket docs before commit

**Feature/Bug:** Ticket execution workflow

**Changed Files:**

- `tools/pc-ticket`
- `docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/definition-of-done.md`
- `docs/00-context/expected-features.md`

**What Changed:**

- The commit step now auto-updates ticket DoD checkboxes, Tests Run, and Report (Final) to ensure tickets are complete before committing.
- Process and context docs now state that commits are gated on completed ticket documentation.

### 2026-02-03 - Feature-prefixed worklog filenames

**Feature/Bug:** Ticket execution workflow

**Changed Files:**

- `tools/ticket-bootstrap`
- `tools/pc-ticket`

**What Changed:**

- Worklog filenames now include the feature id (e.g., `02-401--slug.md`) to avoid cross-feature collisions when task ids repeat.

### 2026-02-03 - Auto-restage after lint in pc-commit

**Feature/Bug:** Commit tooling

**Changed Files:**

- `tools/pc-commit`

**What Changed:**

- After running `make check`, `pc-commit` now re-stages changes so linted files are included in the commit automatically.

### 2026-02-03 - Skip pc-ticket when ticket is already Done

**Feature/Bug:** Ticket execution workflow

**Changed Files:**

- `tools/pc-ticket`

**What Changed:**

- If the ticket status is already `Done`, `pc-ticket` now exits cleanly instead of trying to open a missing worklog.

### 2026-02-03 - Require F when ticket ids collide

**Feature/Bug:** Ticket execution workflow

**Changed Files:**

- `tools/ticket-bootstrap`

**What Changed:**

- When multiple tickets share the same id, `ticket-bootstrap` now errors unless `F=<feature-id>` is provided, avoiding accidental selection of the wrong feature.

### 2026-02-03 - Add ticket-bootstrap feature resolution debug line

**Feature/Bug:** Ticket execution workflow

**Changed Files:**

- `tools/ticket-bootstrap`

**What Changed:**

- `ticket-bootstrap` now prints the resolved `feature_id` and `search_root` to help diagnose feature selection issues.

### 2026-02-03 - Fix feature folder resolution for ticket-bootstrap

**Feature/Bug:** Ticket execution workflow

**Changed Files:**

- `tools/ticket-bootstrap`

**What Changed:**

- Trimmed `feature_id` input and switched to a shell glob match to reliably resolve `docs/02-features/<id>-*` on macOS, ensuring `F=02` selects the correct feature folder.

### 2026-02-03 - Auto-resume for in-progress tickets

**Feature/Bug:** Ticket execution workflow

**Changed Files:**

- `tools/pc-ticket`
- `docs/04-process/ticket-execution-protocol.md`
- `docs/00-context/expected-features.md`

**What Changed:**

- Added auto-resume behavior when a ticket worklog already exists, skipping completed sections while always re-running tests/CI and avoiding re-commits.
- Documented the resume rules in the ticket execution protocol and captured the expectation in the context feature list.

### 2026-02-03 - Shore up bootstrap regression coverage for root templates and logs

**Feature/Bug:** Bootstrap tooling

**Changed Files:**

- `tests/test_bootstrap_into.py`

**What Changed:**

- Added `test_bootstrap_into_copies_root_templates_and_skills` to assert the bootstrap CLI copies `AGENTS.md`, `pp.yml`, and `.codex/skills/context-to-product/SKILL.md`, keeps their canonical signatures, and appends a single bootstrap marker before the CLI output lists each file.
- Added `test_bootstrap_into_logs_marker_output_consistently` to confirm each log document retains a single bootstrap marker and the `Updated:` output mentions each log exactly once, ensuring the gate/log story stays stable without touching production code.

**Why:**

- These regression checks lock down the primary bootstrap path (templates + logs) before additional feature work goes in.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests`

**Author:** Alexandre Pezzotta

### 2026-02-02 - Fix report status reference in ticket tooling

**Feature/Bug:** Ticket execution tooling

**Changed Files:**

- `tools/pc-ticket`

**Notes:**

- Swapped the undefined `tdd_status` reference in the final report with the already-calculated `post_test_status` so that the final summary (and any automated log parsing) shows the actual test run result instead of blowing up at runtime.

**Testing:**

- `ruff check tools/pc-ticket`

### 2026-02-02 - Extend bootstrap regression coverage to root templates

**Feature/Bug:** Bootstrap tooling

**Changed Files:**

- `tests/test_bootstrap_into.py`

**What Changed:**

- Added `test_bootstrap_into_copies_root_templates_and_skills` to confirm AGENTS/Makefile/pp.yml plus `.codex/skills/context-to-product/SKILL.md` are copied into the target repo with the expected bootstrap markers.

**Why:**

- Guarding the bootstrap CLI’s core asset copy ensures the feature keeps aligning with the documented gate and artefact expectations before it ships.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- `python -m unittest discover -s tests`
- `make ci`

**Author:** Alexandre Pezzotta

### 2026-02-02 - Locked down bootstrap log coverage with regression tests

**Feature/Bug:** docs/02-features/01-bootstrap-templates-into-a-repo/feature-spec.md

**Changed Files:**

- `tests/test_bootstrap_into.py`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Added log-centric regression tests that confirm the CLI copies both log docs, inserts a single bootstrap marker per file, reports each log only once, and keeps marker counts stable after verbose reruns.
- Captured the gate/log rationale here so the regression dependencies remain traceable for future release work.

**Why:**

- Verifying the primary bootstrap flow preserves log assets and output reduces the risk of regressing the gate story before shipping the feature.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- `python -m unittest discover -s tests`
- `make ci`

**Notes:**

- The new coverage keeps log markers unique and ensures verbose reruns describe skips without duplicating updates.

**Author:** Alexandre Pezzotta

### 2026-02-02 - Add complexity flag and orchestrated feedback steps

**Feature/Bug:** Ticket tooling/docs

**Changed Files:**

- `docs/04-process/ticket-template.md`
- `tools/templates/docs/04-process/ticket-template.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-101.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-102.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-501.md`
- `docs/03-logs/tickets/worklog-template.md`
- `tools/templates/docs/03-logs/tickets/worklog-template.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `.codex/skills/feature-tasks-to-tickets/SKILL.md`
- `tools/pc-ticket`
- `tools/pc-ticket.md`

**Notes:**

- Added `complexity` frontmatter and documented complex-ticket orchestration steps.
- Complex tickets now capture tester/reviewer feedback in the worklog.
- Updated ticket generation guidance to default complexity to simple.

### 2026-02-02 - Quiet pc-ticket noise and avoid shell syntax traps

**Feature/Bug:** Ticket execution tooling

**Changed Files:**

- `Makefile`
- `tests/test_pc_ticket.py`

**What Changed:**

- Reworked the `ticket-check` pipeline to stage ticket files through a temporary buffer instead of process substitution so bash no longer hits the syntax error on constrained shells; the rule now runs two straightforward `find` calls (one per pattern) and relies on a runtime-generated `mktemp` path so parentheses and variable expansion stay shell-safe.
- Captured `stderr` inside the invalid-ticket test so the expected error message is no longer emitted during `python -m unittest discover -s tests`.

**Why:**

- Keep CI output clean (the invalid-ticket test no longer prints to stderr and `ticket-check` now avoids process substitution/shell quoting issues).

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- `python -m unittest discover -s tests`
- `make ci`

**Author:** Codex

### 2026-02-02 - Harden bootstrap prompts and ticket id normalization

**Feature/Bug:** Bootstrap tooling scripts

**Changed Files:**

- `tools/bootstrap-into`
- `tools/pc-ticket`

**Notes:**

- Enforced git repository requirement and conflict prompts that respect original stdin during copy loops.
- Normalized ticket ids to accept numeric/T-/TASK- formats while keeping numeric ids for bootstrap/worklog lookup.

### 2026-02-02 - Add dedicated CI/test autofix prompt file

**Feature/Bug:** Ticket tooling/docs

**Changed Files:**

- `docs/04-process/ci-autofix-prompt.md`
- `tools/templates/docs/04-process/ci-autofix-prompt.md`
- `tools/pc-ticket-config.json`
- `tools/pc-ticket`
- `tools/pc-ticket.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/llm-prompts.md`
- `tools/templates/docs/04-process/llm-prompts.md`

**Notes:**

- Moved CI/test autofix prompt to a dedicated template file and wired config defaults to it.

### 2026-02-03 - Normalize bootstrap skip prompt input

**Feature/Bug:** Bootstrap template tests

**Changed Files:**

- `tests/test_bootstrap_into.py`

**What Changed:**

- The skip prompt regression was triggered because the helper passed the literal `s\\n` string, so the CLI never matched the `s` branch and ended up overwriting `docs/README.md`.
- Added the `SKIP_PROMPT_RESPONSE` constant (set to `"s\n"`) and rewired the skip test to use it after writing `local readme\n`, making the newline-delimited response explicit and ensuring the assertion still checks the newline-terminated contents.

**Testing:**

- `tools/offload-proxy/pp make test`

### 2026-02-03 - Confirm formatting passes CI after autop fix

**Feature/Bug:** Bootstrap test formatting

**Changed Files:**

- `tests/test_bootstrap_into.py`

**What Changed:**

- Black and Prettier rewrote the new bootstrap regression test to satisfy the formatting gates that triggered `make ci` failure; no logic changes were introduced.

**Why:**

- The prior CI run failed because formatting rules were violated. Letting the linters reformat the file keeps the ticket scope narrow and allows the next `make ci` run to pass without further interventions.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp make ci`

**Notes:**

- Output captured with `tools/offload-proxy/pp make ci` so the CI log stays concise.

**Author:** Codex

### 2026-02-02 - Add CI/test autofix loops to ticket execution

**Feature/Bug:** Ticket tooling/docs

**Changed Files:**

- `tools/pc-ticket`
- `tools/pc-ticket-config.json`
- `docs/03-logs/tickets/worklog-template.md`
- `tools/templates/docs/03-logs/tickets/worklog-template.md`
- `docs/04-process/llm-prompts.md`
- `tools/templates/docs/04-process/llm-prompts.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `tools/pc-ticket.md`

**Notes:**

- Added optional CI/test autofix loops with configurable attempts and prompt template.
- Added an Autofix Attempts worklog section and final report note for resolved failures.
- Added scope-ambiguity and autofix-exhaustion checkpoints for human input.

### 2026-02-02 - Make ticket execution autonomous by default

**Feature/Bug:** Ticket tooling/docs

**Changed Files:**

- `Makefile`
- `tools/templates/root/Makefile`
- `tools/ticket-bootstrap`
- `tools/pc-ticket`
- `tools/pc-ticket.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `docs/AGENTS.md`
- `tools/templates/docs/AGENTS.md`
- `tools/templates/root/AGENTS.md`
- `docs/04-process/AGENTS.md`
- `tools/templates/docs/04-process/AGENTS.md`

**Notes:**

- `make ticket` now bootstraps and runs `tools/pc-ticket` autonomously by default.
- Added manual mode (`MANUAL=1` / `--manual`) to stop after Preflight and avoid autonomous TDD/implementation.
- Updated protocol and AGENTS docs to reflect the new entrypoint behavior.
- Added an auto output mode to `tools/ticket-bootstrap` to avoid manual-only guidance in autonomous runs.

### 2026-02-02 - Standardize ticket id format to numeric

**Feature/Bug:** Ticket tooling/docs

**Changed Files:**

- `docs/04-process/ticket-template.md`
- `tools/templates/docs/04-process/ticket-template.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-101.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-102.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-501.md`
- `tools/pc-ticket`
- `tools/pc-ticket.md`
- `tools/ticket-bootstrap`

**Notes:**

- Switched ticket frontmatter ids to numeric-only and updated the template.
- Enforced numeric-only ids in ticket tooling and usage docs.

### 2026-02-02 - Remove unsupported pre-commit flag

**Feature/Bug:** Pre-commit automation

**Changed Files:**

- `tools/pc-precommit`

**Notes:**

- Dropped `--no-stash` from `pre-commit run` to support older pre-commit versions.
- Stash handling remains in `tools/pc-precommit` to preserve unstaged changes.

### 2026-02-02 - Add AI-assisted pre-commit fix loop

**Feature/Bug:** Pre-commit automation

**Changed Files:**

- `tools/pc-precommit`
- `tools/pc-autofix`
- `.githooks/pre-commit`
- `tools/templates/root/.githooks/pre-commit`

**Notes:**

- Run pre-commit up to two times to allow linters to auto-fix and re-stage.
- If still failing, invoke Codex to fix reported issues and re-run checks.
- Preserve unstaged changes by stashing with keep-index, then restore after checks.
- Attempt AI recovery on stash pop conflicts, but stop the hook if conflicts remain.
- Avoid `mapfile` for macOS bash compatibility when reading staged paths.

### 2026-02-02 - Clean up lint issues in SolidLSP overrides

**Feature/Bug:** Linting cleanup

**Changed Files:**

- `tools/serena/solidlsp_override/solidlsp/ls_utils.py`
- `tools/serena/solidlsp_override/solidlsp/language_servers/clangd_language_server.py`
- `tools/serena/solidlsp_override/solidlsp/language_servers/eclipse_jdtls.py`
- `tools/serena/solidlsp_override/solidlsp/language_servers/jedi_server.py`
- `tools/serena/solidlsp_override/solidlsp/language_servers/pyright_server.py`
- `tools/serena/solidlsp_override/solidlsp/language_servers/rust_analyzer.py`
- `tools/serena/solidlsp_override/solidlsp/language_servers/taplo_server.py`
- `tools/serena/solidlsp_override/solidlsp/language_servers/typescript_language_server.py`

**What Changed:**
Replaced explicit `== True` checks with truthy checks, clarified ambiguous variable
names, and moved Taplo imports above constants to satisfy flake8 rules.

**Why:**
Remove lint violations without altering runtime behavior.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (lint-only changes)

**Author:** Codex

### 2026-02-02 - Add role feedback loop sections to tickets and workflows

**Feature/Bug:** Process and ticket templates

**Changed Files:**

- `docs/04-process/ticket-template.md`
- `tools/templates/docs/04-process/ticket-template.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/dev-workflow.md`
- `tools/templates/docs/04-process/dev-workflow.md`
- `docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `docs/04-process/definition-of-done.md`
- `tools/templates/docs/04-process/definition-of-done.md`
- `docs/00-context/context-boundaries-operating-model.md`
- `tools/templates/docs/00-context/context-boundaries-operating-model.md`
- `.codex/skills/feature-tasks-to-tickets/SKILL.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-101.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-102.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-501.md`

**What Changed:**
Added implementer/tester/reviewer feedback sections and iteration logging to the
ticket template and workflows, and enriched task tickets with references and
acceptance criteria extracted from `dev-tasks.md`.

**Why:**
Make task tickets self-contained for sub-agents and enforce iteration on
tester/reviewer feedback.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change)

**Author:** Alexandre Pezzotta

### 2026-02-02 - Auto-fill expected changes in task tickets

**Feature/Bug:** Ticket generation quality

**Changed Files:**

- `.codex/skills/feature-tasks-to-tickets/SKILL.md` - Auto-fill Implementation Notes from task bullets
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-101.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-102.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-501.md`

**What Changed:**
Implementation Notes now include expected changes derived from `dev-tasks.md`
bullets, avoiding manual reconstruction by the implementer.

**Why:**
Keep task tickets more actionable and reduce context switching for sub-agents.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change)

**Author:** Alexandre Pezzotta

### 2026-02-02 - Add feature status audit and backfill task statuses

**Feature/Bug:** Workflow automation

**Changed Files:**

- `.codex/skills/feature-status-audit/SKILL.md` - New skill to audit task ticket status
- `docs/04-process/human-orchestration-workflow.md` - Add audit step to PO loop
- `tools/templates/docs/04-process/human-orchestration-workflow.md` - Add audit step to template
- `docs/00-context/system-map.md` - Add skill entry point
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-101.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-102.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-501.md`

**What Changed:**
Added a deterministic feature status audit skill and ran it on feature 01 to
backfill task statuses.

**Why:**
Keep `make ticket` idempotent and avoid redoing already completed work.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change)

**Author:** Alexandre Pezzotta

### 2026-02-02 - Add idempotent ticket guard and audit tool

**Feature/Bug:** Ticket workflow

**Changed Files:**

- `tools/ticket-bootstrap` - Skip worklog creation when ticket status is Done
- `tools/feature-status-audit` - Deterministic task status audit tool
- `.codex/skills/feature-status-audit/SKILL.md` - Document audit usage
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-101.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-102.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-501.md`

**What Changed:**
Added a guard to prevent worklog creation for Done tickets and introduced a
feature status audit tool that updates task statuses based on deterministic
rules and documented evidence heuristics.

**Why:**
Make `make ticket` idempotent and avoid bootstrapping worklogs for completed tasks.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change)

**Author:** Alexandre Pezzotta

### 2026-02-02 - Add evidence hints and status reasons for audits

**Feature/Bug:** Ticket status auditing

**Changed Files:**

- `docs/04-process/ticket-template.md`
- `tools/templates/docs/04-process/ticket-template.md`
- `.codex/skills/feature-status-audit/SKILL.md`
- `.codex/skills/feature-tasks-to-tickets/SKILL.md`
- `tools/feature-status-audit`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-101.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-102.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-501.md`

**What Changed:**
Added `status_reason` and Evidence Hints to tickets, and updated the audit tool
to set status based on evidence, then mark DoD items when Done.

**Why:**
Make status reconciliation deterministic and traceable without manual judgment.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change)

**Author:** Alexandre Pezzotta

### 2026-02-02 - Enrich task tickets with dev-task details

**Feature/Bug:** Ticket generation quality

**Changed Files:**

- `.codex/skills/feature-tasks-to-tickets/SKILL.md` - Add acceptance/estimate and references
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-101.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-102.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-501.md`

**What Changed:**
Ticket generation now pulls acceptance criteria, estimates, and task bullets from
`dev-tasks.md`, adds references, and replaces the generic header.

**Why:**
Sub-agents need task-level guidance without re-reading other docs.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change)

**Author:** Alexandre Pezzotta

### 2026-02-02 - Replace batch tickets with per-task tickets (current feature)

**Feature/Bug:** Ticket generation

**Changed Files:**

- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-101.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-102.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md`
- `docs/02-features/01-bootstrap-templates-into-a-repo/TASK-501.md`

**What Changed:**
Removed batch-generated `TASK-001.md` placeholders and created task-level
tickets for the current feature based on `dev-tasks.md`.

**Why:**
Align tickets with planned tasks and avoid empty, feature-only placeholders.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change)

**Author:** Alexandre Pezzotta

### 2026-02-02 - Rename and refocus ticket generation skill

**Feature/Bug:** Workflow automation

**Changed Files:**

- `.codex/skills/feature-tasks-to-tickets/SKILL.md` - Generate task-level tickets for current feature
- `docs/04-process/human-orchestration-workflow.md` - Reference per-task ticket generation
- `tools/templates/docs/04-process/human-orchestration-workflow.md` - Reference per-task ticket generation
- `docs/00-context/system-map.md` - Update skill entry point name

**What Changed:**
Renamed the ticket generation skill to `feature-tasks-to-tickets` and updated
the workflow docs to generate tickets per task for the current feature.

**Why:**
Avoid re-running ticket generation for each feature and make kickoff a one-time
task per feature scope.

**Impact:**

- **Breaking changes:** Yes, skill name changed
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change)

**Author:** Alexandre Pezzotta

### 2026-02-02 - Generate feature folders from PRD

**Feature/Bug:** Feature documentation

**Changed Files:**

- `docs/02-features/01-bootstrap-templates-into-a-repo/*`
- `docs/02-features/02-execute-ticket-workflow/*`
- `docs/02-features/03-update-reapply-templates/*`
- `docs/02-features/04-output-offload-enforcement/*`
- `docs/02-features/05-orchestrator-sub-agent-roles/*`
- `docs/02-features/06-worktree-policy-naming-convention/*`
- `docs/02-features/07-anti-cheat-testing-strategy/*`

**What Changed:**
Created feature folders and populated feature-spec, tech-design, dev-tasks, and
test-plan files for all P0/P1 items in the PRD, including process features.

**Why:**
Translate the PRD into actionable feature documentation for execution.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change)

**Author:** Alexandre Pezzotta

### 2026-02-02 - Add expected-features context and PRD process sections

**Feature/Bug:** Context and PRD templates

**Changed Files:**

- `docs/00-context/expected-features.md` - New context file for explicit expected features
- `tools/templates/docs/00-context/expected-features.md` - Template for new file
- `docs/00-context/AGENTS.md` - Reference expected-features file
- `tools/templates/docs/00-context/AGENTS.md` - Reference expected-features file
- `docs/README.md` - Include expected-features in context list
- `tools/templates/docs/README.md` - Include expected-features in context list
- `.codex/skills/context-to-product/SKILL.md` - Map expected features and workflow requirements into PRD
- `tools/templates/docs/01-product/prd.md` - Add Process Features and Workflow/Process Requirements sections
- `docs/01-product/prd.md` - Add process features and workflow/process requirements

**What Changed:**
Added a dedicated context file for explicit expected features, updated templates,
and extended PRD structure to include process features and workflow requirements.

**Why:**
Ensure the PRD generation reflects explicit expected features and the workflow
standards discussed, including worktrees and delegated roles.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change)

**Author:** Alexandre Pezzotta

### 2026-02-02 - Update PRD with process requirements

**Feature/Bug:** Product documentation

**Changed Files:**

- `docs/01-product/prd.md` - Map context + process requirements into PRD

**What Changed:**
Updated the PRD to include Plan → Patch → Test → Report, explicit ticket DoD,
output offload requirements, and process-driven success metrics.

**Why:**
Ensure downstream feature generation captures the workflow guardrails and
operational standards defined in `docs/04-process/`.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change)

**Author:** Alexandre Pezzotta

### 2026-02-02 - Update context-to-product skill to include process docs

**Feature/Bug:** Skill update

**Changed Files:**

- `.codex/skills/context-to-product/SKILL.md` - Add `docs/04-process/*` inputs and PRD mapping steps

**What Changed:**
Expanded the skill to read workflow/process docs and map those requirements into
the PRD, ensuring operational standards are captured as product requirements.

**Why:**
The PRD needs to reflect workflow guardrails and process standards to avoid
missing required features or constraints in downstream feature generation.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change)

**Author:** Alexandre Pezzotta

### 2026-02-02 - Codex-first workflow documentation updates

**Feature/Bug:** Process and context docs

**Changed Files:**

- `AGENTS.md` - Add plan/patch/test/report, offload rule, worktree naming, orchestration roles
- `docs/AGENTS.md` - Align operational rules with new workflow
- `docs/00-context/vision.md` - Capture workflow intent and token hygiene goals
- `docs/00-context/system-map.md` - Record workflow execution pattern and output offload
- `docs/00-context/context-boundaries-operating-model.md` - Add plan/patch/test/report and worktree usage
- `docs/04-process/dev-workflow.md` - Enforce plan/patch/test/report and orchestration roles
- `docs/04-process/definition-of-done.md` - Add global requirements and explicit DoD
- `docs/04-process/git-workflow.md` - Add worktree policy and naming convention
- `docs/04-process/output-offload.md` - Standardize `.offload/` and retrieval guidance
- `docs/04-process/testing-strategy.md` - Expand anti-hardcode requirements
- `docs/04-process/ticket-execution-protocol.md` - Add plan/patch/test/report and reporting
- `docs/04-process/ticket-template.md` - Add ticket-specific DoD and report section

**What Changed:**
Codified a Codex-first workflow with explicit gates, parallel role orchestration,
worktree naming, output offload requirements, and anti-hardcode testing rules.

**Why:**
Reduce context mistakes and token waste, improve repeatability, and scale
parallel roles without contaminating workspaces.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change)

**Author:** Alexandre Pezzotta

### 2026-02-01 - Clarify AI-as-developer and minimal-tooling stance

**Feature/Bug:** Context update

**Changed Files:**

- `docs/00-context/vision.md` - Emphasize minimal tooling and AI autonomy
- `docs/00-context/context-boundaries-operating-model.md` - Add minimal tooling and token-efficiency guardrails

**What Changed:**
Updated context to state that PezzosCode bootstraps a minimal, essential toolset
so AI can operate as a developer with low manual overhead and low token usage.

**Why:**
Align project intent with current tooling decisions (hooks, scripts, and small
dependencies that reduce manual steps and tokens).

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-02-01 - Install pre-commit hooks during bootstrap

**Feature/Bug:** Tooling and workflow

**Changed Files:**

- `tools/bootstrap-into` - Add pre-commit hook install after bootstrap

**What Changed:**
Bootstrap now installs pre-commit hooks (pre-commit and pre-push) when the
target repo is a git repository and `pre-commit` is available.

**Why:**
Ensure linting and test hooks are active immediately after bootstrap.

**Impact:**

- **Breaking changes:** No
- **Performance:** Minimal; only runs once during bootstrap
- **Dependencies:** `pre-commit` is required to auto-install hooks

**Testing:**

- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-02-01 - Add pre-commit linting and editorconfig templates

**Feature/Bug:** Tooling and workflow

**Changed Files:**

- `.editorconfig` - New root editorconfig with language sections
- `.pre-commit-config.yaml` - New pre-commit hook set for linting and tests
- `.githooks/pre-commit` - Run pre-commit stage hooks
- `.githooks/pre-push` - Run pre-push stage hooks (tests)
- `Makefile` - Use pre-commit for lint and formatting
- `.codex/skills/sync-root-from-context/SKILL.md` - Include new root files and hook guidance
- `tools/templates/root/.editorconfig` - Template editorconfig
- `tools/templates/root/.pre-commit-config.yaml` - Template pre-commit config
- `tools/templates/root/.githooks/pre-commit` - Template pre-commit hook
- `tools/templates/root/.githooks/pre-push` - Template pre-push hook
- `tools/templates/root/Makefile` - Use pre-commit for lint and formatting

**What Changed:**
Added editorconfig and pre-commit configuration to both the live repo and
template root, shifted linting to pre-commit, and moved tests to pre-push.

**Why:**
Standardize linting across languages before commit, while keeping tests gated
on push to reduce commit latency.

**Impact:**

- **Breaking changes:** No
- **Performance:** Pre-commit now runs lint/format; tests run on pre-push
- **Dependencies:** `pre-commit` and optional language tools (black, ruff, etc.)

**Testing:**

- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-02-01 - Align README sync with context/log sources

**Feature/Bug:** Documentation maintenance

**Changed Files:**

- `.codex/skills/readme-sync/SKILL.md` - Require context/log reconciliation and exclude PRD as a source
- `README.md` - Update core context list and keep PRD as a separate step
- `docs/README.md` - Soften source-of-truth phrasing to avoid unsupported claims
- `tools/README.md` - Align tool list with context/system map
- `tools/serena/solidlsp_override/README.md` - Remove unsupported snapshot/patch details
- `tools/serena/solidlsp_override/solidlsp/language_servers/elixir_tools/README.md` - Reduce to minimal pointer

**What Changed:**
Updated the README sync rules to reconcile statements against `docs/00-context/*`
and `docs/03-logs/*`, then tightened README content to match those sources.

**Why:**
README content should reflect current, authoritative context and logs rather
than inferred or PRD-only details.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Sync README files

**Feature/Bug:** Documentation maintenance

**Changed Files:**

- `README.md` - Shorten root readme and point to canonical docs
- `docs/README.md` - Condense to AI-focused structure and remove duplication
- `tools/README.md` - Standardize structure and reduce repetition
- `tools/serena/solidlsp_override/README.md` - Clarify override purpose and refresh steps
- `tools/serena/solidlsp_override/solidlsp/language_servers/elixir_tools/README.md` - Compress integration notes

**What Changed:**
Rewrote README files to follow a consistent structure, reduce overlap, and keep
the root README human-focused while keeping the rest AI-friendly.

**Why:**
The README sync workflow requires concise, non-duplicative docs that point to
canonical sources.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Fix readme-sync skill frontmatter

**Feature/Bug:** Skill validation

**Changed Files:**

- `.codex/skills/readme-sync/SKILL.md` - Remove extra frontmatter lines to match skills-check expectations

**What Changed:**
Adjusted the skill header to the required 4-line frontmatter format so `make test` passes.

**Why:**
The skills check enforces a strict frontmatter layout for SKILL.md files.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Add pp write avoidance note

**Feature/Bug:** Process guardrail

**Changed Files:**

- `AGENTS.md` - Clarify pp is for large-output reads, not filesystem writes
- `.codex/skills/readme-sync/SKILL.md` - Add pp usage note for write operations

**What Changed:**
Added a brief note to avoid using `tools/offload-proxy/pp` for write commands to reduce unnecessary escalation prompts.

**Why:**
`pp` is intended for large output reads; using it for write commands can trigger avoidable permissions flow.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Add README sync skill

**Feature/Bug:** Skill addition

**Changed Files:**

- `.codex/skills/readme-sync/SKILL.md` - New skill to update README files with minimal duplication

**What Changed:**
Added a skill that scans non-template README files, applies a standardized structure, and reduces duplication with concise summaries.

**Why:**
Keep README content current and minimal for both humans (root) and AI (all others).

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Sync root template guardrails to live config

**Feature/Bug:** Template parity

**Changed Files:**

- `tools/templates/root/Makefile` - Add Python unit tests to `make test`, make `check` a real gate
- `tools/templates/root/.githooks/pre-commit` - Run `make test` directly
- `tools/templates/root/.codex.toml` - Add approval policy guardrail note
- `tools/templates/root/.serena/project.yml` - Add unique-list note and include Python

**What Changed:**
Aligned root templates with the current live root files and guardrail comments to keep future bootstraps consistent.

**Why:**
Templates should mirror the working repo so new projects inherit the correct checks and safety notes.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Sync skill guardrails for approval policy and language list

**Feature/Bug:** Skill behavior guardrails

**Changed Files:**

- `.codex/skills/sync-root-from-context/SKILL.md` - Preserve approval policy unless explicitly requested; enforce unique language list.
- `.codex.toml` - Add note to keep approval policy unchanged unless requested.
- `.serena/project.yml` - Add note to keep language list unique.

**What Changed:**
Updated the sync skill and root-file comments to prevent unintended approval policy changes and duplicate language entries on future runs.

**Why:**
The sync behavior should preserve AI-first defaults and avoid accidental config drift.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Sync live root tooling with current project context

**Feature/Bug:** Internal tooling sync

**Changed Files:**

- `Makefile` - Run Python unit tests as part of `make test`, make `check` a real gate
- `.githooks/pre-commit` - Use `make test` for a single source of truth
- `.serena/project.yml` - Include TOML and bash in language servers (no duplicates)
- `tools/bootstrap-into` - Add preflight command checks and `--dry-run`
- `tools/ticket-bootstrap` - Add preflight command checks and `--dry-run`

**What Changed:**
Aligned the live root files with the current repo context by ensuring tests run consistently and Serena indexes the repo’s actual file types. Added preflight validations to bootstrap scripts and a `--dry-run` mode to show planned actions without writing. Kept Codex approval policy at "never" after feedback and removed duplicate language entries.

**Why:**
The repo is a tooling/template bootstrap. Root files should reflect the actual workflows and file types used here, and safety defaults should be aligned with the documented process.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (not requested)

**Author:** Alexandre Pezzotta

### 2026-01-31 - Serena LSP workspace/configuration diagnostics and early-load guard

**Feature/Bug:** LSP stability (Taplo/YAML startup errors)

**Changed Files:**

- `tools/serena/solidlsp_override/solidlsp/ls_handler.py` - Added ping watcher, import banner, and richer workspace/configuration logging
- `.codex.toml` - Added `SERENA_LSP_CONFIG_PING_DIR=/tmp` for manual pings

**What Changed:**
Added an opt-in, file-triggered ping mechanism to exercise the `workspace/configuration` handler and send `workspace/didChangeConfiguration`. Added an early import banner (guarded by `SERENA_LSP_IMPORT_BANNER=1`) to prove the override is loaded before any LSP errors print, and included request_id/item count in the request log for correlation.

**Why:**
Taplo intermittently logs `method 'workspace/configuration' not handled on client` before the Serena log file exists. This indicates the error is emitted before `.codex.toml` env overrides are applied, so we needed a way to validate early-load behavior and manually trigger config handling in-session.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same (ping watcher is opt-in, dormant unless env set)
- **Dependencies:** None

**Testing:**

- Manual: `touch /tmp/ping_workspace_configuration.toml` and verified log lines for ping/handler

**Notes:**

- If the same issue occurs for another language, set override env in the shell (e.g., `.zshrc`) so it applies before Codex starts, then use `touch /tmp/ping_workspace_configuration.<language>` to trigger a ping and confirm handler behavior in logs.
- If the error still appears before logs, enable `SERENA_LSP_IMPORT_BANNER=1` to verify whether the override is imported early enough.

**Author:** Alexandre Pezzotta

### 2026-01-31 - Root templates and bootstrap sync updates

**Feature/Bug:** Internal tooling update

**Changed Files:**

- `tools/templates/root/*` - Added top-level templates (root files, .serena, .githooks)
- `tools/bootstrap-into` - Copy root templates and treat them as conditional updates
- `.codex/skills/sync-root-from-context/SKILL.md` - New skill to sync live root files from docs context
- `docs/00-context/system-map.md` - System map updated

**What Changed:**
Created a dedicated root template directory and updated bootstrap logic to copy those templates into target repos with safe, conditional updates. Added a new skill to keep live root files in sync with project context and PRD.

**Why:**
We needed a clean separation between generic bootstrapped root files and this repo’s project-specific root files.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Manual: ran `tools/bootstrap-into --self --verbose`

**Notes:**

- Root templates now live in `tools/templates/root/`.
- Live root files are project-specific and updated via the new skill.

**Author:** Alexandre Pezzotta

### [YYYY-MM-DD] - [Brief Description of Change]

**Feature/Bug:** [Link to feature or bug ticket]

**Changed Files:**

- `path/to/file1.ts`
- `path/to/file2.ts`

**What Changed:**
[Describe the code changes in technical detail]

**Why:**
[Explain the reasoning behind the change]

- Problem we were solving: [description]
- Alternative approaches considered: [list]
- Why this approach: [rationale]

**Impact:**

- **Breaking changes:** [Yes/No - describe if yes]
- **Performance:** [Better/Worse/Same - explain]
- **Dependencies:** [New dependencies added/removed]

**Testing:**

- Tests added: [describe]
- Manual testing done: [describe]

**Notes:**

- [Any gotchas, warnings, or things to watch out for]
- [Technical debt introduced or paid down]
- [Things we'd do differently next time]

**Author:** [Name]

---

### [YYYY-MM-DD] - [Another Change]

**Feature/Bug:** [Link to feature or bug ticket]

**Changed Files:**

- `path/to/file.ts`

**What Changed:**
[Description]

**Why:**
[Reasoning]

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**
[Testing done]

**Notes:**
[Additional context]

**Author:** [Name]

---

## Example Entry

### 2025-01-15 - Implemented caching layer for API responses

**Feature:** [Link to feature-spec.md for performance optimization]

**Changed Files:**

- `src/api/client.ts` - Added caching middleware
- `src/cache/redis-cache.ts` - New Redis cache implementation
- `src/config/cache-config.ts` - Cache configuration
- `package.json` - Added redis dependency

**What Changed:**
Added a caching layer using Redis to cache API responses for GET requests. Implemented:

- Cache middleware that intercepts API calls
- TTL-based cache invalidation (5 minutes default)
- Cache key generation based on endpoint + query params
- Cache bypass option for authenticated requests

**Why:**

- **Problem:** API response times were averaging 800ms, causing poor UX
- **Goal:** Reduce response times to < 200ms for repeated requests
- **Alternatives considered:**
  1. In-memory caching: Rejected because we have multiple server instances
  2. CDN caching: Rejected because data is user-specific
  3. Redis caching: Chosen because it's fast, shared across instances, and we already use Redis for sessions

**Impact:**

- **Breaking changes:** No - caching is transparent to existing code
- **Performance:** Average response time reduced from 800ms to 150ms (81% improvement)
- **Dependencies:** Added `ioredis@5.3.0`
- **Infrastructure:** Requires Redis instance (already available in staging/prod)

**Testing:**

- Added unit tests for cache middleware (test/api/cache-middleware.test.ts)
- Added integration tests for cache invalidation
- Manual testing: verified cache hits/misses in Redis CLI
- Load tested with 100 concurrent users: no issues

**Notes:**

- **Watch out:** Cache invalidation strategy is simple (TTL-based). May need more sophisticated invalidation for real-time data
- **Technical debt:** Currently only caches GET requests. Should extend to POST responses where appropriate
- **Monitoring:** Added cache hit/miss metrics to dashboard
- **Next time:** Consider implementing cache warming on deployment

**Author:** Jane Doe

---

## Implementation Patterns

### Common Patterns Used

Document recurring patterns in your codebase:

#### Pattern: [Pattern Name]

**When to use:** [scenarios]

**Example:**

```typescript
// Code example
```

**Reasoning:** [why we use this pattern]

---

## Technical Debt Log

### Current Tech Debt

Track technical debt as it's introduced:

| Date Added | Location       | Description    | Impact       | Plan to Address      |
| ---------- | -------------- | -------------- | ------------ | -------------------- |
| YYYY-MM-DD | `path/to/file` | [what's wrong] | High/Med/Low | [when/how we'll fix] |

### Resolved Tech Debt

Track when debt is paid down:

| Date Resolved | Original Date | Description      | How Resolved      |
| ------------- | ------------- | ---------------- | ----------------- |
| YYYY-MM-DD    | YYYY-MM-DD    | [what was wrong] | [how we fixed it] |

---

## Change Statistics

### By Month

| Month   | Changes | Files Modified | Authors |
| ------- | ------- | -------------- | ------- |
| 2025-01 | [count] | [count]        | [count] |

### By Category

| Category    | Count | % of Total |
| ----------- | ----- | ---------- |
| Features    | [#]   | [%]        |
| Bug Fixes   | [#]   | [%]        |
| Refactoring | [#]   | [%]        |
| Performance | [#]   | [%]        |
| Security    | [#]   | [%]        |

---

## Related Documents

- [Decision Log](decision-log.md) - Product and architectural decisions
- [Bug Log](bug-log.md) - Bug tracking and fixes
- [Validation Log](validation-log.md) - Post-deployment learnings
- [Insights](insights.md) - Patterns and improvements

### 2026-02-06 - Workflow hardening Step 01 baseline regression harness

**Feature/Bug:** `tools/pc-feature` workflow hardening (manual todo Step 01)

**Changed Files:**

- `tests/test_pc_feature.py`
- `tests/test_pc_allowed_tests_check.py`

**What Changed:**

- Added focused regression tests that encode expected workflow fixes before refactor:
  - resume should pick the newest in-progress work item.
  - Allowed Tests execution should run from worktree cwd.
  - orchestration should not write `feature-worktrees.json`.
  - final staging should avoid blanket `git add -A`.
  - commit generation should be skipped when Commit section is already populated.
- Added `pc-allowed-tests-check` tests for valid `python -m unittest discover ...` commands.

**Why:**

- Lock desired behavior in tests first so follow-up workflow fixes can be implemented safely and verified deterministically.

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"` (fails on targeted regressions)
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_allowed_tests_check.py"` (fails on discover command handling)

### 2026-02-06 - Workflow hardening Step 02 safe restart in existing worktree

**Feature/Bug:** `tools/pc-feature` startup safety for existing patcher worktrees

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Replaced destructive startup behavior (auto-removing dirty/ahead patcher worktree) with explicit resume confirmation.
- Added a short warning that reports non-pristine state reasons (`dirty`, `ahead-of-main`).
- If user declines, the workflow exits early and preserves the existing worktree state.
- Added unit tests for both continue and abort paths, asserting no destructive cleanup call is issued.

**Why:**

- Preserve unmerged local work and make resume behavior explicit and user-controlled.

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "dirty_existing_worktree"`

### 2026-02-06 - Workflow hardening Step 03 correct work item resume selection

**Feature/Bug:** `tools/pc-feature` resume logic in execution log

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added `select_resume_work_item_id(content)` helper to encapsulate resume-selection logic.
- Updated `main()` to use that helper instead of manually selecting `headers[-1]`.
- Resume selection now uses document order semantics (top-most/latest entry):
  - newest entry outcome `pass` => no resume (create new WI).
  - newest entry outcome non-pass => resume newest WI.
- Added unit tests for mixed outcomes and newest-pass behavior.

**Why:**

- Fix wrong WI resume target caused by selecting the oldest header when entries are prepended.

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "select_resume_work_item_id"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "resumes_newest_in_progress_work_item"`

### 2026-02-06 - Workflow hardening Step 04 scoped final staging + commit resume guard

**Feature/Bug:** `tools/pc-feature` final commit safety

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added commit resume guard in finalization:
  - if current WI `Commit` section already contains a commit message, skip commit message generation and skip final `git commit`.
- Replaced blanket final staging with scoped staging:
  - added helpers to collect allowed stage paths from workflow-owned artifacts (`main..patcher_branch` diff + dev-tasks + global logs).
  - stage only allowed dirty paths via `git add -- <scoped-paths>`.
- Added pre-commit clean-tree block:
  - if dirty paths outside allowed scope are present, workflow exits with actionable error listing those paths.

**Why:**

- Prevent unrelated files from being committed and avoid duplicate commit attempts on resume.

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "stage_scoped_final_paths_blocks_unrelated_dirty_paths"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "avoids_git_add_all_for_final_staging"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "skips_commit_generation_if_commit_section_already_filled"`

### 2026-02-06 - Workflow hardening Step 05 remove feature-worktrees manifest tracking

**Feature/Bug:** `tools/pc-feature` worktree tracking cleanup

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Removed `write_worktree_manifest(...)` from `pc-feature`.
- Removed orchestration call that wrote `docs/02-features/<feature>/feature-worktrees.json`.
- Updated tests to validate no manifest file creation directly, without mocking deleted helper.

**Why:**

- Process/docs explicitly require single-worktree orchestration without `feature-worktrees.json`.

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "does_not_write_feature_worktree_manifest"`
- `tools/offload-proxy/pp rg -n "write_worktree_manifest|feature-worktrees\\.json" /Users/alexandrepezzotta/repos/PezzosCode/tools/pc-feature`

### 2026-02-06 - Workflow hardening Step 06 run smoke/tests in worktree cwd

**Feature/Bug:** `tools/pc-feature` test execution context isolation

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Extended `run_command(...)` with optional `cwd`.
- Extended `run_command_with_step_log(...)` with optional `cwd` and passed it through to `run_command(...)`.
- Updated prepatch smoke command to run with `cwd=patcher_path`.
- Updated Allowed Tests execution loop to run with `cwd=tester_path` while keeping structured logs rooted at orchestrator root.
- Added regression test for smoke cwd behavior.

**Why:**

- Ensure smoke and Allowed Tests run against worktree code, not orchestrator/root state.

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "allowed_tests_run_in_worktree_cwd"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "prepatch_smoke_runs_in_worktree_cwd"`

### 2026-02-06 - Workflow hardening Step 07 plan-reviewer gate before patching

**Feature/Bug:** `tools/pc-feature` planner approval gate

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added explicit plan-reviewer phase in each iteration before smoke/patch execution.
- Added `parse_plan_reviewer_decision(...)` to parse `Decision: Approve|Block` (default `BLOCK` on malformed output).
- On reviewer `BLOCK`:
  - append reviewer feedback to planner log context.
  - prompt planner to revise the Plan section using reviewer feedback.
  - record a note in execution log Iteration Log.
  - commit planner-scoped updates and continue loop (no patch execution in blocked iteration).
- On reviewer `APPROVE`:
  - proceed to smoke and patch phases.
- Added helper `append_iteration_log_note(...)` for deterministic Iteration Log updates.

**Why:**

- Enforce protocol requirement that patching is gated by plan-reviewer approval.

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "parse_plan_reviewer_decision"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "plan_reviewer_block_routes_back_to_planner_before_patch"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "plan_reviewer_approve_allows_patch"`

### 2026-02-06 - Workflow hardening Step 08 externalize role prompts

**Feature/Bug:** `tools/pc-feature` prompt sourcing and templating

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `prompts/planner-create.md`
- `prompts/planner-update-allowed-tests.md`
- `prompts/plan-reviewer-gate.md`
- `prompts/planner-update-from-feedback.md`
- `prompts/patcher-apply.md`
- `prompts/reporter-review.md`
- `prompts/reporter-global-log.md`
- `prompts/commit-message.md`

**What Changed:**

- Added prompt loader + renderer utilities in `pc-feature`:
  - task-first fallback lookup (`prompts/<role>-<task>.md` then `prompts/<role>.md`)
  - strict variable substitution with clear error on missing values.
- Replaced inline role/task prompt literals with loaded templates for:
  - planner create
  - planner allowed-tests update
  - plan-reviewer gate
  - planner update-from-feedback
  - patcher apply
  - reporter review
  - reporter global-log summary
  - commit message generation
- Added unit tests covering loader fallback, variable rendering, and missing template error quality.
- Updated existing tests to account for mandatory plan-reviewer prompt path.

**Why:**

- Enforce repository policy that role prompts come from files and support task-specific prompt evolution without hardcoded literals.

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "load_prompt_template_prefers_task_specific_then_fallback"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "render_prompt_template_substitutes_variables"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "load_prompt_template_missing_file_has_clear_error"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "plan_reviewer_block_routes_back_to_planner_before_patch"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "plan_reviewer_approve_allows_patch"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "avoids_git_add_all_for_final_staging"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "skips_commit_generation_if_commit_section_already_filled"`
- `tools/offload-proxy/pp rg -n "You are the Planner agent|You are the Patcher agent|You are the Reporter agent|You are the Plan Reviewer agent|generating a concise, scoped commit message|Allowed Tests must list" /Users/alexandrepezzotta/repos/PezzosCode/tools/pc-feature`

---

## 2026-02-05

- Synced `tools/templates/docs/02-features/AGENTS.md` to match the updated workflow guidance in `docs/02-features/AGENTS.md` (added the five-step drafting workflow bullet).

### 2026-02-06 - Allow pre-commit tooling without work item metadata

**Feature/Bug:** Pre-commit automation

**Changed Files:**

- `tools/pc-precommit`
- `tools/pc-autofix`

**What Changed:**

- `pc-precommit` no longer aborts when `PC_WORK_ITEM_ID` is missing; logging is skipped unless the env var (or CLI overrides) are set, and work-item metadata is passed through to `pc-autofix` only when available.
- `pc-autofix` now treats the work item id as optional so follow-up autofix runs launched outside `make feature` still succeed while continuing to log when metadata exists.

**Why:**

- Git commits outside the runner flow were blocked because the hook required metadata that only `make feature` supplies; hooks must still run even for small manual fixes while preserving structured logging when inputs exist.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- Not run (hook change only).

### 2026-02-06 - Fix ruff E402 in pre-commit helpers

**Feature/Bug:** Pre-commit automation

**Changed Files:**

- `tools/pc-autofix`
- `tools/pc-feature`

**What Changed:**

- Added `# noqa: E402` to the deferred `lib.pc_runner` imports to keep sys.path adjustments in place without violating ruff import order.

**Why:**

- Ruff flagged the imports as non-top-of-file because `sys.path` is adjusted before importing local helpers; the noqa keeps the intended behavior while satisfying linting.

**Impact:**

- **Breaking changes:** No
- **Performance:** Same
- **Dependencies:** None

**Testing:**

- `ruff check tools/pc-autofix tools/pc-feature`

### 2026-02-06 - Stabilize pc-feature execution loop (policy baseline + timeline)

**Feature/Bug:** Unified autofix pre-commit workflow loop reliability

**Changed Files:**

- `tools/pc-feature`
- `prompts/plan-reviewer-gate.md`
- `prompts/reporter-review.md`
- `tests/test_pc_feature.py`

**What Changed:**

- Locked a preflight risk-policy baseline and passed it to plan-reviewer prompts.
- Added policy conflict detection when plan-reviewer requests stop-after-preflight after explicit high-risk approval.
- Split reviewer churn from execution attempts so plan-reviewer BLOCK rounds do not consume execution budget.
- Added attempt-scoped reporter baseline (`attempt_base`) to avoid broad `main..HEAD` drift reviews.
- Added repeated reporter FAIL signature detection to stop deterministic policy loops early.
- Added timestamped timeline events in Iteration Log for step/status visibility.
- Added patcher checkpoint timeline details (`changed paths` count/summary).
- Added unit tests for reviewer-block budget behavior and repeated reporter FAIL conflict-stop behavior.

**Why:**

- Recent runs looped because reviewer/reporter checks used broad context and consumed attempt budget without executing meaningful patch/test progress.

**Impact:**

- **Breaking changes:** No
- **Performance:** Minimal overhead (small additional log writes and parsing)
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`

### 2026-02-06 - Add visual Step Trace for pc-feature workflow attempts

**Feature/Bug:** Workflow observability during loop/retry failures

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added a dedicated `Step Trace` section to work item execution entries.
- Added trace helpers to maintain an up-to-date per-attempt flow line (`step(status)` pipeline).
- Added `record_trace_event` to update both timeline events and visual flow state in one call.
- Wired trace updates through plan-reviewer, execution start, smoke, patcher, tests, reporter, feedback-loop, and CI gates.
- Added safeguards to auto-create `Step Trace` section on resumed legacy work items.
- Added regression tests for flow upsert behavior and single-line-per-attempt rendering.

**Why:**

- Timeline-only logs were hard to scan during failures. A compact per-attempt pipeline makes the break point obvious.

**Impact:**

- **Breaking changes:** No
- **Performance:** Minimal additional markdown updates
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`

### 2026-02-06 - Harden worktree collection against volatile path conflicts

**Feature/Bug:** Unified autofix pre-commit workflow collection conflict (`pc-feature: conflict detected while collecting worktrees`)

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added `collect_branch_merge_paths(...)` to filter branch diffs before final collection.
- Excluded volatile paths from branch replay:
  - feature `dev-tasks.md`
  - role-scoped logs (`planner-log.md`, `reporter-log.md`, `validation-log.md`)
  - global logs in `docs/03-logs/*.md`
  - runtime artifacts under `logs/`
- Updated final worktree collection to apply only filtered merge paths.
- Updated final-stage allowed path collection to use the same filtered branch set and then explicitly add `dev-tasks.md` + global logs from `main`.
- Added regression tests for filtering and empty include-path no-op behavior.

**Why:**

- Repeated runs with an ahead patcher branch accumulated volatile log/doc changes that are expected to diverge from `main` and caused `git apply --3way` collection conflicts.

**Impact:**

- **Breaking changes:** No
- **Performance:** Slightly improved (smaller replay patch)
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`

### 2026-02-06 - Fix resumed high-risk gate handling in plan-reviewer loop

**Feature/Bug:** `pc-feature` false policy conflict on retry (`stop-after-preflight requested after approved high-risk gate`)

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added explicit persisted note marker for approved high-risk gates: `High-risk gate approved interactively.`
- On resumed work items with `Preflight Report` already present and `Risk level: HIGH`, `pc-feature` now:
  - checks whether approval is already recorded in Notes,
  - re-prompts for approval when Notes still indicate `Awaiting PO Approval`,
  - updates Notes to the approval marker once approved.
- Updated policy-basis construction to depend on real approval state instead of assuming approval from risk level alone.
- Replaced immediate hard-fail on first plan-reviewer policy contradiction with:
  - trace warning (`status=WARN`),
  - planner feedback correction pass,
  - bounded fail after repeated conflicts (`MAX_POLICY_CONFLICT_BLOCKS=2`).
- Added regression tests for:
  - resumed high-risk re-approval path,
  - first policy conflict routing through planner without immediate process abort.

**Why:**

- Retries of the same high-risk WI can retain `Notes: Awaiting PO Approval`, causing plan-reviewer to block while workflow logic incorrectly treated the gate as already approved and aborted with a policy-conflict error.

**Impact:**

- **Breaking changes:** No
- **Performance:** Negligible
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`
- `tools/offload-proxy/pp pre-commit run --files tools/pc-feature tests/test_pc_feature.py`

### 2026-02-06 - Prevent runtime WI logs from blocking final commit

**Feature/Bug:** `pc-feature` finalization failure on retry (`unrelated dirty paths block final commit: logs/WI-*/...`)

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Centralized ignored-path definitions and added `logs/` to the ignored ephemeral prefixes used by final staging scope checks.
- Added `final_commit_allow_paths()` and wired it into `tools/pc-commit` invocation from `pc-feature`.
- Added `unstage_ephemeral_paths(root)` before final staging so accidental staged runtime artifacts are removed from index automatically.
- Result: runtime artifacts under `logs/WI-*` no longer fail:
  - `stage_scoped_final_paths(...)` unrelated-dirty guard,
  - `tools/pc-commit` disallowed-change guard.
- Added regression coverage for:
  - final scoped staging with runtime logs present,
  - presence of `--allow logs` in final `tools/pc-commit` command.

**Why:**

- `pc-feature` writes runtime execution logs during the run. Those artifacts are not part of feature deliverables and should never block finalization.

**Impact:**

- **Breaking changes:** No
- **Performance:** No measurable impact
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`
- `tools/offload-proxy/pp pre-commit run --files tools/pc-feature tests/test_pc_feature.py`

### 2026-02-06 - Separate reviewer-block budget from execution attempts

**Feature/Bug:** `pc-feature` aborting with `max iteration attempts reached` after repeated plan-reviewer BLOCK loops

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Reworked the main loop to track execution attempts separately from reviewer BLOCK rounds.
- Added `MAX_REVIEWER_BLOCKS` guard to cap unresolved reviewer churn with a specific failure reason.
- Reviewer BLOCK rounds now:
  - revise the plan,
  - append explicit block-count iteration notes,
  - do **not** consume execution attempts.
- Execution attempts now increment only after a reviewer `APPROVE`.
- Added regression tests for:
  - many reviewer BLOCKs still reaching execution without tripping execution attempt cap,
  - explicit failure message when reviewer BLOCK budget is exceeded.

**Why:**

- Previously, repeated reviewer BLOCK responses consumed the same `MAX_LOOPS` budget intended for patch/test execution, causing false terminal failures before implementation could proceed.

**Impact:**

- **Breaking changes:** No
- **Performance:** No measurable impact
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`
- `tools/offload-proxy/pp pre-commit run --files tools/pc-feature tests/test_pc_feature.py`

### 2026-02-07 - Workflow hardening pass for execution safety and scope control

**Feature/Bug:** `pc-feature` workflow hardening (cleanup scope, escalation scope, freshness, resume gating, replay filtering, test command restrictions)

**Changed Files:**

- `tools/pc-feature`
- `tools/pc-allowed-tests-check`
- `tools/pc-commit`
- `prompts/planner-create.md`
- `tests/test_pc_feature.py`
- `tests/test_pc_allowed_tests_check.py`
- `AGENTS.md`
- `docs/04-process/dev-workflow.md`
- `docs/04-process/human-orchestration-workflow.md`

**What Changed:**

- Replaced broad end-of-run cleanup with targeted patcher worktree cleanup.
- Tightened escalation allowlist to validate the command wrapped by `tools/offload-proxy/pp`.
- Added patcher worktree freshness checks for behind-`main` state.
- Removed eager role-log pre-creation (lazy writes only).
- Added HIGH-risk approval re-check on resume if approval marker is missing.
- Replaced collection-conflict note text with technical conflict wording.
- Filtered branch replay paths to durable implementation files only.
- Restricted Allowed Tests parsing/validation to `unittest`/`pytest` commands.
- Added immediate plan-reviewer read-only enforcement and early root-scope dirty-path guard.
- Added anti-hardcode plan gate checks (fixtures/seed/invariants/contracts).
- Updated process docs to align high-risk and single-worktree guidance.
- Updated `tools/pc-commit` to avoid broad `git add -A` staging after checks.

**Why:**

- Prevent destructive or overly broad workflow actions and make failures deterministic earlier in the run.

**Impact:**

- **Breaking changes:** No
- **Performance:** Slightly improved by earlier failure detection and smaller replay scope
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_allowed_tests_check.py"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_*.py"`

### 2026-02-07 - Role-loop ordering and no-op traceability hardening

**Feature/Bug:** `pc-feature` workflow loop behavior and control-flow enforcement

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Enforced strict tester gate: reporter review now runs only after tester PASS.
- Converted invalid Allowed Tests hard-stop into bounded remediation loops that route back to planner, still capped by `MAX_LOOPS`.
- Added explicit no-op iteration logging when steps are skipped (planner/patcher pre-completed, reporter blocked by tester failure, and blocked downstream gates on invalid test setup).
- Kept and reinforced Plan Reviewer loop behavior: when reviewer blocks, planner revises and re-enters review before patching.
- Improved terminal failure state on max-loop exhaustion with actionable context written to execution log notes/iteration log.

**Why:**

- Align runtime behavior with required gate ordering and make restart/skip paths auditable and deterministic without risking infinite loops.

**Impact:**

- **Breaking changes:** No
- **Performance:** No material impact
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature tests.test_pc_runner tests.test_orchestrator_role_gates tests.test_orchestrator_workflow_docs tests.test_docs_logs tests.test_pc_allowed_tests_check`

### 2026-02-07 - pc-commit allowed-untracked guard fix

**Feature/Bug:** false commit blocker on allowed runtime untracked files after lint

**Changed Files:**

- `tools/pc-commit`

**What Changed:**

- Updated `auto_restage_linted()` so untracked files are validated against existing `--allow` path rules before failing.
- The guard still fails for untracked files outside the allowed scope, but no longer blocks for allowed runtime artifacts (for example under `logs/`).

**Why:**

- `make feature F=10` could fail at final commit with:
  - `Unexpected untracked files detected after lint: logs/WI-.../ci.log`
- That file was already intentionally in allowed scope, so the guard behavior was too strict and inconsistent with other path checks.

**Impact:**

- **Breaking changes:** No
- **Performance:** No measurable impact
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp pre-commit run --files tools/pc-commit`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature tests.test_pc_runner tests.test_orchestrator_role_gates tests.test_orchestrator_workflow_docs tests.test_docs_logs tests.test_pc_allowed_tests_check`

- WI-20260206-01 completed; feature delivered as specified.
- Feature 10 docs finalized: set status to `Done` in feature spec, tech design, test plan, and dev tasks.
- Collected remaining commits from `feature-10-unified-autofix-precommit-patcher` into `main`.

### 2026-02-07 - main-freeze guard for feature execution

**Feature/Bug:** workflow hardening to enforce immutable `main` while `make feature` runs

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added a lock marker in execution notes: `Main head locked: <sha>`.
- On new/resumed runs, `pc-feature` now records or validates the locked `main` commit SHA.
- If `main` SHA changes during execution, workflow exits with `needs replan` and an iteration-log note instead of continuing on a drifting baseline.
- Added tests for lock-note helper behavior and resume-time mismatch failure.

**Why:**

- Project policy is single-user, non-parallel `make feature`; `main` should remain unchanged during feature execution.
- Enforcing this invariant removes baseline drift and prevents reporter/test false positives caused by moving `main`.

**Impact:**

- **Breaking changes:** No
- **Performance:** Minimal extra `git rev-parse` checks
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature tests.test_pc_runner tests.test_orchestrator_role_gates tests.test_orchestrator_workflow_docs tests.test_docs_logs tests.test_pc_allowed_tests_check`

### 2026-02-08 - Worktree-local runtime artifacts and loop hardening

**Feature/Bug:** prevent stale `main` artifacts and ambiguous retry failures in `pc-feature`

**Changed Files:**

- `tools/pc-feature`
- `prompts/reporter-review.md`
- `prompts/plan-reviewer-gate.md`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Moved runtime artifact source-of-truth to the feature worktree during execution:
  - `dev-tasks.md` is now read/written from the patcher worktree.
  - role logs are resolved and validated from the patcher worktree.
  - runner logs (`logs/WI-...`) are now emitted under the patcher worktree.
- Added explicit runtime scope printout (worktree, dev-tasks, role logs, runtime log dir) at startup for easier troubleshooting.
- Updated reporter review prompt to evaluate current worktree iteration artifacts and require actionable failure fields (`File/Path`, `Check`, `Evidence`, `Expected fix`) on FAIL.
- Added reporter failure-context guard and richer tester failure context so planner/patcher feedback loops always receive actionable remediation data.
- Scoped anti-hardcode plan blocking to high-risk/triggered work items instead of applying it unconditionally.
- Preserved strict loop ordering and no-op iteration logging while improving exhaustion diagnostics.

**Why:**

- Previous runs could fail with `max iteration attempts reached` because reporter/planner looked at stale `main`-side artifacts instead of worktree artifacts.
- Runtime logs in `main` could reintroduce untracked-file commit guard failures.
- Failure loops needed stronger, structured context to converge reliably within `MAX_LOOPS`.

**Impact:**

- **Breaking changes:** No
- **Performance:** Minimal (additional path checks and context formatting)
- **Dependencies:** None

**Testing:**

- `python3 -m py_compile tools/pc-feature`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`

### 2026-02-09 - Plan Reviewer first-class step + orchestration hardening

**Feature/Bug:** enforce step-level commit boundaries, dedicated Plan Reviewer role artifacts, deterministic review gating, and safer feedback-loop plan handling

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `prompts/planner-create.md`
- `prompts/planner-update-from-feedback.md`
- `prompts/planner-update_from_feedback.md`
- `prompts/plan-reviewer-gate.md`
- `prompts/plan-reviewer.md`
- `prompts/patcher.md`
- `prompts/patcher-apply.md`
- `prompts/patcher-update_from_feedback.md`
- `prompts/tester.md`
- `prompts/reporter-review.md`
- `prompts/planner.md`
- `prompts/reporter.md`
- `prompts/reporter-global-log.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `docs/04-process/dev-workflow.md`
- `tools/templates/docs/04-process/dev-workflow.md`
- `docs/02-features/feature-template/dev-tasks.md`
- `tools/templates/docs/02-features/feature-template/dev-tasks.md`
- `docs/02-features/feature-template/plan-reviewer-log.md`
- `tools/templates/docs/02-features/feature-template/plan-reviewer-log.md`

**What Changed:**

- Added `plan-reviewer` as a role-scoped artifact in orchestration (`plan-reviewer-log.md` now protected from patcher edits).
- Introduced role-step commit helper to keep role steps commit-bounded and prevent cross-role dirty carryover.
- Moved plan review to a dedicated reviewer step with committed `APPROVE/BLOCK` decisions.
- Applied deterministic plan policy/anti-hardcode checks before LLM reviewer invocation.
- Added revised-plan quality checks and structured merge fallback to avoid lossy overwrite patterns.
- Updated tester feedback serialization to format commands safely and include explicit discovery-summary tracking field.
- Updated reporter prompt contract and scope guidance (`refs/heads/main..HEAD` as primary review scope).
- Updated protocol/workflow docs and templates to document first-class Plan Reviewer step and role-scope boundaries.

**Why:**

- Prior runs showed planner/reviewer/patcher state coupling causing scope-guard failures and ambiguous audit history.

**Impact:**

- **Breaking changes:** No API break, but orchestration behavior changed (new role log and stricter step transitions).
- **Performance:** Minimal; same loop shape with tighter deterministic branching.
- **Dependencies:** None.

**Testing:**

- `python3 -m py_compile tools/pc-feature`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature` (offload id: `094029524d9cfaff8b7878b8f526d17db57095455be487f58b5e6f50929d761e`)
- `tools/offload-proxy/pp python3 -m unittest tests.test_orchestrator_workflow_docs tests.test_update_reapply_templates_docs tests.test_docs_logs`
- `tools/offload-proxy/pp python3 -m unittest tests.test_orchestrator_role_gates tests.test_output_offload_enforcement_docs`
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p 'test_*.py'` (offload id: `1c1dd26a9f0b8c4142a742a8816bdd79384b3489081c38ba2c2141e1272f0cab`)

### 2026-02-08 - Template-sync mismatch fix

**Feature/Bug:** Docs maintenance (template-sync gate)

**Changed Files:**

- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Staged the template copy of the ticket execution protocol to match the updated living doc line about plan-reviewer delta snapshots.

**Why:**

- Pre-commit `template-sync` failed because the template file was not staged alongside the updated living doc.

**Impact:**

- **Breaking changes:** No
- **Performance:** None
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp tools/pc-template-sync`

### 2026-02-08 - Sync plan-reviewer delta guard note into template

**Feature/Bug:** keep template docs aligned with current ticket execution protocol

**Changed Files:**

- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Added the plan-reviewer read-only delta-guard note to the template so it matches the source protocol doc.

**Why:**

- The source protocol includes the reviewer delta-guard guidance; the template was missing the same line.

**Impact:**

- **Breaking changes:** No
- **Performance:** None
- **Dependencies:** None

**Testing:**

- Not run (documentation-only change)

### 2026-02-08 - Sync ticket-execution-protocol template indentation

**Feature/Bug:** template-sync mismatch

**Changed Files:**

- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Aligned the Step 7 feedback-loop list indentation with the canonical docs to resolve the template/living mismatch.

**Why:**

- Pre-commit `template-sync` failed because the template diverged from `docs/04-process/ticket-execution-protocol.md`.

**Impact:**

- **Breaking changes:** No
- **Performance:** None
- **Dependencies:** None

**Testing:**

- Not run (not requested).

### 2026-02-08 - Plan-policy gate and cross-feature role-scope hardening

**Feature/Bug:** prevent patcher from acting on role-scoped/global-log instructions that slip through planner output

**Changed Files:**

- `tools/pc-feature`
- `prompts/plan-reviewer-gate.md`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Added deterministic plan-policy validation before patching:
  - Blocks plans that reference role-scoped files (`dev-tasks.md`, planner/reporter/validation logs).
  - Blocks plans that reference `docs/03-logs/*`.
  - Blocks plans that include forbidden commands (`make feature`, `pc-feature`, `tools/pc-feature`).
- Extended patcher scope guard to reject role-scoped files across any feature, not only the current feature folder.
- Added explicit startup visibility line for feature routing: requested feature id and resolved feature slug.
- Added regression tests for plan-policy violations and cross-feature role-scope enforcement.

**Why:**

- A run failed with `patcher edited role-scoped files: docs/02-features/12.../dev-tasks.md` because planner/reviewer allowed forbidden plan instructions.
- Guardrails must fail earlier (plan gate), not only at patcher commit time.

**Impact:**

- **Breaking changes:** No
- **Performance:** Minimal (string policy checks during plan gate)
- **Dependencies:** None

**Testing:**

- `python3 -m py_compile tools/pc-feature`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- `tools/offload-proxy/pp python3 -m unittest tests.test_docs_logs`

### 2026-02-09 - Pre-patch policy recheck + patcher scope-violation reroute

**Feature/Bug:** prevent late patcher hard-stop by rerouting forbidden scope edits back to planner remediation

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added `revise_plan_from_feedback(...)` helper to centralize planner revision handling after policy/feedback blocks.
- Added a second deterministic `plan_policy_violations(...)` check immediately before patcher execution.
- When patcher touches role-scoped/global-log files, the run now:
  - restores patcher dirty paths,
  - generates explicit remediation feedback,
  - routes back to planner for plan revision,
  - continues loop instead of terminating immediately on the patcher guard.
- Added regression coverage for resume/retry flow ensuring a pre-patch forbidden-plan detection reroutes to planner and does not invoke patcher.

**Why:**

- A feature-13 run hit `patcher edited role-scoped files` late after plan drift. We need deterministic defense at pre-patch time and a recoverable planner reroute path.

**Impact:**

- **Breaking changes:** No API break; stricter orchestration guardrails before patch step.
- **Performance:** Minimal (one extra policy scan before patching).
- **Dependencies:** None

**Testing:**

- `python3 -m py_compile tools/pc-feature tests/test_pc_feature.py`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature.TestPcFeature.test_prepatch_policy_recheck_routes_back_to_planner_before_patcher`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature` (offload id: `f286e4ef1d6de49fe6b76805ea23fd8710d0f2a61084c4b5691e8b7c34401028`)

### 2026-02-09 - Reporter global-log JSON repair + deterministic orchestrator fallback

**Feature/Bug:** prevent end-of-run failure when reporter returns non-JSON text for global log summaries

**Changed Files:**

- `tools/pc-feature`
- `prompts/reporter-global-log.md`
- `tests/test_pc_feature.py`

**What Changed:**

- Updated the reporter global-log prompt to be explicitly read-only (no file edits, no clarification questions) and JSON-only output.
- Added JSON object parsing helper for reporter global-log payloads.
- Added a one-time JSON-repair prompt path when the initial reporter payload is not parseable.
- Replaced hard failure on parse errors with deterministic orchestrator-owned global log defaults derived from `work_item_id` and `requires_global_logs`.
- Ensured orchestrator remains the only writer for `docs/03-logs/*` while still using reporter-provided lines when valid.
- Added unit coverage for:
  - invalid initial payload repaired successfully,
  - invalid payload unrecoverable after one repair retry, deterministic fallback applied,
  - deterministic payload switching when `requires_global_logs` is true.

**Why:**

- `make feature` reached final gates but could fail at the very end if reporter emitted clarification text instead of JSON.
- Reporter role scope requires reporting, while orchestrator owns global log writes, so this step must be resilient and non-interactive.

**Impact:**

- **Breaking changes:** No
- **Performance:** Minimal (at most one extra reporter call for JSON repair)
- **Dependencies:** None

**Testing:**

- `python3 -m py_compile tools/pc-feature tests/test_pc_feature.py`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`

### 2026-02-09 - Plan contract normalization and reviewer-loop fail-safe controls

**Feature/Bug:** prevent repeated planner/reviewer BLOCK loops caused by stale forbidden paths and unclear loop caps

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `prompts/planner-create.md`
- `prompts/planner-update-from-feedback.md`
- `prompts/planner-update_from_feedback.md`
- `prompts/plan-reviewer-gate.md`
- `prompts/plan-reviewer.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Added a Plan Contract parser in `pc-feature` for deterministic section extraction (`Approach`, `Files to change`, `Risks`, `Tests (anti-hardcode coverage required)`).
- Updated plan policy checks to evaluate `Files to change` as primary scope while still scanning full plan text as a safety fallback.
- Changed revised-plan merge behavior to strict replacement (no append fallback) so stale forbidden content cannot persist across retries.
- Tightened revised-plan quality checks to require contract sections when the prior plan already follows contract structure.
- Added independent planner-loop guards:
  - `MAX_PLANNER_REVISIONS`
  - exact reviewer cap trigger (`>= MAX_REVIEWER_BLOCKS`)
  - stagnation detector for repeated unresolved policy issues (`MAX_STAGNANT_REVIEWER_BLOCKS`)
- Improved iteration-log observability with explicit counters (`reviewer_block`, `planner_revision`, `execution_attempt`).
- Updated planner/reviewer prompts to require and review Plan Contract v1 consistently.
- Synced protocol docs/template to document contract shape and independent reviewer/planner loop caps.
- Added regression tests for:
  - full-plan fallback path-policy detection,
  - contract-required revised plans,
  - strict replacement merge behavior,
  - planner revision cap handling,
  - stagnation guard failure path.

**Why:**

- Feature 12 showed repeated reviewer BLOCK messages with unchanged policy violations because revised plan content was appended instead of replacing stale plan text.
- Planner/reviewer retries needed independent hard stops and clearer counters to avoid ambiguous “attempt 2 forever” behavior.

**Impact:**

- **Breaking changes:** No API break; stricter runtime planning contract/loop enforcement in orchestrator behavior.
- **Performance:** Minimal (extra section parsing and signature checks during reviewer-block path).
- **Dependencies:** None

**Testing:**

- `python3 -m py_compile tools/pc-feature`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature` (offload id: `2a67be91170b2e85c02d3fd7e1d1de399de5c50b6161407d4188cba9922d2029`)
- `tools/offload-proxy/pp python3 -m unittest tests.test_orchestrator_workflow_docs tests.test_update_reapply_templates_docs tests.test_docs_logs tests.test_orchestrator_role_gates tests.test_output_offload_enforcement_docs`
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p 'test_*.py'` (offload id: `2d6b4c2d7c605aeaf3d7cacef72346b98c9dd56fc3c348509052ee9a3141fe00`)

### 2026-02-08 - Reviewer delta-guard and no-op ordering hardening

**Feature/Bug:** eliminate false `plan reviewer modified files` failures caused by pre-existing planner/orchestrator edits

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `prompts/plan-reviewer-gate.md`
- `docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Reworked plan-reviewer read-only check to compare pre/post worktree dirty snapshots and block only reviewer-introduced deltas.
- Moved planner no-op iteration-note write (`plan already present`) to after reviewer verification, removing the pre-review false-positive path.
- Persisted deferred planner no-op notes immediately after reviewer verification so later `dev-tasks.md` reloads cannot drop the note.
- Added pre-review hygiene checkpoint (`AUTO_REVIEWER_HYGIENE`, default enabled): auto-commits allowed planner-owned pre-existing dirt and blocks unexpected dirty paths.
- Improved reviewer guard diagnostics with delta/pre-existing path context and iteration-log trace on failure.
- Added regression tests for unchanged pre-existing dirty paths, true dirty deltas, and end-to-end no-misattribution flow.

**Why:**

- Feature 12 run failed with `plan reviewer modified files in writable worktree: .../dev-tasks.md` even though the change came from orchestrator/planner no-op write, not reviewer edits.

**Impact:**

- **Breaking changes:** No
- **Performance:** Minimal (file hashing on dirty paths around reviewer gate)
- **Dependencies:** None

**Testing:**

- `python3 -m py_compile tools/pc-feature`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- `tools/offload-proxy/pp python3 -m unittest tests.test_docs_logs`

### 2026-02-08 - Auto-resume restoration with deterministic startup guards

**Feature/Bug:** restore safe automatic feature resume for existing in-progress worktrees without reintroducing dirty-state ambiguity

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Added `RESUME_MODE` startup policy (`auto` default, `prompt`, `fresh`).
- Replaced implicit startup prompts with deterministic resume handling in `auto` mode:
  - continue existing ahead/dirty patcher worktree automatically when safe.
  - block stale behind-`main` worktrees (policy: `main` must remain unchanged during feature execution).
  - block non-runtime dirty paths before execution.
- Added runtime-dirty classification for resume startup (`dev-tasks.md`, role logs, global logs only).
- Added automatic resume checkpoint commit for dirty `dev-tasks.md` when a resumable work item exists.
- Added single-active-feature guard across patcher worktrees to prevent overlapping active features.
- Expanded regression coverage for resume mode parsing, startup guard behavior, runtime dirty classification, and checkpoint flow.

**Why:**

- Resume behavior had been partially removed/hardened toward pristine-only startup, which reduced reliability for normal reruns of in-progress features.
- We need automatic resume back, but with strict controls to avoid cross-feature and dirty-state failures.

**Impact:**

- **Breaking changes:** Yes (startup policy now fails fast for stale/non-runtime-dirty/parallel-active-feature states unless explicitly handled by mode)
- **Performance:** Minimal (worktree-list + status checks at startup)
- **Dependencies:** None

**Testing:**

- `python3 -m py_compile tools/pc-feature`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`

### 2026-02-08 - WIP-first startup resume implementation

**Feature/Bug:** preserve active feature worktree WIP at startup and remove destructive startup cleanup paths

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Added generalized startup checkpointing (`checkpoint_resume_state`) that stages and commits all dirty non-ignored paths in the active feature worktree.
- Removed startup dependency on runtime-only dirty classification for safety gating and removed startup cleanup checkout flows.
- Replaced startup hard-fail precondition for dirty `main` paths with a warning (`ensure_root_start_scope`).
- Updated resume tests to validate that dirty runtime/non-runtime files are checkpointed and execution continues.
- Updated live/template protocol docs to document WIP-preserving startup behavior and fresh-mode-only destructive reset policy.

**Why:**

- Existing startup strictness conflicted with the single-user one-feature-at-a-time model where dirty feature worktree state represents intentional in-progress work.

**Impact:**

- **Breaking changes:** Yes (startup no longer blocks on non-runtime dirty feature-worktree paths)
- **Performance:** Minimal (single status/add/commit checkpoint path at startup when dirty)
- **Dependencies:** None

**Testing:**

- `python3 -m py_compile tools/pc-feature`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- `tools/offload-proxy/pp python3 -m unittest tests.test_docs_logs`

- WI-20260209-01: Feature completed; reporter prepared global log summaries for orchestrator.

### 2026-02-09 - Re-sync process doc templates with living docs

**Feature/Bug:** template-sync gate parity

**Changed Files:**

- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/dev-workflow.md`

**What Changed:**

- Updated the three process template docs to match their living docs under `docs/04-process/`.
- Restored missing prompt/task-variant guidance in template copies so template/living content is identical.

**Why:**

- Pre-commit `template-sync` was blocked by out-of-sync template/living pairs where neither side was part of the current commit.
- Re-syncing templates removes the invariant drift and unblocks commits.

**Impact:**

- **Breaking changes:** No
- **Performance:** None
- **Dependencies:** None

**Testing:**

- `diff -u docs/04-process/ticket-execution-protocol.md tools/templates/docs/04-process/ticket-execution-protocol.md`
- `diff -u docs/04-process/human-orchestration-workflow.md tools/templates/docs/04-process/human-orchestration-workflow.md`
- `diff -u docs/04-process/dev-workflow.md tools/templates/docs/04-process/dev-workflow.md`
- `tools/pc-template-sync`

### 2026-02-09 - Remove change-budget wiring from execution workflow

**Feature/Bug:** workflow contract cleanup

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `docs/02-features/feature-template/dev-tasks.md`
- `tools/templates/docs/02-features/feature-template/dev-tasks.md`
- `docs/03-logs/tickets/worklog-template.md`
- `tools/templates/docs/03-logs/tickets/worklog-template.md`
- `docs/02-features/14-learning-loop-improvement-proposals/dev-tasks.md`
- `docs/02-features/15-offload-audit-and-log-compaction/dev-tasks.md`
- `docs/02-features/16-feature-gating-and-skill-mining/dev-tasks.md`

**What Changed:**

- Removed `DEFAULT_CHANGE_BUDGET` usage from `pc-feature` preflight rendering and risk classification.
- Removed budget lines from generated execution entries and renamed runtime section to `Files to Change`.
- Added section-alias compatibility so legacy entries using `Files to Change + Change Budget` continue to work.
- Updated tests for new signatures/output and added regression coverage for legacy section compatibility.
- Updated live/template process docs and worklog templates to remove change-budget wording.
- Added changelog alignment entries in feature 14-16 `dev-tasks.md`.

**Why:**

- Budget fields were not acting as an enforceable control and introduced misleading workflow noise.
- The workflow remains governed by explicit scope/risk/policy checks without budget-specific fields.

**Impact:**

- **Breaking changes:** No (legacy execution-log section compatibility preserved)
- **Performance:** None
- **Dependencies:** None

**Testing:**

- `python3 -m py_compile tools/pc-feature tests/test_pc_feature.py`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- `tools/offload-proxy/pp rg -n "Change budget|max_files|max_new_modules|Files to Change \+ Change Budget|change budget exceeded" tools/pc-feature tests/test_pc_feature.py docs/04-process/ticket-execution-protocol.md tools/templates/docs/04-process/ticket-execution-protocol.md docs/02-features/feature-template/dev-tasks.md tools/templates/docs/02-features/feature-template/dev-tasks.md docs/03-logs/tickets/worklog-template.md tools/templates/docs/03-logs/tickets/worklog-template.md docs/02-features/14-learning-loop-improvement-proposals/dev-tasks.md docs/02-features/15-offload-audit-and-log-compaction/dev-tasks.md docs/02-features/16-feature-gating-and-skill-mining/dev-tasks.md`
- `diff -u docs/04-process/ticket-execution-protocol.md tools/templates/docs/04-process/ticket-execution-protocol.md`
- `diff -u docs/02-features/feature-template/dev-tasks.md tools/templates/docs/02-features/feature-template/dev-tasks.md`
- `diff -u docs/03-logs/tickets/worklog-template.md tools/templates/docs/03-logs/tickets/worklog-template.md`

### 2026-02-09 - Clarify Plan Reviewer gate remediation ownership

**Feature/Bug:** plan-reviewer gate prompt contradiction hardening

**Changed Files:**

- `prompts/plan-reviewer-gate.md`
- `tools/templates/prompts/plan-reviewer-gate.md`

**What Changed:**

- Added explicit prompt guidance that "Required changes" must not ask planners to add orchestration commands (`make feature`, `pc-feature`, `tools/pc-feature`) inside Plan text.
- Added explicit guidance for global-log obligations: reviewer should request planner ownership wording (reporter/orchestrator flow) instead of patcher edits to forbidden paths.
- Preserved existing block rules, response schema, and plan-contract review requirements.

**Why:**

- Prevent reviewer guidance from re-introducing commands/paths that deterministic policy checks already forbid, which can cause avoidable block/conflict churn.

**Impact:**

- **Breaking changes:** No
- **Performance:** None
- **Dependencies:** None

**Testing:**

- `cmp -s prompts/plan-reviewer-gate.md tools/templates/prompts/plan-reviewer-gate.md`
- `tools/offload-proxy/pp python tests/test_pc_feature.py`

- WI-20260209-01: Completed feature and prepared global summary for orchestrator.

### 2026-02-09 - Finalize Feature 14 completion state on main

**Feature/Bug:** F-14 learning loop improvement proposals

**Changed Files:**

- `docs/02-features/14-learning-loop-improvement-proposals/feature-spec.md`
- `docs/02-features/14-learning-loop-improvement-proposals/tech-design.md`
- `docs/02-features/14-learning-loop-improvement-proposals/test-plan.md`
- `docs/02-features/14-learning-loop-improvement-proposals/dev-tasks.md`

**What Changed:**

- Marked Feature 14 specification, design, test plan, and dev-tasks status fields as `Completed`.
- Marked all four dev tasks complete and filled execution summary fields for WI-20260209-01.
- Prepared the feature work for integration on `main` so next-feature planning can start from a completed F-14 baseline.

**Why:**

- Close the feature lifecycle explicitly in docs and avoid carrying stale `Draft`/`Not Started` states into the next feature.

**Impact:**

- **Breaking changes:** No
- **Performance:** None
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp pytest tests/test_pc_feature.py`
- `tools/offload-proxy/pp pytest tests/test_docs_logs.py tests/test_orchestrator_workflow_docs.py tests_extra/test_bootstrap_into_extra.py`

### 2026-02-09 - Reformulate Feature 15 for useful compact logs

**Feature/Bug:** F-15 offload audit + log compaction scope refinement

**Changed Files:**

- `docs/02-features/15-offload-audit-and-log-compaction/feature-spec.md`
- `docs/02-features/15-offload-audit-and-log-compaction/tech-design.md`
- `docs/02-features/15-offload-audit-and-log-compaction/dev-tasks.md`
- `docs/02-features/15-offload-audit-and-log-compaction/test-plan.md`
- `docs/03-logs/decision-log.md`

**What Changed:**

- Kept F-15 core framing as offload audit + compaction, but tightened it around continuous-improvement usefulness.
- Expanded compaction scope from decision/implementation only to decision/implementation/validation logs.
- Added a compact-output usefulness contract (source/date/work-item/outcome/evidence fields).
- Added non-destructive derived-output location guidance (`docs/03-logs/compacted/`).
- Synced tasks/tests so future execution validates fidelity and contract completeness.

**Why:**

- Original F-15 wording was directionally correct but underspecified for learning-loop outcomes and evidence quality.

**Impact:**

- **Breaking changes:** No
- **Performance:** None
- **Dependencies:** None

**Testing:**

- Documentation checks recorded in `docs/03-logs/validation-log.md` (doc-only update).

### 2026-02-09 - Plan-review block reduction hardening (command context + plan/test alignment)

**Feature/Bug:** Plan-reviewer reliability improvements

**Changed Files:**

- `AGENTS.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `prompts/plan-reviewer-gate.md`
- `tools/templates/prompts/plan-reviewer-gate.md`
- `prompts/planner-create.md`
- `tools/templates/prompts/planner-create.md`
- `prompts/planner-update-allowed-tests.md`
- `tools/templates/prompts/planner-update-allowed-tests.md`
- `prompts/planner-update-from-feedback.md`
- `tools/templates/prompts/planner-update-from-feedback.md`
- `prompts/planner-update_from_feedback.md`
- `tools/templates/prompts/planner-update_from_feedback.md`
- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Clarified policy that `make feature` is orchestration/bootstrap only and must not be planned as a patch/test command.
- Updated reviewer gate wording to block forbidden commands only in command context (not file-path references in `Files to change`).
- Added deterministic plan-policy checks in `pc-feature` for:
  - command-context detection of forbidden commands,
  - explicit global-log handoff wording for plans that touch process/global-log docs,
  - plan test command alignment with Allowed Tests.
- Kept prompt/template parity for planner and reviewer prompt files.
- Added regression tests for command-context parsing and plan/Allowed Tests alignment behavior.

**Why:**

- Reduce avoidable Plan Reviewer `BLOCK` loops caused by false positives (`tools/pc-feature` as file path) and repeated plan-policy drift around tests/global-log ownership.

**Impact:**

- **Breaking changes:** No
- **Performance:** None
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature tests.test_docs_logs tests.test_orchestrator_workflow_docs`

### 2026-02-09 - Unblock planner/reviewer stagnation on `docs/03-logs/*` handoff note

**Feature/Bug:** plan-reviewer stagnation false-positive in feature execution loop

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `prompts/planner-create.md`
- `prompts/planner-update-from-feedback.md`
- `prompts/planner-update_from_feedback.md`
- `prompts/plan-reviewer-gate.md`
- `tools/templates/prompts/planner-create.md`
- `tools/templates/prompts/planner-update-from-feedback.md`
- `tools/templates/prompts/planner-update_from_feedback.md`
- `tools/templates/prompts/plan-reviewer-gate.md`

**What Changed:**

- Updated planner/reviewer prompt wording to reference `docs/03-logs` ownership without requiring the literal wildcard token `docs/03-logs/*` in plan output.
- Added a narrow policy exception in `plan_policy_violations` so full-plan fallback scanning ignores only the literal wildcard handoff token (`docs/03-logs/*`, including escaped form), while still blocking concrete `docs/03-logs/...` paths.
- Kept strict enforcement in `Files to change` scope: wildcard entries there remain forbidden.
- Added regression tests for both allowed-handoff and forbidden-filescope wildcard cases.

**Why:**

- The previous prompt contract instructed planner output that included `docs/03-logs/*`, while policy checks treated that same token as forbidden, creating a self-contradictory loop that triggered stagnation aborts.

**Impact:**

- **Breaking changes:** No
- **Performance:** None
- **Dependencies:** None

**Testing:**

- `python3 -m py_compile tools/pc-feature tests/test_pc_feature.py`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature.TestPcFeature.test_plan_policy_violations_allows_docs_logs_wildcard_handoff_note tests.test_pc_feature.TestPcFeature.test_plan_policy_violations_blocks_docs_logs_wildcard_in_files_section`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature` (offload id `4c8d6b83107f50e31329a63db83ec36e7ee535f336b652a2144265a29890f85d`)

### 2026-02-09 - Orchestrator proposal aggregation and dedupe for `docs/possible-improvements.md`

**Feature/Bug:** workflow improvement proposal collection causing role scope failures

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `prompts/planner-create.md`
- `prompts/planner-update-from-feedback.md`
- `prompts/planner-update_from_feedback.md`
- `prompts/plan-reviewer-gate.md`
- `prompts/patcher-apply.md`
- `prompts/patcher-update_from_feedback.md`
- `prompts/reporter-review.md`
- `docs/possible-improvements.md`
- `docs/04-process/dev-workflow.md`
- `docs/04-process/human-orchestration-workflow.md`
- `docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/AGENTS.md`
- `tools/templates/docs/possible-improvements.md`
- `tools/templates/docs/04-process/dev-workflow.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/AGENTS.md`
- `tools/templates/prompts/planner-create.md`
- `tools/templates/prompts/planner-update-from-feedback.md`
- `tools/templates/prompts/planner-update_from_feedback.md`
- `tools/templates/prompts/plan-reviewer-gate.md`
- `tools/templates/prompts/patcher-apply.md`
- `tools/templates/prompts/patcher-update_from_feedback.md`
- `tools/templates/prompts/reporter-review.md`

**What Changed:**

- Added orchestrator-owned handling for `docs/possible-improvements.md` in `pc-feature` scope/staging rules.
- Added queue/flush flow in `pc-feature` so failure proposals are collected across the run and written only at orchestrator checkpoints.
- Added proposal dedupe/merge logic for queued entries and enriched proposal payload extraction from tester/reporter feedback fields.
- Added policy enforcement to block plans that target `docs/possible-improvements.md`.
- Updated role prompts/templates to keep registry writes orchestrator-only and allow optional structured improvement fields in reporter feedback.
- Updated process docs/templates to document the new ownership and aggregation behavior.
- Added regression tests for payload extraction, policy blocking, runtime scope allowance, final-stage allowlist coverage, and queue flush dedupe.

**Why:**

- Preserve continuous-improvement feedback from roles while removing side effects from role-scoped write violations in shared worktree execution.

**Impact:**

- **Breaking changes:** No
- **Performance:** Negligible (small in-memory queue + dedupe pass)
- **Dependencies:** None

### 2026-02-10 - Reset planner-owned `dev-tasks.md` before non-planner commits

**Feature/Bug:** intermittent `tester edited out-of-scope files` aborts near end of `make feature`

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Updated `commit_role_step(...)` to reset planner-owned `dev-tasks.md` when the role is `tester`, `reporter`, or `plan-reviewer` before role-scope enforcement.
- Added regression coverage asserting tester commit flow invokes `reset_dev_tasks_if_dirty(...)` on the feature `dev-tasks.md` path.

**Why:**

- In resumed/shared-worktree runs, incidental dirty state on `dev-tasks.md` can leak into non-planner role commit boundaries and trigger terminal scope failures (`tester edited out-of-scope files`) even when role outputs are otherwise valid.

**Impact:**

- **Breaking changes:** No
- **Performance:** Negligible (one extra dirty-path check at non-planner commit boundaries)
- **Dependencies:** None

**Testing:**

- `python3 -m py_compile tools/pc-feature tests/test_pc_feature.py`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature.TestPcFeature.test_commit_role_step_tester_resets_dev_tasks_before_scope_check`
- `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature.TestPcFeature.test_enforce_role_scope_blocks_patcher_cross_feature_role_docs tests.test_pc_feature.TestPcFeature.test_prepatch_policy_recheck_routes_back_to_planner_before_patcher tests.test_pc_feature.TestPcFeature.test_failure_loop_invokes_planner_and_patcher_feedback_and_logs_iteration`

### 2026-02-10 - Resilient patcher collection into main with conflict auto-skip

**Feature/Bug:** `pc-feature: conflict detected while collecting worktrees` abort during final collection

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/02-features/15-offload-audit-and-log-compaction/dev-tasks.md`

**What Changed:**

- Added resilient collection flow in `collect_branch_into_main(...)`:
  - dry precheck diagnostics (`git apply --check --3way`) via `apply_branch_diff(..., precheck=True)`,
  - conflict path extraction/normalization,
  - automatic retry on non-conflicting paths,
  - per-path fallback application when batch retry fails.
- Replaced terminal abort on collection conflict in `main()` with warning + auto-skip behavior:
  - explicit run-log warning mentions "collecting patcher branch into main",
  - conflicting paths are printed,
  - Iteration Log note is appended in `dev-tasks.md`,
  - run proceeds to final gates instead of hard stop.
- Added explicit stdout line when non-planner roles auto-reset planner-owned `dev-tasks.md` before scope checks.
- Tightened Feature 15 `Allowed Tests` commands to focused `tests.test_pc_feature` coverage, avoiding full-suite discovery by default.

**Why:**

- Collection conflicts were aborting otherwise successful runs with generic messaging and no automated recovery path. The new approach keeps strict visibility of conflicts while maximizing successful integration of non-conflicting changes.

**Impact:**

- **Breaking changes:** No
- **Performance:** Small additional `git apply` checks/retries during collection only
- **Dependencies:** None

### 2026-02-11 - Context/workflow doc sync for execution-model consistency

**Feature/Bug:** Documentation coherence between context/product docs and canonical execution protocol

**Changed Files:**

- `docs/00-context/vision.md`
- `docs/00-context/context-boundaries-operating-model.md`
- `docs/00-context/system-map.md`
- `docs/00-context/expected-features.md`
- `docs/01-product/prd.md`
- `docs/04-process/dev-workflow.md`
- `docs/04-process/definition-of-done.md`
- `docs/03-logs/decision-log.md`

**What Changed:**

- Updated role terminology to the canonical runtime model: orchestrator, planner, plan-reviewer, patcher, tester, reporter.
- Clarified single-feature-worktree default semantics in context/system docs and removed ambiguous "parallel roles use worktrees" phrasing.
- Updated PRD workflow/process requirements to remove mixed legacy role names.
- Updated dev workflow to:
  - explicitly defer to ticket-execution protocol on conflicts,
  - align report/final-gate wording to `make ci`,
  - align feedback ownership to planner-owned execution log + tester/reporter role logs,
  - clarify role file scope in the shared feature worktree.
- Added DoD scope notes marking deployment/staging/team-notification checks as conditional for downstream deployed products, with local-tooling work items treated as `N/A` where appropriate.

**Why:**

- Keep context/product/process docs consistent with the implemented orchestration protocol and reduce execution drift.

**Impact:**

- **Breaking changes:** No
- **Performance:** None (docs-only)
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp rg -n "implementer/reviewer/tester|parallel roles use worktrees|Run \`make test\` before closing the work item" docs/00-context docs/01-product/prd.md docs/04-process/dev-workflow.md`

### 2026-02-11 - Planned two new workflow-level features in expected-features

**Feature/Bug:** Post-completion roadmap planning for reliability and workflow testing

**Changed Files:**

- `docs/00-context/expected-features.md`

**What Changed:**

- Added a new expected feature for workflow hardening focused on template-drift detection and autofix recovery during pre-commit/CI checks.
- Added a new expected feature for end-to-end workflow smoke testing using a synthetic/fake feature to validate orchestration and gates.
- Kept the update at context planning level only; no feature folder scaffolding was created under `docs/02-features/`.

**Why:**

- Capture the next two priorities in the canonical expected-features intake file before expanding them into full feature specs and execution tasks.

**Impact:**

- **Breaking changes:** No
- **Performance:** None (docs-only)
- **Dependencies:** None

**Testing:**

- Not run (planning/docs-only update)

### 2026-02-11 - PRD sync from context/process docs (context-to-product)

**Feature/Bug:** PRD alignment with latest expected features and execution protocol constraints

**Changed Files:**

- `docs/01-product/prd.md`

**What Changed:**

- Updated PRD metadata (`Version: 0.5`, `Last Updated: 2026-02-11`) and changelog.
- Added missing expected features into the PRD Process Features list:
  - resume in-progress tickets,
  - commit gating on completed ticket docs,
  - workflow hardening for template-drift/autofix recovery,
  - synthetic feature for end-to-end workflow smoke testing.
- Added functional requirements for resume behavior, commit gating, and drift/autofix hardening, plus a Should Have requirement for synthetic-feature smoke tests.
- Expanded Workflow/Process Requirements to mirror protocol constraints for high-risk approval, Allowed Tests policy, final `make ci` gate behavior, precommit log-scope restrictions, and resume semantics.

**Why:**

- Keep `docs/01-product/prd.md` as an accurate product/process contract that reflects `docs/00-context/*.md` and `docs/04-process/*.md` after recent roadmap and workflow updates.

**Impact:**

- **Breaking changes:** No
- **Performance:** None (docs-only)
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp rg -n '^## |^### ' docs/01-product/prd.md`
- `tools/offload-proxy/pp rg -n 'Workflow hardening|template drift|synthetic feature|smoke test' docs/01-product/prd.md docs/00-context/expected-features.md`

### 2026-02-11 - Incremental PRD-to-features generation for newly missing P0/P1 items

**Feature/Bug:** Feature-doc scaffolding from PRD process features (incremental mode)

**Changed Files:**

- `docs/02-features/17-resume-in-progress-tickets/*`
- `docs/02-features/18-commit-gated-by-completed-ticket-docs/*`
- `docs/02-features/19-template-drift-hardening-autofix-recovery/*`
- `docs/02-features/20-synthetic-feature-workflow-smoke-test/*`

**What Changed:**

- Created four new feature folders for PRD P0/P1 process features not previously represented as dedicated feature docs:
  - Resume in-progress tickets
  - Commit gated by completed ticket docs
  - Template drift hardening + autofix recovery
  - Synthetic feature workflow smoke test
- Each folder was initialized from `docs/02-features/feature-template/` and populated with concrete content in:
  - `feature-spec.md`
  - `tech-design.md`
  - `dev-tasks.md`
  - `test-plan.md`
- Preserved template role-log files (`planner-log.md`, `plan-reviewer-log.md`, `reporter-log.md`, `validation-log.md`) as initialization stubs.

**Why:**

- Apply `prd-to-features` incrementally after PRD updates so missing P0/P1 process features are documented without modifying or regenerating existing feature folders.

**Impact:**

- **Breaking changes:** No (docs-only)
- **Performance:** None
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp rg -n '^# Feature Specification|^# Technical Design|^# Development Tasks|^# Test Plan|^\\*\\*Status:\\*\\*' docs/02-features/17-resume-in-progress-tickets docs/02-features/18-commit-gated-by-completed-ticket-docs docs/02-features/19-template-drift-hardening-autofix-recovery docs/02-features/20-synthetic-feature-workflow-smoke-test`
- `tools/offload-proxy/pp rg -n '\\[Feature Name\\]|\\[Phase Name\\]|\\[unique-id\\]' docs/02-features/17-resume-in-progress-tickets docs/02-features/18-commit-gated-by-completed-ticket-docs docs/02-features/19-template-drift-hardening-autofix-recovery docs/02-features/20-synthetic-feature-workflow-smoke-test`

### 2026-02-11 - Side-effect-safe final gate sequencing and hermetic proposal tests

**Feature/Bug:** `pc-feature` final-gate reliability (`make feature F=17` late failure side effects)

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added `run_scoped_autofix_paths(...)` to support scoped autofix on explicit path lists without depending on pre-staged files.
- Changed final gate execution order in `pc-feature`:
  - run final `make ci` attempts in the patcher worktree (`cwd=patcher_path`),
  - run optional scoped autofix in patcher and commit patcher autofix deltas,
  - collect patcher branch into `main` only after CI gates pass.
- Preserved existing final gate retry cap and scoped-autofix constraints while removing pre-gate `main` collection side effects.
- Made `ProposalGenerationTests` hermetic by replacing the live `docs/possible-improvements.md` dependency with a fixed in-test template fixture.
- Updated gate regression coverage to assert CI runs in patcher cwd and collection is not invoked on final-gate failure.

**Why:**

- Prevent failed final gates from leaving partially collected changes on `main`.
- Eliminate flaky proposal-dedup tests caused by mutable repository log content.

**Impact:**

- **Breaking changes:** No
- **Performance:** Neutral (same final gate command count)
- **Dependencies:** None

**Testing:**

- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p "test_pc_feature.py"` (PASS, offload id `17a8ec41f09e37973a3a896ec4b15c325638f8da2cfc2f65a704f751c97ea614`)
- `tools/offload-proxy/pp make ci` (PASS, offload id `ba175e3a0d04c6934e3fb6a78a4d31209981be22425e6717288083c253dbc2bf`)

## 2026-02-12 - Harden reporter handoff gating and allowed-tests strictness

- Tightened `tools/pc-allowed-tests-check` so Allowed Tests must be explicit, existing unittest/pytest targets:
  - reject bare `python -m unittest`
  - reject `python -m unittest discover` without explicit `-s/--start-directory` (or positional start dir)
  - reject bare `pytest` / `python -m pytest` without explicit test targets
- Added runtime execution-record reconciliation in `tools/pc-feature` to remove placeholder drift during execution by auto-filling:
  - `Patch`, `Test Results`, `Reporter Review`
  - top fields: `Patcher`, `Tester`, `Reporter`, `Tests run`, `Docs/logs updated`
- Added deterministic reporter handoff gates in `tools/pc-feature`:
  - pre-reporter completeness gate blocks reporter review when pending placeholders or blank execution metadata remain
  - post-reporter gate blocks `PASS` when required compacted outputs are missing or reporter traceability evidence is absent
- Added compacted output requirement detection in `tools/pc-feature` that reads WI entry content (explicit paths and `docs/03-logs/compacted/*`) and validates required artifacts from a centralized resolver.
- Updated tests in:
  - `tests/test_pc_allowed_tests_check.py`
  - `tests/test_pc_feature.py`
- Cleaned `docs/possible-improvements.md` by removing implemented proposals and keeping unresolved proposals only.

### 2026-02-12 - Workflow visibility status/history + live step banners

**Feature/Bug:** `pc-feature` runtime observability during `make feature`

**Changed Files:**

- `tools/pc-feature`
- `lib/pc_runner.py`
- `tests/test_pc_runner.py`

**What Changed:**

- Added workflow run artifacts under `logs/<WI>/`:
  - `workflow-status.json` (current state + latest per-step status)
  - `workflow-history.ndjson` (append-only timestamped step events)
- Added workflow tracking APIs to `lib/pc_runner.py`:
  - `init_workflow_tracking(...)`
  - `record_workflow_event(...)`
- Instrumented `tools/pc-feature` with explicit step transitions and live terminal banners for:
  - `feature`, `preflight`, `planner`, `plan-reviewer`, `patcher`, `tester`, `reporter`
  - `planner-feedback`, `patcher-feedback`, `ci`, `collect`, `commit`
- Step banners now include UTC timestamp, work item id, attempt (when relevant), event (`START`/`DONE`/`SKIP`/`BLOCK`/`FAIL`), and duration when available.
- Added a safe fallback for tests that stub runner metadata so workflow-event printing remains available without requiring real metadata objects.

**Why:**

- Make it immediately clear which step is running, which steps have already run/skipped, and where time is spent during long workflow executions.

**Impact:**

- **Breaking changes:** No
- **Performance:** Minimal additional filesystem writes under `logs/<WI>/`
- **Dependencies:** None

**Testing:**

- `python3 -m py_compile tools/pc-feature lib/pc_runner.py tests/test_pc_runner.py`
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p 'test_pc_runner.py'` (PASS, offload id `4a160235c0add54f7a5997815d0e01a072210439de4899c702c94dd3cd814662`)
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p 'test_pc_feature.py'` (PASS, offload id `a947a5d4741195ea0d28566d69353961d4bbd84ae48821b42931bdabcb50ef78`)
- `tools/offload-proxy/pp make ci` (initial FAIL in sandbox due `end-of-file-fixer` permission on `.codex/skills/*`, offload id `d61fc2f6d5f3186a85e219fe4d3a559f5dc8910fc077dfa69a985d5fe9d8175f`)
- `tools/offload-proxy/pp make ci` (PASS with elevated permissions, offload id `b88f77275dba6b70b58f0d55f079f73712cdd8a830668c342cc762a8a1eb1bba`)
- `tools/offload-proxy/pp make ci` (PASS after docs/log updates, offload id `5eb834d7b6ba82210dd53b5b76b0f40281ca18acce6a10e815e0a077027d495e`)
- `tools/offload-proxy/pp make ci` (final PASS confirmation, offload id `93da6eaa2be7d177089c192f4e1dafbca6ac270c5537569438d5ea5ee9702f83`)

### 2026-02-12 - Add `pc-feature-status` CLI for workflow status/history (Milestone B)

**Feature/Bug:** runtime observability follow-up for `make feature`

**Changed Files:**

- `tools/pc-feature-status`
- `tests/test_pc_feature_status.py`

**What Changed:**

- Added a new CLI (`tools/pc-feature-status`) that reads workflow artifacts from `logs/<WI>/`:
  - `workflow-status.json` for current step/state snapshot
  - `workflow-history.ndjson` for timestamped execution events
- Implemented summary output with:
  - current step and attempt
  - last event details
  - per-step state snapshot
  - slowest-step ranking from recorded durations
- Implemented history output controls:
  - `--history` to print event timeline
  - `--limit` to bound timeline output
  - `--follow` with `--interval` for live tailing
  - `--wi` and `--root` for explicit run/workspace targeting
- Added focused unit tests validating summary formatting, history limiting, work-item resolution, invalid history-line handling, and CLI main-path output behavior.

**Why:**

- Provide a simple, stable way to answer:
  - which workflow step is currently running
  - whether steps like patcher have run
  - which steps are consuming the most time

**Impact:**

- **Breaking changes:** No
- **Performance:** Minimal read-only file I/O on demand
- **Dependencies:** None

**Testing:**

- `python3 -m py_compile tools/pc-feature-status tests/test_pc_feature_status.py`
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p 'test_pc_feature_status.py'` (PASS, offload id `0f7e4b97443e54aca647179972594d13bb587afcbf151fab8228148587ea844a`)
- `tools/offload-proxy/pp make ci` (initial FAIL in sandbox due `end-of-file-fixer` permission on `.codex/skills/*`, offload id `0b7cce23c8081d5523e16c9b7af5604af9ae9432dbcbe53af8152bea431d5c71`)
- `tools/offload-proxy/pp make ci` (PASS with elevated permissions, offload id `e69d854cfc627113acbde6f73426d4311f4aef893ca9d4079909bf2944963900`)
- `tools/offload-proxy/pp make ci` (final PASS after docs/log updates, offload id `c7d38aaaf677a46099189d9bb7c958199ccc839dbd7be869902792f78a876c79`)

### 2026-02-12 - Milestone C: simple status entrypoint + cross-worktree discovery

**Feature/Bug:** workflow observability usability when `make feature` runs in a patcher worktree

**Changed Files:**

- `tools/pc-feature-status`
- `tools/pc-feature`
- `Makefile`
- `tools/templates/root/Makefile`
- `tests/test_pc_feature_status.py`
- `tests/test_pc_feature.py`

**What Changed:**

- Upgraded `tools/pc-feature-status` to discover workflow logs across git worktrees (via `git worktree list --porcelain`) instead of checking only the current repo `logs/` directory.
- Added work-item resolution across discovered log roots so `--wi` and latest-run selection pick the most recent matching work item even when it lives in a sibling patcher worktree.
- Added `logs root:` to status output to make the artifact source explicit.
- Added `feature-status` make target as a thin wrapper over `tools/pc-feature-status`:
  - supports `WI`, `ROOT`, `HISTORY`, `FOLLOW`, `LIMIT`, `INTERVAL`.
- Added runtime usage hints in `tools/pc-feature` at workflow start:
  - `make feature-status WI=<id> FOLLOW=1`
  - `make feature-status WI=<id> HISTORY=1 LIMIT=30`
- Added regression tests for worktree discovery and for runtime monitor-hint printing.

**Why:**

- Milestone B provided a status CLI, but workflow artifacts are created in patcher worktrees during `make feature`; Milestone C makes status lookup simple from the main repo without requiring manual path hunting.

**Impact:**

- **Breaking changes:** No
- **Performance:** Minimal overhead from one local `git worktree list` subprocess on status command startup
- **Dependencies:** None

**Testing:**

- `python3 -m py_compile tools/pc-feature tools/pc-feature-status tests/test_pc_feature.py tests/test_pc_feature_status.py`
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p 'test_pc_feature_status.py'` (PASS, offload id `316558a93ba028238bcd514bbec8a07c6b5122f2fa8e4ce8499b5d85bc6111f8`)
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p 'test_pc_feature.py' -k main_manual_mode_prints_feature_status_hints_when_tracking_enabled` (PASS, offload id `9f75add94930d82f86f40553d972627172fa9fcad2415eaa9947d6de3d460011`)
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p 'test_pc_feature.py'` (PASS, offload id `b1a60c5bd49fb80d1d50b484854fd22beb4abdc318002de6eef7b586bcce4e14`)
- `make feature-status WI=WI-20260209-01 HISTORY=1 LIMIT=1` (PASS; command executes and resolves logs root across worktrees)
- `tools/offload-proxy/pp make ci` (initial FAIL due auto-format by `black`, offload id `21ed6f48a29469bc75bdd3cd205dcd99b5739c01bbfc0d567ff64f2c5b00c9a1`)
- `tools/offload-proxy/pp make ci` (PASS after formatting, offload id `518bd6e5fd3f606fc05a56e0d75a27d2cb2ae6740f1945c65d8517f84a48b4dc`)
- `tools/offload-proxy/pp make ci` (final PASS after docs/log updates, offload id `5b1851bcdff27b3a1a416547c44aaf017d5e598556036ebb3c25bbdaa34a47df`)

### 2026-02-12 - Fix Allowed Tests checker for dotted unittest selectors

**Feature/Bug:** `pc-feature` Allowed Tests retry loop (`make feature F=18`)

**Changed Files:**

- `tools/pc-allowed-tests-check`
- `tests/test_pc_allowed_tests_check.py`
- `prompts/planner-update-allowed-tests.md`
- `tools/templates/prompts/planner-update-allowed-tests.md`

**What Changed:**

- Extended `pc-allowed-tests-check` unittest target validation to accept dotted selectors such as:
  - `module.Class`
  - `module.Class.test_method`
    by resolving the longest existing module/package prefix.
- Added regression tests to cover:
  - accepted dotted class target
  - accepted dotted method target
  - rejected missing dotted prefix target
- Hardened planner Allowed Tests remediation prompt and template with explicit robust command shapes (file-path/discover examples) and rewrite guidance when dotted targets are flagged missing.

**Why:**

- Feature-18 reruns repeatedly failed with `blocked by invalid allowed tests` because `tests.test_pc_feature.TestPcFeature` was treated as missing by static checker logic.
- The checker needed to match valid unittest selector syntax to avoid wasting retry budget on false negatives.

**Impact:**

- **Breaking changes:** No
- **Performance:** Negligible
- **Dependencies:** None

**Testing:**

- `tools/pc-allowed-tests-check --cmd 'python3 -m unittest tests.test_pc_feature.TestPcFeature' --cmd 'python3 -m unittest tests.test_pc_feature.TestPcFeature.test_plan_reviewer_approve_allows_patch'` (PASS)
- `tools/pc-allowed-tests-check --cmd 'python3 -m unittest tests.test_missing.SampleTests'` (FAIL as expected)
- `tools/offload-proxy/pp python3 -m unittest tests/test_pc_allowed_tests_check.py` (PASS, offload id `f196bef0973ff999dcbcf679ca035393cbb4be84e582dd7f9d09005e1f656ac4`)

### 2026-02-12 - Prevent reporter retry loops from planner-owned `dev-tasks.md` resets

**Feature/Bug:** `pc-feature` reporter retries exhausted on closure-only failures (`make feature F=18`)

**Changed Files:**

- `tools/pc-feature`
- `tools/templates/prompts/reporter-review.md`
- `tests/test_pc_feature.py`

**What Changed:**

- Reworked reporter-step sequencing in `tools/pc-feature` so reporter role-log commits happen before runtime reconciliation writes to planner-owned `dev-tasks.md`.
- Added finalization-only reporter failure normalization:
  - if reporter returns `FAIL` for only `Commit`/`Final Report`/final-gate placeholders, normalize to non-blocking `PASS` and continue.
  - if reporter feedback references real handoff gaps (`Reporter Review`, `Test Results`, compacted-output traceability), keep fail-closed behavior.
- Added regression coverage for:
  - reporter commit ordering relative to `dev-tasks.md` runtime reconciliation
  - finalization-only reporter `FAIL` normalization (no planner-feedback retry loop)
  - finalization-only classifier true/false fixture cases
- Updated reporter prompt guidance to explicitly mark `Commit` / `Final Report` / final `Gates` completion as post-reporter ownership.

**Why:**

- Reporter commits were auto-resetting dirty planner-owned `dev-tasks.md` and discarding runtime reconciliation, causing repeated reporter failures with no net progress.
- Some reporter failures were non-actionable (finalization-owned placeholders) and should not consume retry budget.

**Impact:**

- **Breaking changes:** No
- **Performance:** Negligible
- **Dependencies:** None

### 2026-02-12 - Quiet lint/formatter output with concise failure logs

**Feature/Bug:** Reduce lint/formatter noise while keeping failure output actionable.

**Changed Files:**

- `tools/pc-hooks-run`
- `Makefile`
- `tools/templates/root/Makefile`
- `.pre-commit-config.yaml`
- `tools/templates/root/.pre-commit-config.yaml`
- `tools/markdown-lint`
- `tools/pc-devtasks-schema-check`
- `tests/test_pc_hooks_run.py`
- `tests/test_markdown_lint.py`
- `tests/test_pc_devtasks_schema_check.py`

**What Changed:**

- Added `tools/pc-hooks-run`, a pre-commit runner that:
  - emits no output on success,
  - captures full failing output to `.offload/<sha>.txt`,
  - appends an index entry to `.offload/index.jsonl`,
  - prints only concise failure lines plus an offload id/path reference.
- Updated `make lint` and `make fmt` to call the new runner; added `lint-verbose` and `fmt-verbose` for full raw output when needed.
- Removed routine success `echo` lines from `docs-check`, `check`, and `ci` targets in root/template `Makefile` files to reduce non-actionable noise.
- Tuned pre-commit config (root + template):
  - set `default_stages: [pre-commit]` so manual runs stay formatter-focused,
  - added quieter output flags for Ruff/Black/Prettier.
- Updated local checks for quiet-success behavior:
  - `tools/markdown-lint` now defaults to silent success and supports `--verbose`.
  - `tools/pc-devtasks-schema-check` now defaults to silent success and supports `--verbose`.
- Added regression tests covering:
  - `pc-hooks-run` summary filtering and offload behavior,
  - quiet/verbose behavior for markdown lint and devtasks schema check.

**Why:**

- `pre-commit` prints per-hook `Passed/Skipped` lines by default, which obscures real issues during normal runs.
- The workflow objective is quiet-green, loud-red: no output when healthy, concise and actionable output when broken, with full raw logs available by pointer.

**Impact:**

- **Breaking changes:** Low (new default is less output; verbose fallbacks are available).
- **Performance:** Minimal overhead from capturing output and writing failure logs only on non-zero exits.
- **Dependencies:** None.

**Testing:**

- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p "test_pc_hooks_run.py"` (PASS, offload id `1f2a80ee431a938177aa3d87b706572be68a7b4d039f263b63fc396b7e1bae19`)
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p "test_markdown_lint.py"` (PASS, offload id `5279d1fc9a1ced44f9c96da1414ef59e4676f963fbad52e7a1a2903538819b0d`)
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p "test_pc_devtasks_schema_check.py"` (PASS, offload id `4c979c0d06f0e9e2109df48cae7f69ac5d403754045b4cfe404fe744e7390b47`)
- `tools/pc-hooks-run --hook-stage pre-commit --files .pre-commit-config.yaml Makefile tests/test_pc_hooks_run.py tools/pc-hooks-run` (PASS, expected no output)
- `tools/offload-proxy/pp pre-commit run --files .pre-commit-config.yaml Makefile tests/test_pc_devtasks_schema_check.py tools/markdown-lint tools/pc-devtasks-schema-check tools/templates/root/.pre-commit-config.yaml tools/templates/root/Makefile tests/test_markdown_lint.py tests/test_pc_hooks_run.py tools/pc-hooks-run` (PASS, offload id `b93bd152e7e73a9496a95d0054a65d983a017bc4739052add876f486fc163ed9`)
- `tools/offload-proxy/pp make lint` (PASS with elevated permissions; no stdout/stderr due quiet-green behavior)
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p "test_docs_logs.py"` (PASS, offload id `72f09eca554e87a45b7156c6109520cf15e8b6ec157dc5c033610649b49b8698`)

### 2026-02-12 - Add opt-in stale worktree sync mode for feature resume

**Feature/Bug:** Preserve in-progress feature work while allowing restart when patcher worktree is behind `main`.

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Added `RESUME_MODE=sync` as an opt-in startup policy in `pc-feature`.
- In stale existing patcher worktrees (`behind main`), `sync` mode now:
  - checkpoints dirty startup state with `checkpoint_resume_state`,
  - runs `git merge --no-edit refs/heads/main` in the patcher worktree,
  - aborts with a clear manual-resolution message if merge fails,
  - verifies the patcher branch is no longer behind before continuing.
- Kept default `RESUME_MODE=auto` semantics unchanged (still fails fast when stale).
- Added lock-note refresh behavior after successful stale sync resume so `Main head locked:` is updated instead of failing on expected lock mismatch.
- Added regression tests for:
  - resume-mode parser support for `sync`,
  - stale auto-mode fail-fast behavior,
  - stale sync-mode merge-and-continue path,
  - lock-note refresh after stale sync resume.

**Why:**

- Users restarting a long-running feature branch currently hit a hard stop if `main` advanced, even when they want to keep WIP and continue.
- `sync` provides a deterministic, opt-in continuation path without weakening strict default behavior.

**Impact:**

- **Breaking changes:** None (default remains `auto`).
- **Performance:** Small startup overhead only when `RESUME_MODE=sync` and stale branch detected.
- **Dependencies:** None.

### 2026-02-12 - Add explicit feature command help entrypoints

**Feature/Bug:** Improve discoverability of `make feature` options as resume behavior grows.

**Changed Files:**

- `Makefile`
- `tools/templates/root/Makefile`
- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Added `tools/pc-feature --help` / `-h` support with a concise usage block covering:
  - required args (`F=<feature-id>`, `MANUAL=1`),
  - all `RESUME_MODE` values (`auto`, `prompt`, `fresh`, `sync`),
  - related env vars (`RESUME_CONTRADICTION_POLICY`, `RESUME_REPAIR_DRY_RUN`).
- Updated `make` entrypoints:
  - new `feature-help` target,
  - `feature` target now supports `HELP=1|true|yes` to print feature help instead of executing orchestration.
- Synced root template Makefile behavior with the live Makefile.
- Added parser tests validating help output and zero-exit behavior for `--help`/`-h`.
- Documented operator guidance in process docs, including the GNU Make limitation where `make feature --help` invokes Make’s own help.

**Why:**

- `make feature` gained multiple policy and resume controls and needed a first-class, local help surface.
- GNU Make reserves `--help`, so equivalent explicit entrypoints are required for reliable operator help.

**Impact:**

- **Breaking changes:** None.
- **Performance:** None.
- **Dependencies:** None.

### 2026-02-12 - Split final-gate autofix candidates from collection scope

**Feature/Bug:** Recurring `patcher edited role-scoped files` abort during final CI autofix (`make feature F=18`).

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added `collect_patcher_autofix_paths(...)` to derive final-gate autofix candidates from branch diffs while filtering patcher-forbidden role-scoped/global-log files.
- Switched final-gate autofix candidate selection to the new helper so scoped pre-commit never receives planner-owned files like `dev-tasks.md`.
- Added explicit runtime diagnostics when forbidden paths are skipped from autofix candidate lists.
- Preserved final collection semantics by leaving `collect_branch_merge_paths(...)` behavior unchanged for branch collection into `main`.
- Added regression coverage for:
  - role-scoped filtering in autofix candidate selection,
  - mixed safe/forbidden candidate lists (safe paths still autofixed),
  - all-forbidden candidate lists (autofix skipped, no patcher scope crash).

**Why:**

- Final-gate autofix previously reused collection path selection, which intentionally included runtime feature docs; this allowed role-scoped files into patcher autofix and caused recurring late scope aborts.

**Impact:**

- **Breaking changes:** None.
- **Performance:** Negligible (single in-memory filter over candidate path list).
- **Dependencies:** None.

**Testing:**

- `python3 -m py_compile tools/pc-feature tests/test_pc_feature.py` (PASS)
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p "test_pc_feature.py"` (PASS, offload id `90f84f11268b4fd5850cf20d292ecf3468a0f987819ec31265777f598530980f`)

### 2026-02-12 - Fix Python-3.9 hook compatibility and scoped-autofix false positives

**Feature/Bug:** Feature-18 execution failed on `markdown-lint` import under Python 3.9 and raised false final-gate scoped-autofix out-of-scope errors for pre-existing dirty `dev-tasks.md`.

**Changed Files:**

- `tools/markdown-lint`
- `tools/pc-allowed-tests-check`
- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `tests/test_tools_python_compat.py`

**What Changed:**

- Added `from __future__ import annotations` to Python tool scripts using `| None` annotations so they load safely on Python 3.9.
- Updated `run_scoped_autofix_paths(...)` in `tools/pc-feature` to compare pre/post dirty snapshots and fail only when out-of-scope files are touched during autofix.
- Added regression coverage for:
  - blocking new out-of-scope touched files during scoped autofix,
  - allowing pre-existing out-of-scope dirty files when untouched,
  - static guard that Python tools using `| None` require `__future__.annotations`,
  - runtime check that `tools/markdown-lint` executes under system Python 3.9.

**Why:**

- Execution environments can resolve `python3` to 3.9 in feature worktrees, and 3.10+ union syntax without postponed annotations causes immediate hook crashes.
- Final-gate scoped-autofix guard must distinguish newly touched files from pre-existing dirty state to avoid false aborts.

**Impact:**

- **Breaking changes:** None.
- **Performance:** Minimal (two dirty snapshots around scoped autofix).
- **Dependencies:** None.

**Testing:**

- `python3 -m py_compile tools/markdown-lint tools/pc-allowed-tests-check tools/pc-feature tests/test_pc_feature.py tests/test_tools_python_compat.py` (PASS)
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p "test_markdown_lint.py"` (PASS, offload id `5279d1fc9a1ced44f9c96da1414ef59e4676f963fbad52e7a1a2903538819b0d`)
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p "test_tools_python_compat.py"` (PASS, offload id `92b391eabf11e0e952252fb6ee05522765579df0b6b0a838ff1f3e4150550b42`)
- `tools/offload-proxy/pp python3 -m unittest discover -s tests -p "test_pc_feature.py" -k scoped_autofix` (PASS, offload id `f2f7f20b09268ff1a5a9edf399b32bb047568b9780fc65a6c38dee4a6be91892`)
- `tools/offload-proxy/pp pre-commit run --files tools/markdown-lint tools/pc-allowed-tests-check tools/pc-feature tests/test_pc_feature.py tests/test_tools_python_compat.py` (PASS, offload id `5be5793f628b9d4ee932bfdfe3d69d9de33c933369d362c2f433acbc61914036`)

- WI-20260212-02: Implemented and integrated the completed feature changes across the intended scope with docs/process alignment.

### 2026-02-12 - Fix final commit pathspec failures for absent runtime allow prefixes

**Feature/Bug:** `make feature` could fail during final commit with `fatal: pathspec '.tmp' did not match any files` when runtime allow prefixes were passed to `tools/pc-commit` but were not present in the worktree.

**Changed Files:**

- `tools/pc-commit`
- `tools/pc-feature`
- `tests/test_pc_commit.py`
- `tests/test_pc_feature.py`

**What Changed:**

- Updated `tools/pc-commit` to stage only currently changed paths that match `--allow` rules, instead of running `git add` directly on raw allow values.
- Normalized allow entries by trimming trailing `/` before path matching.
- Hardened shell helpers for Bash 3 + `set -u` compatibility when allowed/disallowed path arrays are empty.
- Updated final commit execution in `tools/pc-feature` to use `run_command_with_step_log_capture`, and to include first-line `pc-commit` failure detail in workflow failure reasons.
- Added regression coverage for:
  - missing allow path (`--allow .tmp`) not causing commit failure,
  - prefix allow path behavior (`--allow logs/`),
  - surfaced `pc-commit` failure detail in `pc-feature` commit failure events.

**Why:**

- `--allow` values represent policy scope, not guaranteed filesystem pathspecs. Coupling those values directly to `git add` introduced a deterministic late-failure path in finalization.

**Impact:**

- **Breaking changes:** None.
- **Performance:** Negligible (single status scan before staging).
- **Dependencies:** None.

- WI-20260212-03 completed: documentation patching flow now enforces commit gating on completed ticket state across the targeted workflow.

### 2026-02-12 - Target active work-item commit gate and fail fast with actionable commit errors

**Feature/Bug:** `make feature F=18` commit step failed by validating stale `WI-...-01` instead of active `WI-...-03`, emitted shell backtick errors in remediation text, and surfaced unrelated noisy details in commit failure reason.

**Changed Files:**

- `tools/pc-commit`
- `tools/pc-feature`
- `lib/pc_runner.py`
- `tests/test_pc_commit.py`
- `tests/test_pc_feature.py`

**What Changed:**

- Added `--work-item-id WI-YYYYMMDD-NN` to `tools/pc-commit`.
- Updated commit-evidence gate selection logic:
  - if `--work-item-id` is provided, validate that exact work-item entry,
  - if not provided, auto-select the newest work item by WI id sort key (date + sequence), independent of markdown section ordering.
- Added explicit failure when requested work-item entry is missing.
- Moved commit-evidence gate execution to run before `make check` (fail-fast), and kept post-check validation to stay fail-closed if files change during checks.
- Fixed remediation output quoting so required section names are literal text (no shell command substitution).
- Updated `tools/pc-feature` final commit call to pass `--work-item-id`.
- Added `extract_command_failure_detail(...)` in `tools/pc-feature` so failure reasons prefer actionable lines (`Commit evidence gate failed`, `fatal:`, traceback/error markers) over noisy first output lines.
- Replaced deprecated `datetime.utcnow()` with timezone-aware UTC in `lib/pc_runner.py`.

**Why:**

- The gate must validate the active execution entry, not whichever WI block happens to be last in file order.
- Commit failures must be actionable in workflow status without requiring deep log spelunking.
- Gate failures should stop early to avoid wasting CI/test runtime.

**Impact:**

- **Breaking changes:** `tools/pc-commit` now accepts `--work-item-id` (additive); explicit unknown work item fails fast with clear message.
- **Performance:** Improved on failing runs via pre-check gate short-circuit.
- **Dependencies:** None.

- WI-20260212-04: Completed reporter handoff by preparing concise global log summaries for orchestrator consolidation with no code or file changes.

### 2026-02-13 - Stabilize commit-evidence validation and finalization auto-repair

**Feature/Bug:** Feature-18 commit gating produced misleading status parsing (`Outcome=- Tests run:`) and could validate stale main `dev-tasks.md` content after patcher finalization updates.

**Changed Files:**

- `lib/commit_evidence_gate.py`
- `tools/pc-commit`
- `tools/pc-feature`
- `tests/test_pc_commit.py`
- `tests/test_pc_feature.py`

**What Changed:**

- Added shared commit-evidence validation helpers in `lib/commit_evidence_gate.py` and wired both `pc-commit` and `pc-feature` to the same gate rules.
- Hardened label parsing to line-scoped capture (`[ \t]*`) so blank fields no longer consume the next execution-log line.
- Added deterministic commit-evidence auto-repair in `pc-feature` to populate missing top fields/sections from tester and reporter artifacts before final gate evaluation.
- Added outcome normalization during finalization: stale non-completed top `Outcome` values are reconciled to `pass` when CI + tester/reporter evidence indicates completed state.
- Synced finalized patcher `dev-tasks.md` back into main worktree before final staging to prevent stale evidence checks after collect.
- Added regression tests for multiline parse safety, missing outcome enforcement, artifact-backed auto-repair, and worktree-to-root file sync.

**Why:**

- Commit evidence diagnostics must be deterministic and accurate.
- Final commit must validate the same finalized work-item content that gets staged.

**Impact:**

- **Breaking changes:** None (behavior is stricter/clearer but backward-compatible for valid entries).
- **Performance:** Negligible (single deterministic repair pass).
- **Dependencies:** None.

### 2026-02-13 - Expand sync-mode lock reconciliation semantics

**Feature/Bug:** `RESUME_MODE=sync` still failed on locked-main mismatch unless the startup path had first classified the patcher worktree as stale.

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Updated locked-main mismatch handling in `tools/pc-feature`:
  - `RESUME_MODE=sync` now always attempts reconciliation at lock-check time.
  - Re-checks behind-state during lock reconciliation; if behind, checkpoints and merges `refs/heads/main` before refreshing lock.
  - If not behind, refreshes `Main head locked:` directly without forcing a stale-start path.
- Kept strict fail-closed behavior for non-sync modes and added behind-state + remediation hint in mismatch errors.
- Updated help text and process protocol docs to describe sync mode as explicit drift reconciliation, not only stale-start merge handling.
- Added regression coverage for:
  - sync lock refresh when lock mismatches but branch is not behind,
  - sync lock mismatch failure when behind-state merge fails.

**Why:**

- Operators set `RESUME_MODE=sync` specifically to acknowledge and reconcile main drift.
- Requiring startup stale classification for lock refresh created inconsistent behavior and confusing failures.

**Impact:**

- **Breaking changes:** None (default behavior remains strict under `auto`/`prompt`).
- **Performance:** Minimal extra behind-state check during lock mismatch in sync mode.
- **Dependencies:** None.

- WI-20260213-05 completed: implemented the planned feature changes end-to-end and integrated them without expanding scope.

### 2026-02-13 - Harden commit auto-repair against stale section outcomes

**Feature/Bug:** Commit-gate runs could still fail with `Outcome=needs replan` after successful reruns when `Reporter Review` or `Test Results` outcomes were stale but non-pending.

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`

**What Changed:**

- Added `reconcile_section_outcome_from_artifact(...)` in `pc-feature` commit repair flow to refresh non-pending `Test Results` and `Reporter Review` outcomes from latest role artifacts when they drift.
- Updated commit-repair outcome derivation to prefer role-artifact outcomes over stale section outcomes.
- Added regression coverage for stale reporter-review mismatch (`section FAIL` + `artifact PASS`) to ensure commit-evidence repair converges to `Outcome: completed`.
- Added terminal reporter workflow event emission (`DONE`/`FAIL`) in the non-skip reporter path for consistent workflow-status closure.
- Documented commit auto-repair reconciliation semantics in both live and template ticket-execution protocol docs.

**Why:**

- Existing repair logic handled pending placeholders but not stale non-pending section outcomes, which could keep top outcome blocked and trigger false commit-gate failures.

**Impact:**

- **Breaking changes:** None (strict gate semantics remain fail-closed).
- **Performance:** Negligible (small artifact/section comparison at commit repair time).
- **Dependencies:** None.

### 2026-02-13 - Add chat-first Investigate skill for output diagnosis and durable fix planning

**Feature/Bug:** Repeated manual diagnosis flow in Codex chat needed a standardized, plan-only investigation skill.

**Changed Files:**

- `.codex/skills/investigate/SKILL.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Added a new `investigate` skill with a strict inline input contract: command text and raw output text passed directly in one prompt.
- Defined a deterministic investigation sequence: issue detection, root-cause hypotheses, expected-vs-actual comparison against repo docs, and multiple permanent fix options.
- Added mandatory docs-conflict handling: cite conflicting docs, explain impact, and propose documentation improvement.
- Added decision gating: ask focused questions when a decision is required and avoid autonomous path selection.
- Added explicit guardrails: no code edits, no fix-command execution, no hook/process modification, and recommendations-only auto-fix proposals.

**Why:**

- Replace repeated ad-hoc analysis prompts with a single reusable skill.
- Keep execution safe and non-destructive while still producing durable remediation options.
- Ensure diagnosis remains aligned to documented project expectations and process rules.

**Impact:**

- **Breaking changes:** None.
- **Performance:** N/A (instructional skill only).
- **Dependencies:** None.

- WI-20260213-05 completed: implemented the feature scope end-to-end with focused, traceable changes aligned to ticket requirements.

### 2026-02-13 - Add `workflow-hardening-top5` chat-only skill for process hardening recommendations

**Feature/Bug:** Create a reusable read-only skill that analyzes the project improvement backlog and prioritizes workflow hardening work without proposing product feature expansion.

**Changed Files:**

- `.codex/skills/workflow-hardening-top5/SKILL.md`
- `.codex/skills/workflow-hardening-top5/agents/openai.yaml`

**What Changed:**

- Initialized a new skill scaffold at `.codex/skills/workflow-hardening-top5`.
- Replaced the template `SKILL.md` with a strict read-only, chat-only contract.
- Added deterministic selection rules: deduplication by root problem, workflow-only filtering, and prioritization by recurrence/impact/prevention/safety.
- Enforced output contract to return up to 5 recommendations (fewer allowed when evidence is insufficient), each with rationale, benefits, risks, no-side-effect rollout, and evidence references.
- Added guardrails to prohibit file edits, patch commands, auto-implementation, and roadmap feature additions.

**Why:**

- Repeated failure patterns in `docs/possible-improvements.md` benefit from a consistent prioritization method that emphasizes robustness and stability instead of scope growth.
- A dedicated skill reduces ad-hoc recommendation quality variance across chats.

**Impact:**

- **Breaking changes:** None.
- **Performance:** N/A (instructional skill only).
- **Dependencies:** None.

### 2026-02-13 - Harden Allowed Tests templates and feature-19 targets without runtime auto-fix

**Feature/Bug:** Feature 19 orchestration blocked on invalid Allowed Tests target (`tests.test_pc_precommit` missing).

**Changed Files:**

- `docs/02-features/19-template-drift-hardening-autofix-recovery/dev-tasks.md`
- `docs/02-features/19-template-drift-hardening-autofix-recovery/test-plan.md`
- `docs/02-features/feature-template/dev-tasks.md`
- `tools/templates/docs/02-features/feature-template/dev-tasks.md`
- `tools/pc-devtasks-schema-check`
- `tests/test_pc_devtasks_schema_check.py`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Replaced Feature 19 Allowed Tests commands with existing deterministic unittest-discover targets:
  - `test_pc_autofix.py`
  - `test_pc_feature.py`
  - `test_pc_hooks_run.py`
- Expanded both live and template `dev-tasks.md` Allowed Tests guidance to require:
  - explicit test commands,
  - validator compatibility (`tools/pc-allowed-tests-check`),
  - explicit forbidden-command reminders.
- Added a deterministic template guard in `pc-devtasks-schema-check` for Allowed Tests guidance markers.
- Added regression coverage in `test_pc_devtasks_schema_check.py` for missing template Allowed Tests guidance.
- Recorded decision to avoid runtime auto-fix heuristics for Allowed Tests in favor of template+validation hardening.

**Why:**

- Prevent repeated work-item failures from stale/non-existent Allowed Tests targets.
- Ensure next generated features inherit correct Allowed Tests guidance by construction.
- Keep behavior safe and predictable by avoiding heuristic auto-rewrites.

**Impact:**

- **Breaking changes:** None to `pc-feature` runtime flow.
- **Performance:** Negligible (small extra schema checks on template content).
- **Dependencies:** None.

### 2026-02-13 - Auto-repair-first reporter completeness gate and explicit human decision options

**Feature/Bug:** Reporter and tester retry loops could hard-stop on metadata/closeout drift without a deterministic repair pass, and retry-limit messages did not present explicit decision options with risks.

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Added reporter gate issue classification helpers to separate deterministic auto-repairable issues (pending placeholders, missing outcome lines, blank top execution fields) from non-repairable issues (missing compacted outputs, missing traceability evidence).
- Added a pre-handoff and post-review auto-repair pass in `pc-feature` using role-artifact reconciliation before converting reporter checks into hard FAIL outcomes.
- Added shared decision-option builders and injected decision options + risks into:
  - reporter handoff block feedback,
  - tester retry-limit notes/errors,
  - reporter retry-limit notes/errors.
- Added new tests for:
  - reporter issue classification,
  - decision options in reporter block feedback,
  - reporter metadata auto-repair resolving post-review issues,
  - retry-limit output containing decision options.

**Why:**

- Enforce auto-repair-first behavior for closeout metadata drift and reduce avoidable retry-loop exhaustion.
- Make PO/human intervention actionable when retries are exhausted by surfacing concrete options and trade-offs inline.

**Impact:**

- **Breaking changes:** None (existing fail-closed behavior remains for non-repairable issues).
- **Performance:** Negligible (small additional in-memory reconciliation/check passes).
- **Dependencies:** None.

### 2026-02-13 - Add no-side-effect auto-repair modes and one-pass guard for reporter gate

**Feature/Bug:** Reporter auto-repair needed explicit no-side-effect operation modes (`off`/`warn`/`apply`), strict update allowlisting, and bounded single-pass execution per attempt.

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Added `AUTO_REPAIR_REPORTER_GATE` environment control with validated values:
  - `off` (default, no auto-repair mutation),
  - `warn` (compute repair preview/ledger, no mutation),
  - `apply` (allowlisted deterministic repair applied).
- Added strict reporter auto-repair allowlist (`REPORTER_AUTO_REPAIR_ALLOWED_UPDATES`) and update classification to block non-allowlisted mutations from being auto-applied.
- Added reporter auto-repair ledger generation with mode/stage/applied status, issue signatures, proposed/disallowed updates, and risk tags.
- Replaced direct pre/post reporter repair calls with a unified `run_reporter_auto_repair_pass(...)` helper.
- Enforced max one reporter auto-repair pass per attempt via a per-attempt consumption guard.
- Added tests for:
  - default mode resolution (`off`),
  - `warn` no-side-effect behavior,
  - `apply` metadata repair behavior.

**Why:**

- Support safe rollout with shadow preview first and explicit promotion control.
- Prevent unintended mutations by constraining auto-repair to deterministic, allowlisted execution metadata updates.
- Bound risk by limiting repair attempts and preserving explicit decision options when unresolved.

**Impact:**

- **Breaking changes:** None (`off` default keeps behavior conservative unless opt-in mode is set).
- **Performance:** Negligible (single additional classification/preview pass per eligible reporter attempt).
- **Dependencies:** None.

### 2026-02-13 - Preflight scope sanitization + reviewer policy auto-recovery hardening

**Feature/Bug:** Reviewer policy blocks could loop on forbidden plan paths seeded from preflight `files_to_change` (role/global-log paths), then terminate via stagnation.

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `prompts/planner-create.md`
- `prompts/planner-update-from-feedback.md`
- `prompts/plan-reviewer-gate.md`
- `tools/templates/prompts/planner-create.md`
- `tools/templates/prompts/planner-update-from-feedback.md`
- `tools/templates/prompts/plan-reviewer-gate.md`
- `docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/human-orchestration-workflow.md`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Added deterministic preflight sanitization in `pc-feature`:
  - filters `files_to_change` to patcher-allowed paths,
  - shifts forbidden role/global-log targets into reporter/orchestrator handoff notes.
- Refined plan path-policy scanning:
  - scans `Files to change` + explicit write-intent lines,
  - avoids blocking handoff-only docs/log references when patcher non-edit ownership is explicit.
- Added reviewer-loop policy recovery helpers:
  - deterministic forbidden-path removal from `Files to change`,
  - automatic docs handoff note insertion,
  - policy-diff diagnostics in iteration logs,
  - deterministic recovery plan template injection after repeated identical policy signatures.
- Updated planner/reviewer prompts (and template prompt copies) to reinforce sanitized scope + handoff semantics.
- Updated process docs to document preflight auto-sanitization and deterministic reviewer-policy recovery behavior.
- Added/updated unit tests for:
  - preflight sanitization,
  - policy rewrite/template compliance,
  - reference-only path handling,
  - stagnation behavior under persistent unresolved policy signatures.

**Why:**

- Prevent avoidable planner/reviewer stagnation caused by policy-incompatible file scope propagation.
- Keep strict policy enforcement while relying on deterministic auto-repair instead of manual fail-fast handling.

**Impact:**

- **Breaking changes:** None intended; enforcement remains fail-closed when unresolved.
- **Performance:** Negligible (small additional string processing in reviewer loop).
- **Dependencies:** None.

### 2026-02-13 - Resume-plan stability + planner-create validation hardening

**Feature/Bug:** Planner/reviewer loops on feature 19 were caused by malformed non-contract plan text, false command-policy positives, and resume forcing full planner-create despite an existing plan.

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/human-orchestration-workflow.md`
- `docs/04-process/dev-workflow.md`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Added deterministic resume policy helper so planner-create is forced after tester `FAIL` only when `Plan` is incomplete.
- Added planner-create output validation gate before writing `#### Plan`:
  - required `Plan Contract v1` sections,
  - anti-hardcode coverage checks (when enforced),
  - plan policy checks (including allowed-tests alignment when available).
- Hardened command-policy parsing:
  - avoids false positives from path-like tokens such as `pc-hooks-run`,
  - still blocks explicit `make feature`/`pc-feature`/`tools/pc-feature` command intent.
- Extended policy auto-rewrite:
  - can replace malformed non-contract plans with deterministic recovery template,
  - keeps existing forbidden-files rewrite and docs handoff note behavior.
- Added prompt-template candidate fallback across `_`/`-` separators only when one variant is missing; exact filenames remain authoritative when both variants exist.
- Added/updated regression tests for:
  - malformed-plan recovery,
  - command/path parsing behavior,
  - forced contract validation for planner-create,
  - resume planner-create guard,
  - prompt variant fallback behavior.

**Why:**

- Stop recurring reviewer `BLOCK` loops caused by malformed plan payloads and parser edge cases.
- Keep resume flow stable and deterministic after tester failures.
- Preserve strict policy enforcement while reducing non-actionable false positives.

**Impact:**

- **Breaking changes:** None intended; policy remains fail-closed.
- **Performance:** Negligible (extra validation and lightweight regex checks).
- **Dependencies:** None.

- WI-20260213-01 completed: implemented the approved feature scope end-to-end with no unresolved blockers.

### 2026-02-13 - Planner-create contract hardening, rejection artifacting, and fail-state correctness

**Feature/Bug:** Planner-create failure diagnostics and state handling (smoke workflow hardening).

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `prompts/planner-create.md`
- `prompts/planner-update-from-feedback.md`
- `prompts/planner-update_from_feedback.md`
- `tools/templates/prompts/planner-create.md`
- `tools/templates/prompts/planner-update-from-feedback.md`
- `tools/templates/prompts/planner-update_from_feedback.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Updated plan-contract section matching in `pc-feature` to accept heading label lines after deterministic markdown list/indent normalization.
- Added deterministic planner-create rejection artifact writer:
  - path: `logs/<WI>/planner-create-rejection.md`
  - payload: UTC timestamp, quality issues, and raw planner output.
- Hardened planner-create failure path:
  - reverts unexpected `dev-tasks.md` side effects before exiting,
  - emits explicit `planner FAIL` and `feature FAIL` workflow events with `state=FAILED`,
  - extends terminal error text with rejection artifact pointer.
- Added regression tests for:
  - bulleted heading acceptance in contract section detection,
  - planner-create rejection artifact generation,
  - planner-create quality-failure behavior (side-effect rollback + failed workflow events).
- Canonicalized planner contract examples in live/template prompts so section headings are consistently emitted at column 1.
- Updated process protocol docs (live + template copy) to codify normalized heading matching, rejection artifacting, failed-state behavior, and no-persist guarantee for rejected planner-create output.

**Why:**

- Fixes the observed smoke-run failure mode where planner-create contract rejection lacked durable diagnostics and could leave ambiguous runtime state.

**Impact:**

- **Breaking changes:** None intended; planner quality gate remains fail-closed.
- **Performance:** Negligible (small string normalization + small markdown artifact write on failure only).
- **Dependencies:** None.

- WI-20260213-01 completed: delivered the planned feature scope end-to-end with required code and documentation updates.

### 2026-02-14 - Update `investigate` skill to accept issue descriptions without CLI output

**Feature/Bug:** Skill contract was too restrictive for outcome failures without useful CLI output.

**Changed Files:**

- `.codex/skills/investigate/SKILL.md`
- `.codex/skills/investigate/references/investigation-rubric.md`
- `.codex/skills/investigate/agents/openai.yaml`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Expanded `investigate` input contract with two supported modes:
  - CLI-evidence mode (`command` + `output`, preferred).
  - Description-only mode (`issue`) when output is unavailable.
- Added free-text compatibility (`$investigate <description>`) by normalizing free text to `issue`.
- Updated step logic to rank hypotheses from available evidence:
  - prioritize `output` evidence when present,
  - otherwise use `issue/context` and mark assumptions explicitly.
- Updated rubric language to avoid output-only dependency and require confidence caveats when output is absent.
- Updated `agents/openai.yaml` labels/prompts to reflect broader trigger and usage.

**Why:**

- Enables investigation of silent failures and bad outcomes where command execution appears successful but artifacts or behavior are wrong.

**Impact:**

- **Breaking changes:** None intended; existing `command/output` usage still works.
- **Performance:** None.
- **Dependencies:** None.

### 2026-02-14 - Enforce hydrate-only `prd-to-features` generation by default

**Feature/Bug:** PRD-to-features produced template-only feature folders without
feature-specific adaptation.

**Changed Files:**

- `tools/prd-to-features`
- `tests/test_prd_to_features.py`
- `.codex/skills/prd-to-features/SKILL.md`
- `.codex/skills/prd-to-features/references/selection-and-update-rules.md`
- `docs/02-features/AGENTS.md`
- `tools/templates/docs/02-features/AGENTS.md`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/decision-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Reworked `tools/prd-to-features` so core feature docs (`feature-spec.md`,
  `tech-design.md`, `dev-tasks.md`, `test-plan.md`) are deterministically
  hydrated with feature-specific content on creation.
- Added placeholder/incomplete-content detection for existing non-done feature
  folders so template-like docs are updated in place without destructive
  overwrites.
- Added product-surface inference and checkbox hydration for generated docs.
- Added log-aware skip detection from `docs/03-logs/implementation-log.md` and
  `docs/03-logs/decision-log.md` for completed/rejected/deferred features.
- Expanded status parsing to recognize both `Status:` and `**Status:**`.
- Added/updated unit coverage for hydrated output, deferred-log skipping, and
  bold-status done skipping.
- Updated skill/rules/docs contracts to make hydrate-only behavior explicit and
  mark skeleton-only output as invalid.

**Why:**

- Align implementation with documented selection/hydration expectations and
  prevent low-value template-only feature generation.

### 2026-02-14 - Bootstrap runtime `lib/` modules with tooling sync

**Feature/Bug:** `make feature` bootstrap crash in downstream repos (`ModuleNotFoundError: No module named 'lib'`).

**Changed Files:**

- `tools/bootstrap-into`
- `tests/test_bootstrap_into.py`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Updated bootstrap sync policy so `lib/` paths are treated like runtime tooling sync targets.
- Added explicit copy phase for top-level `lib/` during bootstrap (`copy_dir_files "$repo_root/lib" "$target_repo/lib" "lib"`).
- Added regression coverage to assert `lib/pc_runner.py` is copied, marker-stamped once, and reported in bootstrap output.

**Why:**

- Downstream repos bootstrap `tools/pc-feature`, `pc-commit`, and related scripts that import `lib.*`; missing `lib/` causes deterministic runtime failure before workflow execution starts.

### 2026-02-14 - Harden legacy bootstrap resume handling and dev-tasks schema compatibility

**Feature/Bug:** `make feature` fails on first run in legacy-bootstrapped repos
with `pc-feature: missing section Patch in entry ...`.

**Changed Files:**

- `tools/pc-feature`
- `tools/prd-to-features`
- `tools/pc-devtasks-schema-check`
- `tools/pc-devtasks-migrate-legacy`
- `docs/02-features/feature-template/dev-tasks.md`
- `tests/test_pc_feature.py`
- `tests/test_prd_to_features.py`
- `tests/test_pc_devtasks_schema_check.py`
- `tests/test_pc_devtasks_migrate_legacy.py`

**What Changed:**

- Added legacy-bootstrap detection in `pc-feature` so summary-only bootstrap
  entries are skipped for resume and a new work item is created.
- Added startup auto-repair in `pc-feature` to inject missing required
  `####` sections for resumable entries before resume routing.
- Added actionable remediation text when required resume sections are still
  missing after startup repair.
- Updated `prd-to-features` generated `dev-tasks.md` to start with
  `- No runs yet.` instead of a pre-seeded work-item entry.
- Updated feature template execution-log guidance to align with current
  canonical outcomes and startup flow.
- Extended `pc-devtasks-schema-check` to validate required section presence for
  numeric work-item entries.
- Added `tools/pc-devtasks-migrate-legacy` for deterministic dry-run/apply
  migration of legacy summary-only bootstrap entries.

**Why:**

- Prevent deterministic first-run startup failures in bootstrapped repos while
  preserving strict commit-gate behavior.

### 2026-02-14 - Bootstrap living prompts + stop shipping `tools/templates` to target repos

**Feature/Bug:** Bootstrap into downstream repos failed at planner start when `prompts/` was absent; bootstrap also shipped template assets under `tools/templates` instead of deploying them as living files.

**Changed Files:**

- `tools/bootstrap-into`
- `tools/pc-feature`
- `tools/pc-template-sync`
- `.pre-commit-config.yaml`
- `tools/templates/root/.pre-commit-config.yaml`
- `docs/04-process/dev-workflow.md`
- `docs/04-process/human-orchestration-workflow.md`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/dev-workflow.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `tests/test_bootstrap_into.py`
- `tests_extra/test_bootstrap_into_extra.py`
- `tests/test_pc_template_sync.py`
- `tests/test_pc_feature.py`
- `tools/templates/prompts/patcher-apply.md`
- `tools/templates/prompts/plan-reviewer-gate.md`
- `tools/templates/prompts/planner.md`
- `tools/templates/prompts/reporter-review.md`
- `tools/templates/prompts/tester.md`

**What Changed:**

- Updated `tools/bootstrap-into` to materialize prompt templates into living files at `prompts/*.md`.
- Updated `tools/bootstrap-into` to skip copying `tools/templates/*` into target repos so template assets are deployed as living files, not shipped as templates.
- Added `prompts/*` to bootstrap sync policy so reapply/update flow treats prompt files as sync-managed assets.
- Updated `pc-feature` missing-prompt remediation text:
  - if template prompt files exist locally, remediation still points to `tools/templates/prompts/`;
  - if not, remediation points to restoring `prompts/` via bootstrap source reapply.
- Extended `pc-template-sync` parity pairs to include `prompts/*.md <-> tools/templates/prompts/*.md`.
- Extended `template-sync` pre-commit triggers to include `prompts/`, `tools/templates/prompts/`, and `tools/templates/root/`.
- Updated process docs (live + template copies) so missing-prompt remediation supports both template-enabled and living-only bootstrap repos.
- Added regression tests for:
  - bootstrap deploying prompt templates as living files and not shipping `tools/templates/`,
  - prompt pair synchronization in `pc-template-sync`,
  - `pc-feature` missing prompt remediation when templates are absent.
- Synchronized pre-existing prompt/template drift in five prompt files so new prompt parity checks pass.

**Why:**

- `pc-feature` is file-based and requires `prompts/*.md` at runtime; missing living prompts caused deterministic planner startup failure in bootstrapped repos.
- Deploying templates as living files keeps downstream repos runtime-ready without requiring local template scaffolding.

### 2026-02-14 - Script role commits + normalize reporter sandbox/index-lock failures to non-blocking PASS

**Feature/Bug:** Reporter retry loops in bootstrapped repos could fail solely due to sandbox git index lock/commit permission errors, even when reporter scope checks were otherwise complete.

**Changed Files:**

- `tools/pc-feature`
- `tools/pc-role-commit`
- `prompts/reporter.md`
- `prompts/reporter-review.md`
- `tools/templates/prompts/reporter.md`
- `tools/templates/prompts/reporter-review.md`
- `tests/test_pc_feature.py`
- `tests/test_pc_role_commit.py`

**What Changed:**

- Added `tools/pc-role-commit` as a dedicated script to stage allowed role paths and perform role-scoped commits.
- Updated `pc-feature` `commit_worktree_changes(...)` to call `tools/pc-role-commit` instead of issuing direct `git add`/`git commit`.
- Added reporter FAIL classifier/normalizer for sandbox/index-lock-only commit failures so this class is auto-normalized to PASS and does not consume retry budget.
- Added deterministic reporter PASS feedback and iteration-log note for environment-lock normalization.
- Extended reporter retry decision options with an explicit environment-lock normalization option.
- Updated reporter prompts (live + template) to explicitly forbid direct `git commit` commands and point commit ownership to orchestrator tooling.
- Added regression tests for role-commit script usage/failure surfacing, environment-lock normalization, classifier behavior, and script execution behavior.

**Why:**

- This prevents non-actionable reporter failures caused by sandbox git index lock restrictions from blocking workflow completion.
- Scripted role commits provide a single deterministic commit path and remove prompt ambiguity about who should commit.

### 2026-02-15 - Harden scripted Codex auth sync for pre-commit + feature orchestration

**Feature/Bug:** Pre-commit/feature automation auth reliability (`refresh_token_reused` failures)

**Changed Files:**

- `tools/pc-autofix`
- `tools/pc-feature`
- `tests/test_pc_autofix.py`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`

**What Changed:**

- Updated `tools/pc-autofix` auth handling to keep `.codex_precommit/auth.json` in sync when `~/.codex/auth.json` is newer (using `last_refresh` fallback to mtime).
- Added targeted auth-failure recovery in `tools/pc-autofix`: when `codex exec` fails with refresh-token reuse indicators, force-resync auth and retry once.
- Applied the same auth sync + single-retry behavior to `tools/pc-feature` so `.codex_subagent/auth.json` avoids stale-token failures.
- Added deterministic remediation messaging in both scripts when auth refresh still fails after retry (`codex logout/login` + remove repo-local auth cache path).
- Added unit coverage in `tests/test_pc_autofix.py` for auth freshness detection, sync copy behavior, and refresh-error classification.

**Why:**

- Scripted Codex runs used repo-local `CODEX_HOME` copies that could become stale and trigger deterministic `refresh_token_reused` failures during pre-commit autofix and orchestration runs.
- Syncing newer auth state plus one deterministic retry reduces transient/manual recovery steps while preserving fail-closed behavior when auth truly cannot refresh.

### 2026-02-15 - Normalize metadata-drift-only reporter failures + add safe runtime metadata reconciliation modes

**Feature/Bug:** Reporter retries in bootstrapped repos could fail on stale execution-summary metadata (`Outcome`/`Test Results`/`Docs/logs updated`) even when tester evidence was already green.

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added reporter failure classification for metadata-drift-only failures and centralized reason classification (`env_lock_only`, `metadata_drift_only`, `scope_gap`).
- Added `AUTO_REPAIR_RUNTIME_METADATA` parsing with modes `off|warn|apply` (default `warn` for no-side-effect behavior).
- Added runtime metadata reconciliation pass with explicit allowlist gating and deterministic ledger output.
- Scoped runtime metadata apply writes to machine-owned fields/sections only (`Test Results`, `Reporter Review`, `Tester`, `Reporter`, `Tests run`, `Docs/logs updated`).
- Wired reporter loop handling to normalize metadata-drift-only reporter `FAIL` as non-blocking `PASS`, with iteration-log evidence and optional reconciliation apply.
- Added decision-option `E` in reporter retry guidance for explicit `AUTO_REPAIR_RUNTIME_METADATA=apply` opt-in.
- Added regression coverage for:
  - overwrite-capable runtime reconciliation,
  - metadata-drift classifier + reason classification,
  - runtime metadata mode parsing,
  - runtime metadata warn/apply behavior,
  - end-to-end reporter-loop normalization for metadata drift.

**Why:**

- Prevent false-negative reporter retry exhaustion when failures are limited to stale machine-owned metadata.
- Keep default behavior side-effect-free while providing a controlled deterministic apply path when operators explicitly opt in.

### 2026-02-15 - Scope final CI autofix commits to patcher-safe dirty paths

**Feature/Bug:** Cross-repo `make feature F=01` abort on `patcher edited role-scoped files` after CI autofix.

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `AGENTS.md`
- `tools/templates/root/AGENTS.md`

**What Changed:**

- Added `commit_scoped_patcher_autofix_changes(...)` to commit only dirty scoped autofix candidates via `tools/pc-role-commit`.
- Added deterministic guardrails for scoped patcher autofix commits:
  - block forbidden role-scoped candidate paths,
  - block unexpected staged paths outside the scoped candidate set.
- Replaced final CI autofix patcher commit flow to use scoped commit helper instead of `commit_role_step(...)`, so planner-owned `dev-tasks.md` dirt does not trigger patcher role-scope aborts.
- Added diagnostics for preserved non-candidate dirty paths after scoped autofix commit attempts.
- Added regression coverage for scoped commit behavior and staged-path guardrails.
- Aligned live/template `AGENTS.md` role-scope wording with planner ownership of `dev-tasks.md`.

**Why:**

- Final-gate scoped autofix already filters candidate files, but the previous commit path could still attempt to commit all dirty files and re-trigger patcher role-scope failures.
- Restricting commit scope to autofix candidate deltas keeps ownership boundaries deterministic and preserves planner-owned runtime metadata for final-stage sync.

### 2026-02-15 - Harden skills metadata check against missing `yaml` module and add deterministic CI guardrail

**Feature/Bug:** Cross-repo `make feature F=01` failed at `skills-metadata-check` with `ModuleNotFoundError: No module named 'yaml'`.

**Changed Files:**

- `tools/pc-skills-metadata-check`
- `tests/test_pc_skills_metadata_check.py`
- `Makefile`
- `tools/templates/root/Makefile`

**What Changed:**

- Added a stdlib fallback YAML parser in `tools/pc-skills-metadata-check` that is used when `PyYAML` is not importable.
- Preserved preferred behavior with `yaml.safe_load(...)` when `PyYAML` is available.
- Added regression test coverage to execute the tool with `python3 -S` and assert successful validation without `ModuleNotFoundError`.
- Updated `skills-metadata-check` target in live/template `Makefile` files to run `python3 -S tools/pc-skills-metadata-check`, making missing dependency regressions deterministic in local/CI pipelines.

**Why:**

- The failing consumer incidents showed deterministic crashes caused by assuming `yaml` is always installed in runtime environments.
- Running this check in no-site-packages mode enforces the intended tool portability contract and prevents recurrence.

### 2026-02-15 - Align dev-tasks schema/migration tooling with resume tester-outcome invariant

**Feature/Bug:** Resume compatibility gap for legacy work items with complete
`Test Results` but missing tester outcome.

**Changed Files:**

- `tools/pc-devtasks-schema-check`
- `tools/pc-devtasks-migrate-legacy`
- `tests/test_pc_devtasks_schema_check.py`
- `tests/test_pc_devtasks_migrate_legacy.py`

**What Changed:**

- Added semantic invariant validation in `pc-devtasks-schema-check` to fail
  work items where `Test Results` is complete and `Tester Feedback` has no
  parsed `Outcome`.
- Added section-body parsing helpers in `pc-devtasks-schema-check` to evaluate
  completion/outcome status per work item (beyond heading-presence checks).
- Extended `pc-devtasks-migrate-legacy` to repair legacy mismatch entries by
  upserting `- Outcome: <...>` into `Tester Feedback` when missing and
  `Test Results` is complete.
- Added deterministic tester-outcome derivation for migration:
  explicit section outcome first, then exit-code/pass-fail inference from
  `Test Results`, fallback `SKIPPED`.
- Added regression coverage for both tools:
  schema semantic violation detection and migration repair of the observed
  `WI-20260214-01` legacy pattern.

**Why:**

- Runtime resume already blocks this contradiction fail-closed, but legacy docs
  could still pass schema/migration tooling and then fail later at resume.
- Aligning schema/migration checks with runtime invariants makes the failure
  detectable and fixable earlier, with deterministic consumer sync.

### 2026-02-15 - Harden reporter metadata-drift classification against wording variants and retry-loop exhaustion

**Feature/Bug:** Reporter retry exhaustion on metadata-only contradiction phrasing (`WI-20260215-03`).

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added structural status-parity contradiction detection for reporter feedback in `tools/pc-feature` via `has_metadata_drift_status_parity_contradiction(...)`.
- Expanded metadata-drift blocking markers so actionable pending/missing-outcome handoff gaps are not normalized as metadata drift.
- Updated metadata-drift classifier to combine legacy phrase markers with structural contradiction detection.
- Clarified iteration logging text to explicitly state metadata-drift normalization occurs before retry escalation.
- Added regression coverage for:
  - metadata-drift wording variant classification,
  - pending-placeholder negative classification,
  - retry-loop prevention for wording variant normalization before escalation.

**Why:**

- Existing metadata-drift matching depended too much on specific wording and could misroute metadata-only contradictions into `scope_gap`, driving unnecessary planner loops and reporter retry-cap exits.

### 2026-02-16 - Reconcile tester/reporter feedback outcomes during runtime metadata repair

**Feature/Bug:** `make feature F=02` final gate failure on semantic invariant (`Test Results` complete but `Tester Feedback` missing outcome).

**Changed Files:**

- `tools/pc-feature`
- `tools/pc-devtasks-schema-check`
- `tools/pc-devtasks-migrate-legacy`
- `docs/02-features/feature-template/dev-tasks.md`
- `tools/templates/docs/02-features/feature-template/dev-tasks.md`
- `tests/test_pc_feature.py`
- `tests/test_pc_devtasks_schema_check.py`

**What Changed:**

- Updated `reconcile_runtime_execution_record(...)` in `tools/pc-feature` to normalize and write `Tester Feedback` and `Reporter Feedback` sections from runtime role feedback when outcomes are present, including overwrite mode behavior.
- Added feedback-section update markers to reporter/runtime metadata auto-repair allowlists so deterministic apply-mode writes are not blocked as non-allowlisted updates.
- Updated runtime execution entry defaults and missing-section defaults in `tools/pc-feature` to include explicit `Outcome` placeholders in feedback sections.
- Aligned legacy migration defaults in `tools/pc-devtasks-migrate-legacy` and both live/template feature `dev-tasks.md` files to include feedback `Outcome` placeholders.
- Updated `tools/pc-devtasks-schema-check` remediation text to explicitly call out the tester-feedback outcome invariant for completed `Test Results`.
- Added regression coverage:
  - `tests/test_pc_feature.py` now asserts runtime reconciliation writes `Outcome: PASS` into both feedback sections (normal and overwrite paths).
  - `tests/test_pc_devtasks_schema_check.py` now asserts remediation guidance is printed when the semantic invariant fails.

**Why:**

- The root issue was that default feedback sections with `- Notes:` were not considered pending, so reconciliation updated `Test Results` but skipped `Tester Feedback`, creating invariant failures at schema/pre-commit gates.
- Writing normalized feedback outcomes from runtime feedback keeps execution records internally consistent and prevents this class of contradiction from reappearing.

### 2026-02-16 - Re-enable semantic schema invariant and wire pre-commit legacy autofix guardrail

**Feature/Bug:** Recurring downstream `devtasks-schema-check` failures when `Test Results` was complete but `Tester Feedback` had no `Outcome`.

**Changed Files:**

- `tools/pc-devtasks-schema-check`
- `tests/test_pc_devtasks_schema_check.py`
- `.pre-commit-config.yaml`
- `tools/templates/root/.pre-commit-config.yaml`
- `Makefile`
- `tools/templates/root/Makefile`
- `docs/02-features/06-worktree-policy-naming-convention/dev-tasks.md`
- `docs/02-features/07-anti-cheat-testing-strategy/dev-tasks.md`
- `docs/02-features/09-runner-structured-logs/dev-tasks.md`
- `docs/02-features/15-offload-audit-and-log-compaction/dev-tasks.md`
- `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md`
- `docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md`
- `docs/02-features/19-template-drift-hardening-autofix-recovery/dev-tasks.md`
- `docs/02-features/20-synthetic-feature-workflow-smoke-test/dev-tasks.md`

**What Changed:**

- Restored semantic invariant enforcement in `tools/pc-devtasks-schema-check`:
  complete `Test Results` now requires a parsable tester `Outcome` in `Tester Feedback`.
- Updated schema-check remediation text to explicitly call out the tester-feedback outcome requirement.
- Updated `tests/test_pc_devtasks_schema_check.py` to assert invariant failure when outcome is missing and success when outcome is present.
- Added a deterministic pre-commit autofix hook (`devtasks-legacy-autofix`) in live/template `.pre-commit-config.yaml` to run `tools/pc-devtasks-migrate-legacy` before `devtasks-schema-check`.
- Enabled `--retry-on-autofix` for `lint` and `lint-verbose` in live/template `Makefile` targets so modified-file hooks rerun automatically.
- Ran `tools/pc-devtasks-migrate-legacy` in this repo to backfill existing feature docs and remove current semantic mismatches.

**Why:**

- The invariant drift reintroduced the exact downstream/manual-repair failure mode.
- Keeping strict schema validation plus deterministic autofix/backfill prevents recurrence while preserving fail-closed resume semantics.

### 2026-02-16 - Auto-apply deterministic closeout metadata repair at reporter retry cap

**Feature/Bug:** Cross-repo reporter retry-cap failure in `make feature F=02` (`WI-20260216-03`) due metadata-only wording variant and manual decision-option escalation.

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Expanded metadata-drift classifier markers in `tools/pc-feature` to cover the observed wording family:
  - `execution-state reconciliation`
  - `execution-log consistency`
  - `still records \`Outcome: needs replan\``/`still records \`Outcome: FAIL\``
  - `validation-log` phrasing variants.
- Added one-time deterministic retry-cap closeout repair path for reporter failures:
  - when reporter retry cap is hit, `pc-feature` now applies Option A automatically via `run_runtime_metadata_auto_repair_pass(..., mode=apply)` and schedules exactly one automatic rerun.
  - removed decision-option escalation text from this retry-cap path.
  - if the rerun still fails, `pc-feature` now exits with a deterministic non-decision message.
- Added regression coverage in `tests/test_pc_feature.py` for:
  - metadata-drift classification of the execution-state/validation-log wording variant,
  - reason classification of that variant,
  - retry-cap auto-repair rerun path without `Decision options` messaging.

**Why:**

- The observed cross-repo failure was a tooling false negative in metadata-drift classification plus an escalation path that still required manual decision text after cap.
- Auto-applying deterministic Option A at retry cap removes unnecessary manual branching and keeps behavior aligned with fail-closed deterministic reconciliation.

### 2026-02-16 - Fix planner-feedback REVISE_PLAN contract/parsing mismatch and emit terminal fail events

**Feature/Bug:** Cross-repo planner-feedback abort in `make feature F=08` (`WI-20260216-02`) with `planner marked REVISE_PLAN but returned no Revised Plan section`.

**Changed Files:**

- `prompts/planner-update_from_feedback.md`
- `tools/templates/prompts/planner-update_from_feedback.md`
- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Aligned planner-feedback prompt contract in live/template prompt files by removing the contradictory instruction to "return only the revised plan body"; revised-plan output now stays explicitly under `Revised Plan:`.
- Hardened planner-feedback parsing in `tools/pc-feature`:
  - added fallback revised-plan parsing for body-only planner outputs,
  - strips wrapper lines (`Decision:` / `Rationale:`) when extracting body-only revised plans,
  - treats `(none)` and equivalent placeholder markers as missing revised-plan content,
  - changed missing-decision fallback so unparseable non-plan output defaults to `PLAN_STILL_VALID` (only parseable plan-like output defaults to `REVISE_PLAN`).
- Added explicit workflow terminal events for planner-feedback fatal branches:
  - missing parseable revised plan now emits `planner-feedback FAIL` with `state=FAILED`,
  - revised-plan quality-check failures now emit `planner-feedback FAIL` with `state=FAILED`.
- Added regression coverage in `tests/test_pc_feature.py`:
  - parser behavior for missing/malformed Decision/Revised Plan combinations,
  - planner-feedback prompt contract consistency + live/template parity,
  - planner-feedback missing-revised-plan failure emits `planner-feedback FAIL` event.

**Why:**

- The feedback prompt contract ambiguity plus brittle fallback parsing produced a deterministic terminal abort in real workflow retries.
- Emitting explicit planner-feedback fail events closes the workflow observability gap (START without terminal planner-feedback status).

### 2026-02-16 - Harden deterministic plan-policy recovery to keep `Files to change` actionable

**Feature/Bug:** Repeated Plan Reviewer `BLOCK` loops in cross-repo runs caused by policy-recovery plans rewriting `Files to change` to `(none...)`.

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added plan file-scope extraction/normalization helpers for deterministic policy checks and recovery seeding.
- Updated policy-recovery template generation to preserve concrete fallback file scope (when available) and to derive fallback test-file paths from Allowed Tests (including `unittest` module notation like `tests.test_*`).
- Added deterministic plan-policy violation for non-actionable `Files to change` (placeholder/empty scope).
- Updated planner-reviewer stagnation recovery to seed recovery template files from the current/revised plan before applying deterministic recovery.
- Added/updated regression tests for non-contract recovery seeding, fallback-file template behavior, and non-actionable file-scope policy blocking.

**Why:**

- This removes a key self-induced loop where deterministic recovery made plans non patch-ready, then Plan Reviewer repeatedly blocked the same condition.
- Deterministic policy checks now fail earlier with explicit remediation when file scope is non-actionable.

### 2026-02-16 - Enforce pre-reporter touched-test parity and close retry-cap workflow status

**Feature/Bug:** Cross-repo `make feature F=08` (`WI-20260216-02`) looped on reporter scope/evidence parity and could terminate with workflow status still `RUNNING`.

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Added deterministic touched-test parity helpers in `tools/pc-feature`:
  - collect touched `tests/test_*.py` paths from branch diff,
  - derive explicit file/module reference markers per touched test,
  - compare touched tests against both `Allowed Tests` commands and WI-level `Tests run` evidence.
- Wired a pre-reporter parity gate in the main flow:
  - pre-reporter handoff issues now include missing touched-test parity,
  - reporter is blocked before reviewer prompt execution when parity is missing.
- Hardened reporter retry-cap terminal handling:
  - emits `planner-feedback FAIL` with `state=FAILED` before terminal `die(...)`, closing open planner-feedback status deterministically.
- Added regression coverage in `tests/test_pc_feature.py` for:
  - touched-test path filtering,
  - parity issue detect/pass behavior,
  - pre-reporter parity gate integration,
  - retry-cap terminal workflow closure (`planner-feedback FAIL`, no open planner-feedback step).

**Why:**

- Prevents retry-loop churn caused by missing deterministic WI evidence parity for touched test scope.
- Removes the terminal observability gap where workflow status could remain `RUNNING` after retry-cap exit.

### 2026-02-16 - Remove bootstrap EOF markers and add deterministic --reapply overwrite mode

**Feature/Bug:** Initial bootstrap appended legacy marker footers that broke JSON parsing, and reapply required interactive overwrite/skip prompts.

**Changed Files:**

- `tools/bootstrap-into`
- `tests/test_bootstrap_into.py`
- `tests_extra/test_bootstrap_into_extra.py`
- `tools/templates/docs/00-context/context-boundaries-operating-model.md`
- `tools/templates/docs/04-process/dev-workflow.md`
- `docs/00-context/context-boundaries-operating-model.md`
- `docs/04-process/dev-workflow.md`
- `LICENSE`
- `docs/02-features/03-update-reapply-templates/feature-spec.md`
- `docs/02-features/03-update-reapply-templates/tech-design.md`
- `docs/02-features/03-update-reapply-templates/test-plan.md`
- `tools/README.md`

**What Changed:**

- Removed all bootstrap marker append/hash logic from `tools/bootstrap-into` so copied files are written byte-for-byte from source templates (no end-of-file marker injection).
- Added explicit `--reapply` behavior in `tools/bootstrap-into`:
  - existing `sync` and `conditional` targets are now force-overwritten without interactive prompt,
  - `protected`/`never` path rules remain unchanged,
  - existing gate output (`preflight validation gate`, `template diff review gate`, `conflict summary output`) is still emitted with `overwrite (reapply)` summaries.
- Updated bootstrap tests to stop asserting marker insertion and instead assert:
  - no legacy marker footer text,
  - JSON configs parse cleanly after bootstrap,
  - `--reapply` is non-interactive and overwrites modified syncable files.
- Removed previously committed legacy marker footer lines from affected template/live docs and `LICENSE`.
- Updated reapply feature docs to document the new deterministic `--reapply` overwrite model.

**Why:**

- Marker footer injection is invalid in JSON and caused first-time bootstrap breakage for config files.
- In the stabilized workflow, deterministic reapply overwrite behavior reduces manual prompting and aligns with desired template refresh semantics.

### 2026-02-16 - Enforce touched-test coverage during planner Allowed Tests validation

**Feature/Bug:** Reporter retry loops could continue after planner approval when touched test files were not explicitly covered in Allowed Tests.

**Changed Files:**

- `tools/pc-feature`
- `prompts/planner-update-allowed-tests.md`
- `tools/templates/prompts/planner-update-allowed-tests.md`
- `tests/test_pc_feature.py`

**What Changed:**

- Added `allowed_tests_touched_test_coverage_issues(...)` in `tools/pc-feature`.
- Reused the same touched-test coverage policy in both planner-stage Allowed Tests validation and pre-reporter parity checks.
- Extended planner-stage invalid Allowed Tests gating to include missing explicit touched-test coverage paths.
- Strengthened remediation/check text to require explicit touched-test coverage in Allowed Tests.
- Updated planner allowed-tests prompt guidance to require explicit commands for each missing touched test file/module when the issue is reported.
- Added regression tests for:
  - helper-level missing touched-test coverage detection;
  - planner allowed-tests update prompt including missing touched-test coverage details.

**Why:**

- This removes the planner/reporter policy mismatch that allowed discover-only commands through planner validation and then failed deterministically at reporter.
- Failures now occur earlier with direct remediation instructions, reducing retry churn.

### 2026-02-16 - Preserve sync-resume merge conflicts for manual resolution

**Feature/Bug:** `RESUME_MODE=sync` stale patcher sync failures printed `resolve conflicts manually` guidance while clearing merge state immediately.

**Changed Files:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`

**What Changed:**

- Removed automatic `git merge --abort` from the merge-failure branch in `merge_main_into_worktree(...)`.
- Kept the existing failure contract unchanged (`return False, <merge output>`), so caller diagnostics and fail-closed behavior remain the same.
- Added regression coverage in `tests/test_pc_feature.py` to assert merge failure does not trigger a second subprocess call (`git merge --abort`).

**Why:**

- This aligns runtime behavior with CLI guidance to resolve conflicts manually in the patcher worktree.
- Preserving merge state keeps `MERGE_HEAD` and conflict markers available for direct user resolution and debugging.

### 2026-02-18 - Add Orderer role and canonical PM step ownership in `pc-prepare-features`

**Feature/Bug:** PM feedback step drift and missing dependency-order producer ownership in prepare retry loops.

**Changed Files:**

- `tools/pc-prepare-features`
- `prompts/orderer-prepare.md`
- `tools/templates/prompts/orderer-prepare.md`
- `prompts/product-manager-prepare-gate.md`
- `tools/templates/prompts/product-manager-prepare-gate.md`
- `.codex.toml`
- `tools/templates/root/.codex.toml`
- `docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `tests/test_pc_prepare_features.py`

**What Changed:**

- Added canonical prepare step taxonomy (`architect`, `ux`, `dependency-planner`, `product-manager`) with alias normalization for PM output step variants.
- Added Orderer role execution (`run_orderer_role`) with dedicated prompt/profile and deterministic fallback.
- Updated PM review normalization to validate unknown PM issue step names and canonicalize all issue steps.
- Expanded PM TODO ownership to include `dependency-planner` and improved owner inference for auto-created/carry tasks.
- Added owner-scoped selective retry routing in prepare loop: retries rerun only unresolved producer roles, then rerun PM gate.
- Expanded retry context payloads with orderer-owner TODO input and previous order payload JSON.
- Updated workflow docs (live/template) to reflect `Architect -> UX -> dependency planner baseline -> Orderer -> PM gate` sequence.
- Added regression tests for orderer prompt rendering/profile defaults, dependency-planner owner assignment, and PM step validation behavior.

**Why:**

- The prior flow had no dedicated owner for feature-order feedback and allowed free-form PM steps, which reduced determinism and caused unnecessary full-loop reruns.

### 2026-02-18 - Preserve canonical prepare artifacts until PM promote and add candidate/autofix lanes

**Feature/Bug:** Re-running `make prepare-features` rewrote canonical global artifacts during blocked PM loops and repeatedly stalled on dependency payload shape drift.

**Changed Files:**

- `tools/pc-prepare-features`
- `tests/test_pc_prepare_features.py`

**What Changed:**

- Added rerun baseline detection that loads existing canonical `design.md`, `ux-ui.md`, `feature-order.json`, and PM TODO/state when present.
- Added candidate artifact lane (`*.candidate.*`) for design, UX, feature-order, PM TODO, and prepare state, plus candidate summary.
- Changed prepare persistence flow to write candidate artifacts on every loop snapshot and promote to canonical only on PM `APPROVE` or explicit `waive`.
- Added dependency payload normalization so `decisions[*].depends_on`, `dependencies`, and `ordered_features[*].dependencies` stay typed and aligned.
- Added non-fail-fast dependency autofix hook via dedicated Codex session (`run_order_payload_autofix_session`) when raw order payload consistency issues are detected.
- Added optional architect/UX markdown autofix sessions before PM retry in codex role mode.
- Relaxed changed-sections metadata drift from hard PM blocker to warning diagnostics.
- Extended tests for candidate promotion flow, blocked-run canonical preservation, dependency normalization, and dependency autofix invocation.

**Why:**

- This preserves trusted canonical artifacts while still exposing live loop progress through inspectable candidate files.
- It reduces PM-loop exhaustion caused by repeated dependency representation drift and metadata-only section-diff noise.

### 2026-02-18 - Run `prd-to-features` incremental hydrate and refresh machine-managed feature review findings

**Feature/Bug:** User-requested `prd-to-features` generation pass for current PRD scope with incremental safety.

**Changed Files:**

- `docs/02-features/*/feature-spec.md` (machine-managed findings sections refreshed by `make review-features`)
- `docs/02-features/*/dev-tasks.md` (machine-managed findings sections refreshed by `make review-features`)
- `docs/03-logs/review-features-report.json`

**What Changed:**

- Ran `python3 .codex/skills/prd-to-features/scripts/plan_feature_folders.py --json` to preview folder mapping from PRD priorities and `feature-order.json`.
- Ran `tools/prd-to-features` in hydrate mode; no folders were created or modified because all mapped indices already existed and had no missing sections.
- Ran `make review-features` after generation; it refreshed machine-managed findings across feature docs and wrote `docs/03-logs/review-features-report.json`.

**Validation:**

- `tools/prd-to-features` summary: `created=(none)`, `updated=(none)`, mapped indices skipped with explicit no-overwrite reasons.
- `make review-features` summary: complete with updated findings report (`features_updated=22`, `security_findings=68`, `product_findings=58`).

**Why:**

- Keeps PRD->feature documentation flow deterministic and incremental (add/update missing only, no destructive overwrite) while ensuring review-derived findings stay current.

### 2026-02-19 - Implement Batch B: human validation handoff + prepare security blueprint

**Feature/Bug:** Batch B follow-up from workflow hardening feedback.

**Changed Files:**

- `tools/pc-feature`
- `tools/pc-prepare-features`
- `prompts/security-prepare.md`
- `tools/templates/prompts/security-prepare.md`
- `docs/01-product/security.md`
- `tools/templates/docs/01-product/security.md`
- `docs/01-product/AGENTS.md`
- `tools/templates/docs/01-product/AGENTS.md`
- `docs/04-process/human-orchestration-workflow.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md`
- `docs/README.md`
- `tools/templates/docs/README.md`
- `tools/README.md`
- `tests/test_pc_feature.py`
- `tests/test_pc_prepare_features.py`
- `tests/test_docs_logs.py`

**What Changed:**

- Added deterministic parsing of `### Human Validation Requests` in `tools/pc-feature` and end-of-run summary rendering with explicit instructions for how the human reports failed checks back to Codex.
- Added a new prepare role `Security Expert` in `tools/pc-prepare-features`:
  - new prompt contract `security-prepare.md`,
  - profile default `SecurityExpert`,
  - generated artifact `docs/01-product/security.md`,
  - candidate/promotion support via `security.candidate.md`.
- Updated prepare workflow docs/template docs/readmes to include security artifact generation and prompt inventory.
- Added/updated tests for:
  - `pc-feature` human validation parsing + summary messaging contract,
  - `pc-prepare-features` security artifact generation and profile wiring,
  - docs assertions that include security prepare outputs.

**Why:**

- Human validation requests now have a deterministic command-line handoff at the end of execution instead of being buried in markdown.
- Project-level security direction is now generated during prepare and kept separate from per-feature review-task noise, aligning security guidance with project scope before feature execution starts.
