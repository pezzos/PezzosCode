# Feature Specification: Role prompts + Plan Reviewer

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-13`

**Status:** Completed

**Owner:** Developer/PO

**Last Updated:** 2026-02-09

### Summary

Rebaseline the feature to the current prompt architecture. The repository already contains role prompts and a Plan Reviewer gate; this feature now focuses on keeping prompt contracts accurate, preventing prompt drift, and validating gate behavior against the current execution protocol.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** consistent role behavior and reliable plan gating
- **Current pain:** feature wording still reflects “initial prompt creation” while the repository now has an expanded prompt set and stricter gate rules

### Why do they need it?

**As a** developer/PO

**I want to** keep role prompts and the Plan Reviewer gate aligned with the live workflow

**So that** work item execution remains predictable and low-rework

### User Value

- **Value proposition:** predictable Planner/Reviewer/Patcher/Tester/Reporter handoffs
- **Expected impact:** lower replan loops and fewer workflow regressions
- **Priority:** P1 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Maintain a canonical prompt inventory in `prompts/` for planner, plan-reviewer, patcher, tester, reporter, and commit-message flows (including task-specific variants used by `tools/pc-feature`).
- **Requirement 2:** Ensure `tools/pc-feature` loads prompts via `load_prompt_template()`/task fallback instead of hardcoded role prompt bodies.
- **Requirement 3:** Keep `tools/templates/prompts/` synchronized with live prompt files so bootstrap/template sync does not reintroduce drift.
- **Requirement 4:** Keep process references consistent in `docs/04-process/ticket-execution-protocol.md`, `docs/04-process/human-orchestration-workflow.md`, and `docs/04-process/dev-workflow.md` for Plan Reviewer and Allowed Tests behavior.

#### Edge Cases

- **Edge Case 1:** Missing task-specific prompt file should fail with explicit remediation guidance.
- **Edge Case 2:** Plan Reviewer guidance conflicts with risk policy state (for example, resumed HIGH-risk work items).
- **Edge Case 3:** Template prompt files diverge from root prompt files after updates.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Prompt files in `prompts/` and `tools/templates/prompts/` cover the required role/task prompt set used by `tools/pc-feature`.
- `tools/pc-feature` contains prompt-loading references and no embedded long-form role prompt bodies.
- Plan Reviewer gate behavior is covered by tests for approve/block/conflict paths.
- Process docs reference role prompts and Plan Reviewer gate semantics consistently.

## Scope

### In Scope

- Prompt contracts and prompt-file parity
- Plan Reviewer gate wording/guardrails
- Process-doc alignment for role prompts
- Tests covering prompt loading and gate flow

### Out of Scope

- Reordering workflow gates
- New agent roles beyond current Planner/Plan Reviewer/Patcher/Tester/Reporter model
- UI or API surfaces

## Dependencies

### Requires

- **Docs/Process rules:** `docs/04-process/ticket-execution-protocol.md`
- **Workflow docs:** `docs/04-process/dev-workflow.md`, `docs/04-process/human-orchestration-workflow.md`
- **Prompt artifacts:** `prompts/`, `tools/templates/prompts/`

### Blocks

- **None**

## Risks & Considerations

- Prompt drift can silently reintroduce inconsistent role behavior.
- Overly strict reviewer wording can deadlock runs unless conflict handling remains explicit.
