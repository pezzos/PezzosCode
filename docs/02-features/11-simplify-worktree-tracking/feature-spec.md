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
