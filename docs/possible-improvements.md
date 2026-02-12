# Possible Improvements

> **Human-gated proposals generated after failures or friction**
>
> Each entry is a proposal only. Do not auto-apply patches.
>
> `docs/possible-improvements.md` is orchestrator-owned. Roles should propose
> improvements in their feedback fields (`Expected fix`, `Proposed Improvement`,
> `Proposed Patch Location`, `Risks / Trade-offs`); the orchestrator collects,
> clarifies, and deduplicates entries before writing this file.

---

## Entry Template

Use `---` to separate entries; status stays `Proposed` until a human decision.

### Proposal: WI-... - <Step>

**Date:** YYYY-MM-DD
**Work Item:** WI-...
**Agent:** ...
**Step:** ...
**Failure Summary:** ...
**Proposed Improvement:** ...
**Proposed Patch Location:** ...
**Risks / Trade-offs:** ...
**Status:** Proposed | Approved | Rejected
**Decision Log Ref:** DEC-...

---

## Entries

### Proposal: WI-20260212-01 - Report

**Date:** 2026-02-12
**Work Item:** WI-20260212-01
**Agent:** Reporter
**Step:** Report
**Failure Summary:** tester=PASS; reporter=FAIL; tester_feedback=Outcome: PASS Tests run: `python3 -m unittest tests/test_pc_feature.py`; `python3 -m unittest tests/test_docs_logs.py` Notes: Results: `python3 -m unittest tests/test_pc_feature.py` -> 0; `python3 -m unittest tests/test_docs_logs.py` -> 0 Discovery: `python3 -m unittest tests/test_docs_logs.py` => Ran 12 tests Work Item ID: WI-20260212-01; reporter_feedback=Outcome: FAIL Docs/logs updated: `docs/02-features/18-commit-gated-by-completed-ticket-docs/reporter-log.md` (updated locally; commit attempt failed due worktree git index lock permission error) File/Path: `docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md` Check: WI closure completeness for reporter stage and final execution summary fields. Evidence: WI-20260212-01 still has `#### Reporter Re...
**Proposed Improvement:** Add a pre-reporter closure checklist in `dev-tasks.md`to enforce completion of reporter/final-report fields whenever tester result is PASS.
**Proposed Patch Location:**`docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md`
**Risks / Trade-offs:** Unresolved closure placeholders can cause repeated reporter FAIL loops and blur whether remaining work is implementation or workflow bookkeeping.
**Status:** Proposed
**Decision Log Ref:** DEC-TBD

---

### Proposal: WI-20260212-01 - Report

**Date:** 2026-02-12
**Work Item:** WI-20260212-01
**Agent:** Reporter
**Step:** Report
**Failure Summary:** tester=PASS; reporter=FAIL; tester_feedback=Outcome: PASS Tests run: `python3 -m unittest tests/test_pc_feature.py`; `python3 -m unittest tests/test_docs_logs.py` Notes: Results: `python3 -m unittest tests/test_pc_feature.py` -> 0; `python3 -m unittest tests/test_docs_logs.py` -> 0 Discovery: `python3 -m unittest tests/test_docs_logs.py` => Ran 12 tests Work Item ID: WI-20260212-01; reporter_feedback=Outcome: FAIL Docs/logs updated: `docs/02-features/18-commit-gated-by-completed-ticket-docs/reporter-log.md` (updated locally; commit blocked by git index lock permission in this environment) File/Path: `docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md` Check: WI execution record completion and final-report closure consistency against current branch artifacts. Evidence: `validation-log.md` sh...
**Proposed Improvement:** Add an explicit “execution-closure checklist” block in `dev-tasks.md` template so reporter-required fields are completed before reporter reruns.
**Proposed Patch Location:** `docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md`
**Risks / Trade-offs:** Keeping unresolved placeholders while tester is PASS can cause repeated reporter FAIL loops and block finalization despite technically complete implementation/test work.
**Status:** Proposed
**Decision Log Ref:** DEC-TBD

---

### Proposal: WI-20260212-01 - Report

**Date:** 2026-02-12
**Work Item:** WI-20260212-01
**Agent:** Reporter
**Step:** Report
**Failure Summary:** tester=PASS; reporter=FAIL; tester_feedback=Outcome: PASS Tests run: `python3 -m unittest tests/test_pc_feature.py`; `python3 -m unittest tests/test_docs_logs.py` Notes: Results: `python3 -m unittest tests/test_pc_feature.py` -> 0; `python3 -m unittest tests/test_docs_logs.py` -> 0 Discovery: `python3 -m unittest tests/test_docs_logs.py` => Ran 12 tests Work Item ID: WI-20260212-01; reporter_feedback=Outcome: FAIL Docs/logs updated: `docs/02-features/18-commit-gated-by-completed-ticket-docs/reporter-log.md` File/Path: `docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md` Check: WI execution record scope/completeness consistency against current branch state and tester artifact. Evidence: Primary scope checks show in-scope WI artifacts (`git diff --stat refs/heads/main..HEAD`: `dev-tasks.md`,...
**Proposed Improvement:** Reconcile WI-20260212-01 execution fields in `docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md` to match tester evidence (set Reporter, replace stale `needs replan`/FAIL placeholders, fill `Reporter Review`, align test outcome/details with `validation-log.md`), then rerun reporter.
**Proposed Patch Location:** `docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md`
**Risks / Trade-offs:** Reporter: WI execution record scope/completeness consistency against current branch state and tester artifact.; Primary scope checks show in-scope WI artifacts (`git diff --stat refs/head...
**Status:** Proposed
**Decision Log Ref:** DEC-TBD

---

### Proposal: WI-20260212-01 - Test

**Date:** 2026-02-12
**Work Item:** WI-20260212-01
**Agent:** Tester
**Step:** Test
**Failure Summary:** tester=FAIL; reporter=SKIPPED; tester_feedback=Outcome: FAIL Tests run: (none) Notes: Invalid Allowed Tests after planner remediation attempts (missing targets: tests.test_pc_feature.TestPcFeature). Allowed Tests must contain only specific, existing unittest/pytest commands. Do not include `make ci`, `make feature`, `pc-feature`, or placeholders. File/Path: docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md Check: Allowed Tests must list ex...; reporter_feedback=Outcome: SKIPPED Docs/logs updated: reporter deferred Notes: Reporter skipped because tester failed during allowed-tests validation. Work Item ID: WI-20260212-01
**Proposed Improvement:** Allowed Tests must contain only specific, existing unittest/pytest commands. Do not include `make ci`, `make feature`, `pc-feature`, or placeholders.
**Proposed Patch Location:** docs/02-features/18-commit-gated-by-completed-ticket-docs/dev-tasks.md
**Risks / Trade-offs:** Tester: Allowed Tests must list existing scoped unittest/pytest commands.; missing targets: tests.test_pc_feature.TestPcFeature
**Status:** Proposed
**Decision Log Ref:** DEC-TBD

---

### Proposal: WI-20260212-04 - Orchestration

**Date:** 2026-02-12
**Work Item:** WI-20260212-04
**Agent:** pc-feature
**Step:** Orchestration
**Failure Summary:** Loop exhausted at MAX_LOOPS. tester=PASS; reporter=FAIL; tester_feedback=Outcome: PASS Tests run: `python -m pytest tests/test_pc_feature.py::TestPcFeature`; `python3 -m unittest tests.test_docs_logs` Notes: Results: `python -m pytest tests/test_pc_feature.py::TestPcFeature` -> 0; `python3 -m unittest tests.test_docs_logs` -> 0 Discovery: `python -m pytest tests/test_pc_feature.py::TestPcFeature` => collected 130 items; `python3 -m unittest tests.test_docs_logs` => Ran 12 tests Work It...; reporter_feedback=Outcome: FAIL Docs/logs updated: Updated `docs/02-features/17-resume-in-progress-tickets/reporter-log.md` with `### WI-20260212-04 (rerun 2) - 2026-02-12`. File/Path: `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md` Check: Work-item execution record completeness and reporter handoff readiness for `WI-20260212-04`. Evidence: Primary scope view from this run shows in-scope WI artifacts but incomplete ex...
**Proposed Improvement:** TBD - investigate failure and propose remediation.
**Proposed Patch Location:** TBD
**Risks / Trade-offs:** None noted.
**Status:** Proposed
**Decision Log Ref:** DEC-TBD

---

### Proposal: WI-20260211-03 - Orchestration

**Date:** 2026-02-11
**Work Item:** WI-20260211-03
**Agent:** pc-feature
**Step:** Orchestration
**Failure Summary:** Loop exhausted at MAX_LOOPS. tester=PASS; reporter=FAIL; tester_feedback=Outcome: PASS Tests run: `python -m pytest tests/test_pc_feature.py::TestPcFeature`; `python3 -m unittest tests.test_docs_logs` Notes: Results: `python -m pytest tests/test_pc_feature.py::TestPcFeature` -> 0; `python3 -m unittest tests.test_docs_logs` -> 0 Discovery: `python -m pytest tests/test_pc_feature.py::TestPcFeature` => collected 124 items; `python3 -m unittest tests.test_docs_logs` => Ran 12 tests Work It...; reporter_feedback=Outcome: FAIL Docs/logs updated: `docs/02-features/17-resume-in-progress-tickets/reporter-log.md` (added `### WI-20260211-03 - 2026-02-11 (rerun-2)` entry). File/Path: `docs/02-features/17-resume-in-progress-tickets/dev-tasks.md` Check: WI-20260211-03 execution record completeness and consistency with current scope. Evidence: Primary scope checks: `git status --short` shows reporter-log modified and untracked `log...
**Proposed Improvement:** TBD - investigate failure and propose remediation.
**Proposed Patch Location:** TBD
**Risks / Trade-offs:** None noted.
**Status:** Proposed
**Decision Log Ref:** DEC-TBD

---

### Proposal: WI-20260211-02 - Orchestration

**Date:** 2026-02-11
**Work Item:** WI-20260211-02
**Agent:** pc-feature
**Step:** Orchestration
**Failure Summary:** Loop exhausted at MAX_LOOPS. tester=FAIL; reporter=SKIPPED; tester_feedback=Outcome: FAIL Tests run: `python -m pytest tests/test_pc_feature.py::TestPcFeature`; `python3 -m unittest tests.test_docs_logs` Notes: Results: `python -m pytest tests/test_pc_feature.py::TestPcFeature` -> 0; `python3 -m unittest tests.test_docs_logs` -> 1 File/Path: logs/WI-20260211-02/tests.log Check: Allowed Tests commands must all exit 0. Evidence: `python3 -m unittest tests.test_docs_logs` -> 1 Expected fix:...; reporter_feedback=Outcome: SKIPPED Docs/logs updated: reporter deferred Notes: Reporter skipped because tester failed; planner must replan before review. Work Item ID: WI-20260211-02
**Proposed Improvement:** TBD - investigate failure and propose remediation.
**Proposed Patch Location:** TBD
**Risks / Trade-offs:** None noted.
**Status:** Proposed
**Decision Log Ref:** DEC-TBD

---

### Proposal: WI-20260211-02 - Test

**Date:** 2026-02-11
**Work Item:** WI-20260211-02
**Agent:** Tester
**Step:** Test
**Failure Summary:** tester=FAIL; reporter=SKIPPED; tester_feedback=Outcome: FAIL Tests run: `python -m pytest tests/test_pc_feature.py::TestPcFeature`; `python3 -m unittest tests.test_docs_logs` Notes: Results: `python -m pytest tests/test_pc_feature.py::TestPcFeature` -> 0; `python3 -m unittest tests.test_docs_logs` -> 1 File/Path: logs/WI-20260211-02/tests.log Check: Allowed Tests commands must all exit 0. Evidence: `python3 -m unittest tests.test_docs_logs` -> 1 Expected fix:...; reporter_feedback=Outcome: SKIPPED Docs/logs updated: reporter deferred Notes: Reporter skipped because tester failed; planner must replan before review. Work Item ID: WI-20260211-02
**Proposed Improvement:** adjust plan/patch until all allowed tests pass.
**Proposed Patch Location:** logs/WI-20260211-02/tests.log
**Risks / Trade-offs:** Tester: Allowed Tests commands must all exit 0.; `python3 -m unittest tests.test_docs_logs` -> 1
**Status:** Proposed
**Decision Log Ref:** DEC-TBD

---

### Proposal: WI-20260209-01 - Orchestration

**Date:** 2026-02-09
**Work Item:** WI-20260209-01
**Agent:** pc-feature
**Step:** Orchestration
**Failure Summary:** Loop exhausted at MAX*LOOPS. tester=PASS; reporter=FAIL; tester_feedback=Outcome: PASS Tests run: `python -m unittest discover -s tests -p 'test*\_.py'`Notes: Results:`python -m unittest discover -s tests -p 'test\_\_.py'`-> 0 Discovery: no explicit discovery summary found in command output. Work Item ID: WI-20260209-01; reporter_feedback=Outcome: FAIL Docs/logs updated:`docs/02-features/15-offload-audit-and-log-compaction/reporter-log.md`File/Path:`docs/03-logs/compacted/`Check: Compacted outputs must be written to the derived location defined in the feature spec and dev tasks. Evidence:`docs/03-logs/compacted/`is missing; compacted outputs are present under`docs/02-features/WI-20260209-01/compacted`. Feature spec and dev tasks require `doc...
**Proposed Improvement:** TBD - investigate failure and propose remediation.
**Proposed Patch Location:** TBD
**Risks / Trade-offs:** None noted.
**Status:** Proposed
**Decision Log Ref:** DEC-TBD

---

<!-- Add proposals here -->
