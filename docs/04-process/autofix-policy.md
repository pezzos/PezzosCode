# Autofix Policy

## Objective

Maximize autonomous recovery in pre-commit while keeping changes safe and scoped.

## Execution order

1. Run deterministic format/lint/test checks on staged scope.
2. Restage and rerun if deterministic tools changed files.
3. If still failing, run Codex autofix on allowed scope.
4. Run `tools/scope-guard` to block unauthorized edits.
5. Restage allowed files and rerun deterministic checks.
6. Retry fallback once if needed.
7. If still failing, fail closed with actionable output.

## Intervention policy

- No manual approval checkpoint inside pre-commit autofix flow.
- Human intervention only when retry budget is exhausted or policy is violated.

## Scope policy

- Allowed scope starts from staged files.
- Related tests may be added by deterministic mapping.
- Out-of-scope modifications are rejected.
