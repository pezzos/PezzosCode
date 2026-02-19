# PezzosCode UX/UI

## User journeys

### Journey 1: Make a repo execution-ready, then reapply safely

- **Outcomes covered:** **Bootstrap + safe template reapply** (`bootstrap-safe-template-reapply`) -> new/existing repos become execution-ready with idempotent reruns.
- User runs bootstrap in a local repo.
- If template conflicts exist, CLI asks `overwrite`, `merge`, or `skip` and shows scope before applying.
- Success is a concise summary with applied/skipped items and explicit rerun safety.
- Blocked outcome is missing prerequisites or unreadable repo context, with remediation and safe rerun guidance.

### Journey 2: Move one ticket through deterministic gates

- **Outcomes covered:** **Deterministic work-item execution with explicit gates + zero-input defaults** (`deterministic-work-item-execution-with-explicit-gates-zero-input-defaults`) -> Plan -> Patch -> Test -> Report is predictable and auditable with deterministic defaults when optional inputs are omitted; **Orchestrator roles + Plan Reviewer gate + role-specific prompts** (`orchestrator-roles-plan-reviewer-gate-role-specific-prompts`) -> cleaner role separation and plan quality; **Anti-hardcode test policy + synthetic end-to-end smoke feature** (`anti-hardcode-test-policy-synthetic-end-to-end-smoke-feature`) -> better regression resistance via policy/smoke checks.
- Human PO/user starts execution; zero-input defaults populate optional execution fields before preflight.
- System emits preflight (scope, risk, files-to-change, TDD plan, DoD).
- HIGH risk halts at `Awaiting PO Approval` until explicit approval.
- Planner -> Plan Reviewer -> Patcher -> Tester -> Reporter handoffs are explicit; failed review/test/report loops return to Planner with owner-scoped PM TODO ids.
- Success is a completed role loop with final CI gate pass and full evidence.
- Blocked outcomes are missing PO approval, rejected plan, or failing allowed tests.

### Journey 3: Keep traceability high and prompt noise low

- **Outcomes covered:** **Output offload + token budget guardrails + structured logs + shared runner** (`output-offload-token-budget-guardrails-structured-logs-shared-runner`) -> noisy output stays token-efficient and every step is traceable.
- During noisy steps, CLI shows pointer ids and short status instead of long inline output.
- Token budget guardrails force offload when inline output would exceed limits.
- User debugs from `.offload/<id>.txt` and `logs/<WI>/<step>.log` with timestamped prefixes.
- Success is complete troubleshooting context without rerunning expensive commands.
- Blocked outcome is missing offload/log artifact, with explicit rerun/remediation instructions.

### Journey 4: Resume safely and block incomplete commits

- **Outcomes covered:** **Resume safety + deterministic auto-recovery + fail-closed commit gate** (`resume-safety-deterministic-auto-recovery-fail-closed-commit-gate`) -> interrupted runs resume safely and commits require complete evidence; **Single-worktree orchestration + template-drift hardening** (`single-worktree-orchestration-template-drift-hardening`) -> reliable collaboration in a single feature worktree with drift hardening.
- On rerun, system resumes in place, preserves active WIP by default, and re-runs tests/CI.
- Deterministic auto-recovery selects the next stage from persisted execution markers instead of re-planning from scratch.
- Drift repair is scoped and deterministic; unresolved drift returns explicit remediation.
- Commit remains blocked until required planner/tester/reporter evidence is complete.
- Success is resumed completion with a passing fail-closed commit gate.
- Blocked outcomes are unresolved drift, recovery ambiguity, or missing execution evidence.

### Journey 5: Evolve docs incrementally after each run

- **Outcomes covered:** **Incremental PRD-to-features + post-run learning loop** (`incremental-prd-to-features-post-run-learning-loop`) -> feature docs evolve safely and repeated failures are reduced; **Workflow complexity reduction + skill inventory pruning** (`workflow-complexity-reduction-skill-inventory-pruning`) -> fewer execution branches and clearer, supported CLI paths.
- PRD-to-features adds only missing items and skips `Status: Done`.
- If a selected feature is out of order, CLI blocks with missing prerequisite slugs and the next eligible feature so the user can continue without guessing.
- If a deprecated or non-inventory skill path is invoked, CLI blocks and shows the canonical command/path for the pruned workflow.
- Failures can produce improvement proposals for human approval (not auto-applied).
- Success is ordered feature progression using only active, supported workflow paths.
- Blocked outcomes are unmet dependencies or unsupported skill selections.

## Workflows

### Workflow A: Bootstrap + safe template reapply

1. User runs bootstrap command in target repo.
2. System checks prerequisites and repo context.
3. System applies templates/tools/docs with explicit `overwrite|merge|skip` handling.
4. System prints what changed and confirms idempotent rerun behavior.
5. User continues to `context -> PRD -> features`, or is blocked with prerequisite remediation.

### Workflow B: Deterministic work-item execution with explicit gates + zero-input defaults

1. Human PO/user starts execution command.
2. System applies zero-input defaults for optional execution fields, then emits preflight report with risk classification, work-item DoD, and open/carry PM TODO ids for owner routing.
3. HIGH risk stops at `Awaiting PO Approval` until explicit approval is granted.
4. Planner produces plan; Plan Reviewer must approve before any patch.
5. Patcher implements; Tester runs only Allowed Tests, including anti-hardcode policy checks from **Anti-hardcode test policy + synthetic end-to-end smoke feature**.
6. Reporter records outcomes; review/test/report failures loop to Planner with unresolved PM TODOs carried forward.
7. Final `make ci` gate runs only after role-loop success, aligned with **Orchestrator roles + Plan Reviewer gate + role-specific prompts** handoff rules.
8. Success is gated completion; blocked outcomes are approval/review/test gate failures.

### Workflow C: Output offload + token budget guardrails + structured logs + shared runner

1. Deterministic script commands run through shared runner metadata (`work_item_id`, `agent_name`, `run_id`).
2. System evaluates token budget guardrails for each command output.
3. Noisy or over-budget output is offloaded to `.offload/<id>.txt`; CLI surfaces pointer ids instead of inline dumps.
4. CI/tests/precommit/feature steps append structured logs to `logs/<WI>/<step>.log`.
5. User inspects pointer + log path without repeating expensive commands; missing artifacts block completion with remediation.

### Workflow D: Resume safety + deterministic auto-recovery + fail-closed commit gate

1. Rerun detects in-progress state and resumes without duplicating prior sections.
2. Deterministic auto-recovery selects the next valid stage from persisted run state.
3. Completed stages are skipped safely; tests/CI re-run for confidence.
4. Drift detection from **Single-worktree orchestration + template-drift hardening** triggers scoped repair and allowed-file restage only.
5. Commit gate enforces complete execution evidence; missing fields keep commit blocked.
6. Success is resumed completion with commit allowed only after all gates pass.

### Workflow E: Incremental PRD-to-features + post-run learning loop + workflow complexity reduction

1. User runs the feature-generation/update flow.
2. System enforces the pruned skill inventory and canonical workflow path from `workflow-complexity-reduction-skill-inventory-pruning`; unsupported/deprecated paths are blocked with replacement guidance.
3. Incremental PRD-to-features updates add missing feature docs only; existing/done features are preserved.
4. System validates prerequisite dependencies before generation/execution ordering; out-of-order selection is blocked with missing prerequisite slugs and next valid target.
5. Post-run failures are transformed into proposed improvements in the learning loop.
6. Human approves or rejects proposals before any process change is applied.
7. Success is ordered, lower-complexity progression across active feature slugs.

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
