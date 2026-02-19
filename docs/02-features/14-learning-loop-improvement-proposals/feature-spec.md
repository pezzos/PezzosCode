# Feature Specification: Learning loop improvement proposals

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-14`

**Owner:** Developer/PO

**Last Updated:** 2026-02-09

### Summary

Formalize the post-run learning loop so every failed or stalled work item can generate a human-gated improvement proposal in `docs/possible-improvements.md`, with enough structured context to be actionable and non-duplicative.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** reduce repeat failures and accumulate workflow improvements
- **Current pain:** process docs mention proposals, but feature docs are too generic to implement consistent proposal generation/deduplication

### Why do they need it?

**As a** developer/PO

**I want to** capture structured improvement proposals after failed/stalled runs

**So that** recurring issues are converted into explicit, reviewable improvements

### User Value

- **Value proposition:** faster recovery from repeated workflow failures
- **Expected impact:** lower repeat incident rate and clearer improvement backlog
- **Priority:** P1 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Detect failure/stall outcomes from work item execution context (`WI`, `agent`, `step`, failure summary).
- **Requirement 2:** Generate proposal entries in `docs/possible-improvements.md` using the existing template fields.
- **Requirement 3:** Keep proposals human-gated (status starts as `Proposed`; no auto-apply of patches).
- **Requirement 4:** Deduplicate repeated failures by signature (work item + step + normalized failure summary; agent not part of signature) to avoid noisy duplicates.
- **Requirement 5:** Missing execution context uses placeholders (e.g., `Unknown`, `TBD`) and appends a missing-context note in the failure summary.

#### Edge Cases

- **Edge Case 1:** Missing execution context (for example, failure happened before WI metadata was populated).
- **Edge Case 2:** Multiple agents report the same root issue in one run (single proposal, agent list combined).
- **Edge Case 3:** Successful run should not generate proposals.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Failed/stalled `make feature` runs can produce a proposal entry with required fields (`Date`, `Work Item`, `Agent`, `Step`, `Failure Summary`, `Proposed Improvement`, `Status`).
- Proposals are recorded as `Proposed` and are never auto-applied.
- Duplicate proposals for the same failure signature (normalized summary) are merged or skipped with explicit rationale.
- Missing context still produces a proposal with placeholders and a missing-context note.
- Process docs and feature docs use consistent wording for post-run improvement proposals.

## Scope

### In Scope

- Proposal generation rules
- `docs/possible-improvements.md` entry lifecycle (Proposed -> Approved/Rejected by human)
- Deduplication strategy
- Workflow/log integration needed to capture context

### Out of Scope

- Automatic patch application
- Remote ticketing integrations
- Non-workflow proposal sources

## Dependencies

### Requires

- **Process docs:** `docs/04-process/dev-workflow.md`, `docs/04-process/human-orchestration-workflow.md`
- **Proposal registry:** `docs/possible-improvements.md`
- **Workflow engine/logs:** `tools/pc-feature`, `logs/<WI>/<step>.log`

### Blocks

- **None**

## Risks & Considerations

- Low-signal failures can create proposal noise if dedup/signature rules are weak.
- Proposal quality depends on accurate step-level context from workflow logs.

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase            | Blocking | Title                                                              | Risk                                                                                                                                                                                                                         | Action                                                                                                                                                                                                            |
| ---------- | -------- | ------- | ---------------- | -------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-14-001 | High     | patcher | patch            | Yes      | Failure summaries are persisted without secret redaction controls  | Feature docs require writing fail/stall context into `docs/possible-improvements.md`, but no requirement/test enforces masking of tokens, keys, passwords, or PII from logs; sensitive data can be committed to git.         | Add a mandatory redaction pass before proposal write (credential/secret patterns + high-entropy token heuristics), replace matches with `[REDACTED]`, and fail-closed if redaction cannot safely process payload. |
| SEC-14-002 | Medium   | patcher | patch            | Yes      | Untrusted log content is not constrained before markdown insertion | Failure text from execution context can include ANSI/control bytes or crafted markdown content; without sanitization/length limits this can poison docs rendering, mislead reviewers, and create oversized proposal entries. | Normalize proposal fields to safe plaintext (strip control/ANSI chars, escape markdown-sensitive characters where needed), enforce maximum field lengths, and append a truncated note with log pointer.           |
| SEC-14-003 | Medium   | patcher | patch            | Yes      | Dedup signature is collision-prone for incident integrity          | Current signature (`work item + step + normalized summary`, excluding agent) can over-merge distinct failures, allowing security-relevant incidents to be suppressed as duplicates.                                          | Harden dedup with canonical hashing of raw summary + normalized key, and require collision-safe behavior (append separate evidence/collision note instead of silent skip when raw payloads differ).               |
| SEC-14-004 | Medium   | patcher | automated-test   | Yes      | Security abuse cases are missing from automated tests              | Defined tests cover happy-path fail/stall/dedup/success only; regressions in redaction, sanitization, and collision handling can ship undetected.                                                                            | Add automated tests with malicious fixtures: secret-bearing summaries, control-character/markdown payloads, and near-collision dedup inputs; gate completion on these passing.                                    |
| SEC-14-005 | Low      | human   | human-validation | No       | Human gate lacks explicit security review criteria                 | Docs specify `Proposed` human gating but no explicit validation checklist for sensitive-data leakage or unsafe proposal text, increasing approval inconsistency.                                                             | Add a human-validation checklist item requiring verification that proposal entries contain no secrets and no unsafe execution instructions before `Approved`.                                                     |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                                      | Risk                                                                                                                                                                                 | Action                                                                                                                                                             |
| ----------- | -------- | ------- | ---------------- | -------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| PROD-14-001 | High     | patcher | patch            | Yes      | Proposal content safety is not enforced before writing to user-facing docs | Fail/stall summaries can leak secrets or include unsafe/garbled content, which undermines trust in `docs/possible-improvements.md` and creates review friction for the Developer/PO. | Add mandatory pre-write redaction, sanitization, and length limiting with fail-closed behavior if safety processing cannot complete.                               |
| PROD-14-002 | High     | patcher | patch            | Yes      | Dedup logic can suppress distinct user-impacting failures                  | Current signature strategy can over-merge incidents, hiding separate root causes and reducing the learning loop’s value.                                                             | Harden dedup with collision-safe matching (canonical hash + raw-evidence comparison) and record explicit collision rationale instead of silent skip/merge.         |
| PROD-14-003 | Medium   | patcher | automated-test   | Yes      | Acceptance quality lacks adversarial test coverage                         | Without malicious and near-collision fixtures, regressions in redaction, sanitization, and dedup integrity can ship while core acceptance still appears green.                       | Add automated tests for secret-bearing summaries, markdown/control-character payloads, and dedup near-collision cases; make these tests required for completion.   |
| PROD-14-004 | Medium   | patcher | patch            | Yes      | Workflow evidence appears internally inconsistent                          | Feature artifacts show mixed completion signals (e.g., completed status with pending sections), which weakens workflow clarity and approval confidence.                              | Enforce deterministic status consistency checks across feature logs/reports and update generated artifacts so completion evidence is unambiguous.                  |
| PROD-14-005 | Low      | human   | human-validation | No       | Human approval criteria are not explicit enough for proposal quality       | Approvals may be inconsistent if reviewers are not required to verify user-value quality (clear problem statement, actionable improvement, and safe content).                        | Add a human validation checklist for proposal approval covering usefulness, clarity, duplicate rationale, and safety review before status changes from `Proposed`. |

<!-- review-findings:end -->
