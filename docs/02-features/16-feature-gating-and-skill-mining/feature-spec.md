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

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                                      | Risk                                                                                                                                                                                                                                                | Action                                                                                                                                                                                                                                         |
| ---------- | -------- | ------- | -------------- | -------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-16-001 | High     | patcher | patch          | Yes      | Sensitive data can be copied into skill proposals                          | The feature explicitly mines `prompts/`, `logs/`, and `.offload/` and writes evidence references, but no redaction rule is defined; secrets/tokens in those sources can be committed to `docs/possible-improvements.md` and leaked via git history. | Implement fail-closed secret handling in miner output: detect credentials (token/key/password patterns + high-entropy strings), redact values, and store only minimal references (path + line/offset/hash) instead of raw secret-bearing text. |
| SEC-16-002 | High     | patcher | patch          | Yes      | Repository-boundary enforcement is missing for mined inputs                | Input sources are defined as directories, but no canonical path/symlink policy is specified; a symlink or traversal path could cause reading files outside the repo (for example local SSH/config secrets) and include them in proposals.           | Constrain mining to an allowlisted repo-relative set after `realpath` validation, reject paths outside repo root, do not follow symlinks, skip binary files, and cap file size/line length before parsing.                                     |
| SEC-16-003 | Medium   | patcher | automated-test | Yes      | Soft-warning implementation could accidentally bypass hard commit controls | This feature adds non-blocking precommit behavior; without explicit regression tests, exit-code changes can unintentionally weaken existing fail-closed commit checks in the workflow.                                                              | Add regression tests proving existing hard-fail gates still return non-zero while sequencing warnings remain advisory-only; enforce additive warning behavior only.                                                                            |
| SEC-16-004 | Medium   | patcher | automated-test | Yes      | Malformed status parsing can silently suppress governance signal           | Edge cases mention malformed `dev-tasks.md`, but no required fail-closed warning contract is defined; crafted/invalid status lines could evade out-of-order warnings.                                                                               | On parse ambiguity or missing status, emit deterministic `unknown status` warnings with affected feature IDs and remediation text; add tests for malformed, duplicate, and missing status fields.                                              |
| SEC-16-005 | Low      | patcher | patch          | No       | Control-character and markdown injection in mined evidence                 | Logs and offloaded outputs may contain ANSI/control sequences or malicious markdown that can spoof terminal/docs rendering and mislead reviewers.                                                                                                   | Normalize mined text before proposal generation: strip control characters, escape markdown where needed, and render evidence as plain text snippets.                                                                                           |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                           | Risk                                                                                                                                                          | Action                                                                                                                                                                                           |
| ----------- | -------- | ------- | ---------------- | -------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| PROD-16-001 | High     | patcher | patch            | Yes      | Sequencing warning lacks deterministic recovery contract        | If warning copy is inconsistent or incomplete, users cannot recover quickly and may continue out-of-order execution, reducing trust in the governance signal. | Implement a fixed warning template that always includes earlier incomplete feature IDs/statuses, remediation path, and next eligible feature/action; add deterministic output tests.             |
| PROD-16-002 | High     | patcher | patch            | Yes      | Skill-mining quality thresholds are under-specified             | Without explicit repeat/signal thresholds and deduping, low-value proposals will create review fatigue and hide genuinely useful skills.                      | Define bounded mining thresholds (minimum repeats, source diversity, dedupe/cooldown) and enforce them with tests for noisy vs high-signal datasets.                                             |
| PROD-16-003 | Medium   | patcher | automated-test   | Yes      | Soft-warning change may weaken perceived commit protection      | Users may assume hard commit protections still apply even if exit-code behavior regresses, causing unsafe commits.                                            | Add regression coverage proving existing hard-fail gates remain non-zero while sequencing warnings stay advisory-only (aligned with SEC-16-003).                                                 |
| PROD-16-004 | Medium   | human   | human-validation | Yes      | Human approval gate for mined proposals is not operationalized  | If approval criteria are implicit, proposal acceptance will be inconsistent and end-user value will drift.                                                    | Require PO/end-user validation for first proposal batch using a checklist (usefulness, duplication, maintenance cost, security/redaction evidence) with explicit approve/reject outcomes logged. |
| PROD-16-005 | Low      | human   | human-validation | No       | Warning usability is not yet validated in real commit scenarios | Technically correct warnings may still be hard to act on under time pressure, reducing adherence.                                                             | Run human spot checks on warning clarity for single-feature and multi-feature commits and record comprehension feedback.                                                                         |

<!-- review-findings:end -->
