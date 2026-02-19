# Feature Specification: Orchestrator roles + Plan Reviewer gate + role-specific prompts

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-06`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-19

### Summary

Cleaner separation of responsibilities and better plan quality.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO
- **User goals:** Deliver `Orchestrator roles + Plan Reviewer gate + role-specific prompts` with deterministic behavior.
- **Current pain:** PRD intent exists, but feature-level execution details are missing.

### Why do they need it?

**As a** developer/PO

**I want to** implement `Orchestrator roles + Plan Reviewer gate + role-specific prompts`

**So that** the prioritized PRD outcome is delivered reliably.

### User Value

- **Value proposition:** Converts PRD intent into executable feature scope.
- **Expected impact:** Cleaner separation of responsibilities and better plan quality.
- **Priority:** P1.

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Implement `Orchestrator roles + Plan Reviewer gate + role-specific prompts` according to PRD priority `P1`.
- **Requirement 2:** Keep behavior deterministic and idempotent on reruns.
- **Requirement 3:** Document boundaries, success criteria, and evidence paths.

#### Edge Cases

- Missing or ambiguous PRD details require explicit PO clarification.
- Existing implementation artifacts must not be overwritten destructively.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Feature folder content is specific to this PRD item, not template placeholders.
- Functional behavior and tests are defined before patching.
- Scope boundaries and non-goals are explicit.
- Validation evidence is captured in work-item logs.

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

### Blocks

- None currently identified.

## Risks & Considerations

- Source notes: Dedicated planner/reviewer/patcher/tester/reporter
- Ambiguous acceptance criteria can cause rework if not clarified during planning.
