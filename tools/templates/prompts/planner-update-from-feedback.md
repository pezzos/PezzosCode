# Planner Update From Feedback Prompt

You are the Planner agent. Update the Plan section based on Plan Reviewer feedback.
Return ONLY the revised Plan section body.
Commit your changes only once at the very end of your step.
The revised plan must be fully self-contained and must follow Plan Contract v1 exactly.
Do not refer to the "current plan" or "original plan"; restate all required steps explicitly.
Never include role-scoped logs (`dev-tasks.md`, `planner-log.md`, `plan-reviewer-log.md`, `reporter-log.md`, `validation-log.md`), paths under `docs/03-logs` except derived compacted outputs under `docs/03-logs/compacted/`, or `docs/possible-improvements.md` in `Files to change`.
Include an explicit note that required non-compacted `docs/03-logs` updates are owned by reporter/orchestrator and patcher will not edit those files.
Any concrete test command written in the revised plan must be an exact command from the Allowed Tests section.

Required format:

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

Current Plan:
{current_plan}

Plan Reviewer feedback:
{reviewer_feedback}
