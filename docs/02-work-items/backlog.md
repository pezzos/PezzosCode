# Orchestrator Working Memory

This file is not formal ticketing.
It is a practical memory for orchestration queue, state, and arbitration.

## Rules

- Orchestrator owns updates.
- Coder agents may read but should not edit directly.
- Keep entries concise and execution-oriented.

## Job states

- queued
- ready
- dispatched
- running
- revise
- review-ready
- accepted
- done
- blocked

## Entry template

- Task ID:
- Objective:
- Priority: P0 | P1 | P2
- Session ID:
- Scope hint:
- Proposed files:
- Validation commands:
- Dependencies:
- Current state:
- Latest orchestrator decision:
- Next handoff note:

## Arbitration notes

- Task ID:
  - Keep:
  - Rework:
  - Drop:
  - Rationale:
