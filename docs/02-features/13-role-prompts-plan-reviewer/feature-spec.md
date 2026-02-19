# Feature Specification: Role prompts + Plan Reviewer

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-13`

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

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                                              | Risk                                                                                                                                                                                                                                                                 | Action                                                                                                                                                                                                                  |
| ---------- | -------- | ------- | -------------- | -------- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-13-001 | High     | patcher | patch          | Yes      | Prompt loader path confinement is not explicitly enforced                          | Feature requirements require file-based prompt loading with task fallback, but the provided spec/tasks do not require a strict allowlist + path confinement check. Without this, a crafted role/task key could resolve outside `prompts/` and load unintended files. | In `tools/pc-feature`, map role/task identifiers to a fixed allowlist of filenames, canonicalize resolved paths, enforce they stay under the prompt root, and fail closed on unknown identifiers with remediation text. |
| SEC-13-002 | High     | patcher | patch          | Yes      | Plan Reviewer conflict handling is not guaranteed to fail-closed                   | Edge Case 2 calls out reviewer guidance vs HIGH-risk policy conflicts, but acceptance criteria do not explicitly require a hard halt state. A non-fail-closed conflict path can allow work to continue without required PO approval.                                 | Implement explicit conflict behavior that sets `Awaiting PO Approval` and blocks downstream patch/test stages until a recorded human approval is present.                                                               |
| SEC-13-003 | Medium   | patcher | automated-test | Yes      | Prompt/template drift control is not enforced by a mandatory automated parity test | Requirement 3 and Edge Case 3 require template sync, but provided materials do not show a mandatory fail-closed test gate for prompt parity. Drift can reintroduce weaker or outdated prompts during bootstrap/template sync.                                        | Add automated tests that enforce one-to-one inventory and content parity between `prompts/` and `tools/templates/prompts/`; fail test on any mismatch.                                                                  |
| SEC-13-004 | High     | patcher | automated-test | Yes      | Security-critical gate tests are not evidenced as completed                        | Dev tasks and execution log show pending test sections (`Test Results: (pending)`, `Final Report: No runs yet`). Missing evidence means approve/block/conflict and missing-prompt fail-fast controls are unverified.                                                 | Run and record the gate-focused tests for approve, block/retry, policy conflict, and missing prompt handling before feature completion; update validation logs with concrete pass/fail evidence.                        |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                               | Risk                                                                                                                                                                          | Action                                                                                                                                                                           |
| ----------- | -------- | ------- | ---------------- | -------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-13-001 | High     | patcher | patch            | Yes      | Prompt loader can select unintended files                           | If role/task identifiers are not strictly allowlisted and path-confined, users can get inconsistent role behavior and non-deterministic runs, breaking trust in the workflow. | Implement fixed role/task filename allowlists, canonicalize resolved paths, enforce prompt-root confinement, and fail closed on unknown identifiers with clear remediation text. |
| PROD-13-002 | High     | patcher | patch            | Yes      | HIGH-risk conflict path is not proven fail-closed                   | If conflict handling does not hard-stop at approval gates, patch/test can continue without PO authorization, violating user expectations for safety and control.              | Enforce explicit `Awaiting PO Approval` state and block all downstream stages until recorded human approval is present.                                                          |
| PROD-13-003 | Medium   | patcher | automated-test   | Yes      | Prompt/template drift is not gated by mandatory parity tests        | Template reapply can silently reintroduce stale prompt wording, causing role handoff regressions and avoidable replan loops for end users.                                    | Add automated one-to-one inventory and content parity tests between `prompts/` and `tools/templates/prompts/`, failing on any mismatch.                                          |
| PROD-13-004 | High     | patcher | automated-test   | Yes      | Acceptance-critical gate behavior lacks test evidence               | Approve/block/retry/conflict/missing-prompt behavior is not evidenced as executed, so completion quality and user-facing reliability remain unverified.                       | Run and record the gate-focused tests for all required paths and update validation logs with concrete pass/fail evidence.                                                        |
| PROD-13-005 | Medium   | human   | human-validation | Yes      | User-facing gate and remediation wording lacks explicit PO sign-off | Without human validation of blocked/conflict/error messaging, users may not know next actions, increasing failed reruns and workflow friction.                                | Route to PO human-validation with a scripted walkthrough of approve, block/retry, conflict, and missing-prompt scenarios; require explicit sign-off or requested copy fixes.     |

<!-- review-findings:end -->
