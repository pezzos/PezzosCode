# Feature Specification: Commit gated by completed ticket docs

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-18`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-11

### Summary

Prevent commits when ticket documentation is incomplete.
The commit step must verify required execution-log, test, and final-report fields before allowing commit generation.

## User Intent

### Who is this for?

- Primary: Developer/PO relying on execution logs for auditability and handoff quality.

### Why do they need it?

- Incomplete ticket docs weaken confidence in what was changed, validated, and approved.

### User Value

- Stronger traceability for each work item.
- Clear pass/fail criteria before commit.
- Lower risk of undocumented behavior changes.

## Feature Requirements

### Functional Requirements

- [ ] Validate required work-item doc fields before commit is attempted.
- [ ] Block commit with explicit remediation when required sections are missing.
- [ ] Auto-fill deterministic sections where safe (for example, command metadata) without masking missing evidence.
- [ ] Keep role ownership rules (planner/tester/reporter logs) intact.
- [ ] Record commit-gate decision in feature/run logs.

### User Experience Requirements

#### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI

### Non-Functional Requirements

- Commit-gate checks must be deterministic and idempotent.
- Failure messages must identify missing sections precisely.
- Gate evaluation must avoid touching out-of-scope files.

## Acceptance Criteria

### Definition of Done

- Commit is blocked when required execution-doc fields are missing.
- Commit proceeds only when docs satisfy protocol requirements.
- Validation evidence is recorded in logs.

### Test Scenarios

- Missing `Tests Run` section blocks commit and returns remediation.
- Missing final report fields blocks commit.
- Fully complete docs allow commit path to continue.

### Success Metrics

- Decrease in commits with incomplete ticket documentation.
- Faster review due to consistent final report/test evidence.

## Scope

### In Scope

- Commit precheck for execution-doc completeness.
- Deterministic error messaging for missing fields.
- Logging of commit-gate outcomes.

### Out of Scope

- New git workflow model beyond existing `tools/pc-commit` contract.
- Auto-authoring of narrative report content.

## Dependencies

### Requires

- `tools/pc-feature`
- `tools/pc-commit`
- `docs/04-process/ticket-execution-protocol.md`

### Blocks

- Reliable merge collection and release notes quality.

## Risks & Considerations

- Overly strict parsing could block valid commits.
- Overly permissive checks could allow incomplete records.

## Open Questions

- Should missing sections always be hard-blocking, or support feature-level override for manual emergency commits?

## Related Documents

- PRD: `docs/01-product/prd.md`
- Git Workflow: `docs/04-process/git-workflow.md`
- Protocol: `docs/04-process/ticket-execution-protocol.md`

## Automated Review Findings

<!-- review-findings:start -->

### Security Reviewer

| ID         | Severity | Risk                                                                           | Action                                                                                    |
| ---------- | -------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| SEC-18-003 | Medium   | Credentials or tokens may leak into code, logs, or config.                     | Document secret sources, redaction strategy, and prohibited storage locations.            |
| SEC-18-004 | High     | Missing injection controls can expose command, SQL, or script injection paths. | Define escaping/parameterization requirements and add dedicated injection test scenarios. |

### Product Manager

| ID          | Severity | Risk                                                                    | Action                                                                                                     |
| ----------- | -------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| PROD-18-001 | High     | Key product capabilities may be missed during implementation.           | Expand functional requirements to cover primary and edge behaviors with acceptance criteria.               |
| PROD-18-002 | Medium   | Implementation may diverge from intended user path and onboarding flow. | Add explicit user journey steps, entry points, and completion states.                                      |
| PROD-18-003 | Medium   | Cross-feature workflow alignment may be inconsistent.                   | Update `docs/01-product/ux-ui.md` to include 'Commit gated by completed ticket docs' journey and workflow. |
| PROD-18-005 | Low      | Human acceptance timing may be unclear before execution starts.         | Add a `Product Owner test checkpoint` task in dev-tasks before first make feature execution.               |

<!-- review-findings:end -->

## Change Log

| Date       | Version | Changes      | Author |
| ---------- | ------- | ------------ | ------ |
| 2026-02-11 | 0.1     | Initial spec | Codex  |
