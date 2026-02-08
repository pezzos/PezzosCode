# Ticket Execution Protocol (TDD + Gates)

> **Canonical implementation workflow for agents**
>
> For any work item implementation, this protocol is mandatory. It supersedes generic workflow guidance for execution.

---

**Terminology:** A "work item" refers to an execution unit defined in `docs/02-features/<feature>/dev-tasks.md`.

## Scope Control (No Scope Creep)

- Follow Context Boundaries and Non-Goals: `docs/00-context/context-boundaries-operating-model.md`.
- Do not add features, automation, or optimizations beyond the work item.
- If requirements are unclear, stop and ask the PO.
- Ticket-specific Definition of Done must be stated before coding.

## End-to-End Workflow

1. **Work Item Ingestion**
   - Run `make feature F=<feature-id>` to bootstrap and execute the work item.
   - Manual mode (no autonomous TDD/implementation): `make feature MANUAL=1 F=<feature-id>`.
   - Example (one command): `make feature F=01`.
   - Open the work item source: `docs/02-features/<feature>/dev-tasks.md`.
   - Confirm scope, success criteria, and change budget.
   - Complexity flag: `complexity: "simple" | "complex"` recorded in the execution log entry.
   - Complex work items run an orchestrated flow with explicit tester/reporter feedback steps.
   - Work Item IDs increment per feature; the sequence continues across dates.

- Role scope is enforced (planner/tester/reporter log files only; patcher excluded from those files).
- Planner/Tester/Reporter run in the patcher worktree so they review shared content; separate worktrees are not created for those roles.
- Runtime artifacts (`dev-tasks.md`, planner/tester/reporter logs, and `logs/<WI>/...`) are worktree-local during execution and are collected into `main` only after successful completion.
- Use a single worktree per feature and auto-collect into `main` as a single squashed commit (no `feature-worktrees.json`).
  - Tooling must be idempotent: reruns should not corrupt state or report success when a step fails.
- Deterministic steps are executed via a shared runner library with standard metadata injection (`work_item_id`, `agent_name`, `run_id`).
- Logs for CI/tests/precommit/feature runs are written inside the active feature worktree at `logs/<WI>/<step>.log` with `[WI-...][agent][step]` prefix and timestamps.

2. **Resuming a Work Item (Automatic)**
   - If an execution log entry already exists, `make feature` resumes automatically.
   - Startup resume policy is controlled by `RESUME_MODE`:
     - `auto` (default): resume in-progress work and preserve existing feature-worktree WIP.
     - `prompt`: ask before continuing/recreating an existing feature worktree.
     - `fresh`: recreate the feature patcher worktree and start from a clean baseline.
   - Only one feature can be actively in progress at a time; runs fail fast if another feature patcher worktree is ahead/dirty.
   - Existing dirty state in the active feature worktree is treated as work-in-progress and checkpointed at startup.
   - Startup must not discard dirty files in the active feature worktree unless `RESUME_MODE=fresh` is explicitly requested.
   - If an existing feature worktree is behind `main`, auto-resume fails (policy: `main` must stay unchanged while a feature is running).
   - Preflight is skipped if the **Preflight Report** section is already filled.
   - TDD generation is skipped if the **TDD Plan** section is already filled.
   - Tests and CI are always re-run on resume.
   - Commit is skipped if a commit message is already recorded in the worklog.
   - Logs are updated by the automation; do not require manual edits to pass gates.

3. **Preflight Report (Mandatory)**
   - Produce the Preflight Report exactly in the format below.

4. **Risk Classification**
   - Classify the work item as LOW or HIGH risk using the deterministic rules below.

5. **Approval Gate (HIGH Risk Only)**
   - If HIGH, display triggers and request interactive approval to continue (`[y/N]`).
   - Non-interactive runs default to deny unless `APPROVE_HIGH_RISK=1` is set.
   - No implementation work until approval is explicitly granted.
   - Record **Awaiting PO Approval** in the execution log entry.

6. **Plan → Patch → Test → Report**
   - Plan: approach, files, risks, tests, and work-item-specific DoD.
   - Plan is reviewed by Plan Reviewer (no code edits) before patching.
   - Before patching, enforce deterministic plan policy checks and block if the plan includes role-scoped/global log files or forbidden commands (`make feature`, `pc-feature`).
   - Plan-reviewer read-only enforcement uses pre/post worktree dirty snapshots and blocks only reviewer-introduced deltas.
   - Plan must include anti-hardcode coverage (fixtures per critical path, seed strategy, invariant checks, contract boundaries).
   - Block the work item if the Plan/TDD Plan does not state fixture count (>=2 per critical path), seed strategy, and invariant checks.
   - Patch: make the smallest diff that satisfies the work item (TDD where applicable).
   - Test: run agreed checks and record results.
   - Tests must be listed in the **Allowed Tests** section of the dev-tasks execution log (exact commands).
     - Planner must populate Allowed Tests before the Tester runs.
     - The Tester runs only those commands.
     - `make ci`, `make feature`, and `pc-feature` are forbidden as tests.
     - If Allowed Tests remain missing/invalid after planner remediation, fail with explicit remediation guidance (no placeholder smoke commands).
   - Report: summarize what changed, commands run, and outcomes.

7. **Feedback Loop (Planner ↔ Patcher ↔ Tester ↔ Reporter)**
   - dev-tasks execution log is planner-owned; only the Planner edits it.
   - Tester records failures in the feature `validation-log.md`.
   - Reporter records issues and scope gaps in the feature `reporter-log.md`.
   - Planner updates the plan and logs the loop in the execution log entry.
   - Step routing is strict:
     - Planner Reviewer `BLOCK` loops back to Planner revision before patching.
     - Tester `FAIL` loops back to Planner.
     - Tester `PASS` advances to Reporter.
     - Reporter `FAIL` loops back to Planner.
     - Reporter `PASS` is the only success path to final gates/commit.
   - Retry loop is capped by `MAX_LOOPS` to prevent infinite execution.
   - If a step has nothing to do during a retry, record a no-op entry in the iteration log and continue.
   - Repeat until feedback is resolved.

8. **TDD Cycle (when applicable)**
   - Write tests first.
   - Run tests and confirm they fail for the right reason.
   - Implement minimal code changes to pass tests.
   - Re-run tests and confirm they pass.
   - Tests must satisfy the anti-hardcode requirements in `docs/04-process/testing-strategy.md`.

9. **Docs Sync (Mandatory)**
   - Update required docs/logs per dev-tasks execution log entry.
   - Global logs (docs/03-logs) are written only after the feature completes and gates pass.
   - Reporter supplies the global log summaries for decision/implementation/validation logs at completion.
   - Record a gating summary in docs/03-logs/implementation-log.md and validation findings in docs/03-logs/validation-log.md for the Execute work item workflow so the logs mirror the implemented sequence.
   - Enforce the output offload workflow with tools/offload-proxy/pp at each gate and capture compliance decisions in docs/03-logs/decision-log.md.
   - Orchestrator gate handoffs are logged in docs/03-logs/decision-log.md or docs/03-logs/validation-log.md before the PO loop continues.

10. **Gates**

- Run `make ci` only at the final gate after the Plan→Patch→Test→Report loop passes.
- CI attempts are capped at 2 total runs: initial run + optional single autofix rerun.
- Autofix must run deterministic format/lint fixers first, then use Codex only as fallback for unresolved issues.
- Autofix must run pre-commit on the staged scoped file list only (`--files`), re-stage only that same list, and fail if out-of-scope files are touched.
- Precommit-only autofix runs must not modify `docs/03-logs/*` or feature execution logs.
- Autofix prompt template: `docs/04-process/ci-autofix-prompt.md`.

11. **Commit**

- 1 work item = 1 commit.
- Follow commit rules in `docs/04-process/git-workflow.md`.
- Use `tools/pc-commit` to enforce convention and checks.
- Before commit, ensure the planner-owned dev-tasks execution log is complete and role logs contain tester/reporter output.

12. **AI Tooling (preferred)**

- Use Serena for code navigation and symbol-aware edits when available.
- Offload large outputs using `tools/offload-proxy/pp` to reduce token usage.
- Subagent escalations are orchestrator-mediated: subagent returns a structured escalation request, orchestrator validates it against policy allowlist, records decision/action, and executes only approved commands.

---

## Risk Classification (Deterministic)

HIGH RISK if any of the following apply:

- Planned files OR actual changed paths (if available) touch `sanitizer/`, `detectors/`, `restore/`, `git_ops/`, or `metadata/`.
- Changes modify secret-blocking or fail-close behavior.
- Changes affect restore apply semantics or permissions.
- Secret scanning dependencies/policies are added or modified.
- Change budget exceeded (>10 files OR >2 new modules OR cross-cutting refactor impacting 3+ modules).

Otherwise, LOW RISK.

---

## Preflight Report (Mandatory Format)

```
Work Item ID / dev-task ref:
PRD reference / feature mapping:
Risk level: LOW | HIGH (triggers: ...)
Scope summary (in/out):
Non-goals reminder:
Files to change:
Change budget:
TDD plan: tests to write first
Work Item DoD (explicit):
Doc updates planned:
```

---

## Final Report (Mandatory Format)

```
What changed (files):
Tests written (names) + results:
Docs/logs updated checklist:
make ci results:
Commands run (use `pp` for noisy output):
Commit message:
```

---

## References

- Dev workflow (background only): `docs/04-process/dev-workflow.md`
- Definition of Done: `docs/04-process/definition-of-done.md`
- Git workflow: `docs/04-process/git-workflow.md`
- Dev-tasks template: `docs/02-features/feature-template/dev-tasks.md`
- Context boundaries: `docs/00-context/context-boundaries-operating-model.md`
