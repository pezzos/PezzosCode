---
name: refactor-safely
description: Refactor code without changing behavior by preserving invariants, making small reversible steps, and validating with tests. Use when a user requests a safe refactor or asks to improve structure without behavior changes.
---

# Refactor Safely

## Overview
Improve code structure while keeping behavior identical to before.

## Inputs
- Target files or modules.
- Rationale for refactor (readability, maintainability, performance).

## Steps
1) Read current behavior and tests to establish invariants.
2) Identify refactor boundaries that avoid behavior changes.
3) Make small, reversible changes with clear checkpoints.
4) Run tests after each checkpoint.
5) Summarize improvements and any remaining risks.

## Commands
- `rg -n "<symbol-or-file>"`
- Test command (ask if not documented).

## Output
- Cleaner code with identical behavior.

## DoD
- All existing tests pass.
- No observable behavior change.
