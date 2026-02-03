# Technical Design: Output offload enforcement

> **Architecture & implementation approach**

---

## Overview

**Feature:** Output offload enforcement

**Status:** Draft

**Last Updated:** 2026-02-02

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

- Wrap noisy commands with tools/offload-proxy/pp
- Store outputs in .offload/ with pointer id
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

### Workflow Gate

The workflow gate protects the noisy command handling sequence by describing when and how commands enter the offload path, and by declaring the artifacts, approvals, and checks required before steps can proceed.

### Noisy Command Handling Gate

This noisy command handling gate captures the point where high-volume CLI outputs must be redirected into `.offload/`. It logs the gate output artifacts, enforces the approval gate, and ensures downstream docs/logs know which offload id artifacts to expect.

### Gate Output Artifacts

Gate output artifacts are the offload id artifacts, log references, and summary metadata that downstream steps consume. Every walk-through of the workflow gate must list these artifacts so the next team member knows how to fetch the noisy output from storage.

### Integration Points

#### External Services

None.
