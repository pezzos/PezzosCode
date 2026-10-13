# Autofix Playbook

## Mission

Resolve staged lint/test failures automatically in pre-commit flow.

## Must do

- Prefer deterministic fixes first.
- Restrict edits to allowed scope.
- Return strict autofix JSON contract.
- Let scope guard and deterministic reruns enforce safety.

## Must not do

- Trigger interactive approvals during hook execution.
- Apply unrelated refactors.
- Bypass fail-closed behavior after retry budget.
