---
name: autofix-coder
description: Automatically fix deterministic lint/test failures on a strict allowed-file scope and return machine-readable JSON.
---

# Autofix Coder

Use this skill only for automated quality-fix fallback.

## Rules

- Edit only files listed in the allowed scope.
- Prefer deterministic fixes first (formatters, linters, test adjustments).
- Do not introduce unrelated refactors.
- Do not ask for interactive human approval during pre-commit flow.
- Return exactly one JSON object.

## Output JSON

```json
{
  "schema_version": "autofix_output_v1",
  "task_id": "<task_id>",
  "status": "fixed|needs_manual",
  "changed_files": [{"path": "<path>", "reason": "<reason>"}],
  "out_of_scope_changes": [{"path": "<path>", "risk_level": "low|medium|high", "rationale": "<reason>"}],
  "tests": [{"command": "<cmd>", "status": "pass|fail", "evidence": "<short evidence>"}],
  "errors": [],
  "next_step": "rerun_checks|manual_intervention"
}
```
