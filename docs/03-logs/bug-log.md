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

### [BUG-006] - Skill metadata drift was not gated by CI

**Date Discovered:** 2026-02-14

**Discovered By:** Batch B/C process review

**Severity:** Medium

**Status:** Fixed

**Environment:** Development

**Affected Users:** Internal maintainers of `.codex/skills/*`

**Symptoms:**
Skill metadata quality could regress (prompt token mismatch, invalid interface fields, local absolute path leakage) without a dedicated deterministic gate.

**Steps to Reproduce:**

1. Modify skill metadata (for example, remove `$skill-name` from `default_prompt`).
2. Run CI before this fix.
3. Observe no metadata-specific failure signal.

**Expected Behavior:**
CI fails when skill metadata or interface contracts drift.

**Actual Behavior:**
No dedicated check enforced metadata semantics beyond layout/frontmatter basics.

**Root Cause:**
`make test`/`make ci` lacked a validator for `agents/openai.yaml` contracts and portability constraints.

**Fix:**
Added `tools/pc-skills-metadata-check`, integrated `skills-metadata-check` into both live and template Makefiles, and added unit tests.

**Files Changed:**

- `tools/pc-skills-metadata-check`
- `tests/test_pc_skills_metadata_check.py`
- `Makefile`
- `tools/templates/root/Makefile`

**Prevention:**
Fail-closed metadata checks now run in `make test` and `make ci`.

- Tests added: `tests/test_pc_skills_metadata_check.py`
- Process changes: added `skills-metadata-check` Makefile target
- Monitoring added: none

**Related Issues:**

- [DEC-065] - Enforce CI-level skill metadata contracts and explicit invocation for high-impact skill workflows

**Fixed By:** Codex

**Fixed Date:** 2026-02-14

**Deployed:** 2026-02-14

**Verified By:** Codex (`make ci`; offload id `4aa43f23489b633ab1f3fdb605b483ccbca877caf26df6e9850a44f2244a43e6`)

### [BUG-005] - Skill metadata validation blocked by angle brackets in descriptions

**Date Discovered:** 2026-02-14

**Discovered By:** Batch validation run (`quick_validate.py`)

**Severity:** Low

**Status:** Fixed

**Environment:** Development

**Affected Users:** Internal skill maintainers (validation gate)

**Symptoms:**
Skill validation failed during Batch A metadata rollout with `Description cannot contain angle brackets (< or >)`.

**Steps to Reproduce:**

1. Run `python3 /Users/alexandrepezzotta/.codex/skills/.system/skill-creator/scripts/quick_validate.py` against `.codex/skills/create-feature-skeleton` (or the affected skills).
2. Observe validation error for frontmatter `description`.

**Expected Behavior:**
All updated skills pass metadata validation.

**Actual Behavior:**
Validation fails for skills whose descriptions contain placeholder notation like `<feature-name>`.

**Root Cause:**
Frontmatter descriptions were written with angle-bracket placeholders, which are disallowed by the skill validator.

**Fix:**
Replaced angle-bracket placeholders in descriptions with plain-language folder naming references.

**Files Changed:**

- `.codex/skills/create-feature-skeleton/SKILL.md`
- `.codex/skills/feature-status-audit/SKILL.md`
- `.codex/skills/prd-to-features/SKILL.md`

**Prevention:**
Run full-scope `quick_validate.py` before finalizing batch metadata edits and avoid angle-bracket placeholders in frontmatter descriptions.

- Tests added: none (metadata validation already enforces the rule).
- Process changes: keep validator run mandatory for skill metadata edits.
- Monitoring added: none.

**Related Issues:**

- [DEC-064] - Standardize skill interface metadata and portable prompts
- [Validation Log] 2026-02-14 Batch A skill metadata and interface validation

**Fixed By:** Codex

**Fixed Date:** 2026-02-14

**Deployed:** 2026-02-14

**Verified By:** Codex (`quick_validate.py` loop passed for all skills)

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

## 2026-02-11 - Final gate failure could leave partial collection side effects on main

- **ID:** BUG-20260211-01
- **Status:** Fixed
- **Source:** User report (`make feature F=17`)
- **Summary:** Final gate `make ci` could fail after patcher branch collection into `main`, leaving partial staged/dirty `main` updates despite workflow failure.
- **Fix:** Run final CI and scoped autofix in the patcher worktree first, then collect into `main` only after gates pass; add regression coverage asserting no collection on gate failure and hermetic proposal-dedup tests.
- **Validation:** `tools/offload-proxy/pp python3 -m unittest discover -s tests -p "test_pc_feature.py"` (offload id `17a8ec41f09e37973a3a896ec4b15c325638f8da2cfc2f65a704f751c97ea614`); `tools/offload-proxy/pp make ci` (offload id `ba175e3a0d04c6934e3fb6a78a4d31209981be22425e6717288083c253dbc2bf`).

## 2026-02-12 - Invalid Allowed Tests loop on dotted unittest selectors

- **ID:** BUG-20260212-01
- **Status:** Fixed
- **Source:** User report (`make feature F=18`)
- **Summary:** `pc-feature` retried three times and aborted with `blocked by invalid allowed tests` because `python -m unittest tests.test_pc_feature.TestPcFeature` was flagged as a missing target by the checker.
- **Fix:** Updated `tools/pc-allowed-tests-check` to accept dotted unittest class/method selectors when a valid module/package prefix exists; added regression tests and strengthened planner Allowed Tests remediation prompt/examples.
- **Validation:** `tools/pc-allowed-tests-check --cmd 'python3 -m unittest tests.test_pc_feature.TestPcFeature' --cmd 'python3 -m unittest tests.test_pc_feature.TestPcFeature.test_plan_reviewer_approve_allows_patch'` (PASS); `tools/offload-proxy/pp python3 -m unittest tests/test_pc_allowed_tests_check.py` (offload id `f196bef0973ff999dcbcf679ca035393cbb4be84e582dd7f9d09005e1f656ac4`).

## 2026-02-12 - Final-gate autofix candidate list included patcher-forbidden role files

- **ID:** BUG-20260212-02
- **Status:** Fixed
- **Source:** User report (`make feature F=18`)
- **Summary:** Final CI autofix could receive planner-owned feature files (for example `dev-tasks.md`) because candidate selection reused collection-path logic; when pre-commit touched those files, patcher commit aborted with `patcher edited role-scoped files`.
- **Fix:** Added dedicated `collect_patcher_autofix_paths(...)` filtering for final-gate autofix candidates, skipped forbidden candidate paths with explicit diagnostics, and retained existing collection-path behavior for final branch collection.
- **Validation:** `python3 -m py_compile tools/pc-feature tests/test_pc_feature.py` (PASS); `tools/offload-proxy/pp python3 -m unittest discover -s tests -p "test_pc_feature.py"` (PASS, offload id `90f84f11268b4fd5850cf20d292ecf3468a0f987819ec31265777f598530980f`).

## 2026-02-12 - Python 3.9 annotation crash and scoped-autofix false positive in feature-18 runs

- **ID:** BUG-20260212-03
- **Status:** Fixed
- **Source:** User report (`make feature F=18`)
- **Summary:** `markdown-lint` crashed under Python 3.9 (`TypeError` at `list[str] | None`), and final-gate scoped autofix reported out-of-scope changes for planner-owned `dev-tasks.md` even when that path was pre-existing dirty and untouched by autofix.
- **Fix:** Added `from __future__ import annotations` in `tools/markdown-lint` and `tools/pc-allowed-tests-check`; changed `run_scoped_autofix_paths(...)` to enforce scope via pre/post dirty snapshot deltas instead of all current dirty paths; added regression tests for both behaviors.
- **Validation:** `tools/offload-proxy/pp python3 -m unittest discover -s tests -p "test_tools_python_compat.py"` (PASS, offload id `92b391eabf11e0e952252fb6ee05522765579df0b6b0a838ff1f3e4150550b42`); `tools/offload-proxy/pp python3 -m unittest discover -s tests -p "test_pc_feature.py" -k scoped_autofix` (PASS, offload id `f2f7f20b09268ff1a5a9edf399b32bb047568b9780fc65a6c38dee4a6be91892`); `tools/offload-proxy/pp pre-commit run --files tools/markdown-lint tools/pc-allowed-tests-check tools/pc-feature tests/test_pc_feature.py tests/test_tools_python_compat.py` (PASS, offload id `5be5793f628b9d4ee932bfdfe3d69d9de33c933369d362c2f433acbc61914036`).

## 2026-02-13 - Sync-mode still blocked on lock mismatch without stale-start classification

- **ID:** BUG-20260213-01
- **Status:** Fixed
- **Source:** User report (`RESUME_MODE=sync make feature F=18`)
- **Summary:** `pc-feature` aborted with `main branch moved during feature execution` even in `RESUME_MODE=sync` when lock mismatch happened without startup stale classification.
- **Fix:** Updated lock-mismatch handling so `RESUME_MODE=sync` explicitly reconciles drift at lock-check time: merge when behind, otherwise refresh `Main head locked:` directly; kept `auto`/`prompt` fail-closed behavior and improved mismatch diagnostics.
- **Validation:** `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature.TestPcFeature.test_main_sync_mode_refreshes_locked_main_head_without_stale_sync tests.test_pc_feature.TestPcFeature.test_main_sync_mode_lock_mismatch_merge_failure_blocks tests.test_pc_feature.TestPcFeature.test_main_sync_mode_refreshes_locked_main_head_after_stale_sync` (PASS, offload id `4f0c69b4140575a873caf6ab2a99dfdc9025bc6c22fc770e2c730759f38191d6`); `tools/offload-proxy/pp python3 -m unittest tests/test_pc_feature.py` (PASS, offload id `c21d3a5bbd7812de3ed01757a8321e8230c8a1ab26a3a26f60c4cf79da0ebe7a`); `tools/offload-proxy/pp make test` (PASS, offload id `e547790fdd9be8ebfdf2f27874af7637405c1500f15173802a88196dda4d51af`).

## 2026-02-13 - Commit gate false-fail from stale non-pending reporter outcome

- **ID:** BUG-20260213-02
- **Status:** Fixed
- **Source:** User report (`make feature F=18`)
- **Summary:** Commit gate failed with `active ticket status is not completed: Outcome=needs replan` even after PASS reruns because `Reporter Review` stayed stale (`FAIL`) while latest reporter artifact was `PASS`; auto-repair only handled pending placeholders.
- **Fix:** Updated `pc-feature` commit repair to reconcile stale non-pending `Test Results`/`Reporter Review` outcomes from latest role artifacts and to derive top `Outcome` from artifact-first outcomes; added non-skip reporter terminal event emission to keep workflow status consistent.
- **Validation:** `python3 -m py_compile tools/pc-feature tests/test_pc_feature.py` (PASS); `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature.TestPcFeature.test_repair_commit_evidence_from_role_artifacts_fills_missing_fields tests.test_pc_feature.TestPcFeature.test_repair_commit_evidence_from_role_artifacts_reconciles_stale_reporter_review` (PASS, offload id `0d5f19ead2bf9676d74342ac6c647b4bf2294bed713605930a76f4b7d5b1c878`); `tools/offload-proxy/pp python3 -m unittest tests/test_pc_feature.py` (PASS, offload id `76e966c85e9d246bd36099481e193e07331f024f62884fced39365d7b921331d`); `tools/offload-proxy/pp make test` (PASS, offload id `b324a609661e28e2b83831364fc7bcca3aba143bb497e093ff13626bda22418e`).

## 2026-02-14 - Bootstrapped target missing runtime prompts (`prompts/*.md`)

- **ID:** BUG-20260214-01
- **Status:** Fixed
- **Source:** User report (`RESUME_MODE=fresh make feature F=01` in downstream repo)
- **Summary:** `pc-feature` failed at planner startup because bootstrap did not materialize prompt templates into living `prompts/*.md` files; target repos could also carry `tools/templates/*` instead of living-only assets.
- **Fix:** Updated `tools/bootstrap-into` to deploy `tools/templates/prompts/*.md` into `prompts/*.md`, stop copying `tools/templates/*` into target repos, add prompt sync policy for reapply, and align remediation/docs/parity checks.
- **Validation:** `tools/offload-proxy/pp python3 -m unittest discover -s tests -p 'test_bootstrap_into.py'` (PASS, offload id `046d8905c2cbebd57895f0a1e05779dd51c5ea65ecde0263e2ed43f1520edf92`); `tools/offload-proxy/pp python3 -m unittest discover -s tests_extra -p 'test_bootstrap_into_extra.py'` (PASS, offload id `ef2942e72d74fe234eb4a31f57d47d1be35b3519bba2467d6ee21f55ee9e14dc`); `tools/offload-proxy/pp python3 -m unittest discover -s tests -p 'test_pc_template_sync.py'` (PASS, offload id `dfb4f236d75ba74e6478c52cec4691473eda77385960e42b1f5cc0edda7720a9`).

## 2026-02-14 - Reporter retry exhaustion on sandbox git index lock commit errors

- **ID:** BUG-20260214-02
- **Status:** Fixed
- **Source:** User report (`make feature F=01` in a bootstrapped repo)
- **Summary:** Reporter retries could reach max attempts and abort even when reporter scope checks were complete, because feedback FAIL was driven by sandbox git index lock/permission errors during commit (`.git/index.lock`) instead of actionable handoff gaps.
- **Fix:** Added script-based role commits (`tools/pc-role-commit`) and switched `pc-feature` role commit flow to use it; added reporter classifier/normalizer to auto-convert sandbox/index-lock-only FAIL feedback to PASS; updated reporter prompts to forbid direct git commits.
- **Validation:** `tools/offload-proxy/pp python3 -m unittest discover -s tests -p 'test_pc_feature.py'` (PASS, offload id `2e18c264423b922c7aa09722eeb9266e0e21a61e0fea2fad17a4f0800913166b`); `tools/offload-proxy/pp python3 -m unittest discover -s tests -p 'test_pc_role_commit.py'` (PASS, offload id `ad4d35774bf0c86e40f21aa82925827615b66090a0d46b776bc3c936d9fbd14b`).

## 2026-02-15 - Final-gate scoped autofix still hit patcher role-scope abort with dirty `dev-tasks.md`

- **ID:** BUG-20260215-01
- **Status:** Fixed
- **Source:** User report (`make feature F=01` in bootstrapped consumer repo/worktree)
- **Summary:** Final CI autofix path could still abort with `patcher edited role-scoped files: .../dev-tasks.md` because scoped autofix candidate selection was followed by a broad patcher commit step that evaluated all dirty files.
- **Fix:** Added `commit_scoped_patcher_autofix_changes(...)` to commit only dirty patcher-safe candidate paths and block unexpected staged paths; replaced CI autofix `commit_role_step(...)` usage with the scoped helper; aligned AGENTS role-scope wording with planner ownership of `dev-tasks.md`.
- **Validation:** `python3 -m py_compile tools/pc-feature tests/test_pc_feature.py` (PASS); `tools/offload-proxy/pp python3 -m unittest tests/test_pc_feature.py` (PASS, offload id `71d98179d947908fe7819192d67c7de92f1d5792ec54c98ab3df42be8a9c922e`).
