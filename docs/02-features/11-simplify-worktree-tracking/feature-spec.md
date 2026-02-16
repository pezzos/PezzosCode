# Feature Specification: Simplify worktree tracking

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-11`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-05

### Summary

Remove `feature-worktrees.json` and standardize on a single worktree per feature.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** reduce bookkeeping and confusion
- **Current pain:** extra tracking file is unnecessary for single worktree

### Why do they need it?

**As a** developer/PO

**I want to** a simpler worktree policy

**So that** cleaner workflow with fewer files

### User Value

- **Value proposition:** cleaner workflow with fewer files
- **Expected impact:** Lower token burn and fewer regressions
- **Priority:** P0 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Remove references to `feature-worktrees.json`
- **Requirement 2:** Update process docs to single worktree per feature

#### Edge Cases

- **Edge Case 1:** Multiple worktrees exist for a feature
- **Edge Case 2:** Legacy files still present

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Docs and tooling no longer require feature-worktrees.json

## Scope

### In Scope

- Docs/process updates
- Tooling cleanup

### Out of Scope

- Changing worktree naming convention

## Dependencies

### Requires

- **Docs/Process rules:** `docs/04-process/`
- **Templates/tools:** PezzosCode repo

### Blocks

- **None**

## Risks & Considerations

- Older repos relying on the file

## Automated Review Findings

<!-- review-findings:start -->

### Security Reviewer

| ID         | Severity | Risk                                                                           | Action                                                                                           |
| ---------- | -------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| SEC-11-001 | High     | Unvalidated input can trigger data corruption or unsafe behavior.              | Add explicit validation rules, error paths, and anti-bypass tests in feature-spec and dev-tasks. |
| SEC-11-004 | High     | Missing injection controls can expose command, SQL, or script injection paths. | Define escaping/parameterization requirements and add dedicated injection test scenarios.        |
| SEC-11-005 | Medium   | Unsafe defaults can bypass intended runtime protections.                       | Capture required config defaults, permission boundaries, and misconfiguration failure behavior.  |

### Product Manager

| ID          | Severity | Risk                                                                    | Action                                                                                          |
| ----------- | -------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| PROD-11-002 | Medium   | Implementation may diverge from intended user path and onboarding flow. | Add explicit user journey steps, entry points, and completion states.                           |
| PROD-11-003 | Medium   | Cross-feature workflow alignment may be inconsistent.                   | Update `docs/01-product/ux-ui.md` to include 'Simplify worktree tracking' journey and workflow. |
| PROD-11-005 | Low      | Human acceptance timing may be unclear before execution starts.         | Add a `Product Owner test checkpoint` task in dev-tasks before first make feature execution.    |

<!-- review-findings:end -->
