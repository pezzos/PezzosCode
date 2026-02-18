# UX/UI

## User journeys

### 1) Bootstrap or refresh a repository without churn (`bootstrap-safe-template-reapply`, Feature 1)

Outcome reference: New/existing repos become execution-ready with idempotent reruns.

- Trigger: User runs bootstrap/update in a local repository.
- Interaction: Apply templates/tools/docs with explicit overwrite/merge/skip choices on conflicts.
- Success signal: Immediate rerun produces no unintended file churn.
- User-visible result: Repo is execution-ready without manual template repair.

### 2) Execute an approved work item through deterministic gates (`deterministic-work-item-execution-with-explicit-gates`, `orchestrator-roles-plan-reviewer-gate-role-specific-prompts`, `anti-hardcode-test-policy-synthetic-end-to-end-smoke-feature`; Features 2, 6, 7)

Outcome references:

- Feature 2: Plan -> Patch -> Test -> Report runs predictably and is auditable.
- Feature 6: Cleaner separation of responsibilities and better plan quality.
- Feature 7: Better regression resistance and early workflow break detection.
- Trigger: Ticket has preflight scope/risk/files-to-change, TDD plan, and work-item DoD.
- Interaction: Preflight runs first; HIGH-risk pauses for explicit approval; Plan Reviewer must approve before patching; tester enforces allowed tests and anti-hardcode policy.
- User-visible result: Minimal manual intervention with explicit gates and auditable stage decisions.

### 3) Keep execution observable and recover safely after interruption (`output-offload-structured-logs-shared-runner`, `resume-safety-fail-closed-commit-gate-scoped-autofix`, `single-worktree-orchestration-template-drift-hardening`; Features 3, 4, 5)

Outcome references:

- Feature 3: Noisy output stays token-efficient and every step is traceable.
- Feature 4: Interrupted runs resume safely; commits require complete evidence.
- Feature 5: Reliable role collaboration without worktree tracking-file drift.
- Interaction: Noisy commands offload to pointers, structured logs persist per step, resume skips completed deterministic stages, scoped drift repair runs on allowed paths, and commit stays blocked until evidence is complete.
- User-visible result: No silent state loss, clear recovery path, and no commit on incomplete work.

### 4) Improve safely after each run (`incremental-prd-to-features-post-run-learning-loop`, Feature 8)

Outcome reference: Feature docs evolve safely and repeated failures are reduced.

- Interaction: PRD-to-features sync adds missing only and skips completed artifacts; repeated-failure proposals are recorded with WI/agent/step evidence.
- Governance: Improvements are proposal-only until explicit human approval.
- User-visible result: Continuous hardening without resetting completed work.

## Workflows

### Workflow A: Bootstrap and safe reapply (Feature 1)

1. Validate local repo context and prerequisites.
2. Apply templates/tools/docs.
3. Resolve conflicts via overwrite/merge/skip.
4. Print concise created/updated/skipped summary.
5. Allow deterministic rerun with no unintended churn.

### Workflow B: Evidence-first deterministic execution (Features 3, 2, 4, 5, 6, 7)

1. Route noisy command output through `tools/offload-proxy/pp` and capture `.offload/<id>.txt`.
2. Write step logs to `logs/<WI>/<step>.log` with `[WI-...][agent][step]` and timestamps.
3. Run preflight and enforce HIGH-risk approval gate.
4. Enforce stage order: Plan -> Patch -> Test -> Report.
5. Require Plan Reviewer approval before patching; enforce role ownership in one feature worktree.
6. On interruption, resume from saved stage, preserve active WIP by default, rerun tests/CI, and attempt scoped drift recovery.
7. Keep commit fail-closed until required execution/report evidence is complete.
8. Enforce anti-hardcode policy (>=2 fixtures on critical paths, deterministic seeds, invariants, boundary contracts) and synthetic smoke coverage when validating workflow changes.

### Workflow C: Dependency-aligned delivery order (prepare-features guardrail)

- F1 -> F3: bootstrap-safe-template-reapply before output-offload-structured-logs-shared-runner.
- F3 -> F2: evidence substrate before deterministic-work-item-execution-with-explicit-gates.
- F2 -> F4 and F2 -> F5: deterministic orchestration before resume/commit and single-worktree/drift hardening.
- F5 -> F6: worktree ownership hardening before role specialization.
- F4 -> F7: resume/fail-closed controls before synthetic smoke and anti-hardcode hardening.
- F2 + F3 + F6 -> F8: stable orchestration, evidence, and role outputs before incremental PRD sync and learning loop.

### Workflow D: Incremental evolution and learning loop (Feature 8)

1. Sync PRD to features in add-missing mode only.
2. Skip artifacts already marked done.
3. Record repeated-failure proposals with WI/agent/step evidence.
4. Write proposals to `docs/possible-improvements.md`.
5. Apply only after explicit human approval.

## UX constraints

- CLI-only UX; no web/desktop UI flows.
- macOS-first local usage; no Windows support.
- Single-user UX only; no collaboration patterns.
- Command authority is explicit: only human PO/user runs `make feature` and `pc-feature` unless explicit in-run approval is granted.
- Prompting stays minimal and gate-based: conflict resolution, HIGH-risk approval, explicit reset choices.
- Idempotency and recoverability are non-negotiable: avoid duplicate prompts, duplicate log sections, or ambiguous run state.
- Large/noisy outputs must be offloaded; inline output stays concise and pointer-based.
- Observability is mandatory: each critical stage surfaces log paths and offload ids.
- Deterministic steps are script-first via shared runner metadata (`work_item_id`, `agent_name`, `run_id`).
- Scope boundaries stay explicit in UX copy: no daemon/scheduler, no cloud/remote state, and no UI expansion in this project.
