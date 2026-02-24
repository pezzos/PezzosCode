# Feature Specification: Incremental PRD-to-features + post-run learning loop

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-30`

**Owner:** Developer/PO

**Last Updated:** 2026-02-20

### Summary

Feature docs evolve safely and repeated failures are reduced.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO
- **User goals:** Deliver `Incremental PRD-to-features + post-run learning loop` in line with PRD scope and constraints.
- **Current pain:** Feature docs evolve safely and repeated failures are reduced.

### Why do they need it?

**As a** Developer/PO

**I want to** implement `Incremental PRD-to-features + post-run learning loop`

**So that** feature docs evolve safely and repeated failures are reduced.

### User Value

- **Priority:** P1
- **Expected impact:** Feature docs evolve safely and repeated failures are reduced.
- **Source notes:** Add-missing only; human-gated improvements

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [ ] **FR-011:** Post-run improvement proposals with human gate.
  - **Acceptance link:** Failures log errors with `WI/agent/step`, propose a patch (not auto-applied), and record in `docs/possible-improvements.md`.
- [ ] **FR-009:** Incremental prd-to-features generation.
  - **Acceptance link:** Adds missing features only, never deletes existing, skips features with `Status: Done` in `dev-tasks.md`.
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
- `FR-011` acceptance satisfied: Failures log errors with `WI/agent/step`, propose a patch (not auto-applied), and record in `docs/possible-improvements.md`.
- `FR-009` acceptance satisfied: Adds missing features only, never deletes existing, skips features with `Status: Done` in `dev-tasks.md`.
- `FR-012` acceptance satisfied: Existing execution log resumes automatically, completed stages are skipped safely, tests/CI are re-run, and startup does not discard dirty active-worktree state unless explicitly requested.

## Scope

### In Scope

- `Incremental PRD-to-features + post-run learning loop`
- Outcome from PRD: Feature docs evolve safely and repeated failures are reduced.
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

- Source notes: Add-missing only; human-gated improvements
- Ambiguous acceptance criteria can cause rework if not clarified during planning.
