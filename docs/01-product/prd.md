# Product Requirements Document (PRD)

> **Single source of truth for WHAT the product must do**

---

## Overview

**Product Name:** PezzosCode

**Version:** 0.6

**Last Updated:** 2026-02-13

**Status:** Draft

### Executive Summary

<!-- 2-3 sentences describing what this product/feature does and why it matters -->

PezzosCode bootstraps a new project with a standardized, AI-first workflow and tooling.
It enables a single developer/PO to describe features and let AI execute tickets with minimal manual setup.
The focus is simplicity, robustness, idempotent re-runs, and a deterministic Plan → Patch → Test → Report loop.
Deterministic steps are delegated to scripts, observability is improved with structured logs, and PRD → features updates are incremental to prevent regressions.
Execution stays local (macOS CLI), with explicit human gates for HIGH-risk work and strict scope boundaries to avoid workflow drift.

## Problem Statement

### User Pain Points

1. **Bootstrapping AI-first projects is manual and inconsistent**
   - Who experiences it: single developer/PO.
   - Current workaround: manual setup and ad-hoc templates.
   - Impact: wasted time, inconsistent process, broken AI workflows.

2. **AI workflows break on small issues**
   - Who experiences it: single developer/PO.
   - Current workaround: manual fixes and repeated setup.
   - Impact: token waste, loss of momentum, unreliable execution.

3. **Deterministic steps burn tokens**
   - Who experiences it: single developer/PO.
   - Current workaround: ask the LLM to do repeatable tasks.
   - Impact: higher cost, slower iteration, inconsistent outcomes.

4. **Lack of observability hides failures**
   - Who experiences it: single developer/PO.
   - Current workaround: rerun commands and manually scan output.
   - Impact: hard-to-debug failures and repeated CI/test runs.

### Success Criteria

<!-- How we'll know if we've solved the problem -->

| Metric                                  | Current      | Target           | Measure                      |
| --------------------------------------- | ------------ | ---------------- | ---------------------------- |
| Bootstrap in one command                | Manual setup | One command      | Manual verification          |
| Ticket execution reliability            | Inconsistent | Minimal failures | Worklog + user confirmation  |
| Context mistakes (template vs. project) | Occasional   | Rare             | Log entries / corrections    |
| Token waste from large outputs          | High         | Low              | Offload ids + prompt review  |
| CI/test observability                   | Low          | High             | Structured logs + timestamps |

### Success Metrics (Template)

<!-- List the specific, trackable outcomes that define success -->

- **Bootstrap time:** baseline manual, target one command, timeframe immediate, data source user confirmation.
- **Ticket execution success rate:** baseline inconsistent, target reliable for approved tickets, data source worklogs.
- **Idempotent reruns:** baseline manual recovery, target safe rerun without duplication, data source worklogs.
- **Context mistakes:** baseline occasional, target rare, data source implementation/decision logs.
- **Output offload usage:** baseline ad hoc, target mandatory for noisy commands, data source offload ids.

## Users & Use Cases

### Target Users

**Primary Persona: Developer/PO (single user)**

- **Who they are:** Entrepreneur building multiple projects with Codex as the executor.
- **Goals:** Bootstrap projects fast; describe features and let AI implement.
- **Frustrations:** Manual setup, workflow breaks, inconsistent process adherence.
- **Technical level:** Intermediate to advanced (workflow should still be simple).

**Secondary Persona:** None (single-user focus).

### Core Use Cases

#### Use Case 1: Bootstrap a project

**Actor:** Developer/PO

**Preconditions:** Target repo exists (new or existing).

**Main Flow:**

1. User runs bootstrap command.
2. System copies templates/tools into target repo.
3. User begins filling context docs.

**Postconditions:** Repo is ready for PezzosCode workflow.

**Alternative Flows:**

- **Alt 1:** Existing files conflict; user chooses overwrite/merge/skip.

#### Use Case 2: Execute approved tickets

**Actor:** Developer/PO

**Preconditions:** Context, PRD, features, and tickets are defined.

**Main Flow:**

1. User runs ticket execution command.
2. System runs Plan → Patch → Test → Report, with TDD where applicable.
3. System offloads noisy output, records results, and updates logs.
4. User approves gates when required.

**Postconditions:** Ticket is implemented and documented.

## Prioritized Feature List

<!-- Ordered list of features tied to the PRD scope -->

| Priority | Feature                                                         | Outcome                                                           | Notes                                               |
| -------- | --------------------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------- |
| P0       | Bootstrap + safe template reapply                               | New/existing repos become execution-ready with idempotent reruns  | Conflict handling: overwrite/merge/skip             |
| P0       | Deterministic work-item execution with explicit gates           | Plan → Patch → Test → Report runs predictably and is auditable    | Command authority remains with the human PO/user    |
| P0       | Output offload + structured logs + shared runner                | Noisy output stays token-efficient and every step is traceable    | `pp` pointers + `logs/<WI>/<step>.log` + metadata   |
| P0       | Resume safety + fail-closed commit gate + scoped autofix        | Interrupted runs resume safely; commits require complete evidence | Active-WIP preserve by default; strict commit gate  |
| P0       | Single-worktree orchestration + template-drift hardening        | Reliable role collaboration without worktree tracking-file drift  | No `feature-worktrees.json`; deterministic recovery |
| P1       | Orchestrator roles + Plan Reviewer gate + role-specific prompts | Cleaner separation of responsibilities and better plan quality    | Dedicated planner/reviewer/patcher/tester/reporter  |
| P1       | Anti-hardcode test policy + synthetic end-to-end smoke feature  | Better regression resistance and early workflow break detection   | Fixtures + seeds + invariants + boundary contracts  |
| P1       | Incremental PRD-to-features + post-run learning loop            | Feature docs evolve safely and repeated failures are reduced      | Add-missing only; human-gated improvements          |
| P2       | Offload audit + compacted logs + workflow quality nudges        | Better long-run maintainability and signal-to-noise               | Index lifecycle, compact logs, precommit warnings   |

## Process Features

- [ ] Output offload enforcement (P0): Noisy outputs stored in `.offload/` and referenced by id.
- [ ] Resume in-progress tickets (P0): Existing worklog resumes automatically; completed steps are skipped while tests/CI re-run.
- [ ] Commit gated by completed ticket docs (P0): Commit is blocked unless execution log and required report/test fields are complete.
- [ ] Shared runner library (P0): Standardized Codex/Serena execution with metadata + logging helpers.
- [ ] Structured logs for CI/tests/precommit/feature runs (P0): `logs/<WI>/<step>.log` with prefixes and timestamps.
- [ ] Unified autofix script (P0): Single script used by `make ci` and precommit.
- [ ] Precommit restage + vanilla Codex config (P0): `git add -u` after autofix, staged-only fixes, no Serena.
- [ ] Single worktree per feature (P0): Remove `feature-worktrees.json`.
- [ ] Workflow hardening for template drift + autofix recovery (P0): Detect drift between templates/living files, repair only scoped files, re-stage allowed paths, and fail-close on unresolved drift.
- [ ] Orchestrator + sub-agent roles (P1): Clear role separation and gates.
- [ ] Role-specific prompts + Plan Reviewer (P1): Dedicated prompts and plan validation.
- [ ] Incremental prd-to-features (P1): Add missing only; never delete; skip Done.
- [ ] Learning loop proposals (P1): Post-run improvement proposals with human gate.
- [ ] Worktree policy + naming convention (P1): Clean isolation for parallel roles.
- [ ] Anti-cheat testing strategy (P1): Multiple fixtures, seeded randomness, invariants, contract tests.
- [ ] End-to-end workflow smoke test with a synthetic feature (P1): Validate orchestrator gates and resume/log behavior before real feature runs.
- [ ] Offload audit + upgrade plan (P2): Index + list/get/purge with retention.
- [ ] Compact log skills (P2): Compact decision/implementation logs without data loss.
- [ ] Feature gating in precommit (P2): Soft warning when earlier features incomplete.
- [ ] Skill mining from repeated prompts (P2): Propose reusable skills from recurring patterns.

## Requirements

### Functional Requirements

#### Must Have (P0)

- [ ] **FR-001:** Bootstrap a project with PezzosCode templates in one command.
  - **Rationale:** Eliminates manual setup and inconsistency.
  - **Acceptance Criteria:** Templates, tools, and docs are copied into a target repo.

- [ ] **FR-002:** Execute a ticket end-to-end with AI and minimal manual work.
  - **Rationale:** Primary user goal is AI execution with minimal intervention.
  - **Acceptance Criteria:** Plan → Patch → Test → Report with orchestrator gates and feedback-loop restart rules; required role logs and execution evidence are updated.

- [ ] **FR-003:** Require ticket-specific Definition of Done before coding.
  - **Rationale:** Prevent “it kinda works” outcomes and clarify finish lines.
  - **Acceptance Criteria:** Ticket template includes explicit work-item DoD; execution blocks patching until DoD, tests, and report sections are defined.

- [ ] **FR-004:** Offload noisy command output.
  - **Rationale:** Reduce token waste and keep prompts focused.
  - **Acceptance Criteria:** Noisy outputs are stored in `.offload/`, referenced by id, and retrievable through deterministic index metadata.

- [ ] **FR-005:** Provide a shared runner library for tool/script execution.
  - **Rationale:** Standardize Codex/Serena invocation and reduce token waste.
  - **Acceptance Criteria:** Tools can call a shared runner that injects `work_item_id`, `agent_name`, `run_id` and logging helpers.

- [ ] **FR-006:** Write structured, tail-friendly logs for CI/tests/precommit/feature runs.
  - **Rationale:** Improve observability and debugging.
  - **Acceptance Criteria:** Logs are written to `logs/<WI>/<step>.log` with `[WI-...][agent][step]` prefix and timestamps.

- [ ] **FR-007:** Unify autofix logic for CI and precommit.
  - **Rationale:** Prevent divergence between local hooks and CI behavior.
  - **Acceptance Criteria:** One script (e.g., `scripts/pc-ci-check`) is invoked by both `make ci` and precommit.

- [ ] **FR-008:** Precommit re-stages autofix changes and runs Codex with vanilla config.
  - **Rationale:** Ensure staged fixes are applied cleanly without extra noise.
  - **Acceptance Criteria:** Precommit runs `git add -u` after autofix, prints re-staged files, and uses vanilla Codex config without Serena.

- [ ] **FR-009:** Incremental prd-to-features generation.
  - **Rationale:** Prevent regressions and duplication.
  - **Acceptance Criteria:** Adds missing features only, never deletes existing, skips features with `Status: Done` in `dev-tasks.md`.

- [ ] **FR-010:** Role-specific prompts and Plan Reviewer gate.
  - **Rationale:** Increase plan quality and reduce rework.
  - **Acceptance Criteria:** Prompts exist per role and Plan Reviewer approves plan before patching.

- [ ] **FR-011:** Post-run improvement proposals with human gate.
  - **Rationale:** Prevent repeat failures and accumulate learnings.
  - **Acceptance Criteria:** Failures log errors with `WI/agent/step`, propose a patch (not auto-applied), and record in `docs/possible-improvements.md`.

- [ ] **FR-012:** Resume in-progress work items deterministically.
  - **Rationale:** Prevent ticket restarts and preserve work-in-progress after interruptions.
  - **Acceptance Criteria:** Existing execution log resumes automatically, completed stages are skipped safely, tests/CI are re-run, and startup does not discard dirty active-worktree state unless explicitly requested.

- [ ] **FR-013:** Block commits until ticket docs are complete.
  - **Rationale:** Ensure each work item is auditable and complete before merge.
  - **Acceptance Criteria:** Commit step verifies planner-owned execution log and required report/test fields; commit is skipped/blocked if incomplete.

- [ ] **FR-014:** Harden template drift detection and scoped autofix recovery.
  - **Rationale:** Keep template-driven repos reliable when precommit/CI detects out-of-sync files.
  - **Acceptance Criteria:** Workflow detects template/living-file drift, attempts deterministic scoped repairs, re-stages only allowed files, and fails with explicit remediation when unresolved.

- [ ] **FR-015:** Enforce command authority and HIGH-risk approval gates.
  - **Rationale:** Prevent unauthorized or unsafe autonomous execution.
  - **Acceptance Criteria:** Only the human PO/user runs `make feature` / `pc-feature` unless explicitly approved in-run; HIGH-risk work stops after preflight with `Awaiting PO Approval` until explicit approval is granted.

#### Should Have (P1)

- [ ] **FR-101:** Reapply templates to existing repos safely.
  - **Rationale:** Enables template evolution without losing local edits.
  - **Acceptance Criteria:** Conflicts handled by overwrite/merge/skip; idempotent reruns.

- [ ] **FR-102:** Provide a synthetic feature for end-to-end workflow smoke testing.
  - **Rationale:** Catch orchestration/gate regressions with a repeatable collaborative test path.
  - **Acceptance Criteria:** A lightweight synthetic feature can run full Plan → Patch → Test → Report, validate gates/resume/logs, and report pass/fail before real feature execution.

- [ ] **FR-103:** Enforce anti-hardcode testing coverage.
  - **Rationale:** Prevent brittle implementations that only pass shallow examples.
  - **Acceptance Criteria:** Plan/TDD states fixture count (>=2 critical-path fixtures), deterministic seed strategy, invariant assertions, and boundary contract tests.

#### Nice to Have (P2)

- [ ] **FR-201:** Single command to loop over approved features/tickets.
  - **Rationale:** Reduce manual step orchestration.
  - **Acceptance Criteria:** CLI can run the standard loop with user approvals.

### Non-Functional Requirements

#### Performance

- [ ] **NFR-001:** Commands should complete promptly for small/medium repos.
  - **Metric:** Runtime of bootstrap/ticket workflows.
  - **Target:** Reasonable for local developer workflow.

#### Security

- [ ] **NFR-101:** No remote/cloud data transfer.
  - **Rationale:** Keep workflow local and predictable.
  - **Compliance:** None.

#### Usability

- [ ] **NFR-201:** CLI-only with minimal prompts.
  - **Metric:** Number of required prompts per workflow.
  - **Target:** Only necessary gates (e.g., HIGH-risk approvals).

#### Reliability

- [ ] **NFR-301:** Idempotent reruns and recoverable failures.
  - **Metric:** Ability to rerun after error without corruption.
  - **Target:** No duplicate worklog sections or inconsistent status.

#### Determinism

- [ ] **NFR-401:** Predictable execution loop.
  - **Metric:** Plan → Patch → Test → Report always followed.
  - **Target:** Same input yields consistent workflow outputs.

#### Token Efficiency

- [ ] **NFR-501:** Avoid large outputs in prompts.
  - **Metric:** Offload ids used for noisy outputs.
  - **Target:** No large outputs pasted into prompts.

#### Observability

- [ ] **NFR-601:** Traceable, timestamped runs.
  - **Metric:** Log coverage for CI/tests/precommit/feature runs.
  - **Target:** Logs exist under `logs/<WI>/<step>.log` with prefixes and timestamps.

## Workflow/Process Requirements

- Documentation bootstrap sequence is fixed: `docs/00-context` → `docs/01-product/prd.md` → `docs/02-features/*`.
- Plan → Patch → Test → Report is mandatory for every work item.
- `make feature` is orchestration/bootstrap only and never listed as a plan step or Allowed Test command.
- Command authority: only the human PO/user runs `make feature` / `pc-feature` unless explicit per-run approval is granted.
- Preflight report is mandatory and includes scope, risk, files-to-change, TDD plan, and work-item DoD.
- Risk classification is deterministic; HIGH risk requires explicit approval before implementation and records `Awaiting PO Approval` when not granted.
- Ticket-specific Definition of Done is required before coding and must be satisfied before commit.
- Plan Reviewer validates plans before patching (no code edits) and reviewer/tester/reporter failures loop back to Planner until resolved.
- Planner provides Allowed Tests; Tester may run only those commands. `make ci`, `make feature`, and `pc-feature` are forbidden as test commands.
- Anti-hardcode testing policy is enforced: >=2 fixtures per critical path, deterministic seeds, invariant checks, and boundary contract coverage.
- Deterministic steps are delegated to scripts through a shared runner with standard metadata (`work_item_id`, `agent_name`, `run_id`).
- Output offload is mandatory for noisy commands; references use `.offload/<id>.txt` pointers and indexed metadata.
- CI/tests/precommit/feature runs write structured logs to `logs/<WI>/<step>.log` using `[WI-...][agent][step]` prefix + timestamps.
- Resume behavior preserves active feature-worktree WIP by default, supports explicit fresh reset, and always re-runs tests/CI.
- Worktree policy: one feature worktree by default, role ownership boundaries enforced, and no `feature-worktrees.json`.
- `prd-to-features` is incremental: add missing only, never delete existing, and skip `Status: Done`.
- Post-run workflow improvements are proposed by roles and written by orchestrator to `docs/possible-improvements.md` with human approval required for application.
- Final gate runs `make ci` only after role-loop success, with at most two attempts (initial + single autofix rerun).
- Commit gate is fail-closed, enforces complete work-item evidence, and follows `type(scope): summary` via `tools/pc-commit`.
- Precommit-only autofix must remain staged-file-scoped and must not modify `docs/03-logs/*` or feature execution logs.
- Use Serena for symbol-aware navigation/edits when available; otherwise keep deterministic tool/script-first behavior.
- Template/living-file drift hardening and synthetic-feature smoke tests remain required reliability checks.

### Constraints

**Technical Constraints:**

- macOS-first support; no Windows support.
- CLI-only; no UI in this project.
- Requires git, codex, make, and language runtimes as needed.
- Requires output offload wrapper `tools/offload-proxy/pp` for noisy commands.

**Business Constraints:**

- Personal use; optimize for simplicity and robustness.
- MVP stop condition applies: once MVP DoD is met, further implementation requires a new PRD update/version bump.

**Regulatory/Compliance:**

- None.

## User Experience

### User Journey

```
Bootstrap → Context/PRD → Features → Tickets → Execute → Repeat
```

### Key Screens/Interactions

1. **CLI: Bootstrap**
   - Purpose: Seed a repo with templates/tools.
   - Key elements: Command output and optional overwrite/merge/skip prompts.
   - Actions: Run bootstrap/update.

2. **CLI: Execute Ticket**
   - Purpose: Run the ticket workflow with AI.
   - Key elements: Preflight, gates, test results, commit suggestion.
   - Actions: Approve gates when required.

### Error States

| Scenario                          | User Experience | System Behavior             |
| --------------------------------- | --------------- | --------------------------- |
| Missing dependencies              | Clear error     | Fail fast with instructions |
| HIGH-risk ticket without approval | Blocked         | Stop after preflight        |
| Rerun after partial failure       | Resume safely   | Replace-in-place updates    |

## Scope

### Scope Boundaries

- **System boundaries:** local CLI tools, templates, and docs.
- **User boundaries:** single developer/PO; no secondary users.
- **Data boundaries:** local repos and docs only; no remote storage.
- **Platform boundaries:** macOS CLI.

### Non-Goals

- Cloud services or remote state.
- UI or multi-user collaboration.
- Windows support.
- Extra complexity or configuration beyond essentials.

### In Scope

- Bootstrap templates into repos.
- Update/reapply templates safely.
- Execute ticket workflow with AI.

### Out of Scope

- UI/desktop/web interfaces.
- Cloud sync or remote storage.
- Windows support.

### Future Considerations

- Optional loop-assist CLI wrappers are acceptable; any UI/TUI work belongs in a separate project that calls CLI commands.

## Dependencies

### Internal Dependencies

- **Docs/templates:** in `tools/templates/docs`.
- **Tools:** CLI scripts in `tools/`.

### External Dependencies

- **Codex CLI:** required for AI execution.
- **Git/Make:** required for workflow and tests.
- **Language runtimes:** Python/Node/Rust/Go as needed.
- **Output offload wrapper:** `tools/offload-proxy/pp` for noisy commands.

## Risks & Mitigations

| Risk                                                | Impact | Probability | Mitigation                                                 |
| --------------------------------------------------- | ------ | ----------- | ---------------------------------------------------------- |
| Tooling is not idempotent and re-runs corrupt state | High   | Medium      | Replace-in-place updates; tests for idempotency            |
| Template updates are hard to propagate              | High   | Medium      | Safe reapply with skip/merge                               |
| AI workflow burns tokens on repeatable steps        | High   | Medium      | Keep prompts minimal; skip completed work                  |
| Missing dependencies cause failures                 | Med    | Medium      | Preflight checks and clear errors                          |
| Process drift (skipped gates/logs)                  | Med    | Medium      | Enforce Plan → Patch → Test → Report in docs and templates |

## Open Questions

- None currently. Dependencies are assumed to exist locally (git, codex, make), and HIGH-risk approvals are handled via a prompt with optional `approval: "granted"` in ticket frontmatter.

## Appendix

### Related Documents

- docs/00-context/vision.md
- docs/00-context/users.md
- docs/00-context/system-map.md
- docs/00-context/assumptions.md
- docs/00-context/context-boundaries-operating-model.md
- docs/00-context/expected-features.md
- docs/04-process/dev-workflow.md
- docs/04-process/definition-of-done.md
- docs/04-process/testing-strategy.md
- docs/04-process/ticket-execution-protocol.md
- docs/04-process/output-offload.md
- docs/04-process/git-workflow.md

### Change Log

| Date       | Version | Changes                                                                                                         | Author       |
| ---------- | ------- | --------------------------------------------------------------------------------------------------------------- | ------------ |
| 2026-01-30 | 0.1     | Draft PRD from context docs                                                                                     | Primary user |
| 2026-02-02 | 0.2     | Add workflow/process requirements and offload policy                                                            | Primary user |
| 2026-02-02 | 0.3     | Add process features and expected-features mapping                                                              | Primary user |
| 2026-02-05 | 0.4     | Add observability, runner, incremental features, role prompts                                                   | Primary user |
| 2026-02-11 | 0.5     | Sync expected-features + protocol details (resume, gates, hardening, smoke test)                                | Primary user |
| 2026-02-13 | 0.6     | Reconcile PRD with context/process docs: authority gates, anti-hardcode policy, and prioritized feature mapping | Codex        |
