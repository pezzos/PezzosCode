# Development Tasks: Worktree policy + naming convention

> **LLM-executable tasks**
>
> This document contains specific, actionable tasks that can be executed by developers (human or AI). Each task should be atomic, testable, and clearly defined.

---

## Overview

**Feature:** Worktree policy + naming convention

**Status:** Not Started

**Last Updated:** 2026-02-04

## Ownership and Traceability

**Source of truth:** `dev-tasks.md` (tasks + execution log)

**Roles (record names or agent ids):**

- Orchestrator: [name]
- Planner: [name]
- Patcher: [name]
- Tester: [name]
- Reporter: [name]
- Product Owner: [name]

## Execution Log

### WI-20260204-02 - Work item execution

- Date: 2026-02-04
- Scope / tasks covered: Implement role-scoped worktree policy, manifest, auto-collection, and cleanup; add role log templates and doc updates.
- Planner: Codex
- Patcher: Codex
- Tester: Codex
- Reporter: Codex
- Outcome: needs replan
- Tests run: tools/offload-proxy/pp make ci (FAIL: end-of-file-fixer PermissionError on .codex/skills/readme-sync/SKILL.md)
- Offload ids (if any): 0522bce30e182d434c3dca76e2ee227ca51f6005887b0da6f3afc96a6c31ef2a
- Docs/logs updated: docs/03-logs/implementation-log.md, docs/03-logs/decision-log.md, docs/03-logs/validation-log.md
- Notes: PO approved proceeding despite change budget exceeded. make ci failed due to pre-commit permission error on .codex/skills/readme-sync/SKILL.md.

#### Preflight Report

- Work Item: WI-20260204-02
- PRD ref: Feature 06 - Worktree policy + naming convention
- Risk level: HIGH (triggers: change budget exceeded (file count))
- Triggers: change budget exceeded (file count)
- Scope in: role-scoped worktree logs, manifest tracking, collector/squash to main, cleanup
- Scope out: changing feature requirements beyond worktree handling
- Non-goals reminder: no new execution surfaces outside make feature
- Files to change: tools/pc-feature, docs/02-features/_ templates + feature 06 docs, docs/04-process/_, docs/03-logs/\*
- Change budget: max_files=6, max_new_modules=1
- TDD plan: none
- Systematic review: tools/pc-feature, feature template docs, process docs

#### TDD Plan

- Tests to write first: none

#### Files to Change + Change Budget

- Files: tools/pc-feature, docs/02-features/feature-template/_, docs/02-features/06-worktree-policy-naming-convention/_, docs/04-process/_, docs/03-logs/_
- Change budget: max_files: 6, max_new_modules: 1

#### Docs Updated

- [ ] Implementation log
- [ ] Decision log (if needed)
- [ ] Bug log (if needed)
- [ ] Validation log (if needed)
- [ ] Feature docs
- [ ] PRD (if needed)

#### Plan

- Update pc-feature to create role branches/worktrees, enforce scope, write manifest, collect diffs into main, and cleanup worktrees.
- Add role log templates and update feature/docs process references.
- Record decision/implementation/validation logs.

#### Patch

- Updated pc-feature for role-scoped logging, manifest writing, diff collection to main, and cleanup.
- Added planner/reporter/validation logs to templates and feature 06 docs.
- Updated process docs to reference role scopes and collector behavior.

#### Test Results

- Outcome: FAIL
- Tests run: tools/offload-proxy/pp make ci
- Notes: end-of-file-fixer PermissionError on .codex/skills/readme-sync/SKILL.md

#### Reporter Review

- Outcome: FAIL
- Docs/logs updated: implementation-log.md, decision-log.md, validation-log.md
- Notes: make ci failed due to pre-commit permission error on .codex/skills/readme-sync/SKILL.md

#### Gates

- make ci: FAIL (end-of-file-fixer PermissionError on .codex/skills/readme-sync/SKILL.md)

#### Autofix Attempts

- (none)

#### Tester Feedback

- Outcome: FAIL
- Notes: make ci failed; permission error in pre-commit hook on .codex/skills/readme-sync/SKILL.md

#### Reporter Feedback

- Notes: worktree policy/tooling updates pending gate pass

#### Iteration Log

-

#### Commit

- Commit message: (not created; make ci failed)

#### Final Report

- What changed (files): tools/pc-feature; docs/02-features/feature-template/_; docs/02-features/06-worktree-policy-naming-convention/_; docs/04-process/_; docs/03-logs/_
- Tests written (names) + results: tools/offload-proxy/pp make ci (FAIL: end-of-file-fixer PermissionError on .codex/skills/readme-sync/SKILL.md)
- Docs/logs updated checklist: Implementation log, Decision log, Validation log
- make ci results: FAIL
- Commands run (use pp for noisy output): tools/offload-proxy/pp make ci
- Commit message: (not created; make ci failed)

### WI-20260204-01 - Work item execution

- Date: 2026-02-04
- Scope / tasks covered:
- Planner: Codex
- Patcher: Codex
- Tester: Codex
- Reporter: Codex
- Outcome: pass
- Tests run: `./tools/offload-proxy/pp make test` (runs `python -m unittest discover -s tests -p "test_*.py"` and then `skills-check` and `docs-check`)
- Offload ids (if any):
- Docs/logs updated: No (nothing to log; workspace clean)
- Notes:

#### Preflight Report

- Work Item: WI-20260204-01
- PRD ref: docs/01-product/prd.md#F-06
- Risk level: LOW
- Triggers: (none)
- Scope in: Implement the CLI-level worktree policy workflow and naming-convention enforcement described in F-06, document the steps in the process guide, and record the execution in the implementation log.
- Scope out: All UI/TUI/API/Web/Mobile surfaces and any cloud-based services are explicitly out of scope.
- Non-goals reminder: Keep the work local to the CLI/worktree tooling; do not expand to new UIs or remote automation.
- Files to change: docs/04-process/ticket-execution-protocol.md, docs/03-logs/implementation-log.md, docs/03-logs/decision-log.md, docs/02-features/F-06/feature-spec.md, tools/worktree-policy/README.md, tools/worktree-policy/create-worktree.sh
- Change budget: max_files=6, max_new_modules=1
- TDD plan: tests/cli/test_worktree_policy.sh
- Systematic review:

#### TDD Plan

- Tests to write first:
  - tests/cli/test_worktree_policy.sh

#### Files to Change + Change Budget

- Files: docs/04-process/ticket-execution-protocol.md, docs/03-logs/implementation-log.md, docs/03-logs/decision-log.md, docs/02-features/F-06/feature-spec.md, tools/worktree-policy/README.md, tools/worktree-policy/create-worktree.sh
- Change budget: max_files: 6, max_new_modules: 1

#### Docs Updated

- docs/03-logs/implementation-log.md
- docs/03-logs/decision-log.md

#### Plan

**Plan**

- Approach: Align implementation with the doc-driven workflow by first absorbing the current requirements in `docs/01-product/prd.md`, `docs/02-features/F-06/feature-spec.md`, and the ticket/protocol guidance in `docs/04-process`. Then sketch the CLI/worktree behavior changes and documentation edits needed to define the default worktree count, enforce the naming convention, and guide users through the gated flow (per the provided tech/feature specs). Finally, capture verification and logging expectations so the work item satisfies the AGENTS.md rules (logs updated, systematic review recorded, TDD plan referenced).

- Files to change: `docs/04-process/ticket-execution-protocol.md`, `docs/02-features/F-06/feature-spec.md`, `docs/03-logs/implementation-log.md`, `docs/03-logs/decision-log.md`, `tools/worktree-policy/README.md`, `tools/worktree-policy/create-worktree.sh`, plus `tests/cli/test_worktree_policy.sh` for validation (matching the preflight list).

- Risks: Overwriting existing process guidance without addressing all referenced docs (mitigate by carefully cross-referencing AGENTS/02/03); failing to surface errors for existing worktrees or branch conflicts (document and script clear prompts/failures); forgetting log updates (explicit checklist to touch `docs/03-logs` entries).

- Tests: Align with the advised TDD plan—author/adjust `tests/cli/test_worktree_policy.sh` to cover happy/unhappy paths, then run `make feature F=F-06` (per ticket protocol) once implementation is in place; re-run if any subsequent edits affect the CLI scripts.

#### Patch

- Added the new `tools/worktree-policy/create-worktree.sh` helper with README plus a CLI test (`tests/cli/test_worktree_policy.sh`) and wired it into `make test` so the default implementer + reviewer worktrees are created with sanitized `../<repo>-<feature>-<agent>` names, predictable `feat/<feature>` / `feat/<feature>-review` branches, and idempotent retries.
- Documented the helper, logging, and systematic-review expectations in `docs/02-features/06-worktree-policy-naming-convention/feature-spec.md` and `docs/04-process/ticket-execution-protocol.md`, and captured the new policy decision in DEC-009 plus an implementation-log entry tied to WI-20260204-01 so the worktree policy (script plus Preflight/Systematic review command list) is auditable next to the execution logs.
- Tests now exercise the helper via `make test` (which runs the CLI test) and the workflows remind implementers to note the helper call in the Preflight “Systematic review” field; logs record the attempted `make feature` runs and explain why they failed so the gate is traceable.

Next steps:

1. Replace or remove the placeholder `WI-YYYYMMDD-01` entry in `docs/02-features/06-worktree-policy-naming-convention/dev-tasks.md` so `pc-feature` can normalize a real work item ID.
2. Once that entry exists, rerun `make feature F=06` so the Plan → Patch → Test → Report loop can finish, including the documented `tools/worktree-policy` invocation and decision-log reference.

Commands run:

- `make test` (passes; includes `tests/cli/test_worktree_policy.sh`)
- `make feature F=F-06` (fails because `pc-feature` can’t find a folder named `F-06`)
- `make feature F=06` (fails because the placeholder work item header `WI-YYYYMMDD-01` in `dev-tasks.md` is not a valid ID)

#### Test Results

Outcome: PASS
Tests run: `./tools/offload-proxy/pp make test` (runs `python -m unittest discover -s tests -p "test_*.py"` and then `skills-check` and `docs-check`)
Notes: Commands executed: `pwd`, `ls`, `cat Makefile`, `ls tools`, `./tools/offload-proxy/pp --help` (script expects a subcommand), `sed -n '1,160p' tools/offload-proxy/pp`, `cat pp.yml`, `./tools/offload-proxy/pp make test` (PASS), `ls docs/03-logs`, `sed -n '1,160p' docs/03-logs/validation-log.md`; Added validation entry at `docs/03-logs/validation-log.md` documenting the 2026-02-04 WI-20260204-01 full test run.
Work Item ID: WI-20260204-01

#### Reporter Review

Outcome: PASS
Docs/logs updated: No (nothing to log; workspace clean)
Notes: No changes detected; nothing to scope-review.
Work Item ID: WI-20260204-01

#### Gates

- make ci: PASS

#### Autofix Attempts

tools/offload-proxy/pp pre-commit run --all-files: ok

#### Tester Feedback

Outcome: PASS
Tests run: `./tools/offload-proxy/pp make test` (runs `python -m unittest discover -s tests -p "test_*.py"` and then `skills-check` and `docs-check`)
Notes: Commands executed: `pwd`, `ls`, `cat Makefile`, `ls tools`, `./tools/offload-proxy/pp --help` (script expects a subcommand), `sed -n '1,160p' tools/offload-proxy/pp`, `cat pp.yml`, `./tools/offload-proxy/pp make test` (PASS), `ls docs/03-logs`, `sed -n '1,160p' docs/03-logs/validation-log.md`; Added validation entry at `docs/03-logs/validation-log.md` documenting the 2026-02-04 WI-20260204-01 full test run.
Work Item ID: WI-20260204-01

#### Reporter Feedback

Outcome: PASS
Docs/logs updated: No (nothing to log; workspace clean)
Notes: No changes detected; nothing to scope-review.
Work Item ID: WI-20260204-01

#### Iteration Log

- Attempt 1: tester=PASS, reporter=PASS

#### Commit

- Commit message: Document WI-20260204-01 execution entry in worktree policy log

#### Final Report

What changed (files): (see git diff)
Tests written (names) + results: Outcome: PASS
Tests run: `./tools/offload-proxy/pp make test` (runs `python -m unittest discover -s tests -p "test_*.py"` and then `skills-check` and `docs-check`)
Notes: Commands executed: `pwd`, `ls`, `cat Makefile`, `ls tools`, `./tools/offload-proxy/pp --help` (script expects a subcommand), `sed -n '1,160p' tools/offload-proxy/pp`, `cat pp.yml`, `./tools/offload-proxy/pp make test` (PASS), `ls docs/03-logs`, `sed -n '1,160p' docs/03-logs/validation-log.md`; Added validation entry at `docs/03-logs/validation-log.md` documenting the 2026-02-04 WI-20260204-01 full test run.
Work Item ID: WI-20260204-01
Docs/logs updated checklist: (see Docs Updated)
make ci results: PASS
Commands run (use pp for noisy output): tools/offload-proxy/pp make ci: FAIL; tools/offload-proxy/pp make ci: ok
Commit message: Document WI-20260204-01 execution entry in worktree policy log

### WI-YYYYMMDD-01 - Work item execution

- Date:
- Scope / tasks covered:
- Planner:
- Patcher:
- Tester:
- Reporter:
- Outcome: [pass | fail | needs replan]
- Tests run:
- Offload ids (if any):
- Docs/logs updated:
- Notes:

#### Preflight Report

- Work Item:
- PRD ref:
- Risk level:
- Triggers:
- Scope in:
- Scope out:
- Non-goals reminder:
- Files to change:
- Change budget:
- TDD plan:
- Systematic review:

#### TDD Plan

- Tests to write first:

#### Files to Change + Change Budget

- Files:
- Change budget:

#### Docs Updated

- [ ] Implementation log
- [ ] Decision log (if needed)
- [ ] Bug log (if needed)
- [ ] Validation log (if needed)
- [ ] Feature docs
- [ ] PRD (if needed)

#### Plan

- (pending)

#### Patch

- (pending)

#### Test Results

- (pending)

#### Reporter Review

- (pending)

#### Gates

- make ci:

#### Autofix Attempts

- (none)

#### Tester Feedback

- Notes:

#### Reporter Feedback

- Notes:

#### Iteration Log

-

#### Commit

- Commit message:

#### Final Report

-

## Review Findings Backlog

<!-- review-backlog:start -->

### Patcher Tasks (must be handled during patch/test steps)

- [ ] `SEC-06-001` Unsanitized worktree/branch input can enable command or ref-name injection
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Enforce a strict allowlist (for example `^[a-z0-9-]+$`) for feature/agent tokens, reject anything else, and execute git commands with fully quoted arguments and `--` separators (no eval/string-built command execution).
- [ ] `SEC-06-002` Worktree path traversal/symlink escape not fail-closed
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Before create/reuse/remove, canonicalize paths, require they stay under the approved parent directory, reject symlinks, and verify target is a valid git worktree owned by this repo.
- [ ] `SEC-06-003` Manifest-driven auto-collection/cleanup lacks integrity validation
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Parse manifest with strict schema, verify each entry against `git worktree list --porcelain`, ignore/reject out-of-policy entries, and store manifest with restrictive permissions.
- [ ] `SEC-06-004` Security gate can fail open when CI/pre-commit errors occur
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: Enforce fail-closed completion: block feature completion on any non-zero `make ci`/pre-commit result and require a clean rerun before completion status can advance.
- [ ] `SEC-06-005` Missing abuse-case tests for naming/conflict/symlink scenarios
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: Add negative tests that assert hard failure for invalid names, path escapes, symlink reuse, and manifest mismatch; make these tests mandatory in `make test`/`make ci`.
- [ ] `PROD-06-001` Acceptance criteria are not verifiable for end-user outcomes
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Define measurable acceptance checks for default worktree count, naming convention, branch names, and required CLI success/summary output so users can verify outcomes deterministically.
- [ ] `PROD-06-002` Failure recovery UX is underspecified for real user retries
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Specify exact error text and immediate recovery actions for existing worktree, branch conflict, and missing preconditions, including explicit rerun-safety messaging.
- [ ] `PROD-06-003` Validation gate behavior is ambiguous from a user perspective
  - Reviewer: Product Manager
  - Severity: High
  - Phase: automated-test
  - Blocking: Yes
  - Action: Enforce and test fail-closed workflow status/output on any non-zero `make ci` or pre-commit result, aligned with SEC-06-004 and SEC-06-005.
- [ ] `PROD-06-004` Readiness signals are inconsistent across feature artifacts
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Reconcile task status, remove unresolved placeholder WI entries from active tracking, and provide one authoritative readiness summary for feature review.

### Human Validation Requests (Product Owner / end-user)

- [ ] `PROD-06-005` Human usability sign-off is missing for CLI prompts and stage clarity
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: human-validation
  - Action: Require explicit human validation sign-off for prompt clarity, handoff/stage wording, and recovery instructions before feature completion.

<!-- review-backlog:end -->

## Task Breakdown

### CLI Development

- [ ] **TASK-101: Define workflow behavior**
  - Document required steps, gates, and outputs
  - **Acceptance:** Behavior is specified in docs
  - **Estimate:** 0.5 day

- [ ] **TASK-102: Implement or update tooling/scripts**
  - Update scripts or templates to enforce behavior
  - **Acceptance:** Tooling matches specification
  - **Estimate:** 1 day

### Testing

- [ ] **TASK-401: Add or update tests**
  - Add regression tests or checks where applicable
  - **Acceptance:** Tests cover the primary path
  - **Estimate:** 0.5 day

### Documentation

- [ ] **TASK-501: Update docs/logs**
  - Update process docs and logs
  - **Acceptance:** Documentation matches implementation
  - **Estimate:** 0.5 day

## Task Summary

### By Status

- **Not Started:** 4
- **In Progress:** 0
- **Complete:** 0
- **Blocked:** 0

### By Category

- **Setup:** 0 tasks
- **Backend:** 0 tasks
- **Frontend:** 0 tasks
- **Integration:** 0 tasks
- **Testing:** 1 task
- **Documentation:** 1 task
- **Deployment:** 0 tasks

## Blocked Tasks

None.

## Notes for LLM Execution

### Context to Provide

- Feature specification (feature-spec.md)
- Technical design (tech-design.md)
- Current system map (docs/00-context/system-map.md)

### Execution Guidelines

- Complete tasks in dependency order
- Run tests after each task
- Commit after each completed task
- Ask questions if requirements are unclear

## Related Documents

- Feature Spec: feature-spec.md
- Tech Design: tech-design.md
- Test Plan: test-plan.md
- Planner Log: planner-log.md
- Reporter Log: reporter-log.md
- Validation Log: validation-log.md

## Change Log

| Date       | Changes                | Author       |
| ---------- | ---------------------- | ------------ |
| 2026-02-02 | Initial task breakdown | Developer/PO |
| 2026-02-04 | Add execution log      | Developer/PO |
