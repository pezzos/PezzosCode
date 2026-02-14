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

- Feature: Zero-input execution defaults
  - Owner: Developer/PO
  - Problem: Human prompts during normal runs create toil and break flow
  - Outcome: Workflow runs with no manual input unless ambiguity or HIGH risk requires explicit approval
  - Priority: P0
  - Notes: Ask only when required by policy or missing intent

- Feature: Deterministic auto-fix and auto-recovery expansion
  - Owner: Developer/PO
  - Problem: Repeated deterministic failures still require manual intervention
  - Outcome: Common failure classes self-heal (sync, formatting, staging, retry-safe reruns) with fail-closed safeguards
  - Priority: P0
  - Notes: Keep explicit error traces when auto-fix cannot safely proceed

- Feature: Token budget guardrails
  - Owner: Developer/PO
  - Problem: Token consumption drifts up across long or noisy runs
  - Outcome: Prompt/output budgets and compact summaries keep token usage predictable without reducing correctness
  - Priority: P0
  - Notes: Continue enforcing noisy output offload via `tools/offload-proxy/pp`

- Feature: Skill inventory pruning
  - Owner: Developer/PO
  - Problem: Unused or overlapping skills increase maintenance cost and confusion
  - Outcome: Regularly identify and remove/archive low-value skills while preserving required workflows
  - Priority: P1
  - Notes: Keep core skills explicit and easy to discover

- Feature: Workflow complexity reduction
  - Owner: Developer/PO
  - Problem: Redundant script paths and extra configuration increase fragility
  - Outcome: Fewer, clearer execution paths with equivalent or better reliability
  - Priority: P1
  - Notes: Prefer deleting unused branches over adding new abstraction layers

- Feature: Bootstrap/update reliability hardening
  - Owner: Developer/PO
  - Problem: Existing-repo updates can still create drift or conflicts
  - Outcome: Refresh path is predictable, idempotent, and low-friction across new and existing projects
  - Priority: P0
  - Notes: Must remain safe to re-run

- Feature: Regression-focused workflow smoke checks
  - Owner: Developer/PO
  - Problem: Workflow regressions reappear without fast end-to-end checks
  - Outcome: Lightweight recurring checks catch orchestration regressions before real ticket execution
  - Priority: P1
  - Notes: Keep checks deterministic and inexpensive
