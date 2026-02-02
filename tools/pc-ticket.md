# Execute Ticket: `tools/pc-ticket`

Purpose: run the full Ticket Execution Protocol for a single ticket in a single repo/branch.
This is designed for one human, one branch, one ticket at a time. Prefer simple and robust
over flexible.

## Command

```
tools/pc-ticket F=<feature-id> T=<ticket-id> [--config path] [--manual]
```

Examples:

```
tools/pc-ticket F=01 T=101
tools/pc-ticket T=101
tools/pc-ticket F=01 T=101 --manual
```

Ticket ID formats accepted: numeric task ids only (e.g., `101`).
Manual mode: `--manual` stops after Preflight and does not run TDD or implementation.
Default behavior is autonomous TDD + implementation.

## What it does (fixed workflow)

1. **Ticket bootstrap**
   - Runs `tools/ticket-bootstrap T=<id> [F=<feature-id>]`.
   - Fails fast if this command fails.
2. **Preflight**
   - Writes the Preflight Report into the worklog using the required format.
3. **Risk classification**
   - Applies deterministic rules from `docs/04-process/ticket-execution-protocol.md`.
   - If HIGH, sets status to "Awaiting PO Approval", shows the Preflight report, and stops.
4. **TDD (tests first)**
   - Invokes Codex to add tests only.
   - Runs configured tests and records pass/fail in the worklog.
5. **Implementation**
   - Invokes Codex to implement minimal changes to pass tests.
6. **Secondary review**
   - Blocks if the diff violates scope or contains obvious regressions.
7. **CI gate**
   - Runs configured CI command and records results.

## Idempotency rules (required)

The tool must be safe to re-run. It must not corrupt state or mark failures as success.

- **Worklog updates are replace-in-place**: sections are replaced, not appended.
- **Status updates are deterministic**: on HIGH risk, status is set to Awaiting PO Approval.
- **Command status reporting is truthful**: a step is marked ok only if its command succeeded.
- **Reruns are allowed**: re-running should overwrite the same worklog sections with the latest results and re-run tests/CI instead of duplicating entries.
- **No hidden side effects**: do not create extra tickets, docs, or duplicate feature folders.

## Config (defaults)

Uses `tools/pc-ticket-config.json` unless `--config` is provided.

```
{
  "test_cmd": "make test",
  "ci_cmd": "make ci",
  "tdd_require_fail": false
}
```

## Failure policy

- **Fail fast** on any failed shell command required for the workflow.
- **Stop on HIGH risk** after Preflight until PO approval is granted.
- **Block on secondary review** if the review says BLOCK.
- **TDD exception**: the first test run may fail by design; only error if `tdd_require_fail` is true and tests pass.

## Human usage contract (simple)

- One ticket at a time.
- One branch at a time.
- If something fails, fix the underlying issue and re-run the same command.
