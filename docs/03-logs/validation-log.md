# Validation Log

> **What happened after shipping**
>
> A record of what actually happened when features went to production. Did metrics improve? Did users behave as expected? What did we learn?

---

## Purpose

This log captures:

- **Actual outcomes** vs expected outcomes
- **User behavior** with new features
- **Metric changes** after deployment
- **Unexpected consequences** (good and bad)
- **Feedback** from users and stakeholders

This helps with:

- Learning what works and what doesn't
- Improving future estimates and predictions
- Understanding user behavior
- Building better products based on reality, not assumptions

---

## Recent Validations

### 2026-02-08 - Precommit autofix scope hardening validation

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_autofix.py"` (PASS)
- `tools/offload-proxy/pp pre-commit run --files .pre-commit-config.yaml docs/04-process/ci-autofix-prompt.md docs/04-process/git-workflow.md docs/04-process/ticket-execution-protocol.md tools/markdown-lint tools/pc-autofix tools/pc-precommit tools/pc-template-sync tools/templates/docs/04-process/ci-autofix-prompt.md tools/templates/docs/04-process/git-workflow.md tools/templates/docs/04-process/ticket-execution-protocol.md tools/templates/root/.pre-commit-config.yaml tests/test_pc_autofix.py` (PASS)
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"` (PASS; offload id `0c7809944d4bb96d70fef46c4c81277199007a4dd63bb83a13c437a237b419ca`)

### 2026-02-08 - Feature 12 docs rebaseline validation

- `tools/offload-proxy/pp rg -n "link to feature-spec.md|link to dev-tasks.md|link to test-plan.md|link to docs/00-context/system-map.md|\\[link to" docs/02-features/12-incremental-prd-to-features` (PASS: no placeholder links found)
- `tools/offload-proxy/pp rg -n "Last Updated:\\*\\*\\s*2026-02-05" docs/02-features/12-incremental-prd-to-features` (PASS: no stale 2026-02-05 metadata remains)
- `tools/offload-proxy/pp rg -n "add missing features only|never delete existing|Status: Done|incremental: add missing" docs/04-process/human-orchestration-workflow.md docs/01-product/prd.md docs/00-context/expected-features.md` (PASS: policy references match refreshed F-12 wording)

### 2026-02-08 - Feature docs 13-16 rebaseline validation

- `tools/offload-proxy/pp rg -n "link to feature-spec.md|link to dev-tasks.md|link to test-plan.md|link to docs/00-context/system-map.md" docs/02-features/13-role-prompts-plan-reviewer docs/02-features/14-learning-loop-improvement-proposals docs/02-features/15-offload-audit-and-log-compaction docs/02-features/16-feature-gating-and-skill-mining` (PASS: no placeholder links found)
- `tools/offload-proxy/pp rg -n "Last Updated:\\*\\*\\s*2026-02-05" docs/02-features/13-role-prompts-plan-reviewer docs/02-features/14-learning-loop-improvement-proposals docs/02-features/15-offload-audit-and-log-compaction docs/02-features/16-feature-gating-and-skill-mining` (PASS: no stale 2026-02-05 metadata remains in features 13-16 docs)

### 2026-02-07 - Workflow doc sync validation

- Not run (doc-only change; no test command specified).

### 2026-02-06 - Interactive high-risk approval gate validation

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"` (PASS)
- `tools/offload-proxy/pp env APPROVE_HIGH_RISK=1 make feature F=10` (FAIL: existing permission/network/session issues in worktree `.codex_subagent`, unrelated to high-risk prompt logic)

### 2026-02-06 - Step 16 final validation sweep

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"` (PASS)
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_allowed_tests_check.py"` (PASS)
- `tools/offload-proxy/pp make ci` (FAIL: pre-commit `end-of-file-fixer` permission error on `.codex/skills/*`)

### 2026-02-06 - Step 15 autofix scope lockdown validation

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"` (PASS)

### 2026-02-06 - Step 14 escalation broker/worktree ordering validation

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"` (PASS)

### 2026-02-06 - Step 13 deterministic risk trigger validation

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"` (PASS)

### 2026-02-06 - Step 12 Allowed Tests enforcement/parsing validation

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_allowed_tests_check.py"` (PASS)
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"` (PASS)

### 2026-02-06 - Step 11 tools/pc-commit final commit path validation

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"` (PASS)

### 2026-02-06 - Step 10 CI cadence reduction validation

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"` (PASS)

### 2026-02-06 - Step 09 replanning/repatch enforcement validation

- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"` (PASS)

### 2026-02-06 - F-09 completion validation (tests/ci structured logs)

- `tools/offload-proxy/pp make ci` (FAIL: pre-commit `end-of-file-fixer` permission error on `.codex/skills/*`)
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"` (PASS)
- `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_runner.py"` (PASS)

### 2026-02-06 - F-09 log hygiene + per-feature WI IDs validation

- `python -m unittest discover -s tests -p "test_*.py"` (PASS)

### 2026-02-05 - F-08 anti-cheat testing strategy validation

- `pytest tests/test_pc_feature.py` (PASS)
- `pytest tests/test_docs_logs.py tests/test_orchestrator_workflow_docs.py tests_extra/test_bootstrap_into_extra.py` (PASS)

### 2026-02-05 - Ticket execution protocol template sync validation pending

- Not run (no test command specified).

### 2026-02-05 - pc-feature prompt escaping lint fix validated

- `tools/offload-proxy/pp ruff check tools/pc-feature` (PASS)
- `tools/offload-proxy/pp black --check tools/pc-feature` (PASS)

### 2026-02-05 - Worktree ahead-of-main reset validation pending

- Not run (no test command specified).

### 2026-02-05 - Preflight JSON parsing hardening validation pending

- Not run (no test command specified).

### 2026-02-05 - Allowed Tests enforcement validation pending

- Not run (no test command specified).

### 2026-02-05 - pc-feature role isolation hardening validation pending

- Not run (no test command specified).

### 2026-02-04 - pc-feature role-scope fix validation pending

- Not run (no test command specified).

### 2026-02-04 - Template sync hook pass after doc-template alignment

- `tools/offload-proxy/pp tools/pc-template-sync` (PASS)

### 2026-02-04 - Codex exec CODEX_HOME change validation pending

- Set scripted Codex exec to use repo-local `.codex`; no automated validation run yet.

### 2026-02-04 - Template sync hook validation pending

- Added a template/living sync pre-commit hook; no automated validation run yet.

### 2026-02-04 - Worktree policy collector validation pending

- Updated tooling and docs for role-scoped worktrees and auto-collection; no automated validation run yet.

### 2026-02-04 - Shared patcher worktree orchestration validation failed

- `tools/offload-proxy/pp make feature F=07` (FAIL: codex exec network/model refresh errors and Serena MCP startup failure; offload id `33b04a30a6906d5282dc9c03f5331d917720d8652e5246e4065bb53e17aab539`)
- `tools/offload-proxy/pp make ci` (FAIL: end-of-file-fixer PermissionError on `.codex/skills/readme-sync/SKILL.md`; offload id `69e02d94f6d70a8104c949ac3165b511ece1b6a7f334e95a247f0375e31901f3`)

### 2026-02-04 - Ticket 401 - Orchestrator gate docs regression verified

- Added regression tests that assert the workflow gating predicates (TC-WF001..TC-WF004) include the artifact, gate, and audit language required for the orchestrator/sub-agent CLI path.
- `tools/offload-proxy/pp python -m unittest discover -s tests -p test_orchestrator_role_gates.py` (PASS)

### 2026-02-03 - Ticket 102 docs gating regression coverage validated

- Confirmed the orchestrator/sub-agent docs regression suite now checks for TC-WF001, TC-WF002, TC-WF003, and TC-WF004 phrases so the tooling workflow gating tests remain blocked until the required gate descriptions exist.
- `python -m unittest discover -s tests -p test_orchestrator_workflow_docs.py` (PASS)

### 2026-02-03 - Reapply gating output now surfaces during bootstrap runs

- Verified the bootstrap reapply flow emits the preflight validation gate, template diff review gate, and conflict summary output while prompting for overwrite/merge/skip decisions so the regression expectations are satisfied.
- `tools/offload-proxy/pp make test` (PASS)

### 2026-02-03 - Ticket 401 docs gating coverage validated

- Confirmed the new doc regression tests (`tests/test_output_offload_enforcement_docs.py`) enforce TC-D002/TC-D003 by ensuring the output offload test plan plus the Execute ticket feature spec and tech design mention offload IDs and gating behavior.
- `tools/offload-proxy/pp make ci` (PASS)

### 2026-02-03 - Validate offload proxy regression coverage

- Verified the new regression ensures `tools/offload-proxy/pp` stores noisy outputs under `.offload/`, prints the pointer id banner, and honors `always_offload` entries so downstream gates can reference the recorded artifact.
- `tools/offload-proxy/pp python -m unittest discover -s tests -p test_offload_proxy.py` (PASS)

### 2026-02-03 - Validate exit/log expectations via regression tests

- Added `test_update_reapply_exit_code_and_log_outputs`, which skips the README reapply prompt, confirms the template diff and conflict summary phrases appear for `docs/README.md`, and ensures the implementation/validation logs retain exactly one bootstrap marker per file after the skip.
- `tools/offload-proxy/pp python -m unittest discover -s tests -p test_bootstrap_into.py` (PASS)

### 2026-02-03 - Bootstrap tolerates pre-commit install failures

- Verified `bootstrap-into` now prints a warning and continues when `pre-commit install` fails so the CLI can finish reapply runs even when hook installation returns non-zero.
- `tools/offload-proxy/pp make test` (PASS)

### 2026-02-03 - Reapply gating expectation test fails before CLI output changes

- Added a regression that runs the reapply flow against a repo with local edits and asserts the CLI prints the preflight validation gate, template diff review gate, and conflict summary output while prompting for overwrite/merge/skip decisions.
- `tools/offload-proxy/pp python -m unittest discover -s tests -p test_bootstrap_into.py` (FAIL: the CLI is still silent about the gate phrases)

### 2026-02-03 - Reapply gate phrases now emitted

- Verified the reapply workflow now prints the preflight validation gate, template diff review gate, and conflict summary output whenever it prompts before overwriting syncable files.
- `python3 tools/offload-proxy/pp make test` (PASS)

### 2026-02-03 - Document workflow gating tests failing before docs update

- Captured the pre-implementation validation for the update/reapply templates workflow docs by noting the regression tests that check for workflow behavior, gates, and outputs language while they still fail.
- `tools/offload-proxy/pp python -m unittest discover -s tests -p test_update_reapply_templates_docs.py` (FAIL: the feature docs do not yet contain the required phrases)

### 2026-02-03 - Ticket 101 docs gating tests fail initially

- Added `tests/test_output_offload_enforcement_docs.py` to enforce TC-D001/TC-D002/TC-D003 coverage for the output offload enforcement docs before any doc changes land.
- `python -m unittest discover -s tests -p test_output_offload_enforcement_docs.py` (FAIL: feature-spec/tech-design/test-plan do not yet mention the workflow steps, gates, or offload artifacts that these tests require)

### 2026-02-03 - Ticket 101 docs gating phrases documented

- Verified the output offload enforcement docs now describe the workflow steps, approval gate, noisy command handling gate, and offload artifact expectations so TC-D001..D004 can succeed.
- `tools/offload-proxy/pp make test` (PASS)

### 2026-02-03 - Validated bootstrap template and log marker regressions

- Added focused regression checks for `AGENTS.md`, `pp.yml`, `.codex/skills/context-to-product/SKILL.md`, and the gate logs so each file retains a single bootstrap marker and the CLI reports them once.
- `tools/offload-proxy/pp python -m unittest discover -s tests` (PASS)
- `tools/offload-proxy/pp make ci` (PASS)

### 2026-02-03 - Record validation findings for Execute ticket gating steps

- Recorded the validation findings for the Execute work item workflow gating steps and aligned the validation log with the updated execution protocol.
- Not run (documentation-only change).

### 2026-02-02 - Bootstrap CLI log coverage regression

- Added log-focused regression tests in `tests/test_bootstrap_into.py` that confirm the CLI copies both log documents, reports them once, and keeps their bootstrap markers unique even after verbose reruns.
- `python -m unittest discover -s tests` (PASS) and `make ci` (PASS) after the new tests landed.

### 2026-02-02 - Confirmed bootstrap root template coverage

- `python -m unittest discover -s tests` (PASS)
- `make ci` (PASS)
- Verified AGENTS/Makefile/pp.yml and `.codex/skills/context-to-product/SKILL.md` carry bootstrap markers when copied by the CLI, reinforcing the root/template story.

### 2026-02-03 - Validated bootstrap skip test behavior

- Adjusted `test_bootstrap_into_handles_existing_files_skip` so it writes `local readme\n` and sends `input_text="s\n"`, making the skip prompt deterministic.
- `tools/offload-proxy/pp make test` (PASS)

---

## Validation Template

### [Feature Name] - Post-Launch Validation

**Feature:** [Link to feature-spec.md]

**Launched:** YYYY-MM-DD

**Validation Period:** [Date range of data collection]

**Validated By:** [Name/Team]

---

#### Expected Outcomes

[From feature-spec.md success metrics]

| Metric     | Target | Expected Impact |
| ---------- | ------ | --------------- |
| [Metric 1] | [goal] | [prediction]    |
| [Metric 2] | [goal] | [prediction]    |

---

#### Actual Outcomes

| Metric     | Target | Actual   | Δ    | Met?  |
| ---------- | ------ | -------- | ---- | ----- |
| [Metric 1] | [goal] | [actual] | [±%] | ✅/❌ |
| [Metric 2] | [goal] | [actual] | [±%] | ✅/❌ |

---

#### User Behavior Observations

**Usage Stats:**

- Total users who tried feature: [number] ([%] of active users)
- Users who adopted (used > 3 times): [number] ([%] of those who tried)
- Average frequency: [times per day/week/month]
- Time to adoption: [how long before first use]

**Unexpected Behaviors:**

- [Observation 1]: [description and why it's surprising]
- [Observation 2]: [description]

**User Segments:**

- **Power users:** [description of how heavy users behave]
- **Casual users:** [description]
- **Non-adopters:** [who didn't use it and why]

---

#### Qualitative Feedback

**Positive Feedback:**

- "[User quote]"
- "[User quote]"

**Negative Feedback:**

- "[User quote]"
- "[User quote]"

**Feature Requests:**

- [Request 1]: [how many users asked]
- [Request 2]: [how many users asked]

**Support Tickets:**

- Total tickets related to feature: [count]
- Common issues: [list]

---

#### Technical Performance

**Performance Metrics:**
| Metric | Target | Actual | Met? |
|--------|--------|--------|------|
| Response time (p95) | [target] | [actual] | ✅/❌ |
| Error rate | [target] | [actual] | ✅/❌ |
| Uptime | [target] | [actual] | ✅/❌ |

**Incidents:**

- [Count] incidents related to this feature
- [Brief description of any major issues]

**Resource Usage:**

- CPU: [impact]
- Memory: [impact]
- Database: [impact]
- Costs: [any unexpected costs]

---

#### What Went Well

1. **[Success 1]**
   - What happened: [description]
   - Why it worked: [analysis]
   - Takeaway: [what to repeat]

2. **[Success 2]**
   - What happened: [description]
   - Why it worked: [analysis]
   - Takeaway: [what to repeat]

---

#### What Didn't Go Well

1. **[Problem 1]**
   - What happened: [description]
   - Why it didn't work: [analysis]
   - What we'll do differently: [lesson learned]

2. **[Problem 2]**
   - What happened: [description]
   - Why it didn't work: [analysis]
   - What we'll do differently: [lesson learned]

---

#### Surprises

**Positive Surprises:**

- [Something unexpectedly good that happened]
- [Unintended positive consequence]

**Negative Surprises:**

- [Something unexpectedly bad that happened]
- [Unintended negative consequence]

---

#### Hypotheses Validated/Invalidated

| Hypothesis         | Result                                          | Evidence                     |
| ------------------ | ----------------------------------------------- | ---------------------------- |
| [What we believed] | ✅ Validated / ❌ Invalidated / 🤷 Inconclusive | [Data that proves/disproves] |

---

#### Next Steps

**Immediate Actions:**

- [ ] [Action based on learnings]
- [ ] [Bug fix or improvement]
- [ ] [Metric to add/monitor]

**Future Enhancements:**

- [ ] [Feature improvement]
- [ ] [New feature idea]

**Experiments to Run:**

- [ ] [Hypothesis to test]
- [ ] [A/B test to conduct]

---

#### Overall Assessment

**Success Rating:** [1-5 stars] ⭐⭐⭐⭐⭐

**Summary:**
[2-3 paragraph summary of whether this feature achieved its goals, what we learned, and whether we'd do it again]

**Would we build this again?** [Yes/No/Different approach]

**If doing it again, we would:**

- [Change 1]
- [Change 2]

---

## Validation Entries

### Example: Dashboard Redesign - Post-Launch Validation

**Feature:** [Link to docs/02-features/dashboard-redesign/feature-spec.md]

**Launched:** 2025-01-20

**Validation Period:** 2025-01-20 to 2025-02-03 (2 weeks)

**Validated By:** Product team + Analytics

---

#### Expected Outcomes

| Metric               | Target | Expected Impact                      |
| -------------------- | ------ | ------------------------------------ |
| Time on dashboard    | +30%   | Users spend more time exploring data |
| Feature discovery    | +50%   | Users find and use more features     |
| User satisfaction    | +20%   | Higher NPS score                     |
| Task completion rate | +25%   | Users complete tasks faster          |

---

#### Actual Outcomes

| Metric               | Target | Actual | Δ    | Met? |
| -------------------- | ------ | ------ | ---- | ---- |
| Time on dashboard    | +30%   | +45%   | +15% | ✅   |
| Feature discovery    | +50%   | +35%   | -15% | ❌   |
| User satisfaction    | +20%   | +18%   | -2%  | ❌   |
| Task completion rate | +25%   | +40%   | +15% | ✅   |

---

#### User Behavior Observations

**Usage Stats:**

- Total users who saw new dashboard: 10,000 (100% via feature flag rollout)
- Users who actively engaged: 8,500 (85%)
- Average time on dashboard: 8.5 min (up from 5.5 min)
- Daily active dashboard users: +25%

**Unexpected Behaviors:**

- **Power users created custom views:** 30% of power users created custom dashboard layouts within first week (we didn't expect this for first month)
- **Mobile usage dropped:** Mobile dashboard usage dropped 15% - redesign optimized for desktop, didn't translate well to mobile
- **Export feature popular:** CSV export used 3x more than predicted

**User Segments:**

- **Power users (20%):** Created avg 3 custom views, spend 15+ min/day on dashboard
- **Casual users (60%):** Use default view, quick check-ins (2-3 min)
- **Non-adopters (20%):** Reverted to old dashboard via settings toggle

---

#### Qualitative Feedback

**Positive Feedback:**

- "Finally! I can see everything I need at a glance" (47 similar comments)
- "The new charts are beautiful and actually useful" (31 similar)
- "Custom views are a game changer" (23 similar)

**Negative Feedback:**

- "Too cluttered on mobile, can barely read the text" (34 similar comments)
- "Can't find the settings I used to use" (28 similar)
- "Slower to load than old dashboard" (19 similar)

**Feature Requests:**

- Dark mode (142 requests)
- Share custom views with team (87 requests)
- More chart types (56 requests)

**Support Tickets:**

- Total tickets: 89
- Common issues:
  - Can't find export button (32 tickets)
  - Mobile layout broken (27 tickets)
  - Custom view not saving (18 tickets)

---

#### Technical Performance

**Performance Metrics:**
| Metric | Target | Actual | Met? |
|--------|--------|--------|------|
| Load time (p95) | < 2s | 2.8s | ❌ |
| Error rate | < 0.1% | 0.3% | ❌ |
| Uptime | 99.9% | 99.95% | ✅ |

**Incidents:**

- 2 incidents: custom view saving failed intermittently
- 1 performance degradation: database queries not optimized

**Resource Usage:**

- Database queries increased 40% (more data fetched for new widgets)
- API response time increased 300ms on average
- Frontend bundle size increased 150KB (added charting library)

---

#### What Went Well

1. **Custom views exceeded expectations**
   - What happened: Users loved the ability to customize their dashboard, adopted much faster than predicted
   - Why it worked: Gave power users exactly what they wanted, scratched a real itch
   - Takeaway: Features that give users control and customization are high-value

2. **Task completion improved significantly**
   - What happened: Users completed common tasks 40% faster
   - Why it worked: Information architecture improvements, better visual hierarchy
   - Takeaway: UX research and design iteration paid off

---

#### What Didn't Go Well

1. **Mobile experience wasn't prioritized enough**
   - What happened: Mobile usage dropped 15%, many complaints about mobile UX
   - Why it didn't work: Designed desktop-first, didn't test mobile thoroughly
   - What we'll do differently: Design mobile and desktop in parallel, test both equally

2. **Performance regression**
   - What happened: Load time increased 40% (1.8s → 2.8s)
   - Why it didn't work: Added many new features without optimizing queries and bundle
   - What we'll do differently: Set performance budget, monitor during development, not just at launch

3. **Feature discovery lower than expected**
   - What happened: Users found +35% more features (vs target of +50%)
   - Why it didn't work: Some features buried in menus, no onboarding tour
   - What we'll do differently: Add interactive onboarding, better feature highlights

---

#### Surprises

**Positive Surprises:**

- Export feature used 3x more than predicted - users wanted to analyze data externally
- Time on dashboard increased more than expected (+45% vs +30% target) - stickier than anticipated
- Users created custom views immediately, didn't need prompting

**Negative Surprises:**

- 20% of users toggled back to old dashboard (expected < 5%)
- Mobile usage declined (expected neutral impact)
- Support ticket volume 2x higher than expected

---

#### Hypotheses Validated/Invalidated

| Hypothesis                                     | Result          | Evidence                                      |
| ---------------------------------------------- | --------------- | --------------------------------------------- |
| Users want more data on one screen             | ✅ Validated    | Time on dashboard up 45%, positive feedback   |
| Better visual design will improve satisfaction | 🤷 Inconclusive | NPS up only 18% vs 20% target, mixed feedback |
| Users will find features more easily           | ❌ Invalidated  | Feature discovery up only 35% vs 50% target   |
| Mobile usage will remain constant              | ❌ Invalidated  | Mobile usage down 15%                         |

---

#### Next Steps

**Immediate Actions:**

- [ ] Fix mobile layout (P0) - starting next sprint
- [ ] Optimize database queries to reduce load time (P0)
- [ ] Fix custom view saving bug (P0)
- [ ] Add onboarding tour for new features (P1)

**Future Enhancements:**

- [ ] Dark mode (top requested feature)
- [ ] Shared custom views (team feature)
- [ ] More chart types

**Experiments to Run:**

- [ ] A/B test onboarding tour effectiveness
- [ ] Test different chart configurations
- [ ] Try progressive loading to improve perceived performance

---

#### Overall Assessment

**Success Rating:** ⭐⭐⭐⭐ (4/5)

**Summary:**
The dashboard redesign achieved its primary goal of improving task completion (+40%) and exceeded targets for engagement (+45% time on dashboard). Users loved the custom views feature and found the new design more useful.

However, we failed to maintain the mobile experience, resulting in a 15% drop in mobile usage. Performance also regressed, with load times increasing 40%. Feature discovery improved, but less than expected.

Overall, this was a successful launch with clear areas for improvement. The core redesign works well, but we need to fix mobile and performance issues ASAP.

**Would we build this again?** Yes, but with changes

**If doing it again, we would:**

- Design and test mobile experience equally with desktop
- Set and enforce performance budget from day one
- Add onboarding tour in initial release
- Better estimate support ticket volume and staff accordingly
- Do phased rollout (we did 100% in one day, should have done gradual)

---

## Validation Summary

### Features Validated

| Feature            | Launch Date | Success Rating | Key Learnings                               |
| ------------------ | ----------- | -------------- | ------------------------------------------- |
| Dashboard Redesign | 2025-01-20  | ⭐⭐⭐⭐       | Mobile matters, performance budgets crucial |

### Success Rate

- **Exceeded expectations:** [count] features
- **Met expectations:** [count] features
- **Below expectations:** [count] features
- **Failed:** [count] features

### Top Learnings

1. [Key learning across multiple features]
2. [Pattern observed]
3. [Insight for future work]

---

## Related Documents

- [Feature Specs](../02-features/) - Original feature expectations
- [Insights](insights.md) - Patterns and improvements
- [Implementation Log](implementation-log.md) - What was built
- [Bug Log](bug-log.md) - Issues found post-launch

## 2026-02-06 - Workflow hardening Step 01 validation

- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`
- Result: FAIL (expected for baseline harness); targeted regressions reproduced:
  - newest in-progress resume selection
  - worktree cwd for Allowed Tests execution
  - `feature-worktrees.json` side effect
  - blanket `git add -A` final staging
  - commit prompt execution even when Commit section already filled
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_allowed_tests_check.py"`
- Result: FAIL (expected for baseline harness); valid `python -m unittest discover ...` commands are currently flagged as missing.

## 2026-02-06 - Workflow hardening Step 02 validation

- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "dirty_existing_worktree"`
- Result: PASS (`2` tests)
- Verified:
  - continue path keeps existing dirty/ahead patcher worktree and proceeds without cleanup.
  - abort path exits early with explicit preserve-state message.
  - no destructive `remove_worktree` call is issued in either path.

## 2026-02-06 - Workflow hardening Step 03 validation

- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "select_resume_work_item_id"`
- Result: PASS (`2` tests)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "resumes_newest_in_progress_work_item"`
- Result: PASS (`1` test)
- Verified:
  - mixed WI outcomes resume the newest non-pass WI.
  - newest WI with `Outcome: pass` does not resume and triggers new WI creation path.

## 2026-02-06 - Workflow hardening Step 04 validation

- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "stage_scoped_final_paths_blocks_unrelated_dirty_paths"`
- Result: PASS (`1` test)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "avoids_git_add_all_for_final_staging"`
- Result: PASS (`1` test)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "skips_commit_generation_if_commit_section_already_filled"`
- Result: PASS (`1` test)
- Verified:
  - final staging no longer uses blanket `git add -A`.
  - commit generation is skipped when `Commit` section is already filled.
  - unrelated dirty files block final commit with actionable output.

## 2026-02-06 - Workflow hardening Step 05 validation

- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "does_not_write_feature_worktree_manifest"`
- Result: PASS (`1` test)
- Command: `tools/offload-proxy/pp rg -n "write_worktree_manifest|feature-worktrees\\.json" /Users/alexandrepezzotta/repos/PezzosCode/tools/pc-feature`
- Result: no matches (`rg` exit code `1`, expected for empty result)
- Additional safety checks:
  - `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "avoids_git_add_all_for_final_staging"` -> PASS
  - `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "skips_commit_generation_if_commit_section_already_filled"` -> PASS

## 2026-02-06 - Workflow hardening Step 06 validation

- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "allowed_tests_run_in_worktree_cwd"`
- Result: PASS (`1` test)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "prepatch_smoke_runs_in_worktree_cwd"`
- Result: PASS (`1` test)
- Verified:
  - Allowed Tests run with `cwd=tester_path`.
  - Prepatch smoke runs with `cwd=patcher_path`.
  - Structured logging flow remains unchanged (logs written via root metadata path).

## 2026-02-06 - Workflow hardening Step 07 validation

- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "parse_plan_reviewer_decision"`
- Result: PASS (`1` test)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "plan_reviewer_block_routes_back_to_planner_before_patch"`
- Result: PASS (`1` test)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "plan_reviewer_approve_allows_patch"`
- Result: PASS (`1` test)
- Verified:
  - reviewer `BLOCK` triggers planner replan path and loop continuation.
  - reviewer `APPROVE` allows patch phase to execute.
  - patch step is not reached in the blocked iteration.

## 2026-02-06 - Workflow hardening Step 08 validation

- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "load_prompt_template_prefers_task_specific_then_fallback"`
- Result: PASS (`1` test)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "render_prompt_template_substitutes_variables"`
- Result: PASS (`1` test)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "load_prompt_template_missing_file_has_clear_error"`
- Result: PASS (`1` test)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "plan_reviewer_block_routes_back_to_planner_before_patch"`
- Result: PASS (`1` test)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "plan_reviewer_approve_allows_patch"`
- Result: PASS (`1` test)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "avoids_git_add_all_for_final_staging"`
- Result: PASS (`1` test)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py" -k "skips_commit_generation_if_commit_section_already_filled"`
- Result: PASS (`1` test)
- Command: `tools/offload-proxy/pp rg -n "You are the Planner agent|You are the Patcher agent|You are the Reporter agent|You are the Plan Reviewer agent|generating a concise, scoped commit message|Allowed Tests must list" /Users/alexandrepezzotta/repos/PezzosCode/tools/pc-feature`
- Result: no matches (`rg` exit code `1`, expected for empty result)
- Verified:
  - prompt content for role/task executions is now file-sourced.
  - task-specific prompt fallback and variable rendering work deterministically.
  - missing prompt templates fail with explicit checked-path error text.

## 2026-02-06 - Loop stability and visibility validation

- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`
- Result: PASS (`44` tests)
- Verified:
  - Plan-reviewer BLOCK rounds can repeat without consuming execution attempt budget.
  - Reporter review uses attempt-scoped baseline input (`attempt_base`).
  - Repeated identical reporter FAIL with tester PASS now stops with explicit policy-conflict error.
  - Iteration Log records timestamped timeline events with attempt/step/status.

## 2026-02-06 - Visual Step Trace validation

- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`
- Result: PASS (`46` tests)
- Verified:
  - `Step Trace` section is present for execution entries.
  - Trace updates are rendered as a single per-attempt flow line.
  - Multiple events on same attempt update the same flow line (no duplicate attempt lines).
  - Runtime writes flow state across reviewer, patch, tests, reporter, feedback, and CI phases.

## 2026-02-06 - Worktree collection conflict hardening validation

- Command: `tools/offload-proxy/pp git log --oneline --decorate --graph --max-count=80 --all`
- Result: PASS (identified repeated `feature-10-unified-autofix-precommit-patcher` role commits and divergence from `main`)
- Command: `tools/offload-proxy/pp git diff --name-status HEAD..refs/heads/feature-10-unified-autofix-precommit-patcher`
- Result: PASS (confirmed volatile-path drift in branch diff: role logs, global logs, runtime logs, and docs)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`
- Result: PASS (`49` tests)
- Verified:
  - branch replay paths are filtered to durable implementation files.
  - volatile docs/log artifacts are excluded from replay and from branch-derived final staging scope.
  - empty filtered replay set safely no-ops (no diff/apply call).

## 2026-02-06 - High-risk resume policy-conflict fix validation

- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`
- Result: PASS (`51` tests)
- Command: `tools/offload-proxy/pp pre-commit run --files tools/pc-feature tests/test_pc_feature.py`
- Result: PASS
- Verified:
  - resumed high-risk entries with `Notes: Awaiting PO Approval` re-run approval gate before plan-reviewer.
  - approval is persisted with explicit note marker and reused on next retries.
  - first plan-reviewer contradiction against approved high-risk policy records `WARN` and routes planner correction instead of immediate hard-fail.
  - repeated contradiction remains bounded by conflict cap.

## 2026-02-06 - Runtime log finalization guard fix validation

- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`
- Result: PASS (`41` tests)
- Command: `tools/offload-proxy/pp pre-commit run --files tools/pc-feature tests/test_pc_feature.py`
- Result: PASS
- Verified:
  - `stage_scoped_final_paths(...)` ignores runtime `logs/WI-*` artifacts.
  - final `tools/pc-commit` command includes ephemeral allow prefixes, including `logs`.
  - runtime logs no longer trigger `unrelated dirty paths block final commit`.

## 2026-02-06 - Reviewer-block budget separation validation

- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`
- Result: PASS (`43` tests)
- Command: `tools/offload-proxy/pp pre-commit run --files tools/pc-feature tests/test_pc_feature.py`
- Result: PASS
- Verified:
  - repeated reviewer BLOCK rounds do not consume execution-attempt budget.
  - reviewer-block churn now fails with dedicated `max plan-reviewer block attempts reached` message instead of generic max-iteration failure.
  - block-count notes are recorded in iteration log for traceability.

## 2026-02-07 - Execution safety hardening validation

- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_feature.py"`
- Result: PASS (`48` tests)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_pc_allowed_tests_check.py"`
- Result: PASS (`8` tests)
- Command: `tools/offload-proxy/pp python -m unittest discover -s tests -p "test_*.py"`
- Result: PASS (`109` tests)
- Verified:
  - patcher cleanup is scoped to the active feature worktree only.
  - escalation requests wrapped with `tools/offload-proxy/pp` are evaluated by underlying command, not by wrapper prefix.
  - stale behind-`main` patcher worktrees are detected before execution continues.
  - HIGH-risk approval is revalidated on resume when approval marker is missing.
  - branch replay excludes volatile log/doc artifacts and collection conflict notes stay technical.
  - Allowed Tests now reject unsupported shell/general commands and accept only unittest/pytest forms.

## 2026-02-07 - Workflow ordering and retry-loop validation

- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- Result: PASS (`49` tests)
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature tests.test_pc_runner tests.test_orchestrator_role_gates tests.test_orchestrator_workflow_docs tests.test_docs_logs tests.test_pc_allowed_tests_check`
- Result: PASS (`80` tests)
- Verified:
  - reporter review is skipped when tester fails and the loop routes back through planner/patcher feedback.
  - invalid Allowed Tests now produce actionable feedback and retry within bounded `MAX_LOOPS` instead of immediate abort.
  - no-op conditions are written to the execution iteration log when a step has nothing to do.
  - plan-reviewer BLOCK behavior remains iterative (planner revises plan before patching) and still bounded by reviewer block limits.
  - max-loop exhaustion records actionable failure context in the execution log before exiting.

## 2026-02-07 - pc-commit allowed-untracked guard validation

- Command: `tools/offload-proxy/pp pre-commit run --files tools/pc-commit`
- Result: PASS
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature tests.test_pc_runner tests.test_orchestrator_role_gates tests.test_orchestrator_workflow_docs tests.test_docs_logs tests.test_pc_allowed_tests_check`
- Result: PASS (`80` tests)
- Verified:
  - `tools/pc-commit` no longer fails solely due to untracked files that are already covered by `--allow` path/prefix rules.
  - untracked files outside allowed scope still correctly fail commit guard.

- Validation completed; no issues reported.

## 2026-02-07 - Feature 10 closure validation

- Command: `tools/offload-proxy/pp pre-commit run --files docs/02-features/10-unified-autofix-precommit/feature-spec.md docs/02-features/10-unified-autofix-precommit/tech-design.md docs/02-features/10-unified-autofix-precommit/test-plan.md docs/02-features/10-unified-autofix-precommit/dev-tasks.md`
- Result: PASS
- Command: `tools/offload-proxy/pp git log --oneline refs/heads/main..refs/heads/feature-10-unified-autofix-precommit-patcher`
- Result: PASS (`5` commits identified and cherry-picked to `main`)
- Verified:
  - feature-10 documentation statuses are set to `Done`.
  - remaining feature-10 patcher worktree commits are now present on `main`.

## 2026-02-07 - main-freeze guard validation

- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- Result: PASS (`51` tests)
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature tests.test_pc_runner tests.test_orchestrator_role_gates tests.test_orchestrator_workflow_docs tests.test_docs_logs tests.test_pc_allowed_tests_check`
- Result: PASS (`82` tests)
- Verified:
  - `pc-feature` writes/maintains a locked `main` SHA marker in work-item notes.
  - resumed runs fail fast when locked SHA differs from current `refs/heads/main`.
  - execution loop records drift in iteration log and exits safely with `needs replan`.

## 2026-02-08 - Worktree-local runtime artifact validation

- Command: `python3 -m py_compile tools/pc-feature`
- Result: PASS
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- Result: PASS (`53` tests)
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_docs_logs`
- Result: PASS (`7` tests)
- Verified:
  - `pc-feature` resolves runtime `dev-tasks.md` and role logs from the patcher worktree path, not `main`.
  - runner log root is worktree-local (`<worktree>/logs/WI-...`) during execution.
  - reporter/tester failure loops now carry actionable failure context fields for planner/patcher retries.
  - anti-hardcode reviewer blocking remains enforced for high-risk/triggered work items while avoiding unconditional churn on low-risk doc-only work.
- Not run:
  - `make feature F=11` (explicitly skipped in this validation pass per workflow testing rule to avoid invoking `make feature` from the agent side).

## 2026-02-08 - Plan-policy gate hardening validation

- Command: `python3 -m py_compile tools/pc-feature`
- Result: PASS
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- Result: PASS (`56` tests)
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_docs_logs`
- Result: PASS (`7` tests)
- Verified:
  - plan-policy violations are detected pre-patcher (forbidden role-scoped/global-log paths and forbidden commands).
  - policy violations route through planner revision flow instead of invoking patcher directly.
  - patcher role-scope guard now blocks cross-feature role-scoped docs as well.
  - startup output exposes requested feature id and resolved feature slug for run-context visibility.
- Not run:
  - `make feature F=11` (per explicit workflow testing rule to not run `make feature` from agent side).

## 2026-02-08 - Template-sync validation

- Command: `tools/offload-proxy/pp tools/pc-template-sync`
- Result: PASS

## 2026-02-08 - Reviewer delta-guard validation

- Command: `python3 -m py_compile tools/pc-feature`
- Result: PASS
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- Result: PASS (`57` tests)
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_docs_logs`
- Result: PASS (`7` tests)
- Verified:
  - pre-existing unchanged dirty paths do not trigger reviewer-modified failures.
  - reviewer-introduced dirty deltas are still detected and blocked.
  - planner no-op note is recorded after reviewer verification, avoiding false attribution.
  - pre-review hygiene checkpoint remains scoped to planner-owned files and rejects unexpected paths.
- Not run:
  - `make feature F=12` (agent-side execution intentionally skipped per workflow test rule).

## 2026-02-08 - Template-sync mismatch fix validation

- Command: `tools/offload-proxy/pp tools/pc-template-sync`
- Result: PASS

## 2026-02-08 - Reviewer guard follow-up regression validation

- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- Result: PASS (`60` tests)
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_docs_logs`
- Result: PASS (`7` tests)
- Verified:
  - shared `main()` test harness stubs reviewer snapshot paths (`collect_dirty_snapshot`) and tuple-return guard contract.
  - deferred planner no-op iteration notes persist in `dev-tasks.md` when reviewer approves.
  - no `git status` lookups are attempted against non-repository temp directories in unit tests.

## 2026-02-08 - Auto-resume startup hardening validation

- Command: `python3 -m py_compile tools/pc-feature`
- Result: PASS
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- Result: PASS (`67` tests)
- Verified:
  - `RESUME_MODE` parsing supports `auto|prompt|fresh` with deterministic invalid-value failure.
  - existing in-progress feature worktrees auto-resume in `auto` mode without startup prompt.
  - startup blocks non-runtime dirty paths and parallel active feature worktrees.
  - dirty `dev-tasks.md` is checkpointed on resumable work items before preflight clean enforcement.
  - runs fail fast when dirty `dev-tasks.md` exists without an in-progress work item (`RESUME_MODE=fresh` remediation).
- Not run:
  - `make feature F=11` / `make feature F=12` (explicitly skipped per workflow testing rule to avoid agent-side `make feature` execution).

## 2026-02-08 - WIP-first startup resume validation

- Command: `python3 -m py_compile tools/pc-feature`
- Result: PASS
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- Result: PASS (`67` tests, offload id `f881e040b6009cc7e7f6f3b87492c3fd43034906a077903f968afa1ba9929dd8`)
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_docs_logs`
- Result: PASS (`7` tests)
- Verified:
  - startup dirty paths in an active feature worktree are checkpointed and execution continues.
  - startup no longer fails solely because dirty paths are outside runtime-doc subsets.
  - startup does not require explicit `RESUME_MODE=fresh` for dirty `dev-tasks.md` when continuing work.
  - protocol docs and template docs match WIP-preserving resume behavior.

## 2026-02-09 - Plan Reviewer first-class step hardening validation

- Command: `python3 -m py_compile tools/pc-feature`
- Result: PASS
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- Result: PASS (`70` tests, offload id `094029524d9cfaff8b7878b8f526d17db57095455be487f58b5e6f50929d761e`)
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_docs_logs`
- Result: PASS (`7` tests)
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_orchestrator_workflow_docs tests.test_update_reapply_templates_docs tests.test_orchestrator_role_gates tests.test_output_offload_enforcement_docs`
- Result: PASS (`25` tests)
- Command: `tools/offload-proxy/pp python3 -m unittest discover -s tests -p 'test_*.py'`
- Result: PASS (`134` tests, offload id `1c1dd26a9f0b8c4142a742a8816bdd79384b3489081c38ba2c2141e1272f0cab`)
- Verified:
  - Plan Reviewer is treated as a dedicated step with role-scoped artifact handling.
  - deterministic plan policy checks execute before LLM reviewer calls.
  - reporter scope/prompt and tester failure-context contract updates are covered by passing tests.
  - live docs and templates remain aligned after protocol/workflow updates.

## 2026-02-09 - Plan contract + reviewer loop guard validation

- Command: `python3 -m py_compile tools/pc-feature`
- Result: PASS
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_pc_feature`
- Result: PASS (offload id `2a67be91170b2e85c02d3fd7e1d1de399de5c50b6161407d4188cba9922d2029`)
- Command: `tools/offload-proxy/pp python3 -m unittest tests.test_orchestrator_workflow_docs tests.test_update_reapply_templates_docs tests.test_docs_logs tests.test_orchestrator_role_gates tests.test_output_offload_enforcement_docs`
- Result: PASS (`32` tests)
- Command: `tools/offload-proxy/pp python3 -m unittest discover -s tests -p 'test_*.py'`
- Result: PASS (offload id `2d6b4c2d7c605aeaf3d7cacef72346b98c9dd56fc3c348509052ee9a3141fe00`)
- Verified:
  - reviewer-block revised plans now replace prior plan content (no stale append carryover).
  - policy checks use contract `Files to change` section and still catch forbidden paths outside that section via fallback scan.
  - reviewer-block loop stops deterministically on reviewer cap, planner revision cap, or stagnation guard.
  - iteration logs expose per-loop counters for reviewer blocks, planner revisions, and execution attempts.
