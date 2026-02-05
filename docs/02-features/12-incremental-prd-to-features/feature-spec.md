# Feature Specification: Incremental prd-to-features

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-12`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-05

### Summary

Ensure prd-to-features only adds missing features, never deletes existing ones, and skips Done items.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** prevent regressions and duplication
- **Current pain:** regeneration can delete or re-add completed features

### Why do they need it?

**As a** developer/PO

**I want to** incremental feature creation

**So that** stable backlog and fewer surprises

### User Value

- **Value proposition:** stable backlog and fewer surprises
- **Expected impact:** Lower token burn and fewer regressions
- **Priority:** P1 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Add missing features only
- **Requirement 2:** Never delete existing feature folders
- **Requirement 3:** Skip features with `Status: Done` in `dev-tasks.md`

#### Edge Cases

- **Edge Case 1:** Missing or malformed dev-tasks status
- **Edge Case 2:** Feature folder exists without dev-tasks

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Existing feature folders remain untouched

## Scope

### In Scope

- prd-to-features skill behavior
- Docs updates

### Out of Scope

- Changing PRD structure

## Dependencies

### Requires

- **Docs/Process rules:** `docs/04-process/`
- **Templates/tools:** PezzosCode repo

### Blocks

- **None**

## Risks & Considerations

- False negatives if status parsing fails
