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

### Security Expert

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                                      | Risk                                                                                                                                                                                                                     | Action                                                                                                                                                                                                |
| ---------- | -------- | ------- | -------------- | -------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| SEC-20-001 | High     | patcher | patch          | Yes      | Unsanitized work-item identifiers can escape log/offload directories       | The feature depends on artifacts under `logs/<WI>/` and offload pointers, but the provided docs do not require strict validation of `<WI>`/scenario IDs. Traversal values could read/write outside intended directories. | In `tools/pc-feature`, enforce a strict ID format, canonicalize resolved paths, and fail closed if any path is outside approved roots. Add tests for `../`, absolute paths, and symlink-hop attempts. |
| SEC-20-002 | High     | patcher | patch          | Yes      | Allowed Tests policy can be bypassed without shell-safe command validation | Docs require Allowed Tests enforcement but only describe command whitelisting; they do not require shell-free execution or canonical argv matching. Chaining/metacharacter payloads can execute non-allowed commands.    | Execute tests without shell, compare normalized argv against a structured allowlist, and reject metacharacters/multi-command forms. Add negative tests for `;`, `&&`, `                               | `, and `$()` bypass attempts. |
| SEC-20-003 | Medium   | patcher | patch          | Yes      | No secret-redaction control for evidence pointers and structured logs      | The workflow explicitly offloads noisy output and emits evidence pointers, but no redaction requirement is defined. Credentials or sensitive env-derived values can leak into `.offload` files and summaries.            | Implement log/summarization redaction for common secret patterns and sensitive keys, then add fixture tests with seeded fake secrets to verify masking in both logs and pass/fail output.             |
| SEC-20-004 | Medium   | patcher | automated-test | Yes      | Resume-path security is untested against tampered state/artifacts          | Acceptance scenarios include resume behavior, but the provided test scope does not require adversarial cases (tampered resume state or forged stage evidence). This can permit false PASS via manipulated artifacts.     | Add automated tests that alter resume/state/evidence artifacts and assert fail-closed behavior (no stage skip, no completion) until integrity checks pass.                                            |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                                      | Risk                                                                                                                                            | Action                                                                                                                                                                                                                   |
| ----------- | -------- | ------- | ---------------- | -------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| PROD-20-001 | High     | human   | human-validation | Yes      | Smoke-test trigger policy is unresolved                                    | Without a default policy for when to run the smoke test, users can skip it before real work and lose the core regression-prevention value.      | PO must choose and document the default trigger matrix (before each `make feature`, PR CI behavior, and override rules) and approve it in feature docs.                                                                  |
| PROD-20-002 | High     | patcher | automated-test   | Yes      | Failure summary contract is not strict enough for fast recovery            | Pass/fail output can be technically correct but still non-actionable, causing slow troubleshooting and repeated failed runs.                    | Implement a required summary schema with `stage`, `failed_invariant`, `evidence_pointer_or_log_path`, and `next_action`; add automated tests that assert schema presence for baseline-fail and gate-violation scenarios. |
| PROD-20-003 | High     | human   | human-validation | Yes      | Product DoD does not explicitly gate on security blocker closure           | If SEC-20-001 to SEC-20-004 are not part of completion criteria, users may receive a false-safe smoke result that can leak data or be bypassed. | Add explicit release-gate text in feature docs requiring closure evidence for SEC-20-001 through SEC-20-004 before marking this feature complete.                                                                        |
| PROD-20-004 | Medium   | patcher | automated-test   | No       | Runtime bound lacks measurable threshold                                   | A qualitative 'bounded runtime' can drift upward and make frequent use impractical, reducing adoption.                                          | Define concrete runtime budgets for local and CI runs and enforce/report them in automated tests.                                                                                                                        |
| PROD-20-005 | Medium   | human   | human-validation | No       | Human readability of resume/skip/repair states is not explicitly validated | Users may misinterpret resumed vs newly executed stages, leading to incorrect trust in outcomes.                                                | Run a human-validation checklist on one resumed and one fresh run to confirm status wording is unambiguous and evidence pointers are easy to follow.                                                                     |

<!-- review-findings:end -->

## Change Log

| Date       | Version | Changes      | Author |
| ---------- | ------- | ------------ | ------ |
| 2026-02-11 | 0.1     | Initial spec | Codex  |
