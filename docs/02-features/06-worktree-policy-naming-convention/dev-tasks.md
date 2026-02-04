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

## Change Log

| Date       | Changes                | Author       |
| ---------- | ---------------------- | ------------ |
| 2026-02-02 | Initial task breakdown | Developer/PO |
| 2026-02-04 | Add execution log      | Developer/PO |
