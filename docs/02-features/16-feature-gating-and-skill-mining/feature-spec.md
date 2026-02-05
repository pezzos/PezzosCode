# Feature Specification: Feature gating + skill mining

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-16`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-05

### Summary

Add soft feature gating in precommit and mine repeated prompts to propose reusable skills.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** reduce regressions and repetitive work
- **Current pain:** later features advance while earlier ones are incomplete; prompt patterns repeat

### Why do they need it?

**As a** developer/PO

**I want to** soft gating and skill proposals

**So that** better sequencing and reusable workflows

### User Value

- **Value proposition:** better sequencing and reusable workflows
- **Expected impact:** Lower token burn and fewer regressions
- **Priority:** P2 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Soft warning when modifying a feature while earlier features are not Done
- **Requirement 2:** Detect recurring prompt patterns and propose new skills (e.g., `fix-issue.md`)

#### Edge Cases

- **Edge Case 1:** False positive warnings
- **Edge Case 2:** Low-signal prompt patterns

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Warnings are informative and non-blocking

## Scope

### In Scope

- Precommit checks
- Prompt analysis

### Out of Scope

- Hard blocking precommit

## Dependencies

### Requires

- **Docs/Process rules:** `docs/04-process/`
- **Templates/tools:** PezzosCode repo

### Blocks

- **None**

## Risks & Considerations

- Developer fatigue from warnings
