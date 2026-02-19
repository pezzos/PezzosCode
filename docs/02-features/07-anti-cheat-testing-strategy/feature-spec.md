# Feature Specification: Anti-cheat testing strategy

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-07`

**Status:** Shipped

**Owner:** Developer/PO

**Last Updated:** 2026-02-05

### Summary

Require tests that prevent hardcoded responses and validate behavior.

**Superseded by:** `F-08` in `docs/02-features/08-anti-cheat-testing-strategy/`.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** Tests validate behavior through fixtures/invariants/contracts
- **Current pain:** apply anti-cheat test rules is manual or inconsistent

### Why do they need it?

**As a** developer/PO

**I want to** apply anti-cheat test rules

**So that** behavior is real and not hardcoded

### User Value

- **Value proposition:** Tests validate behavior through fixtures/invariants/contracts
- **Expected impact:** Fewer workflow failures and clearer execution gates
- **Priority:** P1 - aligned with PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- [ ] **Requirement 1:** Multiple fixtures per critical path
  - **User action:** Run the relevant CLI/tooling step
  - **System response:** Perform the workflow action
  - **Expected outcome:** Tests validate behavior through fixtures/invariants/contracts

- [ ] **Requirement 2:** Seeded randomness and invariants
  - **User action:** Execute the next required step
  - **System response:** Enforce rules and record results
  - **Expected outcome:** Consistent, repeatable behavior

#### Edge Cases

- [ ] **Edge Case 1:** Single fixture passes a hardcoded implementation
  - **Expected behavior:** Provide a clear prompt or error and avoid state corruption

- [ ] **Edge Case 2:** Unseeded randomness causes flaky tests
  - **Expected behavior:** Fail safely and allow a clean retry

### User Experience Requirements

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

#### User Flow

```
CLI → Run command → Review output → Confirm next step
```

**Detailed Steps:**

1. User runs the relevant CLI command.
2. System executes the workflow step and logs output.
3. User reviews results and proceeds to the next gate.

#### Error Handling

| Scenario          | User Sees      | System Does   | Recovery Path      |
| ----------------- | -------------- | ------------- | ------------------ |
| Flaky tests       | Fail with seed | Stop test run | Re-run with seed   |
| Hardcoded outputs | Test failure   | Stop pipeline | Fix implementation |

### Non-Functional Requirements

- **Performance:** CLI commands complete within reasonable local dev time
- **Scalability:** Single-user workflow; no multi-user scaling needed
- **Security:** Local-only operations, no remote data transfer
- **Compatibility:** macOS-first, CLI-only

## Acceptance Criteria

### Definition of Done

- [ ] All core functionality works as specified
- [ ] Edge cases are handled appropriately
- [ ] Error states are user-friendly
- [ ] Documentation is complete
- [ ] Tests are passing
- [ ] Code is reviewed and merged

### Test Scenarios

#### Happy Path

1. **Scenario:** Execute the primary CLI flow
   - **Given:** Repo and dependencies are present
   - **When:** The command is executed
   - **Then:** Output is correct and logs are updated

#### Unhappy Path

1. **Scenario:** Required precondition is missing
   - **Given:** A dependency or approval is missing
   - **When:** The command runs
   - **Then:** Execution stops with a clear error

### Success Metrics

| Metric                | Target   | How Measured                  |
| --------------------- | -------- | ----------------------------- |
| {feature['outcome']}  | Achieved | Logs and user confirmation    |
| Fewer workflow errors | Reduced  | Error summaries               |
| Token waste           | Lower    | Offload ids and prompt review |

## Scope

### In Scope

- Implement the feature as described in the PRD
- Update process docs and templates as needed

### Out of Scope

- UI/TUI interfaces
- Cloud services

## Dependencies

### Requires

- **Docs/Process rules:** `docs/04-process/`
- **Templates/tools:** PezzosCode repo

### Blocks

- **None**

## Risks & Considerations

- Risk of inconsistent adoption without clear documentation
- Risk of skipping gates under time pressure

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                                                     | Risk                                                                                                                                                                                                                | Action                                                                                                                                                                                                               |
| ---------- | -------- | ------- | -------------- | -------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-07-001 | High     | patcher | automated-test | Yes      | Required security-relevant gates are failing                                              | Feature completion is being evaluated with failed gates (`make feature F=07` and `make ci`), so anti-cheat enforcement and pre-commit protections can be bypassed without a verified fail-closed result.            | Fix the branch-gate execution path and the `.codex/skills/readme-sync/SKILL.md` permission error, then rerun `make feature F=07` and `make ci` and record PASS evidence in validation logs before completion.        |
| SEC-07-002 | High     | patcher | patch          | Yes      | Anti-cheat control is currently phrase-based, not behavior-verified                       | Current tests and patch notes show enforcement around explicit wording (e.g., 'multiple fixtures', 'seeded randomness'), which can be satisfied textually while still shipping hardcoded or non-invariant behavior. | Add executable anti-cheat tests that assert real behavior: multiple fixture-driven assertions per critical path, invariant checks across fixture variation, and failure on hardcoded outputs independent of wording. |
| SEC-07-003 | Medium   | patcher | automated-test | Yes      | Seeded-randomness requirement lacks runtime determinism proof                             | Edge case coverage claims seeded randomness, but evidence is limited to policy/wording checks; flaky or nondeterministic tests may still pass review and mask regressions.                                          | Add deterministic test cases that run the same seed multiple times and assert identical outcomes; add a negative test that unseeded paths fail with explicit retry guidance.                                         |
| SEC-07-004 | Medium   | patcher | automated-test | Yes      | Local-only/no-remote-transfer security requirement is undocumented in validation evidence | The feature spec declares local-only operation, but no explicit automated validation is recorded; accidental network egress during workflow execution could leak repo context.                                      | Add a test or execution guard for F-07 workflow paths that asserts no network egress is required/used, and log the validation result in `docs/03-logs/validation-log.md`.                                            |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                                                   | Risk                                                                                                                                                                                               | Action                                                                                                                                                                                              |
| ----------- | -------- | ------- | ---------------- | -------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-07-001 | High     | patcher | automated-test   | Yes      | Required release gates are failing, so user-facing quality is unproven                  | Feature completion is being assessed while `make feature F=07` and `make ci` are failing, which undermines confidence that anti-cheat behavior and guardrails actually protect the user workflow.  | Fix the branch-gate path and `.codex/skills/readme-sync/SKILL.md` permission failure, rerun `make feature F=07` and `make ci`, and record PASS evidence in validation logs before marking complete. |
| PROD-07-002 | High     | patcher | patch            | Yes      | Anti-cheat acceptance is phrase-based instead of behavior-based                         | Current checks can pass by matching wording (for example, 'multiple fixtures' and 'seeded randomness') while still allowing hardcoded or non-general behavior, reducing end-user trust in results. | Add executable behavior tests using multiple fixture variations per critical path, invariant assertions across variants, and explicit failure when outputs are hardcoded regardless of wording.     |
| PROD-07-003 | Medium   | patcher | automated-test   | Yes      | Determinism promise is not validated at runtime                                         | Without repeated-seed runtime checks and negative tests for unseeded execution, users can still experience flaky outcomes and unclear retry confidence.                                            | Add tests that run identical seeds multiple times and assert identical outcomes, plus a negative test where unseeded paths fail with explicit retry guidance.                                       |
| PROD-07-004 | Medium   | patcher | automated-test   | Yes      | Local-only operation claim lacks validation evidence                                    | The feature promises no remote transfer, but no explicit automated proof is recorded; accidental network egress would violate user expectations and trust.                                         | Add a guard/test for no network egress on F-07 workflow paths and log validation evidence in `docs/03-logs/validation-log.md`.                                                                      |
| PROD-07-005 | Medium   | human   | human-validation | Yes      | Acceptance authority is ambiguous because F-07 is marked shipped but superseded by F-08 | Development/testing may optimize or close the wrong artifact, and end-user validation can be signed off against outdated scope.                                                                    | PO must explicitly decide whether F-07 is archival-only or still acceptance-active, map evidence to the authoritative feature, and record sign-off decision.                                        |

<!-- review-findings:end -->
