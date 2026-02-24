# Feature Specification: Bootstrap + safe template reapply

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-22`

**Owner:** Developer/PO

**Last Updated:** 2026-02-20

### Summary

New/existing repos become execution-ready with idempotent reruns.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO
- **User goals:** Deliver `Bootstrap + safe template reapply` in line with PRD scope and constraints.
- **Current pain:** New/existing repos become execution-ready with idempotent reruns.

### Why do they need it?

**As a** Developer/PO

**I want to** implement `Bootstrap + safe template reapply`

**So that** new/existing repos become execution-ready with idempotent reruns.

### User Value

- **Priority:** P0
- **Expected impact:** New/existing repos become execution-ready with idempotent reruns.
- **Source notes:** Conflict handling: overwrite/merge/skip

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [ ] **FR-101:** Reapply templates to existing repos safely.
  - **Acceptance link:** Conflicts handled by overwrite/merge/skip; idempotent reruns.
- [ ] **FR-003:** Require ticket-specific Definition of Done before coding.
  - **Acceptance link:** Ticket template includes explicit work-item DoD; execution blocks patching until DoD, tests, and report sections are defined.
- [ ] **FR-012:** Resume in-progress work items deterministically.
  - **Acceptance link:** Existing execution log resumes automatically, completed stages are skipped safely, tests/CI are re-run, and startup does not discard dirty active-worktree state unless explicitly requested.

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
- `FR-101` acceptance satisfied: Conflicts handled by overwrite/merge/skip; idempotent reruns.
- `FR-003` acceptance satisfied: Ticket template includes explicit work-item DoD; execution blocks patching until DoD, tests, and report sections are defined.
- `FR-012` acceptance satisfied: Existing execution log resumes automatically, completed stages are skipped safely, tests/CI are re-run, and startup does not discard dirty active-worktree state unless explicitly requested.

## Scope

### In Scope

- `Bootstrap + safe template reapply`
- Outcome from PRD: New/existing repos become execution-ready with idempotent reruns.
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

- Source notes: Conflict handling: overwrite/merge/skip
- Ambiguous acceptance criteria can cause rework if not clarified during planning.
