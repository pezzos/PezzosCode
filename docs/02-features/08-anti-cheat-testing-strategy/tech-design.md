# Technical Design: Anti-cheat testing strategy

> **Architecture & implementation approach**

---

## Overview

**Feature:** Anti-cheat testing strategy

**Status:** Complete

**Last Updated:** 2026-02-05

### Summary

Implement CLI-level workflow changes and documentation updates to enforce the behavior.
No new services or external dependencies required.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Technical Requirements

### From Feature Spec

- Multiple fixtures per critical path
- Seeded randomness and invariants
- Performance: reasonable local execution time
- Security: local-only operations

### Technical Constraints

- **Platform:** macOS, local CLI only
- **Browser support:** N/A
- **API limits:** N/A
- **Data constraints:** Local repo files only
- **Performance budget:** Human-paced CLI execution

## Architecture

### System Context

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   User/PO   │────────▶│  CLI Tools  │────────▶│  Repo Docs  │
│             │         │  + Scripts  │         │  + Logs     │
└─────────────┘         └─────────────┘         └─────────────┘
```

### Component Design

#### CLI Commands

- **Command:** `tools/*` or `make` targets
  - **Inputs:** flags/args as defined in docs
  - **Outputs:** stdout/stderr with offload ids if noisy
  - **Exit codes:** `0` success, `1` failure

### Data Model

#### New Data Structures

None. Changes are document- and script-based.

#### Data Flow

1. **Input:** CLI command
2. **Processing:** Validate/gate/execute
3. **Storage:** Docs/logs and optional `.offload/`
4. **Output:** Summary + pointers

### Integration Points

#### External Services

None.
