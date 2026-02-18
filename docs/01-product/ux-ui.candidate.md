# PezzosCode UX/UI

## User journeys

### Journey 1: Make a repo execution-ready, then reapply safely

- **Outcomes covered:** **Bootstrap + safe template reapply** (`bootstrap-safe-template-reapply`) -> new/existing repos become execution-ready with idempotent reruns.
- User runs bootstrap in a local repo.
- If template conflicts exist, CLI asks `overwrite`, `merge`, or `skip` and shows scope before applying.
- Success is a concise summary with applied/skipped items and explicit rerun safety.

### Journey 2: Move one ticket through deterministic gates

- **Outcomes covered:** **Deterministic work-item execution with explicit gates** (`deterministic-work-item-execution-with-explicit-gates`) -> Plan -> Patch -> Test -> Report is predictable and auditable; **Orchestrator roles + Plan Reviewer gate + role-specific prompts** (`orchestrator-roles-plan-reviewer-gate-role-specific-prompts`) -> cleaner role separation and plan quality; **Anti-hardcode test policy + synthetic end-to-end smoke feature** (`anti-hardcode-test-policy-synthetic-end-to-end-smoke-feature`) -> better regression resistance via policy/smoke checks.
- Human PO/user starts execution; system emits preflight (scope, risk, files-to-change, TDD plan, DoD).
- HIGH risk halts at `Awaiting PO Approval` until explicit approval.
- Planner -> Plan Reviewer -> Patcher -> Tester -> Reporter handoffs are explicit; failed review/test/report loops return to Planner with owner-scoped PM TODO ids.

### Journey 3: Keep traceability high and prompt noise low

- **Outcomes covered:** **Output offload + structured logs + shared runner** (`output-offload-structured-logs-shared-runner`) -> noisy output stays token-efficient and every step is traceable.
- During noisy steps, CLI shows pointer ids and short status instead of long inline output.
- User debugs from `.offload/<id>.txt` and `logs/<WI>/<step>.log` with timestamped prefixes.

### Journey 4: Resume safely and block incomplete commits

- **Outcomes covered:** **Resume safety + fail-closed commit gate + scoped autofix** (`resume-safety-fail-closed-commit-gate-scoped-autofix`) -> interrupted runs resume safely and commits require complete evidence; **Single-worktree orchestration + template-drift hardening** (`single-worktree-orchestration-template-drift-hardening`) -> reliable collaboration in a single feature worktree with drift hardening.
- On rerun, system resumes in place, preserves active WIP by default, and re-runs tests/CI.
- Drift repair is scoped and deterministic; unresolved drift returns explicit remediation.
- Commit remains blocked until required planner/tester/reporter evidence is complete.

### Journey 5: Evolve docs incrementally after each run

- **Outcomes covered:** **Incremental PRD-to-features + post-run learning loop** (`incremental-prd-to-features-post-run-learning-loop`) -> feature docs evolve safely and repeated failures are reduced.
- PRD-to-features adds only missing items and skips `Status: Done`.
- If a selected feature is out of order, CLI blocks with missing prerequisite slugs and the next eligible feature so the user can continue without guessing.
- Failures can produce improvement proposals for human approval (not auto-applied).

## Workflows

### Workflow A: Bootstrap + safe template reapply

1. User runs bootstrap command in target repo.
2. System checks prerequisites and repo context.
3. System applies templates/tools/docs with explicit `overwrite|merge|skip` handling.
4. System prints what changed and confirms idempotent rerun behavior.
5. User continues to `context -> PRD -> features`.

### Workflow B: Deterministic work-item execution with explicit gates

1. Human PO/user starts execution command.
2. System emits preflight report with risk classification, work-item DoD, and open/carry PM TODO ids for owner routing.
3. HIGH risk stops at `Awaiting PO Approval` until explicit approval is granted.
4. Planner produces plan; Plan Reviewer must approve before any patch.
5. Patcher implements; Tester runs only Allowed Tests, including anti-hardcode policy checks from **Anti-hardcode test policy + synthetic end-to-end smoke feature**.
6. Reporter records outcomes; review/test/report failures loop to Planner with unresolved PM TODOs carried forward.
7. Final `make ci` gate runs only after role-loop success, aligned with **Orchestrator roles + Plan Reviewer gate + role-specific prompts** handoff rules.

### Workflow C: Output offload + structured logs + shared runner

1. Deterministic script commands run through shared runner metadata (`work_item_id`, `agent_name`, `run_id`).
2. Noisy command output is offloaded to `.offload/<id>.txt`; CLI surfaces pointer ids.
3. CI/tests/precommit/feature steps append structured logs to `logs/<WI>/<step>.log`.
4. User inspects pointer + log path without repeating expensive commands.

### Workflow D: Resume safety + fail-closed commit gate + scoped autofix

1. Rerun detects in-progress state and resumes without duplicating prior sections.
2. Completed stages are skipped safely; tests/CI re-run for confidence.
3. Drift detection from **Single-worktree orchestration + template-drift hardening** triggers scoped repair and allowed-file restage only.
4. Commit gate enforces complete execution evidence; missing fields keep commit blocked.

### Workflow E: Incremental PRD-to-features + post-run learning loop

1. Incremental PRD-to-features updates add missing feature docs only; existing/done features are preserved.
2. System validates prerequisite dependencies before generation/execution ordering; out-of-order selection is blocked with missing prerequisite slugs and next valid target.
3. Post-run failures are transformed into proposed improvements in the learning loop.
4. Human approves or rejects proposals before any process change is applied.

## UX constraints

- CLI-only interaction model on macOS; no web/desktop UI surfaces.
- Single-user optimization: interaction text assumes one Developer/PO persona and avoids team-role ambiguity.
- Prompt minimalism: require input only for true gates (conflict choice, HIGH-risk approval, explicit resets).
- Deterministic wording for gates: HIGH-risk prompt must be explicit, e.g., `Do you approve the HIGH-risk ticket? (y/n)`.
- Deterministic wording for gates: blocked state label must be `Awaiting PO Approval`.
- Idempotent feedback: every run summary must indicate whether work was resumed, skipped, repaired, or newly executed.
- Token-efficiency rule: never paste large command output inline when offload is applicable.
- Observability rule: each critical step must emit a stable log path and machine-searchable prefix.
- Recovery-first errors: every blocking error message must include immediate remediation action and whether rerun is safe.
- Dependency-gate clarity: blocked ordering states must list missing prerequisite feature slugs and the next eligible feature/action.
- Scope guardrails in UX copy: do not introduce UI/cloud/multi-user/Windows language in prompts or docs.
- Role-boundary clarity: user-facing status must identify current role/stage so handoff failures are diagnosable.
