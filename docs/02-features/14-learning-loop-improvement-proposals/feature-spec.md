# Feature Specification: Learning loop improvement proposals

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-14`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-05

### Summary

After `make feature` completes or stops, propose improvements (not auto-applied) and log them for human review.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** avoid repeated failures
- **Current pain:** errors recur without captured improvements

### Why do they need it?

**As a** developer/PO

**I want to** human-gated improvement proposals

**So that** compounding workflow quality

### User Value

- **Value proposition:** compounding workflow quality
- **Expected impact:** Lower token burn and fewer regressions
- **Priority:** P1 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Log script failures with `work_item_id`, `agent_name`, `step`
- **Requirement 2:** Propose a patch after runs stop/complete (no auto-apply)
- **Requirement 3:** Record proposals in `docs/possible-improvements.md`

#### Edge Cases

- **Edge Case 1:** Repeated failures produce duplicate proposals

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Proposals are recorded with status and decision refs

## Scope

### In Scope

- Logging of failures
- Proposal capture

### Out of Scope

- Auto-applying fixes

## Dependencies

### Requires

- **Docs/Process rules:** `docs/04-process/`
- **Templates/tools:** PezzosCode repo

### Blocks

- **None**

## Risks & Considerations

- Proposal noise if failures are trivial
