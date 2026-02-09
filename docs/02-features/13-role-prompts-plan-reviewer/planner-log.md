# Planner Log

## Entries

### WI-20260209-01 - 2026-02-09

Plan Contract v1
Approach:

1. Audit prompt inventory and template parity, then map required prompt paths used by `tools/pc-feature` to existing files.
   Files to change:

- `prompts/`
- `tools/templates/prompts/`
- `tools/pc-feature`
  Risks:
- Missing prompt variants could break `pc-feature` at runtime.
- Prompt/template drift can reintroduce inconsistent role behavior.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Create at least 2 fixtures per critical path (prompt-load success, missing prompt fail, reviewer approve, reviewer block/retry, reviewer conflict) with distinct prompt sets.
- Deterministic seed strategy: Use fixed seed(s) for any randomized fixture inputs or ordering to keep test outputs stable.
- Invariant checks: Assert prompt path resolution invariant (root + template parity) and invariant error messaging for missing prompts.
- Contract boundary coverage: Validate file-based prompt loading boundaries and explicit remediation text for missing task-specific prompts.
- Allowed test commands:
  - `python -m unittest discover -s tests -p "test_*.py"`

2. Align prompt contracts and loader logic with current workflow, ensuring file-based loading and explicit failure guidance.
   Files to change:

- `tools/pc-feature`
- `prompts/`
- `tools/templates/prompts/`
  Risks:
- Over-tightening reviewer wording could deadlock high-risk flows.
- Loader changes could break existing task-specific prompt selection.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Two fixtures for each prompt-loading path (base role and task-specific variant).
- Deterministic seed strategy: Fixed seeds for any generated prompt IDs or ordering.
- Invariant checks: Assert loader always uses `load_prompt_template()`/fallback, never embedded prompt bodies.
- Contract boundary coverage: Ensure missing prompt file throws actionable, user-facing remediation.
- Allowed test commands:
  - `python -m unittest discover -s tests -p "test_*.py"`

3. Add/refresh plan-reviewer gate tests for approve, block/retry, and conflict paths.
   Files to change:

- `tests/test_pc_feature.py`
  Risks:
- Tests could encode outdated gate policy and force incorrect behavior.
  Tests (anti-hardcode coverage required):
- Fixture coverage: Two fixtures per gate outcome with different risk states.
- Deterministic seed strategy: Fixed seeds for gate decision inputs.
- Invariant checks: Assert gate outcome matches risk policy inputs and allowed-tests constraints.
- Contract boundary coverage: Verify explicit failure guidance and next-step instructions on conflict.
- Allowed test commands:
  - `python -m unittest discover -s tests -p "test_*.py"`

4. Sync process docs with prompt/gate semantics and finalize.
   Files to change:

- `docs/04-process/ticket-execution-protocol.md`
- `docs/04-process/dev-workflow.md`
- `docs/04-process/human-orchestration-workflow.md`
  Risks:
- Process docs could diverge from live behavior, causing execution drift.
  Tests (anti-hardcode coverage required):
- Fixture coverage: N/A (docs change).
- Deterministic seed strategy: N/A.
- Invariant checks: Ensure docs reference canonical prompt paths and reviewer gate semantics.
- Contract boundary coverage: Ensure docs specify missing-prompt remediation and allowed-tests behavior.
- Allowed test commands:
  - `python -m unittest discover -s tests -p "test_*.py"`

Work Item ID: WI-20260209-01
