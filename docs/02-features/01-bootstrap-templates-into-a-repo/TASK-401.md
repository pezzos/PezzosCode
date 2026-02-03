---
id: 401
title: "Add or update tests"
prd_ref: "01"
status: "To Do"
status_reason: ""
complexity: "simple"
approval: "" # set to "granted" to resume HIGH risk tickets
change_budget:
  max_files: 10
  max_new_modules: 2
---

# Ticket: Add or update tests

> Simple, consistent ticket format for 1 feature folder or 1 mini change.

## Title

Add or update tests

## Type

- Feature

## Context

- Feature: Bootstrap Templates Into A Repo
- Summary: See feature-spec.md
- Task: Add or update tests
- Acceptance: Tests cover the primary path
- Estimate: 0.5 day
- Derived from dev-tasks.md

## Scope

- **Choose one:** 1 feature folder OR 1 mini change
- In scope: Complete the task as defined in dev-tasks.md
- Out of scope: Unrelated feature work

## PRD Traceability

- PRD feature/order: 01 (P0)
- Link to PRD section: Prioritized Feature List

## Success Criteria

- [ ] Tests cover the primary path
- [ ] Gates and logs updated

## Definition of Done (Ticket-Specific)

- [ ] Tests cover the primary path
- [ ] Relevant tests updated and passing
- [ ] Logs/docs updated if required by this task

## Plan (Draft)

- Add `test_bootstrap_into_copies_root_templates_and_skills` to lock down the root template copies and markers.
- Add `test_bootstrap_into_logs_marker_output_consistently` so the gate logs retain one bootstrap marker and the CLI reports each update once.
- Document the regression coverage and run `make ci` to prove the tests pass.

## Evidence Hints

- [Optional] Add 1-2 objective hints that prove completion (file + anchor).

## References

- Feature spec: feature-spec.md (Summary, Feature Requirements)
- Tech design: tech-design.md (Technical Requirements, Architecture)
- Test plan: test-plan.md (Test Strategy, Test Cases)
- Dev tasks: dev-tasks.md (Task Breakdown for TASK-401)

## Risk Classification

- Risk level: LOW
- Triggers (if HIGH): N/A

## Change Budget

- Max files: 10
- Max new modules: 2
- Max lines changed (estimate): 500

## Human Gates

- [x] Plan validated
- [ ] Diff validated
- [x] Tests validated

## Implementation Notes

- Added `test_bootstrap_into_copies_root_templates_and_skills` to ensure the CLI copies `AGENTS.md`, `pp.yml`, and `.codex/skills/context-to-product/SKILL.md` with exactly one bootstrap marker per file and reports them in the output.
- Added `test_bootstrap_into_logs_marker_output_consistently` to confirm each gate log retains one bootstrap marker and the `Updated:` output mentions every log exactly once, preventing regressions without touching production code.

## Tests Run

- Command(s):
  - `tools/offload-proxy/pp python -m unittest tests/test_bootstrap_into.py` _(fails: ModuleNotFoundError because `tests` is not a package; reran with discover)_
  - `tools/offload-proxy/pp python -m unittest discover -s tests` (PASS)
  - `tools/offload-proxy/pp make ci` (PASS)
- Result(s): All targeted tests and `make ci` pass after rerunning discover.

## Implementer Notes

- Implementation choices: Tests only; added assertions that root templates/log docs keep single bootstrap markers and CLI output mentions each file exactly once, keeping production code untouched.
- Edge cases covered: Marker idempotence when rerunning bootstrap, CLI reporting each log once, and root templates sourcing from the canonical files.
- Files changed:
  - tests/test_bootstrap_into.py
  - docs/03-logs/implementation-log.md
  - docs/03-logs/validation-log.md
  - docs/03-logs/tickets/401--add-or-update-tests.md
  - docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md

## Tester Feedback

- Tests executed: `tools/offload-proxy/pp python -m unittest discover -s tests`, `tools/offload-proxy/pp make ci`
- Failures observed: None
- Suggested fixes: None

## Reviewer Feedback

- Issues found: TBD
- Suggestions: TBD
- Approval status: TBD

## Iteration Log

- [ ] Implementer updated after tester feedback
- [ ] Implementer updated after reviewer feedback

## Logs Updated

- [x] Implementation log
- [ ] Decision log (if needed)
- [ ] Bug log (if needed)
- [x] Validation log (if needed)

## Docs Updated

- [ ] Feature docs (feature-spec/tech-design/dev-tasks/test-plan)
- [ ] PRD (if scope/priority changed)
- [x] Other: docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md

## Report (Final)

- What changed: Added regression tests for root templates/log markers and refreshed the implementation/validation/worklog entries plus this ticket doc.
- Commands run (use `pp` for noisy output): `tools/offload-proxy/pp python -m unittest discover -s tests`, `tools/offload-proxy/pp make ci`
- Results: PASS for the discover run and `make ci`

## Commit

- Message: test: cover bootstrap templates and logs
