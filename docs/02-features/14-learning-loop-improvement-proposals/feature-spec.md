# Feature Specification: Learning loop improvement proposals

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-14`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-08

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
