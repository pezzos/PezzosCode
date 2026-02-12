# Planner Log

## Entries

### WI-20260211-01 - 2026-02-11

Updated `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md` with the planner output for `WI-20260211-01`:

- Filled `#### Plan` using the required `Plan Contract v1` structure at `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md:85`.
- Added exact `Allowed Tests` commands at `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md:72`.
- Ensured all concrete test commands in the plan match Allowed Tests verbatim.
- Enforced planned patcher file-edit scope to exclude disallowed paths, including non-compacted `docs/03-logs/*`, in:
  - `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md:53`
  - `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md:79`
- Added explicit handoff note that non-compacted `docs/03-logs` updates are reporter/orchestrator-owned at `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md:106`.
- Added systematic review command log/results at `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md:55`.

Systematic review commands executed:

- `nl -ba docs/02-features/17-resume-in-progress-tickets/dev-tasks.md | sed -n '60,130p'`
- `nl -ba docs/02-features/17-resume-in-progress-tickets/dev-tasks.md | sed -n '30,95p'`
- `git status --short`
- `git diff -- docs/02-features/17-resume-in-progress-tickets/dev-tasks.md`

Commit status:

- I attempted to commit once at the end, but sandbox permissions blocked git lock creation:
  - `fatal: Unable to create .../index.lock: Operation not permitted`
- No commit was created.

### WI-20260211-01 - 2026-02-11

Updated Allowed Tests to satisfy existence and scope checks.

### WI-20260211-01 - 2026-02-11

Step Planner revise after Plan Reviewer BLOCK at attempt 1.

Decision: Block Reasons: - Plan violates orchestrator scope policy. Required changes: - forbidden path in plan: docs/02-features/17-resume-in-progress-tickets/dev-tasks.md Optional suggestions: - Keep plan files limited to implementation targets; role/global logs are automation-owned.

### WI-20260211-01 - 2026-02-11

Decision: REVISE_PLAN
Rationale: Reporter failure shows a traceability gap not covered by the prior implementation-focused plan, so execution-record consistency must be enforced before approval.

Revised Plan:
Plan Contract v1
Approach:

1. Add/adjust tests that fail when tester/reporter artifacts exist but execution-entry completion signals are still pending, while preserving existing resume-routing expectations.
   Files to change:

- tests/test_pc_feature.py
  Risks:
- Tests may accidentally encode file-format specifics too tightly and become brittle to harmless wording changes.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Include fixtures for complete execution entries, pending execution entries with tester/reporter artifacts present, and clean non-resume runs.
- Deterministic seed strategy: Use fixed fixture content and stable temp paths for repeatable outcomes.
- Invariant checks: Assert identical inputs always produce identical block/continue decisions.
- Contract boundary coverage: Validate boundaries between artifact discovery, execution-entry completeness checks, and mode policy handling.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`

2. Implement execution-record consistency guardrails in orchestration logic so contradictory resume evidence is blocked with explicit reasons.
   Files to change:

- tools/pc-feature
  Risks:
- Over-strict validation could block legitimate recovery paths if edge cases are missed.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Reuse contradictory/complete fixture corpus from step 1 for implementation validation.
- Deterministic seed strategy: Keep checks purely input-derived with no time/order dependence.
- Invariant checks: Ensure guardrails never allow continuation when required completion signals are absent.
- Contract boundary coverage: Confirm explicit mode selections and inferred resume state both pass through the same consistency gate.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`

3. Re-run targeted validation and capture compacted evidence only; hand off role-scoped and non-compacted documentation updates for final reporting pass.
   Files to change:

- docs/03-logs/compacted/
  Risks:
- Incomplete evidence handoff can still delay reporter approval even when code behavior is correct.
  Tests (anti-hardcode coverage required):
- Fixture coverage: N/A for documentation-only evidence step.
- Deterministic seed strategy: N/A for documentation-only evidence step.
- Invariant checks: Evidence must match executed command and resulting guard behavior.
- Contract boundary coverage: Document only this work item’s implemented scope and validation outcome.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`

Required ownership note: Non-compacted `docs/03-logs/*` updates are owned by reporter/orchestrator; patcher will not edit non-compacted `docs/03-logs` files. Role-scoped execution-record updates and reporter rerun handoff remain outside patcher file edits in this plan.

Work Item ID: WI-20260211-01

### WI-20260211-02 - 2026-02-11

Updated `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md` for `WI-20260211-02` with:

- `#### Allowed Tests` populated with exact commands only:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`
- `#### Plan` replaced with the required **Plan Contract v1** structure.
- Anti-hardcode coverage explicitly included in each step:
  - fixture coverage (`>=2 fixtures per critical path`)
  - deterministic seed strategy
  - invariant checks
  - contract boundary coverage
- Required explicit handoff note added:
  - non-compacted `docs/03-logs/*` updates are reporter/orchestrator-owned; patcher will not edit them.
- `#### Docs Updated` adjusted to remove non-compacted `docs/03-logs/*` from planned patcher edits.
- `Systematic review` command log filled with executed commands and outcomes.

I could not complete the requested final commit due sandbox/gitdir permission limits in this environment:
`fatal: Unable to create '/Users/alexandrepezzotta/repos/PezzosCode/.git/worktrees/PezzosCode-17-resume-in-progress-tickets-patcher/index.lock': Operation not permitted`

Current state: modified file is unstaged in working tree (`M docs/02-features/17-resume-in-progress-tickets/dev-tasks.md`).

### WI-20260211-02 - 2026-02-11

Step Planner revise after Plan Reviewer BLOCK at attempt 1.

Decision: Block Reasons: - Plan violates orchestrator scope policy. Required changes: - forbidden path in plan: docs/02-features/17-resume-in-progress-tickets/dev-tasks.md Optional suggestions: - Keep plan files limited to implementation targets; role/global logs are automation-owned.

### WI-20260211-02 - 2026-02-11

Decision: REVISE_PLAN
Rationale: One required Allowed Tests command is failing (`python3 -m unittest tests.test_docs_logs`), so the plan must add explicit remediation to restore full green status before review.
Revised Plan:
Plan Contract v1
Approach:

1. Reproduce and isolate the `tests.test_docs_logs` failure path tied to WI-20260211-02 and identify the exact docs/log contract mismatch causing exit code 1.
   Files to change:

- tests/test_docs_logs.py
- docs/03-logs/compacted/WI-20260211-02-patcher-evidence.md
  Risks:
- Fixing assertions too narrowly could hide a real logging contract regression.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Validate at least one passing and one failing docs/log layout fixture for compacted evidence expectations.
- Deterministic seed strategy: Use static file names/content and fixed temporary directory structure.
- Invariant checks: The same docs tree input must always produce the same pass/fail verdict.
- Contract boundary coverage: Verify boundaries between compacted evidence location rules and WI-scoped evidence content checks.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

2. Patch resume-routing/guardrail implementation and/or test expectations so contradictory in-progress artifacts still fail closed while remaining compliant with docs/log validation rules.
   Files to change:

- tools/pc-feature
- tests/test_pc_feature.py
- tests/test_docs_logs.py
  Risks:
- Behavioral guardrail changes could unintentionally alter valid resume flows.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Keep complete, incomplete, contradictory, and non-resume fixtures with at least two fixtures for each critical path.
- Deterministic seed strategy: Use fixed artifacts and stable temp-path construction; no time/random-dependent logic.
- Invariant checks: Identical artifacts plus mode must always yield identical route and block/continue outcomes.
- Contract boundary coverage: Enforce the same consistency gate for inferred and explicit resume modes while preserving docs/log contract compliance.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

3. Re-run all Allowed Tests, record compacted WI evidence with exact commands and outcomes, and keep patcher edits scoped away from non-compacted docs logs.
   Files to change:

- docs/03-logs/compacted/WI-20260211-02-patcher-evidence.md
  Risks:
- Incomplete or inaccurate evidence can block reporter/orchestrator handoff.
  Tests (anti-hardcode coverage required):
- Fixture coverage: N/A for evidence update; reference executed fixtures from steps 1-2.
- Deterministic seed strategy: Record exact command lines and deterministic outcomes only.
- Invariant checks: Evidence must match executed commands/results verbatim.
- Contract boundary coverage: Limit patcher evidence updates to compacted WI output only.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

Required ownership note: Non-compacted `docs/03-logs/*` updates are owned by reporter/orchestrator, and patcher will not edit non-compacted `docs/03-logs` files.

Work Item ID: WI-20260211-02

### WI-20260211-02 - 2026-02-11

Decision: REVISE_PLAN
Rationale: One allowed test command still exits non-zero, so the plan must tighten failure isolation and acceptance criteria to guarantee both allowed tests pass before handoff.
Revised Plan:
Plan Contract v1
Approach:

1. Reproduce the failing `tests.test_docs_logs` case from WI-20260211-02, inspect the docs/log validation expectation that is failing, and isolate the minimal contract mismatch causing exit code 1.
   Files to change:

- tests/test_docs_logs.py
- docs/03-logs/compacted/WI-20260211-02-patcher-evidence.md
  Risks:
- Misidentifying the failing assertion source could mask a real docs/log policy regression.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Add/verify at least one valid and one invalid fixture layout for compacted WI evidence placement/content rules.
- Deterministic seed strategy: Use fixed fixture names, fixed content, and stable temp-directory structure with no clock/random input.
- Invariant checks: The same fixture tree must always produce the same pass/fail result.
- Contract boundary coverage: Separate checks for evidence path constraints vs evidence content requirements.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

2. Patch the docs/log validator and/or related resume guardrail expectations so contradictory or invalid artifacts still fail closed, while valid WI compacted evidence passes `tests.test_docs_logs`.
   Files to change:

- tools/pc-feature
- tests/test_pc_feature.py
- tests/test_docs_logs.py
  Risks:
- Guardrail adjustments may unintentionally change accepted resume-routing behavior.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Preserve complete, incomplete, contradictory, and non-resume cases with at least two fixtures for each critical branch.
- Deterministic seed strategy: Keep artifact inputs and temp-path creation static; avoid nondeterministic ordering/time dependence.
- Invariant checks: Identical artifacts plus mode must always yield identical route and block/continue decisions.
- Contract boundary coverage: Enforce equal consistency checks for inferred and explicit resume modes while maintaining docs/log contract compliance.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

3. Execute all Allowed Tests until both exit 0, then update compacted WI evidence with exact commands and outcomes to reflect final passing state.
   Files to change:

- docs/03-logs/compacted/WI-20260211-02-patcher-evidence.md
  Risks:
- Evidence drift from actual executed commands/results can block downstream review.
  Tests (anti-hardcode coverage required):
- Fixture coverage: N/A for evidence update; reference fixture coverage completed in steps 1-2.
- Deterministic seed strategy: Record exact command lines and final deterministic exit statuses only.
- Invariant checks: Evidence entries must match executed commands/results exactly.
- Contract boundary coverage: Restrict patcher docs edits to compacted WI evidence only.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

Required ownership note: Non-compacted `docs/03-logs/*` updates are owned by reporter/orchestrator, and patcher will not edit non-compacted `docs/03-logs` files.

Work Item ID: WI-20260211-02

### WI-20260211-02 - 2026-02-11

Decision: REVISE_PLAN
Rationale: One required Allowed Test command (`python3 -m unittest tests.test_docs_logs`) still exits 1, so the current plan is not sufficient to reach a passing gate.
Revised Plan:
Plan Contract v1
Approach:

1. Reproduce and isolate the `tests.test_docs_logs` failure by running only the Allowed Test command, then identify the exact failing assertion and the contract rule it enforces.
   Files to change:

- `tests/test_docs_logs.py`
- `tools/pc-feature`
  Risks:
- Fixing only the symptom could leave the docs/log contract inconsistent with resume guardrails.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Add/verify at least one passing and one failing fixture for compacted WI evidence contract checks.
- Deterministic seed strategy: Use fixed fixture names/content and stable temp paths only; no clock/random input.
- Invariant checks: The same fixture inputs must always produce identical pass/fail outcomes.
- Contract boundary coverage: Validate path-placement rules independently from content-schema rules.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

2. Patch contract enforcement so invalid or contradictory artifacts fail closed while valid compacted WI evidence passes, without regressing resume-routing behavior.
   Files to change:

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `tests/test_docs_logs.py`
  Risks:
- Guardrail changes may accidentally alter explicit vs inferred resume decisions.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Keep complete, incomplete, contradictory, and non-resume branches covered with at least two fixtures for each critical branch.
- Deterministic seed strategy: Keep all artifact inputs static and ordering deterministic.
- Invariant checks: Identical artifacts and mode must always yield the same route/block decision.
- Contract boundary coverage: Enforce parity between inferred and explicit resume consistency checks while preserving docs/log validation constraints.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

3. Run all Allowed Tests until both exit 0, then update compacted WI evidence with exact executed commands and final results.
   Files to change:

- `docs/03-logs/compacted/WI-20260211-02-patcher-evidence.md`
  Risks:
- Evidence can drift from actual execution if not updated from final command outputs only.
  Tests (anti-hardcode coverage required):
- Fixture coverage: N/A for evidence update; reference fixture coverage completed in steps 1-2.
- Deterministic seed strategy: Record exact command strings and deterministic exit codes only.
- Invariant checks: Evidence entries must exactly match executed commands/results.
- Contract boundary coverage: Limit patcher docs edits to compacted outputs only.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

Required ownership note: Non-compacted `docs/03-logs/*` updates are owned by reporter/orchestrator, and patcher will not edit non-compacted `docs/03-logs` files.

Work Item ID: WI-20260211-02

### WI-20260212-03 - 2026-02-12

I updated the planner content for `WI-20260212-03` in `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md`:

- Filled `#### Allowed Tests` with exact commands.
- Replaced `#### Plan` placeholder with a full `Plan Contract v1` body.
- Ensured all in-plan test commands are verbatim from Allowed Tests.
- Added explicit anti-hardcode coverage (fixtures, deterministic seed strategy, invariants, contract boundaries).
- Added the required ownership handoff note that non-compacted `docs/03-logs/*` is reporter/orchestrator-owned.
- Updated `Systematic review` with executed command evidence.

I have not committed yet because I detected an unexpected untracked path in the worktree:

- `logs/WI-20260212-03/`

Per repo instructions, I need your direction before proceeding. Should I:

1. Commit only `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md` and ignore `logs/WI-20260212-03/`, or
2. Include `logs/WI-20260212-03/` in this step?

### WI-20260212-03 - 2026-02-12

Step Planner revise after Plan Reviewer BLOCK at attempt 1.

Decision: Block Reasons: - Plan violates orchestrator scope policy. Required changes: - forbidden path in plan: docs/02-features/17-resume-in-progress-tickets/dev-tasks.md Optional suggestions: - Keep plan files limited to implementation targets; role/global logs are automation-owned.

### WI-20260212-03 - 2026-02-12

Decision: REVISE_PLAN
Rationale: Tester validation passed, but reporter found a release-readiness gap (pending execution record fields) that requires an explicit reporter/orchestrator handoff path in the plan.

Revised Plan:
Plan Contract v1
Approach:

1. Preserve and, if needed, minimally patch resume-state routing and contradiction fail-closed behavior so implementation remains aligned with tested role-transition guarantees.
   Files to change:

- `tools/pc-feature`
  Risks:
- A narrow patch could unintentionally alter non-resume paths if guard ordering is changed.
- Contradiction detection regressions could reintroduce unsafe advancement.
  Tests (anti-hardcode coverage required):
- Fixture coverage: cover planner+reviewer complete, tester failed, reporter complete, contradictory artifacts, and missing critical artifacts.
- Deterministic seed strategy: use fixed fixture trees and stable identifiers/timestamps for repeatable classification.
- Invariant checks: assert no contradictory state advances, no unsafe role skip, and policy guarantees for `auto`/`prompt`/`fresh`.
- Contract boundary coverage: verify transitions at planner->patcher->tester->reporter boundaries and blocking/error boundaries.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

2. Keep regression tests authoritative for resume policies, fail-closed contradictions, mandatory gate reruns, and non-resume flow stability.
   Files to change:

- `tests/test_pc_feature.py`
- `tests/test_docs_logs.py`
  Risks:
- Assertions may drift toward output strings instead of behavior contracts.
- Missing invalid-mix fixtures could leave contradiction edges unguarded.
  Tests (anti-hardcode coverage required):
- Fixture coverage: explicit valid/invalid artifact combinations per role state and mixed-state contradictions.
- Deterministic seed strategy: stable fixture names, deterministic environment inputs, and fixed ordering assumptions.
- Invariant checks: blocked-on-contradiction, mandatory final gates on resumed runs, and no unsafe bypass across policies.
- Contract boundary coverage: CLI-visible outcomes at artifact-presence and policy-selection boundaries.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

3. Publish compacted patcher evidence with explicit reporter/orchestrator handoff requirements for non-code execution-record completion before final reporter re-review.
   Files to change:

- `docs/03-logs/compacted/WI-20260212-03-patcher-evidence.md`
  Risks:
- Handoff ambiguity can cause repeated reporter failures despite passing code/tests.
  Tests (anti-hardcode coverage required):
- Fixture coverage: document which resume and contradiction fixtures were executed.
- Deterministic seed strategy: document stable fixture/seeding conventions used for reproducibility.
- Invariant checks: document verified fail-closed contradiction handling, mandatory gate rerun, and no unsafe step skip.
- Contract boundary coverage: document verified role-transition and blocking boundaries tied to reporter handoff readiness.
- Allowed test commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

Required note: non-compacted `docs/03-logs/*` updates are owned by reporter/orchestrator; patcher will not edit those files.

Work Item ID: WI-20260212-03

### WI-20260212-04 - 2026-02-12

Updated `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md` for `WI-20260212-04` with:

- Filled `#### Allowed Tests` using exact commands:
  - `python -m pytest tests/test_pc_feature.py::TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`
- Replaced `#### Plan` placeholder with a `Plan Contract v1` block in the exact required structure.
- Included explicit anti-hardcode coverage in every approach step:
  - fixture coverage (`>=2 fixtures per critical path`)
  - deterministic seed strategy
  - invariant checks
  - contract boundary coverage
- Ensured all concrete test commands in the plan are verbatim from Allowed Tests.
- Added explicit handoff note: non-compacted `docs/03-logs/*` updates are reporter/orchestrator-owned and patcher will not edit them.
- Added `Systematic review` command log entries in the WI preflight block.

Could not commit due sandbox restrictions on git metadata path:

- `fatal: Unable to create .../.git/worktrees/.../index.lock: Operation not permitted`

So the change is present locally but uncommitted.

### WI-20260212-04 - 2026-02-12

Step Planner revise after Plan Reviewer BLOCK at attempt 1.

Decision: Block Reasons: - Plan violates orchestrator scope policy. Required changes: - forbidden path in plan: docs/02-features/17-resume-in-progress-tickets/dev-tasks.md Optional suggestions: - Keep plan files limited to implementation targets; role/global logs are automation-owned.

### WI-20260212-04 - 2026-02-12

Decision: PLAN_STILL_VALID
Rationale: Tester validations passed and the only failure is missing role-scoped execution metadata in `dev-tasks.md`, which is a reporter/orchestrator handoff artifact rather than a patcher-plan gap.
Revised Plan:
(none)

### WI-20260212-04 - 2026-02-12

Decision: PLAN_STILL_VALID
Rationale: Tester coverage passed and the only remaining failure is reporter-owned execution-record completion in `dev-tasks.md`, which is outside the patcher plan scope.
Revised Plan:
(none)

### WI-20260212-04 - 2026-02-12

Decision: PLAN_STILL_VALID
Rationale: Tester feedback shows all planned implementation and allowed validations passed, and the reporter FAIL is limited to execution-record completion in role-scoped docs outside this plan’s patch scope.
Revised Plan:
(none)

### WI-20260212-05 - 2026-02-12

Updated `WI-20260212-05` in `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md:29` with:

- Exact `Allowed Tests` commands at `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md:71`.
- Full `Plan Contract v1` content (including required anti-hardcode coverage bullets and exact allowed test commands) at `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md:87`.
- Explicit handoff note that non-compacted `docs/03-logs/*` is reporter/orchestrator-owned and patcher will not edit those files at `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md:139`.
- Systematic review command/result entries at `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md:55`.

Systematic review commands executed and outcomes:

1. `mcp__serena__search_for_pattern` for the WI block -> found placeholders and target scope.
2. `mcp__serena__search_for_pattern` for `Allowed Tests` through `Work Item ID` -> verified final structure and required fields.

Commit status:

- Commit could not be created due sandbox permission error writing worktree git lock:
  - `fatal: Unable to create .../.git/worktrees/.../index.lock: Operation not permitted`

Also detected an unexpected untracked path: `logs/WI-20260212-05/` (not modified by me).
If you want, I can proceed with a non-committing handoff only, or adjust around that path per your direction.

### WI-20260212-05 - 2026-02-12

Step Planner revise after Plan Reviewer BLOCK at attempt 1.

Decision: Block Reasons: - Plan violates orchestrator scope policy. Required changes: - forbidden path in plan: docs/02-features/17-resume-in-progress-tickets/dev-tasks.md Optional suggestions: - Keep plan files limited to implementation targets; role/global logs are automation-owned.
