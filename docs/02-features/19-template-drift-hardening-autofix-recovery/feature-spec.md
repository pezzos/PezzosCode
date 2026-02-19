# Feature Specification: Template drift hardening + autofix recovery

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-19`

**Owner:** Developer/PO

**Last Updated:** 2026-02-11

### Summary

Harden the workflow when template files and living files diverge.
Precommit/CI autofix should detect drift, repair only scoped paths, restage allowed files, and fail closed when deterministic repair cannot be trusted.

## User Intent

### Who is this for?

- Primary: Developer/PO maintaining repos bootstrapped from templates.

### Why do they need it?

- Drift between template sources and living project files can repeatedly break precommit/CI and consume manual time.

### User Value

- Faster recovery from drift failures.
- Predictable, scoped autofix behavior.
- Reduced accidental modifications outside intended files.

## Feature Requirements

### Functional Requirements

- [ ] Detect template/living-file drift during precommit and CI autofix stages.
- [ ] Classify drift as safe-auto-fix vs manual-review-required.
- [ ] Apply deterministic scoped repairs for safe cases only.
- [ ] Re-stage only approved/scoped files after autofix.
- [ ] Fail closed with explicit remediation for unresolved or ambiguous drift.

### User Experience Requirements

#### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI

### Non-Functional Requirements

- Drift checks must be deterministic and idempotent.
- Autofix must never silently modify out-of-scope files.
- Drift diagnostics must reference exact files and required actions.

## Acceptance Criteria

### Definition of Done

- Drift is detected before merge/commit gates.
- Safe one-sided drift repairs complete automatically with scoped restaging.
- Ambiguous/multi-sided drift fails with clear remediation steps.
- Behavior is validated in both precommit and CI paths.

### Test Scenarios

- One-sided drift auto-fixed and re-staged successfully.
- Bi-directional conflicting drift blocks with explicit diagnostics.
- Out-of-scope file modification attempt is detected and blocked.

### Success Metrics

- Reduced recurring precommit failures from template drift.
- Reduced manual intervention during drift-related CI failures.

## Scope

### In Scope

- Drift detection and classification.
- Scoped autofix + restage behavior.
- Failure diagnostics and guardrails.

### Out of Scope

- Automatic conflict resolution for semantic multi-file merge conflicts.
- Non-template content synchronization policies.

## Dependencies

### Requires

- `tools/pc-precommit`
- Unified autofix flow used by `make ci`
- Template sources under `tools/templates/`

### Blocks

- Reliable synthetic workflow smoke tests and predictable daily developer flow.

## Risks & Considerations

- Over-aggressive autofix can hide underlying design drift.
- Under-aggressive autofix can keep manual burden high.

## Open Questions

- Which drift categories should remain strictly manual even if a heuristic fix is possible?

## Related Documents

- PRD: `docs/01-product/prd.md`
- Output Offload: `docs/04-process/output-offload.md`
- Protocol: `docs/04-process/ticket-execution-protocol.md`

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase            | Blocking | Title                                                                              | Risk                                                                                                                                                                                                                                                                            | Action                                                                                                                                                                                                                                     |
| ---------- | -------- | ------- | ---------------- | -------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SEC-19-001 | High     | patcher | patch            | Yes      | Scoped autofix boundary is not explicitly hardened against path escape             | The feature requires scoped repairs and blocking out-of-scope changes, but the provided spec/tasks do not require canonical-path and symlink-boundary enforcement. Drift inputs like ../, absolute paths, or symlink escapes could modify/restage files outside intended scope. | Implement fail-closed path controls in the autofix path selection/restage flow: resolve real paths, enforce repo-root + approved-scope prefix checks, reject boundary-crossing symlinks, and emit explicit remediation.                    |
| SEC-19-002 | High     | patcher | automated-test   | Yes      | Security-negative drift tests are not explicitly required by current test contract | Acceptance includes blocking out-of-scope modification attempts, but execution evidence only names broad test targets and does not document adversarial fixtures. A scope-bypass regression could pass without proving this control.                                            | Add explicit automated tests for ../ traversal, absolute-path injection, symlink escape, and path-delimiter edge cases; assert non-zero exit, explicit diagnostics, and zero out-of-scope index/worktree changes.                          |
| SEC-19-003 | Medium   | patcher | patch            | Yes      | Fail-closed behavior lacks explicit transactional rollback semantics               | Docs require fail-closed on ambiguous/unresolved drift, but do not define rollback if partial edits/staging occurred before failure. Partial staged state can leak unintended changes into later commits.                                                                       | Make autofix transactional: classify all drift first, stage only after full validation, and rollback touched scoped files/index on any error or ambiguity before returning failure.                                                        |
| SEC-19-004 | Medium   | human   | human-validation | Yes      | Manual-only drift categories remain undefined                                      | The open question on which drift categories must stay manual leaves policy ambiguity. Without explicit categories, high-risk two-sided/semantic drift may be auto-fixed heuristically.                                                                                          | Define and approve a manual-only denylist in feature docs, then enforce it in code/tests (minimum: bi-directional conflicts, template+living concurrent edits, multi-file semantic conflicts) with hard block and human remediation steps. |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                                                    | Risk                                                                                                                                                        | Action                                                                                                                                                                                                                         |
| ----------- | -------- | ------- | ---------------- | -------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| PROD-19-001 | High     | patcher | patch            | Yes      | Scoped autofix can still violate user expectations without explicit fail-safe boundaries | If drift inputs escape approved paths or partially apply before failure, users can unknowingly commit unrelated changes and lose trust in autofix behavior. | Enforce canonical repo-root path checks and symlink boundary rejection, and make autofix transactional with rollback before any restage; on failure, explicitly confirm that no out-of-scope or partial changes remain staged. |
| PROD-19-002 | High     | patcher | automated-test   | Yes      | Current test contract does not prove guardrails against adversarial drift inputs         | Broad test-suite execution can pass without validating traversal, absolute-path, or symlink bypass attempts, allowing regressions that impact user repos.   | Add explicit negative fixtures for `../` traversal, absolute-path injection, symlink escape, and delimiter edge cases; assert non-zero exit, explicit remediation text, and zero out-of-scope index/worktree changes.          |
| PROD-19-003 | Medium   | patcher | automated-test   | Yes      | Local precommit and CI autofix parity is not explicitly acceptance-tested                | Users may pass locally but fail in CI (or vice versa) with different classifications or remediation guidance, creating workflow confusion and rework.       | Add parity tests that run identical drift fixtures through precommit and CI/autofix paths and assert identical classification, exit codes, and user-facing remediation output.                                                 |
| PROD-19-004 | Medium   | human   | human-validation | Yes      | Manual-review drift categories are not finalized for human sign-off                      | Without an approved manual-only denylist, ambiguous or two-sided drift may be auto-fixed unexpectedly, conflicting with intended UX and risk posture.       | PO/end-user must approve manual-only categories (minimum: bi-directional conflicts, concurrent template+living edits, semantic multi-file conflicts) and required remediation steps before completion.                         |
| PROD-19-005 | Medium   | patcher | patch            | Yes      | Blocked-state UX lacks a deterministic recovery guidance contract                        | Fail-closed outcomes without standardized file-level diagnostics and next commands increase repeat failure loops and reduce workflow clarity.               | Standardize blocked/recovered CLI messaging to include exact files, reason classification, safe rerun command, and stage status; lock this with automated output-contract tests.                                               |
| PROD-19-006 | Low      | human   | human-validation | No       | Post-release user value measurement is underspecified                                    | The team may ship without proving reduction in drift-related manual intervention and failed runs.                                                           | Define baseline and target thresholds for drift-related failures/manual interventions and review in human validation after initial rollout.                                                                                    |

<!-- review-findings:end -->

## Change Log

| Date       | Version | Changes      | Author |
| ---------- | ------- | ------------ | ------ |
| 2026-02-11 | 0.1     | Initial spec | Codex  |
