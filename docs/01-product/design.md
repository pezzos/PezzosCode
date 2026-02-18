# PezzosCode Design

PezzosCode is a local macOS-first CLI architecture for one developer/PO. The design favors deterministic `Plan -> Patch -> Test -> Report` execution, idempotent reruns, explicit authority gates, and low-token observability.

## System architecture

1. Bootstrap plane (`bootstrap-safe-template-reapply`)

- Applies templates/tools/docs into new or existing repos.
- Conflict policy is explicit: `overwrite`, `merge`, `skip`.
- Outcome: execution-ready repos with stable reruns.

2. Evidence plane (`output-offload-structured-logs-shared-runner`)

- Shared runner attaches `work_item_id`, `agent_name`, `run_id`.
- Noisy output is mandatory through `tools/offload-proxy/pp` to `.offload/<id>.txt`.
- Step logs are mandatory at `logs/<WI>/<step>.log` with `[WI-...][agent][step]` + timestamps.
- Outcome: token-efficient runs with auditable traces.

3. Orchestration plane (`deterministic-work-item-execution-with-explicit-gates`)

- Enforces strict `Plan -> Patch -> Test -> Report` stage transitions.
- Enforces human authority for `make feature` and `pc-feature` unless explicit in-run approval exists.
- HIGH-risk tickets stop after preflight in `Awaiting PO Approval`.
- Outcome: predictable, auditable ticket execution.

4. Recovery and integrity plane (`resume-safety-fail-closed-commit-gate-scoped-autofix`, `single-worktree-orchestration-template-drift-hardening`)

- Resume manager restores in-progress WI state, skips completed deterministic stages, reruns tests/CI.
- Commit gate fails closed on missing planner/tester/reporter evidence.
- Drift hardening performs deterministic scoped repair and blocks unresolved drift with remediation.
- Outcome: safe recovery and reliable collaboration integrity.

5. Role governance plane (`orchestrator-roles-plan-reviewer-gate-role-specific-prompts`)

- Dedicated planner/reviewer/patcher/tester/reporter prompts and owned artifacts.
- Plan Reviewer approval is required before patching.
- Outcome: better plan quality and lower rework.

6. Quality and evolution plane (`anti-hardcode-test-policy-synthetic-end-to-end-smoke-feature`, `incremental-prd-to-features-post-run-learning-loop`)

- Anti-hardcode policy enforces multiple fixtures, deterministic seeds, invariants, boundary contracts.
- Synthetic smoke validates gates, resume behavior, logs, and fail-closed completion path.
- Incremental PRD sync is add-missing only; learning loop writes proposal-only improvements requiring human approval.
- Outcome: stronger regression resistance and controlled process evolution.

Authoritative dependency edges for sequencing and `feature-order.json` decisions:

- `bootstrap-safe-template-reapply -> output-offload-structured-logs-shared-runner`
- `output-offload-structured-logs-shared-runner -> deterministic-work-item-execution-with-explicit-gates`
- `deterministic-work-item-execution-with-explicit-gates -> resume-safety-fail-closed-commit-gate-scoped-autofix`
- `deterministic-work-item-execution-with-explicit-gates -> single-worktree-orchestration-template-drift-hardening`
- `single-worktree-orchestration-template-drift-hardening -> orchestrator-roles-plan-reviewer-gate-role-specific-prompts`
- `resume-safety-fail-closed-commit-gate-scoped-autofix -> anti-hardcode-test-policy-synthetic-end-to-end-smoke-feature`
- `deterministic-work-item-execution-with-explicit-gates -> incremental-prd-to-features-post-run-learning-loop`
- `output-offload-structured-logs-shared-runner -> incremental-prd-to-features-post-run-learning-loop`
- `orchestrator-roles-plan-reviewer-gate-role-specific-prompts -> incremental-prd-to-features-post-run-learning-loop`

## Module boundaries

| Module                 | Responsibility                   | Inputs -> Outputs                                            | Boundary rule                                        | Feature linkage                                                                                                         |
| ---------------------- | -------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Template bootstrap     | Apply/reapply templates          | repo + template source -> created/updated/skipped files      | Idempotent apply only                                | `bootstrap-safe-template-reapply`                                                                                       |
| Conflict resolver      | Resolve file collisions          | conflict set + user choice -> resolved files                 | Explicit choice on ambiguity                         | `bootstrap-safe-template-reapply`                                                                                       |
| Shared runner          | Deterministic command execution  | command + metadata -> result + run context                   | Policy-neutral executor                              | `output-offload-structured-logs-shared-runner`                                                                          |
| Offload service        | Persist noisy output             | stdout/stderr -> `.offload/<id>.txt` + index                 | Mandatory for noisy commands                         | `output-offload-structured-logs-shared-runner`                                                                          |
| Structured logging     | Correlated step logs             | stage events -> `logs/<WI>/<step>.log`                       | Stable prefix and timestamps                         | `output-offload-structured-logs-shared-runner`                                                                          |
| Orchestrator core      | Stage machine and gates          | ticket state -> stage transitions                            | Never violate stage order                            | `deterministic-work-item-execution-with-explicit-gates`                                                                 |
| Gate policy engine     | Authority/risk/DoD/commit checks | metadata + evidence -> pass/fail                             | Fail closed on missing approval/evidence             | `deterministic-work-item-execution-with-explicit-gates`, `resume-safety-fail-closed-commit-gate-scoped-autofix`         |
| Resume manager         | Restart interrupted runs         | prior WI logs + state -> resumed execution                   | Preserve active WIP by default; rerun tests/CI       | `resume-safety-fail-closed-commit-gate-scoped-autofix`                                                                  |
| Worktree scope manager | Single-worktree role ownership   | role + feature scope -> allowed paths                        | No `feature-worktrees.json`; block cross-role writes | `single-worktree-orchestration-template-drift-hardening`, `orchestrator-roles-plan-reviewer-gate-role-specific-prompts` |
| Drift hardening        | Detect and repair template drift | template baseline + repo state -> scoped repairs/remediation | Allowed-path repair only                             | `single-worktree-orchestration-template-drift-hardening`                                                                |
| Quality harness        | Anti-hardcode and smoke checks   | test plan + fixtures -> compliance verdict                   | Enforce fixture diversity and invariants             | `anti-hardcode-test-policy-synthetic-end-to-end-smoke-feature`                                                          |
| Incremental sync       | Add-missing PRD -> features      | PRD + feature dirs -> additive updates                       | Never delete; skip Done                              | `incremental-prd-to-features-post-run-learning-loop`                                                                    |
| Learning loop manager  | Failure-driven proposals         | WI evidence -> proposal entries                              | Proposal-only until human approval                   | `incremental-prd-to-features-post-run-learning-loop`                                                                    |

## Infra considerations

- Runtime is local foreground CLI on macOS; no daemon or scheduler.
- Data boundary is repository-local files only; no cloud or remote state.
- Required tools: `git`, `make`, `codex`, language runtimes, and `tools/offload-proxy/pp`.
- Observability baseline is mandatory: `.offload/` pointers plus `logs/<WI>/<step>.log`.
- Deterministic script steps run through shared runner metadata for correlation.
- Serena is preferred when available for symbol-aware edits.

## Design constraints

- Single-user, local CLI scope only; no UI, no multi-user collaboration.
- No Windows support.
- Mandatory workflow order: `Plan -> Patch -> Test -> Report`.
- `make feature` and `pc-feature` are human-authority commands unless explicitly approved in-run.
- HIGH-risk work must stop in `Awaiting PO Approval` until explicit approval.
- Idempotency and recoverability are non-negotiable.
- Noisy output offload is mandatory; large inline output in prompts is disallowed.
- Precommit autofix must be staged-file-scoped and must not change `docs/03-logs/*` or role-owned execution logs.
- PRD-to-features sync is additive only and skips `Status: Done` artifacts.
- Single feature worktree default is required; do not introduce `feature-worktrees.json`.

## Build strategy

Dependency-valid feature order:

1. `bootstrap-safe-template-reapply`
2. `output-offload-structured-logs-shared-runner`
3. `deterministic-work-item-execution-with-explicit-gates`
4. `resume-safety-fail-closed-commit-gate-scoped-autofix`
5. `single-worktree-orchestration-template-drift-hardening`
6. `orchestrator-roles-plan-reviewer-gate-role-specific-prompts`
7. `anti-hardcode-test-policy-synthetic-end-to-end-smoke-feature`
8. `incremental-prd-to-features-post-run-learning-loop`

Phase rollout:

- Phase 1: `F1`, `F3` foundation so all later steps produce structured evidence.
- Phase 2: `F2` deterministic orchestration and mandatory gates.
- Phase 3: `F4`, `F5` resume safety, fail-closed commit integrity, drift hardening.
- Phase 4: `F6`, `F7` role specialization plus anti-hardcode/smoke hardening.
- Phase 5: `F8` incremental document evolution and human-gated learning proposals.

Decision rationales for `feature-order.json`:

- `F1 -> F3`: offload/log substrate depends on bootstrapped template/tool paths.
- `F3 -> F2`: orchestration must emit mandatory evidence by default.
- `F2 -> F4` and `F2 -> F5`: resume and drift controls rely on stable stage markers.
- `F5 -> F6`: role boundaries rely on enforced single-worktree ownership.
- `F4 -> F7`: smoke checks must validate existing recovery/fail-closed behavior.
- `F2 + F3 + F6 -> F8`: incremental sync and learning proposals require stable gates, evidence, and role outputs.

## Feature alignment map

| Feature slug                                                   | Outcome                                                             | Notes                                               | Required dependencies                                                                                                                                                  | Architecture decision                                   | Acceptance signal                                                     |
| -------------------------------------------------------------- | ------------------------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------- |
| `bootstrap-safe-template-reapply`                              | New/existing repos become execution-ready with idempotent reruns    | Conflict handling: overwrite/merge/skip             | None                                                                                                                                                                   | Deterministic bootstrap with explicit conflict resolver | Immediate rerun has no unintended churn                               |
| `output-offload-structured-logs-shared-runner`                 | Noisy output stays token-efficient and every step is traceable      | `pp` pointers + `logs/<WI>/<step>.log` + metadata   | `bootstrap-safe-template-reapply`                                                                                                                                      | Shared runner + mandatory offload/log contract          | Noisy commands emit pointer IDs and correlated logs                   |
| `deterministic-work-item-execution-with-explicit-gates`        | `Plan -> Patch -> Test -> Report` runs predictably and is auditable | Command authority remains with the human PO/user    | `output-offload-structured-logs-shared-runner`                                                                                                                         | Strict state machine + authority/risk/DoD gates         | HIGH-risk pauses at preflight; gate decisions logged                  |
| `resume-safety-fail-closed-commit-gate-scoped-autofix`         | Interrupted runs resume safely; commits require complete evidence   | Active-WIP preserve by default; strict commit gate  | `deterministic-work-item-execution-with-explicit-gates`                                                                                                                | Resume checkpoints and fail-closed evidence gate        | Resume skips completed stages; incomplete evidence blocks commit      |
| `single-worktree-orchestration-template-drift-hardening`       | Reliable role collaboration without worktree tracking-file drift    | No `feature-worktrees.json`; deterministic recovery | `deterministic-work-item-execution-with-explicit-gates`                                                                                                                | Single-worktree ownership and scoped drift repair       | Cross-role edits blocked; unresolved drift returns remediation        |
| `orchestrator-roles-plan-reviewer-gate-role-specific-prompts`  | Cleaner separation of responsibilities and better plan quality      | Dedicated planner/reviewer/patcher/tester/reporter  | `single-worktree-orchestration-template-drift-hardening`                                                                                                               | Dedicated Plan Reviewer gate with role-owned artifacts  | Patch cannot start without reviewer approval                          |
| `anti-hardcode-test-policy-synthetic-end-to-end-smoke-feature` | Better regression resistance and early workflow break detection     | Fixtures + seeds + invariants + boundary contracts  | `resume-safety-fail-closed-commit-gate-scoped-autofix`                                                                                                                 | Anti-hardcode policy plus synthetic smoke contract      | Policy violations fail test stage; smoke validates orchestration path |
| `incremental-prd-to-features-post-run-learning-loop`           | Feature docs evolve safely and repeated failures are reduced        | Add-missing only; human-gated improvements          | `deterministic-work-item-execution-with-explicit-gates`, `output-offload-structured-logs-shared-runner`, `orchestrator-roles-plan-reviewer-gate-role-specific-prompts` | Additive PRD sync + proposal-only learning loop         | Done features untouched; proposals carry WI/agent/step evidence       |
