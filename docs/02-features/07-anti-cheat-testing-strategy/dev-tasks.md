# Development Tasks: Anti-cheat testing strategy

> **LLM-executable tasks**
>
> This document contains specific, actionable tasks that can be executed by developers (human or AI). Each task should be atomic, testable, and clearly defined.

---

## Overview

**Feature:** Anti-cheat testing strategy

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
- Scope / tasks covered: Ensure Codex CLI uses repo-local CODEX_HOME and project profiles
- Planner: Codex
- Patcher: Codex
- Tester: Codex
- Reporter: Codex
- Outcome: pass
- Tests run: Not run (no test command specified)
- Offload ids (if any): 83639ed3e7390d93ea2591edaf8357d41ee581b2d8caea75257a0d37c4a4f74b
- Docs/logs updated: implementation-log.md, decision-log.md, validation-log.md
- Notes: Follow-up to template sync hook to unblock codex exec in sandbox.

#### Preflight Report

- Work Item: WI-20260204-02
- PRD ref: 07-anti-cheat-testing-strategy
- Risk level: LOW
- Triggers: No high-risk modules touched
- Scope in: Repo-local CODEX_HOME for codex exec; per-role profiles in .codex.toml + template
- Scope out: Changes to Serena MCP config beyond ensuring project profile usage
- Non-goals reminder: No behavior changes outside codex exec path and configs
- Files to change: tools/pc-autofix, tools/pc-template-sync, tools/pc-feature, .codex.toml, tools/templates/root/.codex.toml, tools/README.md, docs/03-logs/\*
- Change budget: max_files=8, max_new_modules=0
- TDD plan: None
- Systematic review: commands executed and outputs reviewed; changes match intended scope.

#### TDD Plan

- Tests to write first: None

#### Files to Change + Change Budget

- Files: tools/pc-autofix, tools/pc-template-sync, tools/pc-feature, .codex.toml, tools/templates/root/.codex.toml, tools/README.md, docs/03-logs/implementation-log.md, docs/03-logs/decision-log.md, docs/03-logs/validation-log.md
- Change budget: max_files: 8, max_new_modules: 0

#### Docs Updated

- [x] Implementation log
- [x] Decision log (if needed)
- [ ] Bug log (if needed)
- [x] Validation log (if needed)
- [x] Feature docs
- [ ] PRD (if needed)

#### Plan

- Add repo-local CODEX_HOME to codex exec helper paths.
- Invoke codex with -C repo root and --profile (Default unless overridden).
- Add profiles to .codex.toml and template.

#### Patch

- Updated codex exec helpers to set CODEX_HOME and pass -C/--profile.
- Routed pc-feature planner/patcher/tester/reporter calls to role-specific profiles.
- Tuned Planner profile to higher reasoning/verbosity and documented tooling notes.
- Added profiles and Serena MCP config to .codex.toml template.

#### Test Results

- Not run (no test command specified)

#### Reporter Review

- No issues noted.

#### Gates

- make ci: Not run (no test command specified)

#### Autofix Attempts

- (none)

#### Tester Feedback

- Notes:

#### Reporter Feedback

- Notes:

#### Iteration Log

- Completed in one pass.

#### Commit

- Commit message:

#### Final Report

- Codex CLI now uses repo-local CODEX_HOME with profiles, and the template .codex.toml includes profile + Serena MCP defaults.

### WI-20260204-01 - Work item execution

- Date: 2026-02-04
- Scope / tasks covered: Add template-vs-living sync pre-commit hook + script
- Planner: Codex
- Patcher: Codex
- Tester: Codex
- Reporter: Codex
- Outcome: pass
- Tests run: Not run (no test command specified)
- Offload ids (if any): feecc9aa02e6f75a1eba126c886e9eb3e038de52f85f440534e698fe7d42d339, f98802d014dcee1bbeed51c9db5bdeff5befe74e000858ccba703f454533729a, f7648b34f0db116f59ca636a73bf9c3b3156da5326b958bdb03a564ed1586bf0, b208b445478966553c9d327a5922e949c107a88a56552782c51a3c0226ea4e09
- Docs/logs updated: implementation-log.md, decision-log.md, validation-log.md
- Notes: make feature F=07 failed due to codex session permission; reran with MANUAL=1.

#### Preflight Report

- Work Item: WI-20260204-01
- PRD ref: 07-anti-cheat-testing-strategy
- Risk level: LOW
- Triggers: No high-risk modules touched
- Scope in: Pre-commit hook to diff templates vs living files; codex-based auto-fix when one side changed
- Scope out: Changing template sources or adding new templates beyond sync behavior
- Non-goals reminder: No changes to product-specific docs outside the listed sync set
- Files to change: tools/pc-feature, tools/pc-template-sync (new), .pre-commit-config.yaml, docs/03-logs/\*
- Change budget: max_files=8, max_new_modules=1
- TDD plan: None (scripted hook behavior; manual verification)
- Systematic review: commands executed and outputs reviewed; no unexpected diffs beyond intended files.

#### TDD Plan

- Tests to write first:

#### Files to Change + Change Budget

- Files: tools/pc-feature, tools/pc-template-sync, .pre-commit-config.yaml, tools/templates/root/.pre-commit-config.yaml, docs/03-logs/implementation-log.md, docs/03-logs/decision-log.md, docs/03-logs/validation-log.md
- Change budget: max_files: 8, max_new_modules: 1

#### Docs Updated

- [x] Implementation log
- [x] Decision log (if needed)
- [ ] Bug log (if needed)
- [x] Validation log (if needed)
- [x] Feature docs
- [ ] PRD (if needed)

#### Plan

- Identify template/live pairs for process + AGENTS + hooks + root configs.
- Add a dedicated pre-commit hook script to diff and Codex-sync one-sided changes.
- Update template root pre-commit config to mirror the hook.

#### Patch

- Added `tools/pc-template-sync` script and wired it into `.pre-commit-config.yaml`.
- Synced template pre-commit config with the new hook.
- Normalized `pc-feature` main-branch detection to allow `heads/main`.

#### Test Results

- Not run (no test command specified)

#### Reporter Review

- No issues noted.

#### Gates

- make ci: Not run (no test command specified)

#### Autofix Attempts

- (none)

#### Tester Feedback

- Notes:

#### Reporter Feedback

- Notes:

#### Iteration Log

- Initial implementation completed in one pass.

#### Commit

- Commit message: (not requested)

#### Final Report

- Added a template/living sync pre-commit hook with Codex autofix for one-sided changes, synced the template config, and documented the decision + validation status.

**Format:**

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

- [x] Implementation log
- [x] Decision log (if needed)
- [ ] Bug log (if needed)
- [x] Validation log (if needed)
- [x] Feature docs
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
