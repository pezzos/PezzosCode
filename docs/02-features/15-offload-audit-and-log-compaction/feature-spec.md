# Feature Specification: Offload audit + log compaction

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-15`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-05

### Summary

Audit offload behavior and add log-compaction skills for decision/implementation logs.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** keep offload reliable and logs manageable
- **Current pain:** offload retention and log size are untracked

### Why do they need it?

**As a** developer/PO

**I want to** audit + compaction tools

**So that** lower token usage and easier review

### User Value

- **Value proposition:** lower token usage and easier review
- **Expected impact:** Lower token burn and fewer regressions
- **Priority:** P2 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Add offload index with id/cmd/wi/agent/timestamp/size
- **Requirement 2:** Add list/get/purge commands with retention policy
- **Requirement 3:** Add skills to compact decision and implementation logs

#### Edge Cases

- **Edge Case 1:** Missing offload entries
- **Edge Case 2:** Compaction loses critical context

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Audit index exists and skills produce compact versions

## Scope

### In Scope

- Offload tooling
- Skills

### Out of Scope

- External storage

## Dependencies

### Requires

- **Docs/Process rules:** `docs/04-process/`
- **Templates/tools:** PezzosCode repo

### Blocks

- **None**

## Risks & Considerations

- Retention policy misconfigured
