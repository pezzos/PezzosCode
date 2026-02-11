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

### Proposal: WI-20260209-01 - Report

**Date:** 2026-02-09
**Work Item:** WI-20260209-01
**Agent:** Reporter
**Step:** Report
**Failure Summary:** tester=PASS; reporter=FAIL; tester*feedback=Outcome: PASS Tests run: `python -m unittest discover -s tests -p 'test*\_.py'`Notes: Results:`python -m unittest discover -s tests -p 'test\_\_.py'`-> 0 Discovery: no explicit discovery summary found in command output. Work Item ID: WI-20260209-01; reporter_feedback=Outcome: FAIL Docs/logs updated:`docs/02-features/15-offload-audit-and-log-compaction/reporter-log.md`File/Path:`docs/03-logs/compacted/`Check: Compacted outputs must be written to the derived location defined in the feature spec and dev tasks. Evidence:`docs/03-logs/compacted/`is missing; compacted outputs are present under`docs/02-features/WI-20260209-01/compacted`. Feature spec and dev tasks require `doc...
**Proposed Improvement:** Centralize the compaction output path in a single constant/config to avoid drift.
**Proposed Patch Location:** `tools/pc-feature` or the compaction skill implementation (path resolver)., `docs/03-logs/compacted/`
**Risks / Trade-offs:** None beyond re-running compaction.
**Status:** Proposed
**Decision Log Ref:** DEC-TBD

---

### Proposal: WI-20260209-01 - Report

**Date:** 2026-02-09
**Work Item:** WI-20260209-01
**Agent:** Reporter
**Step:** Report
**Failure Summary:** tester=PASS; reporter=FAIL; tester*feedback=Outcome: PASS Tests run: `python -m unittest discover -s tests -p 'test*\_.py'`Notes: Results:`python -m unittest discover -s tests -p 'test\_\_.py'`-> 0 Discovery: no explicit discovery summary found in command output. Work Item ID: WI-20260209-01; reporter_feedback=Outcome: FAIL Docs/logs updated:`docs/02-features/15-offload-audit-and-log-compaction/reporter-log.md`File/Path:`docs/03-logs/compacted/`Check: Compacted outputs must be written to the derived location defined in the feature spec. Evidence:`docs/03-logs/compacted/`is missing; compacted outputs are present under`docs/02-features/WI-20260209-01/compacted`. Feature spec requires `docs/03-logs/compacted/`. Expe...
**Proposed Improvement:** Proposed Patch Location:
**Proposed Patch Location:** Risks / Trade-offs:, `docs/03-logs/compacted/`**Risks / Trade-offs:** Notes: Tests not run in this step. Existing test logs show`python -m unittest discover -s tests -p 'test\__.py'`exit=0. Global logs in`docs/03-logs/_.md`not updated here due to reporter scope and post-gate guidance.`git add`failed due to`index.lock` permission (worktree git dir outside writable roots), so no commit created.
**Status:** Proposed
**Decision Log Ref:** DEC-TBD

---

### Proposal: WI-20260209-01 - Report

**Date:** 2026-02-09
**Work Item:** WI-20260209-01
**Agent:** Reporter
**Step:** Report
**Failure Summary:** tester=PASS; reporter=FAIL; tester*feedback=Outcome: PASS Tests run: `python -m unittest discover -s tests -p 'test*\_.py'`Notes: Results:`python -m unittest discover -s tests -p 'test\_\_.py'`-> 0 Discovery: no explicit discovery summary found in command output. Work Item ID: WI-20260209-01; reporter_feedback=Outcome: FAIL Docs/logs updated:`docs/02-features/15-offload-audit-and-log-compaction/reporter-log.md`File/Path:`docs/03-logs/compacted/`Check: Required compacted outputs exist for decision/implementation/validation logs. Evidence:`ls -la docs/03-logs`shows no`compacted`directory. Expected fix: Generate compacted outputs under`docs/03-logs/compacted/`and append required traceability entries in`docs/03-l...
**Proposed Improvement:** Generate compacted outputs under `docs/03-logs/compacted/` and append required traceability entries in `docs/03-logs/*`.
**Proposed Patch Location:** `docs/03-logs/compacted/`
**Risks / Trade-offs:** Reporter: Required compacted outputs exist for decision/implementation/validation logs.; `ls -la docs/03-logs` shows no `compacted` directory.
**Status:** Proposed
**Decision Log Ref:** DEC-TBD

---

<!-- Add proposals here -->
