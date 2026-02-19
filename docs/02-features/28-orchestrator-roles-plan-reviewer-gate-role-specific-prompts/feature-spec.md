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

## Automated Review Summary

<!-- review-findings:start -->

### Security Constraints

- `SEC-28-002` Access-control expectations are missing for feature scope
  - Specification constraint: Document required authorization expectations and denied-path behavior for feature actions that can change protected state.
  - Blocking: Yes
- `SEC-28-003` Sensitive-data redaction is undefined for feature logging/output
  - Specification constraint: If this feature writes logs/offload/output artifacts, define redaction rules for secrets and sensitive tokens.
  - Blocking: Yes
- `SEC-28-004` Path-safety constraints are missing for feature file operations
  - Specification constraint: Where feature behavior constructs file paths, define canonicalization, containment checks, and traversal rejection.
  - Blocking: Yes

### Product Constraints

- `PROD-28-002` User journey details are missing
  - Specification constraint: Describe the user journey for this feature including entry point, completion state, and error path expectation.
  - Blocking: Yes
- `PROD-28-005` Acceptance criteria are not measurable
  - Specification constraint: Define measurable acceptance outcomes for this feature so completion can be verified objectively.
  - Blocking: No

<!-- review-findings:end -->
