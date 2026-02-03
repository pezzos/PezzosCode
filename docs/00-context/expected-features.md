# Expected Features

## Purpose

Capture explicit features the human expects, before PRD generation. These are
inputs to the PRD feature list and must be reflected unless explicitly rejected.

## Feature Candidates

- Feature:
  - Owner:
  - Problem:
  - Outcome:
  - Priority: P0 | P1 | P2
  - Notes:

## Current Expected Features

- Feature: Worktree policy for parallel roles
  - Owner: Developer/PO
  - Problem: Parallel roles contaminate each other's context or diffs
  - Outcome: Clean isolation for implementer/reviewer/tester
  - Priority: P1
  - Notes: Naming convention `../<repo_name>-<feature_name>-<agent_name>`

- Feature: Orchestrator + sub-agent roles
  - Owner: Developer/PO
  - Problem: Single agent context gets overloaded
  - Outcome: Clear role separation and predictable gates
  - Priority: P1
  - Notes: Orchestrator approves Plan/Patch/Test/Report

- Feature: Output offload enforcement
  - Owner: Developer/PO
  - Problem: Large outputs waste tokens and derail context
  - Outcome: Noisy outputs stored in `.offload/` and referenced by id
  - Priority: P0
  - Notes: Use `tools/offload-proxy/pp`

- Feature: Resume in-progress tickets
  - Owner: Developer/PO
  - Problem: Interrupted ticket runs should be resumable without restarting from scratch
  - Outcome: Automatic resume when worklog exists; completed steps are skipped; tests/CI re-run
  - Priority: P0
  - Notes: Skip commit if already recorded in the worklog

- Feature: Commit gated by completed ticket docs
  - Owner: Developer/PO
  - Problem: Commits should only happen when ticket documentation is complete and DoD is satisfied
  - Outcome: Auto-fill Tests Run/Report and check DoD before commit
  - Priority: P0
  - Notes: Commit step enforces ticket doc completion

- Feature: Anti-cheat testing strategy
  - Owner: Developer/PO
  - Problem: Hardcoded implementations pass shallow tests
  - Outcome: Tests validate behavior through fixtures/invariants/contracts
  - Priority: P1
  - Notes: Seeded randomness and multiple fixtures
