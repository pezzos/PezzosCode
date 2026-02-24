# Feature Specification: Single-worktree orchestration + template-drift hardening

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-26`

**Owner:** Developer/PO

**Last Updated:** 2026-02-20

### Summary

Reliable role collaboration without worktree tracking-file drift.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO
- **User goals:** Deliver `Single-worktree orchestration + template-drift hardening` in line with PRD scope and constraints.
- **Current pain:** Reliable role collaboration without worktree tracking-file drift.

### Why do they need it?

**As a** Developer/PO

**I want to** implement `Single-worktree orchestration + template-drift hardening`

**So that** reliable role collaboration without worktree tracking-file drift.

### User Value

- **Priority:** P0
- **Expected impact:** Reliable role collaboration without worktree tracking-file drift.
- **Source notes:** No `feature-worktrees.json`; deterministic recovery

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [ ] **FR-014:** Harden template drift detection and scoped autofix recovery.
  - **Acceptance link:** Workflow detects template/living-file drift, attempts deterministic scoped repairs, re-stages only allowed files, and fails with explicit remediation when unresolved.
- [ ] **FR-017:** Enforce token budget guardrails with compact summaries.
  - **Acceptance link:** Each role step records concise summaries, offloads overflow output, and reports deterministic remediation when budget guardrails are exceeded.
- [ ] **FR-018:** Expand deterministic auto-fix and auto-recovery for common failure classes.
  - **Acceptance link:** Sync/formatting/staging/retry-safe rerun failures attempt scoped deterministic repair first; unresolved cases fail closed with explicit remediation.

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
- `FR-014` acceptance satisfied: Workflow detects template/living-file drift, attempts deterministic scoped repairs, re-stages only allowed files, and fails with explicit remediation when unresolved.
- `FR-017` acceptance satisfied: Each role step records concise summaries, offloads overflow output, and reports deterministic remediation when budget guardrails are exceeded.
- `FR-018` acceptance satisfied: Sync/formatting/staging/retry-safe rerun failures attempt scoped deterministic repair first; unresolved cases fail closed with explicit remediation.

## Scope

### In Scope

- `Single-worktree orchestration + template-drift hardening`
- Outcome from PRD: Reliable role collaboration without worktree tracking-file drift.
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

- Source notes: No `feature-worktrees.json`; deterministic recovery
- Ambiguous acceptance criteria can cause rework if not clarified during planning.
