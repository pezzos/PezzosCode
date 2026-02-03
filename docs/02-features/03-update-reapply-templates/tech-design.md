# Technical Design: Update/reapply templates

> **Architecture & implementation approach**

---

## Overview

**Feature:** Update/reapply templates

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

- Detect existing files and avoid destructive overwrites
- Provide overwrite/merge/skip options
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

#### CLI workflow gates and outputs

The CLI workflow gates and outputs describe the checks, confirmations, and summary artifacts (cli preflight validation gate, cli diff review gate, and cli conflict summary output) emitted during each template reapply run, so failures surface actionable next steps.

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
