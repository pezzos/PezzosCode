# Validation Log

## Entries

### WI-20260212-01 - 2026-02-12

Outcome: FAIL
Tests run: (none)
Notes: Invalid Allowed Tests after planner remediation attempts (missing targets: tests.test_pc_feature.TestPcFeature). Allowed Tests must contain only specific, existing unittest/pytest commands. Do not include `make ci`, `make feature`, `pc-feature`, or placeholders.
File/Path: docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md
Check: Allowed Tests must list existing scoped unittest/pytest commands.
Evidence: missing targets: tests.test_pc_feature.TestPcFeature
Expected fix: Allowed Tests must contain only specific, existing unittest/pytest commands. Do not include `make ci`, `make feature`, `pc-feature`, or placeholders.
Work Item ID: WI-20260212-01
