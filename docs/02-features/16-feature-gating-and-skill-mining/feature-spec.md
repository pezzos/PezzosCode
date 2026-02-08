# Feature Specification: Feature gating + skill mining

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-16`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-08

### Summary

Add two lightweight governance capabilities: (1) precommit soft warnings when work bypasses earlier unfinished features, and (2) mining repeated prompt patterns into skill proposals.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** protect implementation order and reuse repeated workflow patterns
- **Current pain:** feature sequencing drift and repeated prompt writing are not surfaced early

### Why do they need it?

**As a** developer/PO

**I want to** receive actionable sequencing warnings and reusable skill proposals

**So that** backlog execution is more disciplined and repetitive work is captured once

### User Value

- **Value proposition:** safer sequencing with lower repetition cost
- **Expected impact:** fewer priority inversions and faster repeated workflows
- **Priority:** P2 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Precommit emits a non-blocking warning when changes target feature `N` while any earlier feature folder has `Status` not set to `Done` in `dev-tasks.md`.
- **Requirement 2:** Warning includes actionable context (earlier feature ids/statuses and remediation path) and allows continued commit.
- **Requirement 3:** Skill-mining scans repeated prompt/task patterns (prompts, workflow logs, offloaded outputs) and generates candidate skill proposals.
- **Requirement 4:** Candidate skills are written as human-gated proposals (not auto-installed/auto-applied).

#### Edge Cases

- **Edge Case 1:** False warnings caused by parsing malformed `dev-tasks.md` status lines.
- **Edge Case 2:** Very low-signal prompt repetition creating noisy skill suggestions.
- **Edge Case 3:** Multi-feature commits where sequencing warning should still be advisory only.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Precommit warning fires for out-of-order feature edits and remains non-blocking.
- Warning message includes earlier incomplete features and expected remediation.
- Skill-mining outputs candidate skills with rationale and evidence references.
- Candidate skills are recorded as proposals for human approval.

## Scope

### In Scope

- Precommit status parsing + warning output
- Skill-mining heuristics for repeated prompt/workflow patterns
- Proposal output format and location
- Tests for warning behavior and mining signal thresholds

### Out of Scope

- Hard-blocking commits
- Automatic skill installation
- External analytics platforms

## Dependencies

### Requires

- **Precommit tooling:** `tools/pc-precommit`
- **Feature status source:** `docs/02-features/*/dev-tasks.md`
- **Prompt/workflow signals:** `prompts/`, `logs/`, `.offload/`
- **Proposal destination:** `docs/possible-improvements.md` (or approved equivalent)

### Blocks

- **None**

## Risks & Considerations

- Warning fatigue can reduce effectiveness if messaging is noisy.
- Skill-mining heuristics need conservative thresholds to avoid low-value proposals.
