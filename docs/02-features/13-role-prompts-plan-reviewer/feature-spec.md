# Feature Specification: Role prompts + Plan Reviewer

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-13`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-05

### Summary

Create role-specific prompts and add a Plan Reviewer gate to validate plans before patching.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** consistent role behavior and higher plan quality
- **Current pain:** role boundaries are inconsistent and plans skip validation

### Why do they need it?

**As a** developer/PO

**I want to** clear prompts for each role

**So that** fewer rework loops

### User Value

- **Value proposition:** fewer rework loops
- **Expected impact:** Lower token burn and fewer regressions
- **Priority:** P1 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Add prompts for planner/plan-reviewer/patcher/tester/reporter
- **Requirement 2:** Plan Reviewer approves plan before patching

#### Edge Cases

- **Edge Case 1:** Plan Reviewer unavailable

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Prompts exist and are referenced in process docs

## Scope

### In Scope

- Prompts
- Process docs

### Out of Scope

- New tooling beyond docs

## Dependencies

### Requires

- **Docs/Process rules:** `docs/04-process/`
- **Templates/tools:** PezzosCode repo

### Blocks

- **None**

## Risks & Considerations

- Prompts go stale without updates
