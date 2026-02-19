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

- Generated at: 2026-02-19T15:40:57Z
- Decision: NOT_READY
- Summary: Release is not ready from a PM perspective: core P0 value paths (bootstrap/reapply, deterministic ticket execution, mandatory offload enforcement completion, and fail-closed commit/drift controls) are still incomplete, with several required features not started.
- Actionable follow-up features: 5

- Feature: Release readiness RR-001 - Complete deterministic ticket execution with authority and risk gates
  - Owner: Product Manager
  - Problem: Primary execution journey is incomplete: execute-ticket workflow is not started and role orchestration remains partial.
  - Outcome: Preflight -> Risk gate -> Plan -> Plan review -> Patch -> Test -> Report runs predictably, with HIGH-risk halting at 'Awaiting PO Approval' until explicit approval.
  - Priority: P0
  - Notes: Must demonstrate protected-command authority behavior for human PO/user.
  - Source: release-readiness (RR-001)
  - Existing Feature Refs: 02-execute-ticket-workflow, 05-orchestrator-sub-agent-roles, 13-role-prompts-plan-reviewer

- Feature: Release readiness RR-002 - Enforce single-worktree orchestration policy for release reliability
  - Owner: Product Manager
  - Problem: Worktree policy/simplification items are not started, leaving orchestration reliability expectations unproven.
  - Outcome: Single-worktree behavior is consistently enforced and role collaboration does not depend on deprecated tracking patterns.
  - Priority: P0
  - Notes: Resolve overlap between policy and simplification tracks into one canonical release behavior.
  - Source: release-readiness (RR-002)
  - Existing Feature Refs: 06-worktree-policy-naming-convention, 11-simplify-worktree-tracking

- Feature: Release readiness RR-003 - Finish mandatory noisy-output offload enforcement
  - Owner: Product Manager
  - Problem: Offload enforcement is still in progress, so token-efficiency and traceability commitments are not yet reliable end-to-end.
  - Outcome: All noisy workflow steps consistently produce `pp` pointer ids and corresponding structured logs.
  - Priority: P0
  - Notes: Runner/log foundation exists; this task closes enforcement coverage gaps.
  - Source: release-readiness (RR-003)
  - Existing Feature Refs: 04-output-offload-enforcement, 09-runner-structured-logs, 15-offload-audit-and-log-compaction

- Feature: Release readiness RR-004 - Implement fail-closed commit gate and scoped drift/autofix recovery
  - Owner: Product Manager
  - Problem: Release integrity is not protected: commit gate and drift-hardening features are not started.
  - Outcome: Commit is blocked until required planner/tester/reporter evidence is complete; unresolved drift/autofix failures fail closed with clear remediation.
  - Priority: P0
  - Notes: Validate behavior on interrupted reruns and dirty active worktree states.
  - Source: release-readiness (RR-004)
  - Existing Feature Refs: 18-commit-gated-by-completed-ticket-docs, 19-template-drift-hardening-autofix-recovery, 17-resume-in-progress-tickets, 10-unified-autofix-precommit

- Feature: Release readiness RR-005 - Ship bootstrap and safe template reapply for new/existing repos
  - Owner: Product Manager
  - Problem: Core onboarding value is missing: bootstrap and reapply capabilities are both not started, so Journey 1 is not deliverable.
  - Outcome: One-command bootstrap plus idempotent overwrite/merge/skip reapply works on clean and existing repos without destructive regressions.
  - Priority: P0
  - Notes: Acceptance should include conflict-path validation and rerun safety proof.
  - Source: release-readiness (RR-005)
  - Existing Feature Refs: 01-bootstrap-templates-into-a-repo, 03-update-reapply-templates

<!-- release-readiness:end -->
