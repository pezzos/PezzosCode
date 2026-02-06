# Workflow Hardening Todo Plan (for `tools/pc-feature`)

Created: 2026-02-06
Scope: Implement the workflow fixes requested for restart behavior, worktree isolation, role gating, protocol enforcement, prompt loading, and safer commit/autofix behavior.

## How To Use This File

- Execute steps in order unless a step explicitly says it can run in parallel.
- Each step is self-contained: context, files, changes, tests, and done criteria are included.
- Keep diffs small. Update docs/templates alongside code when behavior changes.
- Use `tools/offload-proxy/pp` for noisy commands.

## Global Constraints

- Keep single-worktree-per-feature orchestration.
- Do not reintroduce `feature-worktrees.json`.
- `make ci` must not be used in Allowed Tests.
- Final commit path must be scoped (no `git add -A`).
- Respect role scopes and planner ownership of `dev-tasks` execution log.

## Step 01 - Baseline Regression Harness

Context:

- Current behavior has multiple workflow regressions and weak guardrails.
- Add tests first to lock expected behavior before refactoring.

Target files:

- `tests/test_pc_feature.py`
- `tests/test_pc_allowed_tests_check.py` (new, if needed)

Plan:

1. Add focused unit tests for:
   - Resume picks the newest in-progress WI, not the oldest.
   - Allowed tests run with worktree cwd (not root cwd).
   - No `feature-worktrees.json` side effects.
   - Final staging excludes unrelated files (no blanket stage).
   - Commit resume skip when Commit section already populated.
2. Add tests for `tools/pc-allowed-tests-check` covering valid `python -m unittest discover ...` commands.

Validation:

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_allowed_tests_check.py"` (if added)

Done when:

- New tests fail on current behavior and clearly encode expected fixes.

Handoff note:

- Keep tests deterministic by mocking subprocess calls and filesystem where possible.

## Step 02 - Safe Restart In Existing Worktree (No Destructive Reset)

Context:

- Startup currently force-removes dirty/ahead patcher worktrees/branches.
- This can delete unmerged work and blocks safe resume.

Target files:

- `tools/pc-feature`
- `tests/test_pc_feature.py`

Plan:

1. Introduce a pre-run worktree state check:
   - Detect existing feature patcher worktree.
   - Detect dirty status and ahead-of-main status.
2. At workflow start, print explicit warning when worktree is not pristine.
3. Ask user once: continue with existing worktree or abort.
4. If continue: keep using same worktree/branch (no delete/recreate).
5. Remove any cleanup/reset prompt behavior intended to wipe worktree state.
6. Keep hard fail for unsafe branch conditions only (e.g., worktree on `main`).

Validation:

- Simulate dirty/ahead worktree in tests and verify:
  - No `git worktree remove --force` or `git branch -D` is issued.
  - Continue path proceeds.
  - Abort path exits early with message.

Done when:

- Existing worktree state is preserved and resume is explicit/user-confirmed.

Handoff note:

- Keep prompt text short and machine-testable.

## Step 03 - Correct Work Item Resume Selection

Context:

- WI selection currently can pick wrong entry (oldest vs newest ordering bug).

Target files:

- `tools/pc-feature`
- `tests/test_pc_feature.py`

Plan:

1. Rework WI selection logic to choose latest in-progress entry by document order semantics.
2. Preserve behavior: if latest WI has `Outcome: pass`, create a new WI.
3. Add helper function with tests for multiple mixed WI states.

Validation:

- Unit tests for cases:
  - multiple entries with pass/needs replan
  - newest pass -> new WI
  - newest not pass -> resume newest

Done when:

- Resume consistently targets the intended current WI.

## Step 04 - Scoped Final Staging + Commit Resume Rule

Context:

- Final path stages all files (`git add -A`) and always attempts commit.
- This can commit unrelated changes and breaks protocol resume rule.

Target files:

- `tools/pc-feature`
- `tests/test_pc_feature.py`

Plan:

1. Implement commit-resume guard:
   - If Commit section already has commit message, skip final commit step.
2. Track allowed final stage paths from workflow-owned artifacts.
3. Stage only allowed changed files; fail on unexpected dirty paths with actionable message.
4. Add pre-commit clean-tree check for unrelated paths before final commit.

Validation:

- Test: unrelated dirty file present -> workflow blocks before final commit.
- Test: existing Commit section -> commit step skipped.

Done when:

- No blanket staging; resume does not duplicate commit attempts.

## Step 05 - Remove `feature-worktrees.json` Tracking

Context:

- Docs forbid this file, but orchestration still writes it.

Target files:

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md` (only if wording needs clarification)
- `tools/templates/docs/04-process/ticket-execution-protocol.md` (if doc changed)

Plan:

1. Remove `write_worktree_manifest` function and all calls.
2. Ensure worktree discovery relies on naming convention + git worktree metadata only.
3. Add regression test asserting no manifest file creation.

Validation:

- Run unit tests for `pc-feature`.
- Run grep to confirm no `feature-worktrees.json` writes in code paths.

Done when:

- No new manifest files are produced by workflow.

## Step 06 - Execute Allowed Tests In Tester/Patcher Worktree

Context:

- Allowed tests currently run from root/orchestrator context, risking stale code.

Target files:

- `tools/pc-feature`
- `tests/test_pc_feature.py`

Plan:

1. Ensure all Allowed Test commands run with `cwd=tester_path` (or designated worktree path).
2. Ensure prepatch smoke runs in worktree too.
3. Keep structured logs writing under root `logs/<WI>/...` via current metadata root handling.

Validation:

- Unit tests assert subprocess invocation cwd equals worktree path for smoke/tests.

Done when:

- Test execution context is worktree-isolated and deterministic.

## Step 07 - Plan Reviewer Gate (Required Before Patching)

Context:

- Protocol requires Plan Reviewer gate; orchestration does not run it.

Target files:

- `tools/pc-feature`
- `prompts/plan-reviewer.md` (or task-specific variant file)
- `tests/test_pc_feature.py`

Plan:

1. Add explicit plan-reviewer phase after planner writes plan.
2. Parse reviewer result (`Approve` vs `Block`).
3. On `Block`:
   - Append feedback to planner log / WI iteration context.
   - Route back to planner for plan update before patching.
4. On `Approve`:
   - Proceed to patcher.

Validation:

- Unit tests for approve and block branches.

Done when:

- No patch step can execute without plan-reviewer approval in current loop iteration.

## Step 08 - Externalize Role Prompts (No Hardcoded Inline Prompts)

Context:

- Docs require `prompts/<role>.md`; code currently hardcodes role prompts.

Target files:

- `tools/pc-feature`
- `prompts/*.md`
- optional new files: `prompts/planner-create.md`, `prompts/planner-update_from_feedback.md`, `prompts/patcher-update_from_feedback.md`, etc.
- `tests/test_pc_feature.py`

Plan:

1. Add prompt loader utility:
   - First try task-specific file `prompts/<role>-<task>.md`.
   - Fallback to `prompts/<role>.md`.
2. Support template variable substitution (work item id, plan text, feedback, etc.).
3. Replace inline prompt strings with loaded templates for planner/patcher/tester/reporter/plan-reviewer/global-log/commit tasks.

Validation:

- Unit tests for loader fallback and variable rendering.
- Smoke run for missing prompt file error quality.

Done when:

- Role prompt content is sourced from files, not inline literals.

## Step 09 - Feedback Loop Replanning/Repatch Enforcement

Context:

- On tester/reporter fail, loop does not explicitly enforce planner re-evaluation and patch updates based on feedback.

Target files:

- `tools/pc-feature`
- `prompts/planner-update_from_feedback.md` (new)
- `prompts/patcher-update_from_feedback.md` (new)
- `tests/test_pc_feature.py`

Plan:

1. On fail outcome, aggregate tester+reporter feedback text.
2. Run planner feedback task to explicitly decide:
   - plan still valid, or
   - revised plan required.
3. If revised plan required, update Plan section and log iteration note.
4. Trigger patcher feedback task with updated plan and failure notes.
5. Ensure Iteration Log is appended each cycle with decision rationale.

Validation:

- Tests for:
  - reporter/tester fail -> planner feedback task invoked
  - patched re-run path invoked
  - iteration log updated

Done when:

- Failure loop deterministically involves planner + patcher before retest.

## Step 10 - Reduce `make ci` Calls

Context:

- Workflow currently runs CI with retry/autofix loop; user wants fewer full CI runs.

Target files:

- `tools/pc-feature`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `tests/test_pc_feature.py`

Plan:

1. Keep scoped Allowed Tests in loop; forbid `make ci` there.
2. Run `make ci` only in final gate after loop passes.
3. Limit CI attempts to:
   - initial run
   - optional single autofix rerun (max 2 total), or 1 total if desired policy.
4. Ensure docs explicitly state this cadence.

Validation:

- Test command invocation counts for CI path.
- Docs regression tests (if present) updated.

Done when:

- CI execution is reduced and policy is documented.

## Step 11 - Use `tools/pc-commit` For Final Commit

Context:

- Protocol requires `tools/pc-commit`; code currently commits directly with git.

Target files:

- `tools/pc-feature`
- `tools/pc-commit` (if argument support changes needed)
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md` (if behavior wording updated)

Plan:

1. Replace final `git commit` call with `tools/pc-commit` invocation.
2. Ensure commit message generated by reporter/commit task is passed through.
3. Keep commit-resume skip behavior from Step 04.

Validation:

- Unit tests verify `tools/pc-commit` command is used.
- End-to-end smoke for commit path in temp repo fixture.

Done when:

- Final commit path is protocol-compliant.

## Step 12 - Allowed Tests Enforcement Cleanup

Context:

- Policy and checker behavior are inconsistent.
- Placeholder smoke fallback can pass workflow without meaningful validation.

Target files:

- `tools/pc-feature`
- `tools/pc-allowed-tests-check`
- `docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `tests/test_pc_feature.py`
- `tests/test_pc_allowed_tests_check.py`

Plan:

1. Align docs + code to forbid `make ci` in Allowed Tests.
2. Fix `pc-allowed-tests-check` parsing for:
   - `python -m unittest discover -s ... -p ...`
   - other valid unittest/pytest variants already used in repo.
3. Remove non-meaningful placeholder smoke fallback.
4. If Allowed Tests invalid/missing, fail with explicit remediation instructions.

Validation:

- `tools/pc-allowed-tests-check --cmd 'python -m unittest discover -s tests -p "test_*.py"'` returns success.
- New unit tests pass for checker parser.

Done when:

- Allowed Tests are strict, meaningful, and parser-accurate.

## Step 13 - Stronger Deterministic Risk Classification

Context:

- Risk classification currently misses protocol-defined path-based triggers.

Target files:

- `tools/pc-feature`
- `docs/04-process/ticket-execution-protocol.md` (if trigger wording normalization needed)
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `tests/test_pc_feature.py`

Plan:

1. Extend risk classifier to include deterministic path triggers from protocol:
   - `sanitizer/`, `detectors/`, `restore/`, `git_ops/`, `metadata/`.
2. Evaluate both planned file list (preflight) and actual changed paths (if available).
3. Keep existing change budget and semantic triggers.
4. Make trigger reporting explicit in Preflight Report.

Validation:

- Unit tests for each path trigger and mixed trigger scenarios.

Done when:

- Risk output matches protocol trigger rules.

## Step 14 - Subagent Escalation Broker + Worktree Sync Ordering

Context:

- Subagents cannot escalate under forced `approval_policy="never"`.
- Root file edits happen before worktree creation and can drift from worktree state.

Target files:

- `tools/pc-feature`
- `prompts/*` (if escalation request format is prompted)
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md` (if orchestration protocol text changes)
- `tools/templates/docs/04-process/ticket-execution-protocol.md`

Plan:

1. Move worktree creation before any mutable workflow writes, or migrate mutable writes into worktree path first.
2. Define orchestrator-mediated escalation flow:
   - Subagent returns structured escalation request (JSON contract).
   - Orchestrator validates request against allowlist/policy.
   - Orchestrator executes approved command (single control point).
3. Keep PO out of routine escalations by policy; orchestrator remains gatekeeper.
4. Add explicit logging for escalation request/decision/action.

Validation:

- Unit tests for:
  - request parsing and allowlist filtering
  - denied escalation path
  - approved escalation path command dispatch
  - worktree reflects latest workflow state immediately after creation

Done when:

- Escalation is orchestrator-controlled and worktree starts from current intended state.

## Step 15 - Autofix/Precommit Scope Lockdown

Context:

- Autofix currently runs `pre-commit --all-files` and can expand scope.

Target files:

- `tools/pc-feature`
- `tools/pc-precommit` (if reused)
- `tests/test_pc_feature.py`

Plan:

1. Capture staged file list before autofix.
2. Run pre-commit only on that file list.
3. Re-stage only those same files after autofix.
4. Block if autofix attempts to touch out-of-scope files.

Validation:

- Unit tests for staged-file-only behavior and out-of-scope detection.

Done when:

- Autofix cannot broaden the commit scope.

## Step 16 - Final Documentation/Template Sync + End-to-End Validation

Context:

- Behavior changes across orchestration require process docs and templates to stay aligned.

Target files:

- `docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/human-orchestration-workflow.md` (if needed)
- `tools/templates/docs/04-process/ticket-execution-protocol.md`
- `tools/templates/docs/04-process/human-orchestration-workflow.md` (if needed)
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/validation-log.md`
- `docs/03-logs/decision-log.md` (if policy decisions changed)

Plan:

1. Sync docs and templates with implemented behavior.
2. Run focused test suite for changed orchestration behavior.
3. Run `make ci` once final behavior is stable.
4. Update global logs with concise entries for decisions/implementation/validation.

Validation:

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`
- `tools/offload-proxy/pp make ci`

Done when:

- Code, docs, templates, and logs are consistent and CI passes.

## Explicitly Deferred (Per Request)

- Serena startup refresh/network concern is not treated as a blocker in this plan.
- Failure-path worktree cleanup is intentionally not treated as a defect because resume-in-existing-worktree is desired.
