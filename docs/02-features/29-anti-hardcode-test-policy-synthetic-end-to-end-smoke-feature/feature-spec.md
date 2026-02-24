# Feature Specification: Anti-hardcode test policy + synthetic end-to-end smoke feature

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-29`

**Owner:** Developer/PO

**Last Updated:** 2026-02-20

### Summary

Better regression resistance and early workflow break detection.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO
- **User goals:** Deliver `Anti-hardcode test policy + synthetic end-to-end smoke feature` in line with PRD scope and constraints.
- **Current pain:** Better regression resistance and early workflow break detection.

### Why do they need it?

**As a** Developer/PO

**I want to** implement `Anti-hardcode test policy + synthetic end-to-end smoke feature`

**So that** better regression resistance and early workflow break detection.

### User Value

- **Priority:** P1
- **Expected impact:** Better regression resistance and early workflow break detection.
- **Source notes:** Fixtures + seeds + invariants + boundary contracts

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [ ] **FR-102:** Provide a synthetic feature for end-to-end workflow smoke testing.
  - **Acceptance link:** A lightweight synthetic feature can run full Plan → Patch → Test → Report, validate gates/resume/logs, and report pass/fail before real feature execution.
- [ ] **FR-103:** Enforce anti-hardcode testing coverage.
  - **Acceptance link:** Plan/TDD states fixture count (>=2 critical-path fixtures), deterministic seed strategy, invariant assertions, and boundary contract tests.
- [ ] **FR-002:** Execute a ticket end-to-end with AI and minimal manual work.
  - **Acceptance link:** Plan → Patch → Test → Report with orchestrator gates and feedback-loop restart rules; required role logs and execution evidence are updated.

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
- `FR-102` acceptance satisfied: A lightweight synthetic feature can run full Plan → Patch → Test → Report, validate gates/resume/logs, and report pass/fail before real feature execution.
- `FR-103` acceptance satisfied: Plan/TDD states fixture count (>=2 critical-path fixtures), deterministic seed strategy, invariant assertions, and boundary contract tests.
- `FR-002` acceptance satisfied: Plan → Patch → Test → Report with orchestrator gates and feedback-loop restart rules; required role logs and execution evidence are updated.

## Scope

### In Scope

- `Anti-hardcode test policy + synthetic end-to-end smoke feature`
- Outcome from PRD: Better regression resistance and early workflow break detection.
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

- Source notes: Fixtures + seeds + invariants + boundary contracts
- Ambiguous acceptance criteria can cause rework if not clarified during planning.
