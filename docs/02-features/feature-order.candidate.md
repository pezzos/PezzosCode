# Feature Order Plan

> Machine-managed by `tools/pc-prepare-features`.

**Generated At (UTC):** 2026-02-19T10:50:43Z

## Ordered features

| #   | Priority | Slug                                                         | Title                                                           | Dependencies                                                                                                                                                |
| --- | -------- | ------------------------------------------------------------ | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 01  | P0       | bootstrap-safe-template-reapply                              | Bootstrap + safe template reapply                               | (none)                                                                                                                                                      |
| 02  | P0       | output-offload-structured-logs-shared-runner                 | Output offload + structured logs + shared runner                | bootstrap-safe-template-reapply                                                                                                                             |
| 03  | P0       | deterministic-work-item-execution-with-explicit-gates        | Deterministic work-item execution with explicit gates           | bootstrap-safe-template-reapply, output-offload-structured-logs-shared-runner                                                                               |
| 04  | P0       | single-worktree-orchestration-template-drift-hardening       | Single-worktree orchestration + template-drift hardening        | bootstrap-safe-template-reapply, output-offload-structured-logs-shared-runner, deterministic-work-item-execution-with-explicit-gates                        |
| 05  | P0       | resume-safety-fail-closed-commit-gate-scoped-autofix         | Resume safety + fail-closed commit gate + scoped autofix        | output-offload-structured-logs-shared-runner, deterministic-work-item-execution-with-explicit-gates, single-worktree-orchestration-template-drift-hardening |
| 06  | P1       | orchestrator-roles-plan-reviewer-gate-role-specific-prompts  | Orchestrator roles + Plan Reviewer gate + role-specific prompts | deterministic-work-item-execution-with-explicit-gates                                                                                                       |
| 07  | P1       | anti-hardcode-test-policy-synthetic-end-to-end-smoke-feature | Anti-hardcode test policy + synthetic end-to-end smoke feature  | deterministic-work-item-execution-with-explicit-gates, orchestrator-roles-plan-reviewer-gate-role-specific-prompts                                          |
| 08  | P1       | incremental-prd-to-features-post-run-learning-loop           | Incremental PRD-to-features + post-run learning loop            | bootstrap-safe-template-reapply, single-worktree-orchestration-template-drift-hardening, resume-safety-fail-closed-commit-gate-scoped-autofix               |

## Decisions

- `bootstrap-safe-template-reapply`: depends_on=(none); rationale: Establishes the idempotent bootstrap/template baseline and remains the only root prerequisite.
- `output-offload-structured-logs-shared-runner`: depends_on=bootstrap-safe-template-reapply; rationale: Adds shared runner metadata, offload pointers, and structured logs immediately after bootstrap so downstream gates inherit observability.
- `deterministic-work-item-execution-with-explicit-gates`: depends_on=bootstrap-safe-template-reapply, output-offload-structured-logs-shared-runner; rationale: Builds deterministic Plan->Patch->Test->Report and authority/risk gates on top of baseline templates and telemetry infra.
- `single-worktree-orchestration-template-drift-hardening`: depends_on=bootstrap-safe-template-reapply, output-offload-structured-logs-shared-runner, deterministic-work-item-execution-with-explicit-gates; rationale: Applies single-worktree and drift hardening only after bootstrap, telemetry, and orchestration semantics are in place.
- `resume-safety-fail-closed-commit-gate-scoped-autofix`: depends_on=output-offload-structured-logs-shared-runner, deterministic-work-item-execution-with-explicit-gates, single-worktree-orchestration-template-drift-hardening; rationale: Resume checkpoints, scoped autofix, and fail-closed commit gate depend on stable orchestration plus drift-safe recovery and evidence logs.
- `orchestrator-roles-plan-reviewer-gate-role-specific-prompts`: depends_on=deterministic-work-item-execution-with-explicit-gates; rationale: Role separation and mandatory Plan Reviewer gate layer on deterministic execution core; no extra prerequisite is required by the alignment contract.
- `anti-hardcode-test-policy-synthetic-end-to-end-smoke-feature`: depends_on=deterministic-work-item-execution-with-explicit-gates, orchestrator-roles-plan-reviewer-gate-role-specific-prompts; rationale: Anti-hardcode policy and synthetic smoke validation run after deterministic orchestration and role-gated execution are established.
- `incremental-prd-to-features-post-run-learning-loop`: depends_on=bootstrap-safe-template-reapply, single-worktree-orchestration-template-drift-hardening, resume-safety-fail-closed-commit-gate-scoped-autofix; rationale: Incremental PRD reconciliation and learning-loop proposals are sequenced last, after bootstrap baseline plus drift-hardened resume/commit reliability.
