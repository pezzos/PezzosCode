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

## Change Log

| Date       | Version | Changes      | Author |
| ---------- | ------- | ------------ | ------ |
| 2026-02-11 | 0.1     | Initial spec | Codex  |
