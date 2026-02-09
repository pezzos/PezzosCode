# Planner Log

## Entries

### WI-20260209-01 - 2026-02-09

Plan Contract v1
Approach:

1. Confirm proposal trigger/dedup rules and missing-context fallback in spec/test plan wording, keeping process docs aligned.
2. Implement post-run proposal generation + dedup in `tools/pc-feature` and update proposal registry template/example if needed.
3. Add unit/integration-style tests for fail/stall creation, dedup skip/merge, and success-path no-op.

Files to change:

- tools/pc-feature
- docs/possible-improvements.md
- tests/test_learning_loop_proposals.py
- docs/04-process/dev-workflow.md
- docs/04-process/human-orchestration-workflow.md
- docs/02-features/14-learning-loop-improvement-proposals/feature-spec.md
- docs/02-features/14-learning-loop-improvement-proposals/tech-design.md
- docs/02-features/14-learning-loop-improvement-proposals/test-plan.md

Risks:

- Incorrect dedup signature normalization causing either missed merges or over-merging.
- Missing execution context leading to malformed proposals or crashes.

Tests (anti-hardcode coverage required):

- Fixture coverage: At least 2 fixtures per critical path (fail/stall with full context; fail/stall with missing context) plus success-path fixture; ensure dedup path has ≥2 variants.
- Deterministic seed strategy: Use fixed seed for any randomized normalization or ID generation in tests (e.g., `random.seed(0)` or deterministic time/ID stubs).
- Invariant checks: Verify status remains `Proposed`, no proposals on success, and dedup never creates duplicate entries for same signature.
- Contract boundary coverage: Validate inputs from `tools/pc-feature` outcome payloads into proposal writer (missing fields, multiple agents) and ensure writer outputs valid template fields.

- Allowed test commands:
  - `python -m unittest discover -s tests -p "test_*.py"`

Work Item ID: WI-20260209-01

### WI-20260209-01 - 2026-02-09

Updated Allowed Tests to satisfy existence and scope checks.

### WI-20260209-01 - 2026-02-09

Step Planner revise after Plan Reviewer BLOCK at attempt 1.

Decision: Block Reasons: - Plan violates orchestrator scope policy. Required changes: - forbidden command in plan: tools/pc-feature - forbidden command in plan: pc-feature Optional suggestions: - Keep plan files limited to implementation targets; role/global logs are automation-owned.

### WI-20260209-01 - 2026-02-09

Step Planner revise after Plan Reviewer BLOCK at attempt 1.

Decision: Block Reasons: - Tests section specifies `python -m unittest discover -s tests -p "test_*.py"` which is not in the Allowed Tests list (only `pytest ...`). This makes the plan non-compliant with the current test gate. Required changes: - Update the Tests section to use only the allowed pytest commands, or explicitly note that tests will be skipped pending updated allowed commands. Optional suggestions: -...

### WI-20260209-01 - 2026-02-09

Step Planner revise after Plan Reviewer BLOCK at attempt 1.

Decision: Block Reasons: - Tests section lists commands that are not in the Allowed Tests list for this work item, so the plan is not executable under the current gate. Required changes: - Update the plan’s Tests section to use only the allowed commands (`pytest tests/test_pc_feature.py` and/or `pytest tests/test_docs_logs.py tests/test_orchestrator_workflow_docs.py tests_extra/test_bootstrap_into_extra.py`) or ex...

### WI-20260209-01 - 2026-02-09

Step Planner revise after Plan Reviewer BLOCK at attempt 1.

Decision: Block Reasons: - The plan’s Tests section requires `pytest tests/test_learning_loop_proposals.py`, which is not in the Allowed Tests list for this work item. Required changes: - Update the Tests section to only include the allowed commands, or move new tests into a file covered by the allowed commands and update the plan accordingly. Optional suggestions: - If you intend to add a new test file, align its...

### WI-20260209-01 - 2026-02-09

Decision: REVISE_PLAN
Rationale: Reporter found missing integration hook and incorrect multi-agent merge behavior, so implementation steps and tests must be updated.

Revised Plan:
Plan Contract v1
Approach:

1. Integrate proposal generation on fail/stall outcomes by adding a post-run hook that builds a proposal from the outcome payload and calls the updater.
   Files to change:

- tools/pc-feature
- lib/pc_runner.py
  Risks:
- Hook may run in unintended contexts and create duplicate proposals if outcome filtering is wrong.
- Missing or partial outcome fields could cause malformed proposal entries.

2. Fix proposal merge to aggregate distinct agent names per signature while preserving `Proposed` status and existing fields.
   Files to change:

- lib/pc_runner.py
  Risks:
- Agent aggregation could over-merge if signatures are too broad.
- Backward compatibility with existing proposal entries could be broken.

3. Extend tests to cover new hook invocation and multi-agent aggregation semantics for same signature and no-op on success.
   Files to change:

- tests/test_pc_feature.py
  Risks:
- Tests may not cover missing-context boundaries introduced by hook integration.

Tests (anti-hardcode coverage required):

- Fixture coverage: At least 2 fixtures per critical path (fail/stall with full context; fail/stall with missing context) plus success-path fixture; ensure dedup path has at least 2 variants.
- Deterministic seed strategy: Use fixed seed for any randomized normalization or ID generation in tests (e.g., `random.seed(0)` or deterministic time/ID stubs).
- Invariant checks: Verify status remains `Proposed`, no proposals on success, and dedup never creates duplicate entries for same signature while aggregating agents.
- Contract boundary coverage: Validate inputs from post-run outcome payloads into the proposal writer (missing fields, multiple agents) and ensure writer outputs valid template fields.
- Allowed test commands:
  - `pytest tests/test_pc_feature.py`
  - `pytest tests/test_docs_logs.py tests/test_orchestrator_workflow_docs.py tests_extra/test_bootstrap_into_extra.py`

Work Item ID: WI-20260209-01

### WI-20260209-01 - 2026-02-09

Step Planner revise after Plan Reviewer BLOCK at attempt 2.

Decision: Block Reasons: - Plan violates orchestrator scope policy. Required changes: - forbidden command in plan: tools/pc-feature - forbidden command in plan: pc-feature Optional suggestions: - Keep plan files limited to implementation targets; role/global logs are automation-owned.
