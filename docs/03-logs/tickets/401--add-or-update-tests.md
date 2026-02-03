# Ticket Worklog: 401 - "Add or update tests"

## Preflight Report

Ticket ID: T-401
PRD reference / feature mapping: 01
Risk level: LOW (triggers: none)
Scope summary (in/out): In: Add/update regression tests for the bootstrap templates feature to cover the primary path (root template copies, marker idempotence, and CLI gate/log reporting) and refresh the ticket/log documentation tied to TASK-401. | Out: Any unrelated feature work or production code changes not explicitly called out in the dev-tasks.md/test-plan for TASK-401.
Non-goals reminder: No new features beyond the described tests, and no changes that would touch unrelated docs or codebases.
Files to change: tests/test_bootstrap_into.py, docs/03-logs/implementation-log.md, docs/03-logs/validation-log.md, docs/03-logs/tickets/401--add-or-update-tests.md, docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md
Change budget: max_files: 10, max_new_modules: 2
TDD plan: tests to write first: test_bootstrap_into_copies_root_templates_and_skills, test_bootstrap_into_logs_marker_output_consistently
Doc updates planned: docs/03-logs/implementation-log.md, docs/03-logs/validation-log.md, docs/03-logs/tickets/401--add-or-update-tests.md, docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md
Systematic review: tools/ticket-bootstrap T=401 F=01 --auto: ok

## TDD Plan

- Tests to write first:
  - test_bootstrap_into_copies_root_templates_and_skills
  - test_bootstrap_into_logs_marker_output_consistently

## Files to Change + Change Budget

- Files:
  - tests/test_bootstrap_into.py
  - docs/03-logs/implementation-log.md
  - docs/03-logs/validation-log.md
  - docs/03-logs/tickets/401--add-or-update-tests.md
  - docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md
- Change budget: max_files: 10, max_new_modules: 2

## Docs Updated

- [ ] Implementation log
- [ ] Decision log (if needed)
- [ ] Bug log (if needed)
- [ ] Validation log (if needed)
- [ ] Feature docs
- [ ] PRD (if needed)
- [ ] Other: docs/03-logs/implementation-log.md
- [ ] Other: docs/03-logs/validation-log.md
- [ ] Other: docs/03-logs/tickets/401--add-or-update-tests.md
- [ ] Other: docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md

## Implementation Notes

- Added `test_bootstrap_into_copies_root_templates_and_skills` to assert the bootstrap CLI copies `AGENTS.md`, `pp.yml`, and `.codex/skills/context-to-product/SKILL.md`, preserves their canonical signatures, and appends a single bootstrap marker before the CLI output lists each file.
- Added `test_bootstrap_into_logs_marker_output_consistently` to lock down the gate logs so each document keeps one bootstrap marker and the `Updated:` output mentions every log exactly once, matching the feature spec’s log/output story.

## Tests Run

- `tools/offload-proxy/pp python -m unittest tests/test_bootstrap_into.py` _(fails: ModuleNotFoundError because `tests` is not a package; reran with discover)_
- `tools/offload-proxy/pp python -m unittest discover -s tests` (PASS)
- `tools/offload-proxy/pp make ci` (PASS)

## Gates

- make ci: PASS

## Autofix Attempts

- tests (make test) attempt 0: PASS
- ci (make ci) attempt 0: FAIL
- ci (make ci) attempt 1: PASS

## Tester Feedback

- Added regression coverage for the bootstrap root/template flow and the gate log markers, tests + CI pass; no follow-up issues observed.

### 2026-02-03 - Add regression guards for root templates and log markers

**Notes:**

- Added `test_bootstrap_into_copies_root_templates_and_skills` so the CLI’s primary flow copies `AGENTS.md`, `pp.yml`, and `.codex/skills/context-to-product/SKILL.md`, keeps their canonical signatures intact, and appends exactly one bootstrap marker before the output lists each file.
- Added `test_bootstrap_into_logs_marker_output_consistently` to keep the gate logs stable: each log retains one bootstrap marker and the `Updated:` output mentions every log exactly once.
- No production code edits were required; the tests document the feature-spec expectations for the CLI docs/log story.

**Testing:**

- `tools/offload-proxy/pp python -m unittest discover -s tests` (PASS)

## Reviewer Feedback

- TBD

## Commit

- Commit message: docs(tickets): refresh 401 regression test plan

## Final Report

What changed (files):
docs/03-logs/tickets/401--add-or-update-tests.md
Tests written (names) + results:
test_bootstrap_into_copies_root_templates_and_skills, test_bootstrap_into_logs_marker_output_consistently | make test: PASS, make ci: PASS
Docs/logs updated checklist:
docs/03-logs/implementation-log.md, docs/03-logs/validation-log.md, docs/03-logs/tickets/401--add-or-update-tests.md, docs/02-features/01-bootstrap-templates-into-a-repo/TASK-401.md
make ci results:
PASS
Autofix resolved:

- ci: check for added large files..............................................Passed
  Commit message:
  docs(tickets): refresh 401 regression test plan

## Notes

- Resume: existing worklog detected. Preflight=run, TDD plan=skip, commit=skip.
- Resume: TDD plan already filled; skipping test generation step.
- Resume: commit already recorded; skipping commit step.
