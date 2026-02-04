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
