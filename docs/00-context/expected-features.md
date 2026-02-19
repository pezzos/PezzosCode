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

## Release Readiness Follow-up Features (Auto-managed)

<!-- release-readiness:start -->

- Generated at: 2026-02-19T19:17:24Z
- Decision: NOT_READY
- Summary: Release is not ready: key P0 release outcomes in the current PRD baseline remain Not Started (features 22, 23, 25, 26, 27), so the core user promise of deterministic, gated, token-efficient, fail-closed execution is not yet fully releasable.
- Actionable follow-up features: 5

- Feature: Release readiness RR-005 - Ship consolidated P0 bootstrap + safe reapply baseline
  - Owner: Product Manager
  - Problem: Current release baseline marks the consolidated bootstrap/reapply feature as Not Started, leaving ambiguity on whether release evidence aligns to the latest scope.
  - Outcome: Feature 22 is implemented and validated with idempotent reruns, conflict handling (overwrite/merge/skip), and explicit release evidence tied to current PRD scope.
  - Priority: P0
  - Notes: Treat this as scope-alignment closure, not net-new surface area.
  - Source: release-readiness (RR-005)
  - Existing Feature Refs: 22-bootstrap-safe-template-reapply, 01-bootstrap-templates-into-a-repo, 03-update-reapply-templates

- Feature: Release readiness RR-002 - Complete deterministic gated execution with zero-input defaults
  - Owner: Product Manager
  - Problem: The core execution journey is not complete in the consolidated baseline, risking gate bypasses or prompt-heavy behavior versus PM expectations.
  - Outcome: Feature 25 enforces Preflight -> Risk gate -> Plan -> Plan review -> Patch -> Test -> Report with HIGH-risk approval stop state and zero-input defaults outside required gates.
  - Priority: P0
  - Notes: Must include authority control behavior for protected commands.
  - Source: release-readiness (RR-002)
  - Existing Feature Refs: 25-deterministic-work-item-execution-with-explicit-gates-zero-input-defaults, 02-execute-ticket-workflow, 13-role-prompts-plan-reviewer

- Feature: Release readiness RR-001 - Close token guardrail + offload + observability integration
  - Owner: Product Manager
  - Problem: Consolidated guardrail/offload/logging runner feature is Not Started, so token-efficiency and traceability commitments are not yet release-safe as one integrated capability.
  - Outcome: Feature 23 is implemented with enforced offload for noisy output, per-step budget behavior, pointer-based retrieval, and structured logs across role steps.
  - Priority: P0
  - Notes: Require end-to-end evidence from real workflow runs, not isolated script checks.
  - Source: release-readiness (RR-001)
  - Existing Feature Refs: 23-output-offload-token-budget-guardrails-structured-logs-shared-runner, 04-output-offload-enforcement, 09-runner-structured-logs, 15-offload-audit-and-log-compaction

- Feature: Release readiness RR-004 - Finalize single-worktree orchestration + drift-hardening in consolidated scope
  - Owner: Product Manager
  - Problem: Single-worktree reliability and drift-hardening are not complete in the current release baseline, which can undermine predictable orchestration under reruns.
  - Outcome: Feature 26 is implemented with canonical single-worktree behavior, scoped drift repair, and explicit fail-closed remediation paths.
  - Priority: P0
  - Notes: Must align with role-boundary ownership and no tracking-file drift.
  - Source: release-readiness (RR-004)
  - Existing Feature Refs: 26-single-worktree-orchestration-template-drift-hardening, 06-worktree-policy-naming-convention, 11-simplify-worktree-tracking, 19-template-drift-hardening-autofix-recovery

- Feature: Release readiness RR-003 - Deliver fail-closed recovery and commit integrity bundle
  - Owner: Product Manager
  - Problem: Resume safety, deterministic auto-recovery, and commit fail-closed behavior are not complete in the consolidated baseline, creating release integrity risk.
  - Outcome: Feature 27 is implemented with deterministic resume, scoped recovery, required evidence checks, and commit blocking when planner/tester/reporter artifacts are incomplete.
  - Priority: P0
  - Notes: Validate interrupted run and dirty-worktree scenarios.
  - Source: release-readiness (RR-003)
  - Existing Feature Refs: 27-resume-safety-deterministic-auto-recovery-fail-closed-commit-gate, 17-resume-in-progress-tickets, 18-commit-gated-by-completed-ticket-docs, 19-template-drift-hardening-autofix-recovery, 10-unified-autofix-precommit

<!-- release-readiness:end -->
