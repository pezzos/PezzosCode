# Planner Log

## Entries

### WI-20260205-02 - 2026-02-05

Plan summary:

- Align process/testing docs and templates with anti-hardcode requirements.
- Harden `tools/pc-feature` Allowed Tests handling (smoke-only, no `make ci`).
- Restore `tools/pc-ticket` stub for bootstrap regression coverage.
- Run targeted pytest suites and update logs.

Allowed Tests:

- `pytest tests/test_pc_feature.py`
- `pytest tests/test_docs_logs.py tests/test_orchestrator_workflow_docs.py tests_extra/test_bootstrap_into_extra.py`
