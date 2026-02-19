# PezzosCode Product Design

## System architecture

PezzosCode uses a local-first, script-first architecture designed for one developer/PO on macOS. The system optimizes for deterministic execution, idempotent reruns, and auditable evidence rather than feature breadth.

Core runtime flow is a gated state machine:
`Preflight -> Risk gate -> Plan -> Plan review -> Patch -> Test -> Report -> Final CI -> Commit gate`.
If risk is HIGH without explicit approval, execution stops at status `Awaiting PO Approval`.

Architecture layers:

1. CLI control layer for bootstrap/update and work-item execution commands.
2. Orchestration layer that enforces stage order, restart rules, and human gates.
3. Role execution layer for planner, plan-reviewer, patcher, tester, and reporter responsibilities.
4. Deterministic tooling layer using shared runner metadata (`work_item_id`, `agent_name`, `run_id`) plus output offload.
5. Evidence layer that persists logs, role artifacts, and commit-readiness checks.

This structure directly supports P0 outcomes: execution-ready repos (feature 1), predictable and auditable delivery (feature 2), token-efficient traceability (feature 3), and safe resume/commit behavior (feature 4).

## Module boundaries

| Module                             | Owns                                                                          | Boundary rules                                                                                     |
| ---------------------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Template manager                   | Bootstrap and safe reapply of templates; conflict policy overwrite/merge/skip | Must be idempotent; cannot delete feature history or completed artifacts                           |
| Workflow orchestrator              | Stage transitions, gate checks, retries, and loopbacks                        | Must enforce Plan -> Patch -> Test -> Report; cannot bypass Plan Reviewer or tester/reporter loops |
| Role boundary enforcer             | File ownership and role-scoped write constraints                              | Must block writes outside role-owned logs/docs when role restrictions apply                        |
| Shared runner adapter              | Deterministic command execution with standard metadata and log hooks          | Deterministic tasks run via scripts first; avoid ad-hoc LLM execution for repeatable work          |
| Output offload service             | `tools/offload-proxy/pp` integration and pointer/index lifecycle              | No large noisy output in prompts; commands return pointer ids for retrieval                        |
| Observability and evidence store   | Structured logs and run evidence for audit/commit gate                        | Log paths and prefixes are stable and timestamped for tail/readability                             |
| Resume and recovery manager        | In-progress detection, stage skipping, and safe reruns                        | Preserve active WIP by default; re-run tests/CI on resume                                          |
| Drift hardening and scoped autofix | Template/living-file drift detection and deterministic scoped repair          | Repairs must be scoped and fail-closed with explicit remediation if unresolved                     |
| Commit gate                        | Enforces complete work-item evidence before commit                            | Must block commit when required planner/tester/reporter evidence is missing                        |

## Infra considerations

- Platform: macOS-first local CLI execution only; no cloud services, daemons, schedulers, or Windows path assumptions.
- Required local tools: `git`, `make`, `codex`, language runtimes used by target repo, and `tools/offload-proxy/pp`.
- Persistence layout:
  - `.offload/<id>.txt` and metadata index for noisy outputs.
  - `logs/<WI>/<step>.log` for CI/tests/precommit/feature runs with `[WI-...][agent][step]` prefixes and timestamps.
  - `docs/02-features/<feature>/` role artifacts and execution records.
  - `docs/03-logs/` for durable implementation/decision/validation traceability.
- Worktree model: one feature worktree by default; no `feature-worktrees.json`.
- Reliability posture: deterministic scripts for repeatable steps, explicit gate failures, and replace-in-place updates for idempotent reruns.
- Security/data posture: local repo boundaries only; no remote state transfer.

## Design constraints

- Single-user optimization is intentional; no multi-user abstractions.
- CLI-only interaction; no UI/TUI/web layer in this project.
- Human command authority is mandatory for `make feature` and `pc-feature` unless explicit in-run approval is granted.
- HIGH-risk items require explicit approval before implementation; otherwise stop after preflight.
- Plan Reviewer approval is required before patching.
- Allowed Tests policy is enforced; tester cannot run forbidden orchestration commands.
- Output offload is mandatory for noisy commands to control token usage.
- Precommit/CI must share one autofix path; staged-file scope cannot mutate protected logs.
- PRD-to-features updates are incremental add-missing only and must not rewrite completed features.
- Design must preserve idempotency, recoverability, and fail-closed commit behavior as non-negotiables.

## Build strategy

1. Foundation baseline (feature 1): keep bootstrap and safe template reapply as the only root capability so every later phase inherits idempotent repo setup.
2. Shared infra and observability (feature 2): establish output offload + token budget guardrails + structured logs + shared runner metadata used by all downstream execution and validation gates.
3. Deterministic orchestration core (feature 3): enforce gated Plan -> Patch -> Test -> Report, zero-input defaults, authority controls, and HIGH-risk stop conditions.
4. Worktree and drift hardening (feature 4): apply single-worktree orchestration and deterministic template-drift repair once orchestration semantics are stable.
5. Resume and commit integrity (feature 5): add resume checkpoints, deterministic auto-recovery, and fail-closed evidence-based commit gating.
6. Role governance (feature 6): layer role prompts and Plan Reviewer enforcement after core gates and recovery behavior are in place.
7. Quality resilience (feature 7): enforce anti-hardcode test policy and synthetic end-to-end smoke execution to catch regression paths early.
8. Controlled evolution (feature 8): run incremental PRD-to-features reconciliation and human-gated learning-loop proposals without rewriting completed work.
9. Workflow simplification (feature 9): reduce workflow complexity and prune low-value skill inventory/redundant script paths without changing required gates.

Dependency-alignment acceptance condition for downstream ordering artifacts: `bootstrap-safe-template-reapply` is the only root feature and every other feature must declare at least one prerequisite from an earlier phase.

Release sequencing is reliability-first and anchored to explicit prerequisite arrays in the alignment map; ordering follows risk reduction and MVP hardening goals rather than new product surface area. If dependency artifacts diverge from this contract, build readiness is blocked until prerequisite arrays are corrected.

PM feedback resolution: architect-owned prerequisite arrays are now explicit in the Feature alignment map for prepare-features consumption.

Canonical handoff rule for dependency artifacts: each feature row prerequisite array is normative and must be copied unchanged into `feature-order.json` across `decisions[*].depends_on`, `dependencies`, and `ordered_features[*].dependencies`.

## Feature alignment map

Dependency-intent acceptance condition: bootstrap is the only zero-prerequisite row and every other row depends on modules established by earlier features in this map.

UX alignment anchor from `ux-ui.md`: Journey 1 maps to feature 1, Journey 2 maps to features 2/3/6/7, Journey 3 maps to feature 4, Journey 4 maps to feature 5, Journey 5 maps to feature 8, and Journey 6 maps to feature 9.

PM-TODO-059 resolution contract: prerequisite arrays in this table are the architect canonical source for downstream dependency-planner outputs.

| Feature                                                                                                                                                   | Outcome and notes                                                                                                                                           | Architectural alignment                                                                                                            | Prerequisites                                                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bootstrap + safe template reapply (`bootstrap-safe-template-reapply`)                                                                                     | Execution-ready repos with idempotent reruns; conflict handling overwrite/merge/skip                                                                        | Template manager with deterministic merge policy and non-destructive reapply semantics                                             | `[]`                                                                                                                                                                                                            |
| Output offload + token budget guardrails + structured logs + shared runner (`output-offload-token-budget-guardrails-structured-logs-shared-runner`)       | Token-efficient noisy output handling with token-budget guardrails and full traceability via `pp` pointers and `logs/<WI>/<step>.log`                       | Shared runner adapter + offload service + structured observability store with compact summaries and pointer-based retrieval        | [`bootstrap-safe-template-reapply`]                                                                                                                                                                             |
| Deterministic work-item execution with explicit gates + zero-input defaults (`deterministic-work-item-execution-with-explicit-gates-zero-input-defaults`) | Predictable, auditable Plan -> Patch -> Test -> Report with zero-input defaults; prompts only for ambiguity, missing intent, or required HIGH-risk approval | Workflow orchestrator state machine, risk gate, and authority enforcement with zero-input defaults outside explicit approval gates | [`bootstrap-safe-template-reapply`, `output-offload-token-budget-guardrails-structured-logs-shared-runner`]                                                                                                     |
| Single-worktree orchestration + template-drift hardening (`single-worktree-orchestration-template-drift-hardening`)                                       | Reliable role collaboration without worktree tracking drift; deterministic recovery                                                                         | Single-worktree controller and drift hardening module with scoped repair + fail-closed remediation                                 | [`bootstrap-safe-template-reapply`, `output-offload-token-budget-guardrails-structured-logs-shared-runner`, `deterministic-work-item-execution-with-explicit-gates-zero-input-defaults`]                        |
| Resume safety + deterministic auto-recovery + fail-closed commit gate (`resume-safety-deterministic-auto-recovery-fail-closed-commit-gate`)               | Safe interruption recovery with deterministic auto-recovery for common failures and strict evidence-based commit decisions; active WIP preserved by default | Resume manager, deterministic auto-recovery executor, and fail-closed commit gate validator tied to required work-item artifacts   | [`output-offload-token-budget-guardrails-structured-logs-shared-runner`, `deterministic-work-item-execution-with-explicit-gates-zero-input-defaults`, `single-worktree-orchestration-template-drift-hardening`] |
| Orchestrator roles + Plan Reviewer gate + role-specific prompts (`orchestrator-roles-plan-reviewer-gate-role-specific-prompts`)                           | Better plan quality and cleaner responsibility split across planner/reviewer/patcher/tester/reporter                                                        | Role boundary enforcer + role prompt registry + mandatory plan-review gate                                                         | [`deterministic-work-item-execution-with-explicit-gates-zero-input-defaults`]                                                                                                                                   |
| Anti-hardcode test policy + synthetic end-to-end smoke feature (`anti-hardcode-test-policy-synthetic-end-to-end-smoke-feature`)                           | Higher regression resistance using fixtures, seeds, invariants, and boundary contracts                                                                      | Test policy validator and synthetic feature harness integrated into validation stage                                               | [`deterministic-work-item-execution-with-explicit-gates-zero-input-defaults`, `orchestrator-roles-plan-reviewer-gate-role-specific-prompts`]                                                                    |
| Incremental PRD-to-features + post-run learning loop (`incremental-prd-to-features-post-run-learning-loop`)                                               | Safe docs evolution and reduced repeated failures through add-missing updates and human-gated proposals                                                     | Incremental feature reconciler and improvement proposal pipeline writing to `docs/possible-improvements.md`                        | [`bootstrap-safe-template-reapply`, `single-worktree-orchestration-template-drift-hardening`, `resume-safety-deterministic-auto-recovery-fail-closed-commit-gate`]                                              |
| Workflow complexity reduction + skill inventory pruning (`workflow-complexity-reduction-skill-inventory-pruning`)                                         | Lower maintenance overhead with fewer fragile execution paths by removing or archiving low-value skills and redundant script/config paths                   | Workflow-surface reducer and skill inventory governance policy that prunes redundant paths while preserving required gates         | [`deterministic-work-item-execution-with-explicit-gates-zero-input-defaults`, `orchestrator-roles-plan-reviewer-gate-role-specific-prompts`, `incremental-prd-to-features-post-run-learning-loop`]              |
