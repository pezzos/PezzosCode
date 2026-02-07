# Feature Specification: Unified autofix for CI + precommit

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-10`

**Status:** Done

**Owner:** Developer/PO

**Last Updated:** 2026-02-07

### Summary

Use a single autofix script for CI and precommit, re-stage fixes, and run Codex in vanilla config for staged-only fixes.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** consistent autofix behavior across CI and hooks
- **Current pain:** autofix logic diverges and staged fixes are not re-applied

### Why do they need it?

**As a** developer/PO

**I want to** one script used by both CI and precommit

**So that** fewer regressions and predictable fixes

### User Value

- **Value proposition:** fewer regressions and predictable fixes
- **Expected impact:** Lower token burn and fewer regressions
- **Priority:** P0 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Create a unified autofix script used by `make ci` and precommit
- **Requirement 2:** Run `git add -u` after autofix and print modified files
- **Requirement 3:** Ensure precommit uses vanilla Codex config (no Serena MCP)

#### Edge Cases

- **Edge Case 1:** No staged files to fix
- **Edge Case 2:** Autofix fails and must surface clear error

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- CI and precommit both invoke the same script
- Modified files are re-staged and listed

## Scope

### In Scope

- Autofix script
- Precommit behavior
- Docs/process updates

### Out of Scope

- Changing lint/format rules

## Dependencies

### Requires

- **Docs/Process rules:** `docs/04-process/`
- **Templates/tools:** PezzosCode repo

### Blocks

- **None**

## Risks & Considerations

- Unexpected staging of unrelated files
