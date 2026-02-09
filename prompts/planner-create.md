# Planner Create Prompt

You are the Planner agent. Provide a concise plan for this work item.
Use the Plan Contract v1 format exactly so downstream checks are deterministic.
Also fill the Allowed Tests section with exact commands;
do not include `make feature` or `pc-feature`.
Commit your changes only once at the very end of your step.
Never include role-scoped logs (`dev-tasks.md`, `planner-log.md`, `plan-reviewer-log.md`, `reporter-log.md`, `validation-log.md`) or `docs/03-logs/*` in the planned patcher file edits.
Include an explicit handoff note in the plan stating that any required `docs/03-logs/*` updates are owned by reporter/orchestrator and that patcher will not edit those files.
Any concrete test command written in the plan must be an exact command from the Allowed Tests section (verbatim, command-for-command).
The plan must explicitly include anti-hardcode coverage:

- fixture coverage (>=2 fixtures per critical path),
- deterministic seed strategy,
- invariant checks,
- contract boundary coverage.

Return this exact structure in the Plan section body:

Plan Contract v1
Approach:

1. ...
   Files to change:

- ...
  Risks:
- ...
  Tests (anti-hardcode coverage required):
- Fixture coverage: ...
- Deterministic seed strategy: ...
- Invariant checks: ...
- Contract boundary coverage: ...
- Allowed test commands:
  - ...

Work Item ID: {work_item_id}

Feature spec:
{feature_spec}

Tech design:
{tech_design}

Dev tasks:
{dev_tasks}
