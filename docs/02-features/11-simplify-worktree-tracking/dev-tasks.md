# Development Tasks: Simplify worktree tracking

> **LLM-executable tasks**
>
> This document contains specific, actionable tasks that can be executed by developers (human or AI). Each task should be atomic, testable, and clearly defined.

---

## Overview

**Feature:** Simplify worktree tracking

**Status:** Not Started

**Last Updated:** 2026-02-05

## Tasks

- Task 1: Remove file references
- Task 2: Update docs/templates

## Execution Log

- No runs yet.

## Related Documents

- Feature Spec: [link to feature-spec.md]
- Tech Design: [link to tech-design.md]
- Test Plan: [link to test-plan.md]
- Planner Log: [link to planner-log.md]
- Reporter Log: [link to reporter-log.md]
- Validation Log: [link to validation-log.md]

## Change Log

| Date       | Changes                | Author       |
| ---------- | ---------------------- | ------------ |
| 2026-02-05 | Initial task breakdown | Primary user |

## Review Findings Backlog

<!-- review-backlog:start -->

### Security Reviewer Tasks

- [ ] `SEC-11-001` Input validation controls are not explicit
  - Severity: High
  - Action: Add explicit validation rules, error paths, and anti-bypass tests in feature-spec and dev-tasks.
- [ ] `SEC-11-004` Injection defenses are not explicit
  - Severity: High
  - Action: Define escaping/parameterization requirements and add dedicated injection test scenarios.
- [ ] `SEC-11-005` Infrastructure misconfiguration guardrails are missing
  - Severity: Medium
  - Action: Capture required config defaults, permission boundaries, and misconfiguration failure behavior.

### Product Manager Tasks

- [ ] `PROD-11-002` User journey details are missing in feature docs
  - Severity: Medium
  - Action: Add explicit user journey steps, entry points, and completion states.
- [ ] `PROD-11-003` Global UX blueprint does not reference this feature
  - Severity: Medium
  - Action: Update `docs/01-product/ux-ui.md` to include 'Simplify worktree tracking' journey and workflow.
- [ ] `PROD-11-005` PO validation checkpoint is missing
  - Severity: Low
  - Action: Add a `Product Owner test checkpoint` task in dev-tasks before first make feature execution.

<!-- review-backlog:end -->
