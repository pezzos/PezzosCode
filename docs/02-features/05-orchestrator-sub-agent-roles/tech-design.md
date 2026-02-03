# Technical Design: Orchestrator + sub-agent roles

> **Architecture & implementation approach**

---

## Overview

**Feature:** Orchestrator + sub-agent roles

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

- Define orchestrator, implementer, reviewer, tester roles
- Map role outputs to Plan/Patch/Test/Report gates
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

### Gates & Outputs

Gates and outputs per role: Plan gate (Orchestrator) outputs the plan summary, Patch gate (Implementer) outputs artifacts/logs, Test gate (Tester) outputs pass/fail proofs, Report gate (Reviewer) outputs recommendations.

Each gate handoff persists the required artifact to the docs/logs targets so downstream roles can verify readiness before proceeding.

### Integration Points

#### External Services

None.
