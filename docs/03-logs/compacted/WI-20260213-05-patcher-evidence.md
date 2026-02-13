# WI-20260213-05 Patcher Evidence (Compacted)

- Date: 2026-02-13
- Work Item: WI-20260213-05
- Scope: commit gate enforcement for completed-only ticket status plus required evidence parsing boundaries.

## Commands Executed

- `python3 -m unittest tests.test_pc_feature.TestPcFeature` -> PASS.
- `python3 -m unittest tests.test_docs_logs` -> PASS.

## Commit Gate Fixtures

### Fixture: completed-allow

- Expected route: allow
- Deterministic artifact state: `Outcome: completed` plus non-empty `Test Results`, `Commit`, and `Final Report`.
- Commit evidence gate accepts completed ticket docs with required evidence.

### Fixture: non-completed-block

- Expected route: block
- Deterministic artifact state: `Outcome: pass` or `Outcome: needs replan`.
- Gate failed closed for non-completed ticket status.

### Fixture: malformed-evidence-block

- Expected route: block
- Deterministic artifact state: malformed/duplicate required heading or empty required section body.
- Commit evidence gate rejects malformed or missing required evidence.

### Fixture: snapshot-clean-allow

- Expected route: allow
- Deterministic artifact state: no tracked shell snapshot paths in `git diff --name-status refs/heads/main..HEAD`.
- Scope check passes when no tracked shell snapshot artifacts exist in `refs/heads/main..HEAD`.

### Fixture: snapshot-contaminated-block

- Expected route: block
- Deterministic artifact state: tracked-added/deleted/other shell snapshot paths under `.codex_subagent/shell_snapshots/`.
- Scope check fails closed when tracked shell snapshot artifacts are present in branch diff.

## Invariant Checks

- Commit is blocked unless normalized top-level `Outcome` is exactly `completed`.
- Commit is blocked when `Tests run` is missing/empty.
- Commit is blocked when required sections are missing, duplicated, malformed, or empty.
- Branch scope is blocked when tracked shell snapshot artifacts are present under `.codex_subagent/shell_snapshots/`.

## Contract Boundaries

- Compacted evidence is accepted only under `docs/03-logs/compacted/`.
- Required fixture markers are deterministic and validated by `tests/test_docs_logs.py`.
- Runtime shell snapshots under `.codex_subagent/shell_snapshots/` are excluded from feature scope and must be removed before reporter/commit revalidation.
- Allowed test command strings are fixed to:
  - `python3 -m unittest tests.test_pc_feature.TestPcFeature`
  - `python3 -m unittest tests.test_docs_logs`

## Ownership Note

Non-compacted `docs/03-logs/*` updates are owned by reporter/orchestrator; patcher did not edit those files.
