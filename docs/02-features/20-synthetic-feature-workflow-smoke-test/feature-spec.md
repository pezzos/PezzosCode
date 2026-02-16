# Feature Specification: Synthetic feature workflow smoke test

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-20`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-11

### Summary

Provide a lightweight synthetic feature that exercises the full Plan -> Patch -> Test -> Report workflow.
The smoke test validates orchestration, gates, resume behavior, and structured logs before running high-value real features.

## User Intent

### Who is this for?

- Primary: Developer/PO who wants a fast confidence check of workflow health.

### Why do they need it?

- Regressions in orchestration logic are costly when discovered mid-feature.

### User Value

- Early detection of workflow regressions.
- Repeatable collaboration test path for patcher/tester/reporter loop.
- Faster troubleshooting due to known synthetic baseline.

## Feature Requirements

### Functional Requirements

- [ ] Provide a synthetic feature fixture runnable in local workflow.
- [ ] Execute full role loop and final gate using deterministic criteria.
- [ ] Validate key invariants: role routing, Allowed Tests enforcement, resume behavior, structured logging.
- [ ] Emit a concise pass/fail summary with evidence pointers.
- [ ] Keep runtime bounded so the smoke test is practical for frequent use.

### User Experience Requirements

#### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI

### Non-Functional Requirements

- Smoke test must be deterministic and idempotent.
- Synthetic fixture must remain lightweight and isolated from production features.
- Failures must point to actionable workflow stage diagnostics.

## Acceptance Criteria

### Definition of Done

- Synthetic feature run can validate workflow end-to-end on demand.
- Pass/fail outcome clearly identifies failed stage and log evidence.
- Smoke test can run before real feature execution with minimal setup.

### Test Scenarios

- Healthy baseline run passes all stages.
- Introduced gate violation fails at expected stage.
- Resume-path scenario confirms restart routing still works.

### Success Metrics

- Faster detection of orchestration regressions.
- Reduced failed real-feature runs caused by workflow drift.

## Scope

### In Scope

- Synthetic fixture definition and runner integration.
- End-to-end workflow assertions.
- Pass/fail reporting and evidence references.

### Out of Scope

- Full product behavior testing beyond workflow mechanics.
- Long-running load/performance benchmarking.

## Dependencies

### Requires

- `tools/pc-feature`
- Existing test harness (`tests/`)
- Structured logs in `logs/<WI>/`

### Blocks

- Reliable pre-flight confidence checks for future workflow changes.

## Risks & Considerations

- Overly complex synthetic fixture can become flaky and expensive.
- Underpowered assertions may miss critical regressions.

## Open Questions

- Should the smoke test run on every PR/local CI, or only before planned feature execution?

## Related Documents

- PRD: `docs/01-product/prd.md`
- Protocol: `docs/04-process/ticket-execution-protocol.md`
- Testing Strategy: `docs/04-process/testing-strategy.md`

## Automated Review Findings

<!-- review-findings:start -->

### Security Reviewer

| ID         | Severity | Risk                                                                           | Action                                                                                           |
| ---------- | -------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| SEC-20-001 | High     | Unvalidated input can trigger data corruption or unsafe behavior.              | Add explicit validation rules, error paths, and anti-bypass tests in feature-spec and dev-tasks. |
| SEC-20-003 | Medium   | Credentials or tokens may leak into code, logs, or config.                     | Document secret sources, redaction strategy, and prohibited storage locations.                   |
| SEC-20-004 | High     | Missing injection controls can expose command, SQL, or script injection paths. | Define escaping/parameterization requirements and add dedicated injection test scenarios.        |
| SEC-20-005 | Medium   | Unsafe defaults can bypass intended runtime protections.                       | Capture required config defaults, permission boundaries, and misconfiguration failure behavior.  |

### Product Manager

| ID          | Severity | Risk                                                                    | Action                                                                                                     |
| ----------- | -------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| PROD-20-001 | High     | Key product capabilities may be missed during implementation.           | Expand functional requirements to cover primary and edge behaviors with acceptance criteria.               |
| PROD-20-002 | Medium   | Implementation may diverge from intended user path and onboarding flow. | Add explicit user journey steps, entry points, and completion states.                                      |
| PROD-20-003 | Medium   | Cross-feature workflow alignment may be inconsistent.                   | Update `docs/01-product/ux-ui.md` to include 'Synthetic feature workflow smoke test' journey and workflow. |
| PROD-20-005 | Low      | Human acceptance timing may be unclear before execution starts.         | Add a `Product Owner test checkpoint` task in dev-tasks before first make feature execution.               |

<!-- review-findings:end -->

## Change Log

| Date       | Version | Changes      | Author |
| ---------- | ------- | ------------ | ------ |
| 2026-02-11 | 0.1     | Initial spec | Codex  |
