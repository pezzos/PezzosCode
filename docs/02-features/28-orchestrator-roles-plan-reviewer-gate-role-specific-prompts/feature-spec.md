# Feature Specification: Orchestrator roles + Plan Reviewer gate + role-specific prompts

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-28`

**Owner:** Developer/PO

**Last Updated:** 2026-02-20

### Summary

Cleaner separation of responsibilities and better plan quality.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO
- **User goals:** Deliver `Orchestrator roles + Plan Reviewer gate + role-specific prompts` in line with PRD scope and constraints.
- **Current pain:** Cleaner separation of responsibilities and better plan quality.

### Why do they need it?

**As a** Developer/PO

**I want to** implement `Orchestrator roles + Plan Reviewer gate + role-specific prompts`

**So that** cleaner separation of responsibilities and better plan quality.

### User Value

- **Priority:** P1
- **Expected impact:** Cleaner separation of responsibilities and better plan quality.
- **Source notes:** Dedicated planner/reviewer/patcher/tester/reporter

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [ ] **FR-010:** Role-specific prompts and Plan Reviewer gate.
  - **Acceptance link:** Prompts exist per role and Plan Reviewer approves plan before patching.
- [ ] **FR-002:** Execute a ticket end-to-end with AI and minimal manual work.
  - **Acceptance link:** Plan → Patch → Test → Report with orchestrator gates and feedback-loop restart rules; required role logs and execution evidence are updated.
- [ ] **FR-102:** Provide a synthetic feature for end-to-end workflow smoke testing.
  - **Acceptance link:** A lightweight synthetic feature can run full Plan → Patch → Test → Report, validate gates/resume/logs, and report pass/fail before real feature execution.

#### Edge Cases

- Missing or ambiguous PRD details require explicit PO clarification.
- Existing implementation artifacts must not be overwritten destructively.
- Dependency preconditions must fail closed with actionable errors.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Generated docs contain no unresolved feature-template placeholders.
- Feature requirements in this spec map to executable tasks and tests.
- Dependencies and scope boundaries remain explicit and testable.
- Validation evidence is captured in work-item logs.
- `FR-010` acceptance satisfied: Prompts exist per role and Plan Reviewer approves plan before patching.
- `FR-002` acceptance satisfied: Plan → Patch → Test → Report with orchestrator gates and feedback-loop restart rules; required role logs and execution evidence are updated.
- `FR-102` acceptance satisfied: A lightweight synthetic feature can run full Plan → Patch → Test → Report, validate gates/resume/logs, and report pass/fail before real feature execution.

## Scope

### In Scope

- `Orchestrator roles + Plan Reviewer gate + role-specific prompts`
- Outcome from PRD: Cleaner separation of responsibilities and better plan quality.
- Feature-level documentation needed for Plan -> Patch -> Test -> Report.

### Out of Scope

- Unrelated product changes.
- New workflow automation beyond this feature.
- Destructive rewrites of completed feature folders.

## Dependencies

### Requires

- `docs/01-product/prd.md`
- `docs/02-features/AGENTS.md`
- `docs/04-process/ticket-execution-protocol.md`
- (none)

### Blocks

- None currently identified.

## Risks & Considerations

- Source notes: Dedicated planner/reviewer/patcher/tester/reporter
- Ambiguous acceptance criteria can cause rework if not clarified during planning.
