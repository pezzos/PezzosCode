# Feature Specification: Resume safety + deterministic auto-recovery + fail-closed commit gate

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-27`

**Owner:** Developer/PO

**Last Updated:** 2026-02-20

### Summary

Interrupted runs resume safely; common deterministic failures self-heal safely.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO
- **User goals:** Deliver `Resume safety + deterministic auto-recovery + fail-closed commit gate` in line with PRD scope and constraints.
- **Current pain:** Interrupted runs resume safely; common deterministic failures self-heal safely.

### Why do they need it?

**As a** Developer/PO

**I want to** implement `Resume safety + deterministic auto-recovery + fail-closed commit gate`

**So that** interrupted runs resume safely; common deterministic failures self-heal safely.

### User Value

- **Priority:** P0
- **Expected impact:** Interrupted runs resume safely; common deterministic failures self-heal safely.
- **Source notes:** Active-WIP preserve by default; strict commit gate

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [ ] **FR-018:** Expand deterministic auto-fix and auto-recovery for common failure classes.
  - **Acceptance link:** Sync/formatting/staging/retry-safe rerun failures attempt scoped deterministic repair first; unresolved cases fail closed with explicit remediation.
- [ ] **FR-011:** Post-run improvement proposals with human gate.
  - **Acceptance link:** Failures log errors with `WI/agent/step`, propose a patch (not auto-applied), and record in `docs/possible-improvements.md`.
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
- `FR-018` acceptance satisfied: Sync/formatting/staging/retry-safe rerun failures attempt scoped deterministic repair first; unresolved cases fail closed with explicit remediation.
- `FR-011` acceptance satisfied: Failures log errors with `WI/agent/step`, propose a patch (not auto-applied), and record in `docs/possible-improvements.md`.
- `FR-012` acceptance satisfied: Existing execution log resumes automatically, completed stages are skipped safely, tests/CI are re-run, and startup does not discard dirty active-worktree state unless explicitly requested.

## Scope

### In Scope

- `Resume safety + deterministic auto-recovery + fail-closed commit gate`
- Outcome from PRD: Interrupted runs resume safely; common deterministic failures self-heal safely.
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

- Source notes: Active-WIP preserve by default; strict commit gate
- Ambiguous acceptance criteria can cause rework if not clarified during planning.
