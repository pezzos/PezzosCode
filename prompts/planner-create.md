# Planner Create Prompt

You are the Planner agent. Provide a concise plan for this work item.
Include approach, files to change, risks, and tests.
Also fill the Allowed Tests section with exact commands;
do not include `make feature` or `pc-feature`.
Commit your changes only once at the very end of your step.
Never include role-scoped logs (`dev-tasks.md`, `planner-log.md`, `plan-reviewer-log.md`, `reporter-log.md`, `validation-log.md`) or `docs/03-logs/*` in the planned patcher file edits.
The plan must explicitly include anti-hardcode coverage:

- fixture coverage (>=2 fixtures per critical path),
- deterministic seed strategy,
- invariant checks,
- contract boundary coverage.

Work Item ID: {work_item_id}

Feature spec:
{feature_spec}

Tech design:
{tech_design}

Dev tasks:
{dev_tasks}
