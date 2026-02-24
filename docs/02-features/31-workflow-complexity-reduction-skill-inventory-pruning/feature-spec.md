# Feature Specification: Workflow complexity reduction + skill inventory pruning

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-31`

**Owner:** Developer/PO

**Last Updated:** 2026-02-20

### Summary

Lower maintenance overhead with fewer fragile execution paths.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO
- **User goals:** Deliver `Workflow complexity reduction + skill inventory pruning` in line with PRD scope and constraints.
- **Current pain:** Lower maintenance overhead with fewer fragile execution paths.

### Why do they need it?

**As a** Developer/PO

**I want to** implement `Workflow complexity reduction + skill inventory pruning`

**So that** lower maintenance overhead with fewer fragile execution paths.

### User Value

- **Priority:** P1
- **Expected impact:** Lower maintenance overhead with fewer fragile execution paths.
- **Source notes:** Remove/archive low-value skills and redundant script/config paths

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [ ] **FR-104:** Prune low-value skill inventory regularly.
  - **Acceptance link:** Workflow includes periodic review to remove/archive unused or redundant skills while preserving required execution capabilities.
- [ ] **FR-105:** Reduce redundant execution paths and configuration complexity.
  - **Acceptance link:** Equivalent behavior is maintained while consolidating redundant paths; removed paths are documented with rollback notes.
- [ ] **FR-005:** Provide a shared runner library for tool/script execution.
  - **Acceptance link:** Tools can call a shared runner that injects `work_item_id`, `agent_name`, `run_id` and logging helpers.

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
- `FR-104` acceptance satisfied: Workflow includes periodic review to remove/archive unused or redundant skills while preserving required execution capabilities.
- `FR-105` acceptance satisfied: Equivalent behavior is maintained while consolidating redundant paths; removed paths are documented with rollback notes.
- `FR-005` acceptance satisfied: Tools can call a shared runner that injects `work_item_id`, `agent_name`, `run_id` and logging helpers.

## Scope

### In Scope

- `Workflow complexity reduction + skill inventory pruning`
- Outcome from PRD: Lower maintenance overhead with fewer fragile execution paths.
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

- Source notes: Remove/archive low-value skills and redundant script/config paths
- Ambiguous acceptance criteria can cause rework if not clarified during planning.
