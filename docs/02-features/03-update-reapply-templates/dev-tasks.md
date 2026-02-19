# Development Tasks: Update/reapply templates

> **LLM-executable tasks**
>
> This document contains specific, actionable tasks that can be executed by developers (human or AI). Each task should be atomic, testable, and clearly defined.

---

## Overview

**Feature:** Update/reapply templates

Status: Not Started

**Last Updated:** 2026-02-02

## Execution Log

- No runs yet.

## Review Findings Backlog

<!-- review-backlog:start -->

### Patcher Tasks

- [ ] `SEC-03-002` Access-control expectations are missing for feature scope
  - Action: Add explicit authN/authZ requirements and denied-path behavior for this feature where privileged actions are possible.
  - Acceptance: Feature docs and tests include at least one denied-path scenario proving unauthorized access is blocked.
- [ ] `SEC-03-003` Sensitive-data redaction is undefined for feature logging/output
  - Action: Define and enforce redaction/masking rules before feature-owned log or offload writes, and add regression coverage with synthetic secret values.
  - Acceptance: Validation evidence proves sensitive tokens are masked in feature-generated logs/offload artifacts.
- [ ] `SEC-03-004` Path-safety constraints are missing for feature file operations
  - Action: Add explicit path-safety rules (allowlist + canonical containment checks) for feature file paths and cover traversal attempts in tests.
  - Acceptance: Tests include traversal/absolute-path attempts and verify the feature fails closed without writing outside allowed roots.

### Human Validation Requests (Product Owner / end-user)

- [ ] `PROD-03-004` Human validation checkpoint is missing
  - Action: Add a Product Owner / end-user validation checkpoint in dev-tasks with clear expected outcome statements.
  - Acceptance: Dev-tasks includes at least one explicit human validation checkpoint with expected pass/fail criteria.

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

## Change Log

| Date       | Changes                | Author       |
| ---------- | ---------------------- | ------------ |
| 2026-02-02 | Initial task breakdown | Developer/PO |
