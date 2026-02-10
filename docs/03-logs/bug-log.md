# Bug Log

> **Bugs, fixes, regressions**
>
> A chronological record of bugs discovered, how they were fixed, and whether they recurred. This helps identify patterns, prevent regressions, and improve quality over time.

---

## Purpose

This log tracks:

- **Bugs discovered** in production, staging, or development
- **Root causes** and how they were fixed
- **Patterns** in what breaks and why
- **Regressions** when old bugs resurface

This helps with:

- Understanding what types of bugs are common
- Preventing similar bugs in the future
- Identifying areas of the codebase that need improvement
- Training new team members on common pitfalls

---

## Bug Template

### [BUG-XXX] - [Short Description]

**Date Discovered:** YYYY-MM-DD

**Discovered By:** [Name/User Report/Monitoring]

**Severity:** [Critical | High | Medium | Low]

**Status:** [Open | In Progress | Fixed | Closed | Wontfix]

**Environment:** [Production | Staging | Development]

**Affected Users:** [Number/percentage of users affected]

**Symptoms:**
[What users see or experience]

**Steps to Reproduce:**

1. [Action 1]
2. [Action 2]
3. [Result]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Root Cause:**
[Technical explanation of why the bug occurred]

**Fix:**
[How it was fixed - technical details]

**Files Changed:**

- `path/to/file1.ts`
- `path/to/file2.ts`

**Prevention:**
[How we can prevent this type of bug in the future]

- Tests added: [describe]
- Process changes: [describe]
- Monitoring added: [describe]

**Related Issues:**

- Similar to [BUG-XXX]
- Caused by [Change in implementation-log]

**Fixed By:** [Name]

**Fixed Date:** YYYY-MM-DD

**Deployed:** YYYY-MM-DD

**Verified By:** [Name]

---

## Active Bugs

### Critical (P0)

> Must fix immediately, blocking users

| Bug ID    | Description         | Age (days) | Assigned To | Status   |
| --------- | ------------------- | ---------- | ----------- | -------- |
| [BUG-XXX] | [Brief description] | [#]        | [Name]      | [Status] |

### High Priority (P1)

> Impacting significant functionality, fix ASAP

| Bug ID    | Description         | Age (days) | Assigned To | Status   |
| --------- | ------------------- | ---------- | ----------- | -------- |
| [BUG-XXX] | [Brief description] | [#]        | [Name]      | [Status] |

### Medium Priority (P2)

> Fix in next sprint

| Bug ID    | Description         | Age (days) | Assigned To | Status   |
| --------- | ------------------- | ---------- | ----------- | -------- |
| [BUG-XXX] | [Brief description] | [#]        | [Name]      | [Status] |

### Low Priority (P3)

> Fix when convenient

| Bug ID    | Description         | Age (days) | Assigned To | Status   |
| --------- | ------------------- | ---------- | ----------- | -------- |
| [BUG-XXX] | [Brief description] | [#]        | [Name]      | [Status] |

---

## Resolved Bugs

### [BUG-004] - `pc-feature` loop reads stale `dev-tasks.md` from `main`

**Date Discovered:** 2026-02-08

**Discovered By:** CLI run (`make feature F=11`)

**Severity:** High

**Status:** Fixed

**Environment:** Development

**Affected Users:** Anyone resuming/retrying a feature where worktree state diverges from `main`.

**Symptoms:**
Execution ends with `pc-feature: max iteration attempts reached; check execution log` even when tester/reporter outputs in the feature worktree indicate progress.

**Steps to Reproduce:**

1. Run `make feature F=11` with an existing patcher worktree and multiple prior loop artifacts.
2. Let planner/tester/reporter iterate.
3. Observe max-loop exhaustion with inconsistent role feedback caused by stale execution context.

**Expected Behavior:**
All runtime workflow artifacts are read/written in the active feature worktree; retry loops should use current artifacts.

**Actual Behavior:**
`dev-tasks.md` and runtime logs were sourced from `main` while roles executed in worktree, causing stale review context and loop churn.

**Root Cause:**
`pc-feature` mixed runtime paths: role execution happened in patcher worktree, but work-item execution log and runner logs were still rooted in `main`.

**Fix:**
Resolve runtime artifacts (`dev-tasks.md`, role logs, `logs/WI-*`) from the patcher worktree; add startup path scope printout and enforce actionable failure context in retry loops.

**Files Changed:**

- `tools/pc-feature`
- `prompts/reporter-review.md`
- `prompts/plan-reviewer-gate.md`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`

**Prevention:**

- Tests added: unit coverage for worktree-local runtime paths and failure-context guards.
- Process changes: ticket execution protocol now explicitly states runtime artifacts remain in worktree until final success/collection.

**Fixed By:** Codex

**Fixed Date:** 2026-02-08

### [BUG-005] - Planner/reviewer can allow forbidden patcher targets

**Date Discovered:** 2026-02-08

**Discovered By:** CLI run (`make feature F=11`) failure report

**Severity:** High

**Status:** Fixed

**Environment:** Development

**Affected Users:** Feature runs where planner output includes role-scoped/global-log edits.

**Symptoms:**
`pc-feature` aborts late with `patcher edited role-scoped files: docs/02-features/<other-feature>/dev-tasks.md`.

**Root Cause:**
Role-scope guard existed at patcher stage, but no deterministic pre-patcher policy gate blocked forbidden plan instructions when reviewer approved them.

**Fix:**
Added orchestrator-side plan-policy validation before patcher execution and expanded patcher guard to block role-scoped docs across all features.

**Files Changed:**

- `tools/pc-feature`
- `prompts/plan-reviewer-gate.md`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`

**Prevention:**

- Tests added for policy violation detection and cross-feature role-scope blocking.
- Process updated to require deterministic pre-patcher plan policy checks.

**Fixed By:** Codex

**Fixed Date:** 2026-02-08

### [BUG-006] - Reviewer read-only guard falsely blames pre-existing planner edits

**Date Discovered:** 2026-02-08

**Discovered By:** CLI run (`make feature F=12`) failure report

**Severity:** High

**Status:** Fixed

**Environment:** Development

**Affected Users:** Any resumed/retried feature run where planner/orchestrator wrote `dev-tasks.md` before reviewer execution.

**Symptoms:**
`pc-feature` aborts with `plan reviewer modified files in writable worktree: .../dev-tasks.md` when reviewer did not edit files.

**Root Cause:**
Read-only guard checked for any dirty files after reviewer step; it did not differentiate pre-existing dirt from reviewer-introduced changes.

**Fix:**
Switched reviewer guard to pre/post dirty snapshot delta checks, moved planner no-op write to post-reviewer verification, and added pre-review hygiene checkpointing for planner-owned files.

**Files Changed:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `prompts/plan-reviewer-gate.md`
- `docs/04-process/ticket-execution-protocol.md`

**Prevention:**

- Added unit/integration regression tests for unchanged pre-existing dirty paths and real reviewer dirty deltas.
- Added explicit process note that reviewer enforcement is delta-based.

**Fixed By:** Codex

**Fixed Date:** 2026-02-08

### [BUG-007] - Auto-resume path missing deterministic startup handling for existing feature worktrees

**Date Discovered:** 2026-02-08

**Discovered By:** workflow regression review (`make feature` rerun behavior)

**Severity:** High

**Status:** Fixed

**Environment:** Development

**Affected Users:** Anyone rerunning `make feature` on an existing in-progress feature worktree.

**Symptoms:**

- Resume could require manual prompt flow or fail unpredictably with dirty/stale/parallel state.
- Existing runtime state in `dev-tasks.md` could be lost or rejected without actionable startup policy.

**Root Cause:**

Resume startup relied on prompt-era heuristics and pristine assumptions, without a deterministic state model for:

- mode selection,
- dirty-scope validation,
- stale/behind-main rejection,
- cross-feature active-worktree exclusion.

**Fix:**

- Added `RESUME_MODE` (`auto|prompt|fresh`) and made `auto` deterministic default.
- Added single-active-feature startup guard across patcher worktrees.
- Added runtime vs non-runtime dirty classification and fail-fast diagnostics.
- Added auto-checkpoint commit for dirty `dev-tasks.md` when a resumable work item exists.
- Updated tests to cover resume startup policy and failure modes.

**Files Changed:**

- `tools/pc-feature`
- `tests/test_pc_feature.py`
- `docs/04-process/ticket-execution-protocol.md`

**Prevention:**

- Regression tests for startup mode parsing and resume-state classification.
- Explicit workflow docs for resume mode behavior and stale/main-freeze constraints.

**Fixed By:** Codex

**Fixed Date:** 2026-02-08

### [BUG-003] - Allowed Tests prose triggers invalid command execution

**Date Discovered:** 2026-02-05

**Discovered By:** CLI run (`make feature F=08`)

**Severity:** Medium

**Status:** Fixed

**Environment:** Development

**Affected Users:** Anyone running `make feature` when the planner returns narrative Allowed Tests.

**Symptoms:**
`tools/offload-proxy/pp` attempts to execute non-command tokens (e.g., “Totally” or backticked text), causing `FileNotFoundError`.

**Steps to Reproduce:**

1. Run `make feature F=08`.
2. Allow the planner to populate Allowed Tests with prose instead of exact commands.
3. Observe `pp` failures when executing tests.

**Root Cause:**
Allowed Tests parsing accepted any non-empty line (excluding the placeholder), so narrative text was treated as executable commands.

**Fix:**
Normalize Allowed Tests entries and accept only command-like lines; strip `tools/offload-proxy/pp` and reject backticks or unknown command starters.

**Regression Tests:**

- None (logic covered by manual run).

### [BUG-002] - Shared worktree role-scope false positive

**Date Discovered:** 2026-02-04

**Discovered By:** CLI run (`make feature F=07`)

**Severity:** Medium

**Status:** Fixed

**Environment:** Development

**Affected Users:** Any user resuming a work item with prefilled Plan section

**Symptoms:**
`pc-feature` fails with `tester edited out-of-scope files` when planner-log is created but no planner step runs.

**Steps to Reproduce:**

1. Ensure a work item already has a completed Plan section.
2. Run `make feature F=07`.
3. Observe: tester step fails with out-of-scope error on `planner-log.md`.

**Expected Behavior:**
Role enforcement should only consider files the role modifies.

**Actual Behavior:**
Unneeded role logs were created up-front, causing false positives.

**Root Cause:**
`pc-feature` pre-created all role logs in the shared patcher worktree, leaving untracked role logs when a role step is skipped.

**Fix:**
Create role logs lazily, immediately before writing each role's log entry.

**Files Changed:**

- `tools/pc-feature`
- `docs/03-logs/implementation-log.md`
- `docs/03-logs/bug-log.md`
- `docs/03-logs/validation-log.md`

**Prevention:**

- Process changes: Avoid pre-creating role-scoped files in shared worktrees.

**Fixed By:** Codex

**Fixed Date:** 2026-02-04

### [BUG-001] - Users Unable to Save Profile Changes

**Date Discovered:** 2025-01-15

**Discovered By:** User report (support ticket #1234)

**Severity:** High

**Status:** Fixed

**Environment:** Production

**Affected Users:** ~5% of users (estimated 500 users)

**Symptoms:**
Users click "Save" button on profile page, see loading spinner, then nothing happens. Changes are not saved. No error message shown.

**Steps to Reproduce:**

1. Log in as user
2. Go to Profile page
3. Change email address
4. Click "Save"
5. Observe: spinner shows briefly, then disappears, but email not updated

**Expected Behavior:**
Profile should update and show success message

**Actual Behavior:**
No update, no feedback, just spinner disappearing

**Root Cause:**
API endpoint `/api/profile` was returning 401 Unauthorized due to middleware checking for `userId` in token payload, but we changed token structure to use `user_id` (underscore) in a recent update. Frontend was sending valid token but backend was rejecting it.

**Why It Wasn't Caught:**

- Tests were mocking the auth middleware
- We didn't have E2E tests for profile update
- Change was deployed without full regression testing

**Fix:**

1. Updated auth middleware to check both `userId` and `user_id` for backward compatibility
2. Added migration to reissue tokens with correct structure
3. Added explicit error handling in frontend to show error messages

**Files Changed:**

- `src/middleware/auth.ts` - Added backward compatibility
- `src/components/Profile/ProfileForm.tsx` - Added error handling
- `tests/e2e/profile.spec.ts` - Added E2E test for profile update

**Prevention:**

- **Added E2E test** for profile update flow
- **Added monitoring** for 401 errors on profile endpoint
- **Process change:** All token structure changes require migration plan
- **Added test case** to verify backward compatibility of auth changes

**Related Issues:**

- [DEC-003] Decision to change token structure

**Fixed By:** John Smith

**Fixed Date:** 2025-01-16

**Deployed:** 2025-01-16 14:30 UTC

**Verified By:** QA team + 10 affected users

**Time to Fix:** 1 day (discovered afternoon, fixed next morning)

---

### [BUG-002] - Memory Leak in Dashboard Component

**Date Discovered:** 2025-01-18

**Discovered By:** Monitoring alert (high memory usage)

**Severity:** Medium

**Status:** Fixed

**Environment:** Production

**Affected Users:** Users who keep dashboard open for > 1 hour

**Symptoms:**
Browser tab becomes slow and unresponsive after dashboard is open for extended periods. Memory usage grows continuously.

**Steps to Reproduce:**

1. Open dashboard
2. Leave tab open for 1+ hour
3. Observe increasing memory usage in browser task manager

**Expected Behavior:**
Memory usage should remain stable

**Actual Behavior:**
Memory grows from 50MB to 500MB+ over time

**Root Cause:**
`setInterval` in Dashboard component was not being cleaned up on component unmount. Additionally, WebSocket connection was accumulating listeners on every re-render.

```typescript
// Buggy code:
useEffect(() => {
  setInterval(() => {
    fetchDashboardData();
  }, 30000);
  // Missing cleanup!
}, []);
```

**Fix:**
Added proper cleanup in useEffect:

```typescript
useEffect(() => {
  const intervalId = setInterval(() => {
    fetchDashboardData();
  }, 30000);

  return () => {
    clearInterval(intervalId);
  };
}, [fetchDashboardData]);
```

**Files Changed:**

- `src/components/Dashboard/Dashboard.tsx`
- `src/hooks/useWebSocket.ts`

**Prevention:**

- **Added linting rule** to warn about setInterval without cleanup
- **Added E2E test** that keeps dashboard open and monitors memory
- **Code review checklist** now includes "Are effects cleaned up?"
- **Added monitoring** for client-side memory usage

**Fixed By:** Sarah Johnson

**Fixed Date:** 2025-01-19

**Deployed:** 2025-01-19

**Verified By:** Load testing team

**Time to Fix:** 1 day

---

## Bug Patterns

### Common Bug Types

Track patterns to improve processes:

| Category                     | Count | % of Total | Prevention Strategy                  |
| ---------------------------- | ----- | ---------- | ------------------------------------ |
| Authentication/Authorization | [#]   | [%]        | Better E2E tests for auth flows      |
| Memory Leaks                 | [#]   | [%]        | Linting rules, code review checklist |
| Race Conditions              | [#]   | [%]        | Better async handling patterns       |
| Null/Undefined Errors        | [#]   | [%]        | Stricter TypeScript config           |
| Validation Errors            | [#]   | [%]        | Schema validation library            |
| CSS/Layout Issues            | [#]   | [%]        | Visual regression testing            |

### Most Buggy Areas

| Component/Module | Bug Count | Action Needed            |
| ---------------- | --------- | ------------------------ |
| [Path/Component] | [#]       | [Refactor/Add tests/etc] |

### Recurring Bugs

Bugs that keep coming back:

| Bug Pattern           | Times Occurred | Root Cause               | Permanent Fix    |
| --------------------- | -------------- | ------------------------ | ---------------- |
| [Pattern description] | [#]            | [Why it keeps happening] | [How to stop it] |

---

## Bug Statistics

### By Month

| Month   | Bugs Reported | Bugs Fixed | Still Open | Avg Time to Fix |
| ------- | ------------- | ---------- | ---------- | --------------- |
| 2025-01 | [#]           | [#]        | [#]        | [days]          |

### By Severity

| Severity | Opened | Fixed | Fix Rate |
| -------- | ------ | ----- | -------- |
| Critical | [#]    | [#]   | [%]      |
| High     | [#]    | [#]   | [%]      |
| Medium   | [#]    | [#]   | [%]      |
| Low      | [#]    | [#]   | [%]      |

### By Source

| Source               | Count | % of Total |
| -------------------- | ----- | ---------- |
| User Reports         | [#]   | [%]        |
| Monitoring/Alerts    | [#]   | [%]        |
| Internal Testing     | [#]   | [%]        |
| Production Incidents | [#]   | [%]        |

---

## Regression Tracking

Bugs that came back after being fixed:

| Original Bug | First Fixed | Regressed  | Times Regressed | Permanent Fix Date |
| ------------ | ----------- | ---------- | --------------- | ------------------ |
| [BUG-XXX]    | YYYY-MM-DD  | YYYY-MM-DD | [#]             | YYYY-MM-DD         |

---

## Won't Fix

Bugs we've decided not to fix, and why:

### [BUG-XXX] - [Description]

**Reason:** [Why we won't fix]
**Workaround:** [What users can do instead]
**Date Closed:** YYYY-MM-DD

---

## Related Documents

- [Implementation Log](implementation-log.md) - Code changes that may introduce bugs
- [Validation Log](validation-log.md) - Production issues after shipping
- [Test Plans](../02-features/*/test-plan.md) - Testing strategies
- [Insights](insights.md) - Learnings from bugs

## 2026-02-09 - Reporter global-log JSON parse failure at final gate

- **ID:** BUG-20260209-01
- **Status:** Fixed
- **Source:** Internal testing (`make feature`)
- **Summary:** `pc-feature` aborted after successful gates when reporter global-log output was non-JSON and parse failed.
- **Fix:** Added one JSON-repair retry and deterministic orchestrator fallback log payload generation.
- **Validation:** `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature` (offload id `2cbaa4db1d7a72f88c194ac728a304bdaa5e801327d99c96cb0de68ac7b0da69`).

## 2026-02-09 - Late patcher role-scope abort after plan drift

- **ID:** BUG-20260209-02
- **Status:** Fixed
- **Source:** Internal feature run (`make feature F=13`)
- **Summary:** A resumed/retried run reached patcher and aborted on `patcher edited role-scoped files` instead of rerouting to planner with remediation.
- **Fix:** Added pre-patch deterministic policy recheck and planner reroute flow for patcher role-scope/global-log violations.
- **Validation:** `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature` (offload id `f286e4ef1d6de49fe6b76805ea23fd8710d0f2a61084c4b5691e8b7c34401028`).

## 2026-02-09 - Planner/reviewer stagnation from wildcard handoff token

- **ID:** BUG-20260209-03
- **Status:** Fixed
- **Source:** Internal feature run (`make feature F=15`)
- **Summary:** Planner prompts required a handoff sentence containing `docs/03-logs/*`, but deterministic policy checks treated the same token as a forbidden path and repeatedly blocked plan revisions until stagnation abort.
- **Fix:** Updated planner/reviewer prompt wording to avoid mandatory wildcard-token output and added a narrow policy exception that ignores only literal wildcard handoff tokens in full-plan fallback scans (while still blocking `Files to change` wildcard/global-log edits).
- **Validation:** `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature` (offload id `4c8d6b83107f50e31329a63db83ec36e7ee535f336b652a2144265a29890f85d`) and direct policy replay on `WI-20260209-01` plan (`violations_count=0`).

## 2026-02-10 - Tester out-of-scope abort on planner-owned `dev-tasks.md`

- **ID:** BUG-20260210-01
- **Status:** Fixed
- **Source:** User report (`make feature F=15`)
- **Summary:** `pc-feature` could abort late with `tester edited out-of-scope files: docs/02-features/.../dev-tasks.md` when planner-owned `dev-tasks.md` remained dirty at tester commit time in a shared/resumed worktree.
- **Fix:** `commit_role_step(...)` now discards planner-owned `dev-tasks.md` deltas for non-planner roles (`tester`, `reporter`, `plan-reviewer`) before enforcing role scope.
- **Validation:** `python3 -m py_compile tools/pc-feature tests/test_pc_feature.py`; `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature.TestPcFeature.test_commit_role_step_tester_resets_dev_tasks_before_scope_check`.
