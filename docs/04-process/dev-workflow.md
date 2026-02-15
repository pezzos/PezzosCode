# Development Workflow

> **Daily dev loop (human + LLM)**
>
> How we work together with AI to build features, fix bugs, and ship code. This is the playbook for productive human-LLM collaboration.

---

## Purpose

This document defines:

- **How humans and LLMs collaborate** on development
- **The daily workflow** from idea to production
- **Quality gates** and checks along the way
- **Tools and processes** we use

---

## Workflow Overview

```
Idea/Task → Plan → Implement → Test → Review → Deploy → Validate → Learn
     ↑                                                                ↓
     └────────────────────── Feedback Loop ─────────────────────────┘
```

For work item execution, follow the canonical protocol in `docs/04-process/ticket-execution-protocol.md`.
Prefer Serena for symbol-aware navigation and edits when available.
Execution is **Plan → Patch → Test → Report** (mandatory for every work item).

## Documentation Workflow (Template Bootstrapping)

Use this sequence when starting a new project with this template:

1. **Context first (`docs/00-context/`)**
   - Fill `vision.md`, `users.md`, `system-map.md`, and `assumptions.md`.
   - Ensure user definitions and boundaries are explicit.
2. **Product definition (`docs/01-product/prd.md`)**
   - Populate success metrics, non-goals, scope boundaries, and the prioritized feature list.
   - Tie each feature to user outcomes and context.
3. **Feature specs (`docs/02-features/`)**
   - For each P0/P1 feature, create a folder from the template.
   - Fully fill `feature-spec.md`, `tech-design.md`, `dev-tasks.md`, and `test-plan.md`.
4. **Validate completeness**
   - Confirm no TODOs remain in the generated feature docs.
   - Cross-check PRD scope against feature folders.

## Root File Sync (After Context/PRD Changes)

When project context or the PRD changes, update the live root files (e.g. `AGENTS.md`,
`.codex.toml`, `.serena/project.yml`) to match the real project. Use the
`sync-root-from-context` skill to read `docs/00-context/` and `docs/01-product/prd.md`,
then align the live root files without modifying templates.

## Work Item Scope (Hard Rule)

- **1 work item = 1 feature folder** (new feature spec, design, tasks, tests in `docs/02-features/<feature-name>/`)
- **or 1 mini change** (single, isolated change in existing feature or shared code)
- Work items are defined and tracked in `dev-tasks.md` with an execution log entry per loop.
- If the scope is bigger, split the feature into multiple smaller features before execution.

## Exact Steps (Per Work Item)

1. **Open/define work item**
   - Open `docs/02-features/<feature>/dev-tasks.md`.
   - Clarify scope and success criteria.
   - Confirm whether this is a _feature folder_ or _mini change_.
   - Add a new execution log entry header for the loop.
2. **Plan**
   - LLM proposes approach, files to change, risks, and tests.
   - Use the five-step workflow: data model → pure logic → edge cases → UI → integration.
   - **Plan Reviewer gate:** validate the plan before coding (no code edits).
   - **Orchestrator gate:** approve the plan before coding.
3. **Patch**
   - Make the smallest possible diff to satisfy the work item.
   - Self-review the diff and confirm scope correctness.
   - **Orchestrator gate:** approve the diff before running tests.
4. **Test**
   - Run the agreed tests and record results (use `pp` for noisy output).
   - Ensure logs are written to `logs/<WI>/<step>.log` with `[WI-...][agent][step]` prefix.
   - **Orchestrator gate:** validate test results before marking done.
5. **Report**
   - Summarize changes, commands run, and results.
   - Update logs and documentation.
   - If the run failed or stalled, roles propose workflow improvements in feedback fields and the orchestrator records a clarified, deduplicated entry in `docs/possible-improvements.md`.
   - Create commit with the agreed message format.
   - Run `make test` before closing the work item.

## Orchestrator Gates (Required)

- **Plan validation:** before any code changes (performed by Plan Reviewer, approved by Orchestrator).
- **Diff validation:** after changes, before tests or merge.
- **Test validation:** after tests run, before closing work item.

## Feedback Loop (Required)

- Tester writes failures in the execution log entry.
- Reporter reviews scope and completeness and records issues in the execution log entry.
- Planner updates the plan and Patcher updates the patch.
- On resume after tester `FAIL`, planner revises the existing `Plan` from feedback; do not regenerate a new plan when the plan section is already complete.
- Plan policy checks treat backticked `tools/pc-feature` references as file-path prose unless explicit command intent (run/execute/args) is present.
- Improvements are proposed by roles and persisted only by the orchestrator in `docs/possible-improvements.md`.
- Repeat until feedback is resolved and tests pass.

## Orchestrator + Roles (Parallel Mode)

Use separate sessions when parallelizing work. Use a single feature worktree by default:

- **Orchestrator:** keeps scope, approves gates, merges outputs.
- **Planner:** produces and updates the plan.
- **Plan Reviewer:** critiques/approves the plan (no code edits).
- **Patcher:** produces the patch.
- **Tester:** runs tests and reports failures.
- **Reporter:** reviews changes, checks scope, reports to PO.
- **Product Owner:** approves final report and scope changes.

Preferred worktree naming: `../<repo_name>-<feature_name>-<agent_name>`.

Use `prompts/<role>.md` and task variants like `prompts/<role>-<task>.md` (for example `plan-reviewer-gate`, `patcher-apply`, `planner-update_from_feedback`) for role-specific instructions.
If a prompt file is missing, restore it under `prompts/` and rerun the step (prompt loading is file-based only). In template-enabled repos, copy from `tools/templates/prompts/`; in living-only bootstrap repos, re-run bootstrap from the source tooling repo.

Role worktree scope:

- Planner writes only `docs/02-features/<feature>/planner-log.md`.
- Plan Reviewer writes only `docs/02-features/<feature>/plan-reviewer-log.md`.
- Tester writes only `docs/02-features/<feature>/validation-log.md`.
- Reporter writes only `docs/02-features/<feature>/reporter-log.md`.
- Patcher can edit anywhere except the role-scoped log files.
- Orchestrator uses a single worktree per feature and squashes all role outputs into `main`.

---

## Phase 1: Planning

### Human Responsibilities

1. **Define the problem**
   - What are we trying to solve?
   - Who is this for?
   - Why does it matter?

2. **Set success criteria**
   - How will we know it works?
   - What metrics matter?

3. **Clarify constraints**
   - Timeline/deadline
   - Technical limitations
   - Must-haves vs nice-to-haves

### LLM Responsibilities

1. **Ask clarifying questions**
   - Surface ambiguities
   - Identify missing requirements
   - Challenge assumptions

2. **Research the codebase**
   - Find relevant existing code
   - Identify patterns to follow
   - Surface potential conflicts

3. **Propose approach**
   - Suggest implementation strategy
   - Identify files to change
   - Estimate scope and complexity

### Outputs

- [ ] Feature spec or clear task description
- [ ] Technical approach agreed upon
- [ ] Success criteria defined
- [ ] Files/areas of codebase identified

---

## Phase 2: Implementation

### LLM Responsibilities

1. **Write code**
   - Follow existing patterns
   - Write self-documenting code
   - Include helpful comments for complex logic
   - Think about edge cases

2. **Write tests**
   - Unit tests for logic
   - Integration tests for APIs
   - E2E tests for critical paths
   - Test edge cases and errors

3. **Update documentation**
   - Update relevant docs (API docs, README, etc.)
   - Add code comments where needed
   - Update system map if architecture changes

### Human Responsibilities

1. **Review code as it's written**
   - Check approach makes sense
   - Verify edge cases considered
   - Ensure code is readable

2. **Test manually**
   - Try the feature in browser/app
   - Look for UX issues
   - Verify it solves the problem

3. **Provide feedback**
   - Request changes if needed
   - Clarify requirements if misunderstood

### Quality Checks

- [ ] Code follows existing patterns
- [ ] Tests cover main paths and edge cases
- [ ] No security vulnerabilities (injection, XSS, etc.)
- [ ] Performance is acceptable
- [ ] Code is readable and maintainable
- [ ] Documentation updated

---

## Phase 3: Testing

### Automated Testing

**Unit Tests**

- Test individual functions/components
- Mock dependencies
- Fast and focused

**Integration Tests**

- Test component interactions
- Test API endpoints
- Use test database

**E2E Tests**

- Test critical user flows
- Run in real browser
- Catch integration issues

### Manual Testing

**Developer Testing**

- Test happy path
- Test error cases
- Test edge cases
- Test on different browsers/devices (if UI)

**QA Testing** (if applicable)

- Follow test plan
- Exploratory testing
- Accessibility testing
- Performance testing

### Checklist

- [ ] All tests passing
- [ ] Manual testing complete
- [ ] No console errors
- [ ] Accessibility verified (keyboard nav, screen reader)
- [ ] Responsive design works (if UI)
- [ ] Performance acceptable

---

## Phase 4: Code Review

### Before Requesting Review

- [ ] Code is complete
- [ ] Tests are passing
- [ ] Self-review done (read your own code)
- [ ] Documentation updated
- [ ] PR description explains what/why

### PR Description Template

```markdown
## What

[Brief description of what changed]

## Why

[Why we made this change]

## How

[Technical approach, key decisions]

## Testing

- [ ] Unit tests added/updated
- [ ] Manual testing done
- [ ] E2E tests added/updated (if applicable)

## Screenshots (if UI changes)

[Screenshots of before/after]

## Checklist

- [ ] Code follows style guide
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No new security issues
- [ ] Performance impact considered
```

### Code Review Guidelines

**What to Look For:**

- **Correctness:** Does the code do what it's supposed to?
- **Tests:** Are edge cases covered?
- **Readability:** Can you understand it?
- **Maintainability:** Can it be changed easily later?
- **Performance:** Are there obvious inefficiencies?
- **Security:** Any vulnerabilities?

**Good Feedback:**

- Be specific: "This function could be simplified" + example
- Explain why: "This approach might cause race conditions because..."
- Ask questions: "What happens if this API call fails?"
- Praise good work: "Nice abstraction, this is very readable"

**Review Checklist:**

- [ ] Logic is correct
- [ ] Tests are comprehensive
- [ ] Code is readable
- [ ] No security issues
- [ ] No performance issues
- [ ] Documentation updated
- [ ] Follows existing patterns

---

## Phase 5: Deployment

### Pre-Deployment

- [ ] All tests passing in CI
- [ ] Code review approved
- [ ] Branch is up-to-date with main
- [ ] Feature flag configured (if needed)

### Deployment Process

**1. Merge to Main**

```bash
git checkout main
git pull origin main
git merge feature-branch
git push origin main
```

**2. Deploy to Staging**

- Automated via CI/CD
- Verify deployment succeeded
- Smoke test on staging

**3. Deploy to Production**

- Automated via CI/CD (or manual trigger)
- Monitor deployment
- Verify health checks passing

**4. Enable Feature** (if behind feature flag)

- Start with internal users (0-1%)
- Gradual rollout (1% → 10% → 50% → 100%)
- Monitor metrics and errors at each step

### Post-Deployment

- [ ] Feature works in production
- [ ] No spike in errors
- [ ] Metrics look healthy
- [ ] Rollback plan ready if needed

---

## Phase 6: Validation

### Immediate (First Hour)

- Monitor error rates
- Check performance metrics
- Watch for user complaints
- Verify analytics tracking

### Short Term (First Week)

- Track feature usage
- Monitor success metrics
- Collect user feedback
- Watch for unexpected behavior

### Long Term (First Month)

- Analyze impact on key metrics
- Compare to success criteria
- Identify improvements needed
- Document learnings

### Update Logs

- [ ] Implementation log updated (what we built)
- [ ] Validation log updated (what actually happened)
- [ ] Bug log updated (if bugs found)
- [ ] Insights updated (what we learned)

---

## Phase 7: Iteration

### Based on Validation

- Did we hit our goals? If not, why?
- What's working well?
- What needs improvement?
- What did we learn?

### Next Steps

- Bug fixes (if needed)
- Improvements based on feedback
- New features based on usage patterns
- Documentation of learnings

---

## Human-LLM Collaboration Tips

### When to Use LLM

**Great for LLM:**

- Writing boilerplate code
- Generating tests
- Refactoring code
- Finding bugs
- Explaining complex code
- Suggesting approaches
- Researching codebase

**Not Great for LLM:**

- Making product decisions
- Understanding user needs (without context)
- Creative problem solving requiring deep domain knowledge
- Evaluating trade-offs without guidance

### How to Prompt LLM Effectively

**Be Specific:**

- ❌ "Add a feature for users"
- ✅ "Add a button to the user profile page that lets users export their data as CSV"

**Provide Context:**

- Link to relevant docs
- Share existing patterns to follow
- Explain why you need this
- Define success criteria

**Iterate:**

- Start with plan, get feedback
- Implement incrementally
- Review and refine
- Test thoroughly

**Examples of Good Prompts:**

```
"I need to add a new API endpoint for exporting user data.
It should:
- Require authentication
- Return CSV format
- Include all user data except passwords
- Follow the same pattern as the /api/users/:id endpoint
Can you create a plan for this?"
```

```
"This function is hard to read. Can you refactor it to be
more clear? Keep the same functionality, but break it into
smaller functions with descriptive names."
```

```
"I'm getting a race condition bug in the checkout flow.
When users click submit twice quickly, we create two orders.
Can you help me debug and fix this?"
```

---

## Tools We Use

### Development

- **IDE:** [Your IDE]
- **Version Control:** Git + GitHub/GitLab
- **Package Manager:** [npm/yarn/pnpm/etc]
- **Build Tool:** [Vite/webpack/etc]

### Testing

- **Unit Tests:** [Jest/Vitest/pytest/etc]
- **E2E Tests:** [Playwright/Cypress/etc]
- **Test Coverage:** [Coverage tool]

### CI/CD

- **CI Platform:** [GitHub Actions/CircleCI/etc]
- **Deployment:** [Vercel/AWS/etc]
- **Monitoring:** [Sentry/Datadog/etc]

### Documentation

- **Docs:** This `/docs` folder
- **API Docs:** [Swagger/Postman/etc]
- **Architecture:** System map in `/docs/00-context/`

### LLM Tools

- **Coding Assistant:** [GitHub Copilot/Claude/etc]
- **Chat Interface:** [ChatGPT/Claude/etc]
- **Code Review:** [AI-assisted review tool if any]

---

## Emergency Procedures

### Production Bug

**1. Assess Severity**

- Critical (all users affected, data loss): Fix immediately
- High (major feature broken): Fix within hours
- Medium (minor feature issue): Fix within day
- Low (cosmetic issue): Fix in next sprint

**2. Immediate Action**

- Rollback if possible and safe
- Add monitoring/logging if needed
- Communicate to team/users

**3. Fix**

- Reproduce bug
- Find root cause
- Write test that catches bug
- Fix bug
- Verify fix works
- Deploy fix

**4. Post-Mortem**

- Document in bug log
- Identify why it wasn't caught
- Add prevention measures
- Update processes if needed

---

### Rollback Procedure

**When to Rollback:**

- Error rate spikes significantly
- Critical feature broken
- Security vulnerability discovered
- Performance degradation severe

**How to Rollback:**

```bash
# If using feature flag
Set feature flag to 0% in admin panel

# If need to revert deploy
git revert [commit-hash]
git push origin main
# Trigger deployment

# If database migration
Run down migration
Verify data integrity
```

**After Rollback:**

- Communicate to team
- Investigate root cause
- Fix issue
- Re-deploy with fix

---

## Definition of Done

A task is "done" when:

- [ ] Code is written and reviewed
- [ ] Tests are written and passing
- [ ] Manually tested and verified
- [ ] Documentation updated
- [ ] Deployed to production
- [ ] Feature flag enabled (if applicable)
- [ ] Metrics tracking working
- [ ] Team informed
- [ ] Logs updated

See [definition-of-done.md](definition-of-done.md) for details.

---

## Related Documents

- [Definition of Done](definition-of-done.md)
- [LLM Prompts](llm-prompts.md)
- [Testing Strategy](../02-features/*/test-plan.md)
- [Deployment Guide](../00-context/system-map.md)

<!-- PezzosCode bootstrap sha256:1bc8a192f3c2d28c12eca2bd747cdd65f13a9ebb4e1674b789f40917262c8c78 -->
