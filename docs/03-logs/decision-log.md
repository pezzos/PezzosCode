# Decision Log

> **Architectural & product decisions**
>
> A record of significant decisions, the context in which they were made, alternatives considered, and outcomes. This prevents revisiting old debates and helps understand why things are the way they are.

---

## Purpose

This log captures:

- **Major technical decisions** (architecture, frameworks, tools)
- **Product decisions** (features, priorities, scope)
- **Process decisions** (workflows, policies)

For each decision, we document:

- The context and problem
- Options considered
- Decision made and rationale
- Expected outcomes
- Actual outcomes (after implementation)

---

## Decision Template

### [DEC-XXX] - [Decision Title]

**Date:** YYYY-MM-DD

**Status:** [Proposed | Accepted | Implemented | Superseded]

**Decision Makers:** [Who was involved]

**Context:**
[What situation led to this decision? What problem are we solving?]

**Problem Statement:**
[Clear description of the problem or question]

**Options Considered:**

#### Option 1: [Name]

**Description:** [What this option entails]

**Pros:**

- [Benefit 1]
- [Benefit 2]

**Cons:**

- [Drawback 1]
- [Drawback 2]

**Estimated effort:** [time/complexity]

#### Option 2: [Name]

**Description:** [What this option entails]

**Pros:**

- [Benefit 1]
- [Benefit 2]

**Cons:**

- [Drawback 1]
- [Drawback 2]

**Estimated effort:** [time/complexity]

#### Option 3: [Name]

[Same format...]

**Decision:**
We chose **Option [X]: [Name]**

**Rationale:**
[Why we chose this option over the others. Key factors that influenced the decision.]

**Implications:**

- [What this means for the codebase]
- [What this means for the team]
- [What this means for users]

**Success Criteria:**

- [How we'll know if this was the right decision]
- [Metrics to track]

**Review Date:** [When we'll revisit this decision]

**Actual Outcome:** _[Fill in after implementation]_
[What actually happened? Was the decision correct? What would we do differently?]

---

## Decisions

### [DEC-006] - Dev-tasks as execution source with role loop

**Date:** 2026-02-04

**Status:** Superseded

**Decision Makers:** Alexandre Pezzotta

**Context:**
Per-task ticket files duplicate Plan/Patch/Test/Report scaffolding already present in feature dev-tasks and the execution protocol.

**Problem Statement:**
How do we reduce duplicated ticket overhead while preserving traceability, ownership, and workflow rigor?

**Options Considered:**

#### Option 1: Keep per-task ticket files

**Pros:**

- Clear, separate artifacts per task
- Existing tooling compatibility

**Cons:**

- Duplicated process overhead
- Repeated Plan/Patch/Test/Report scaffolding

**Estimated effort:** Ongoing overhead per task

#### Option 2: Use dev-tasks as the single execution source of truth

**Pros:**

- Single place to plan, execute, and log
- Less duplication and faster iteration

**Cons:**

- Requires explicit execution log and role ownership fields
- Some tools may still expect ticket wrappers

**Estimated effort:** Moderate doc/process updates

#### Option 3: Hybrid (dev-tasks source, tickets optional)

**Pros:**

- Minimizes duplication
- Preserves compatibility when tools require `TASK-XXX.md`

**Cons:**

- Requires clear rules on when tickets are created

**Estimated effort:** Low to moderate

**Decision:**
We chose **Option 3: Hybrid (dev-tasks source, tickets optional)**.

**Rationale:**
This preserves traceability via dev-tasks execution logs while removing unnecessary per-task ticket overhead. Optional ticket wrappers remain available for tooling compatibility.

**Implications:**

- `dev-tasks.md` is the execution source of truth.
- Execution logs capture Planner/Patcher/Tester/Reporter roles and outcomes.
- `TASK-XXX.md` files are optional and only created when required by tools.

**Success Criteria:**

- Fewer duplicated process steps without losing auditability.
- Clear role handoffs captured inside dev-tasks execution logs.

**Review Date:** 2026-03-04

**Actual Outcome:** Superseded by DEC-008 (remove ticket wrappers and ticket-generation workflow).

### [DEC-007] - Split oversized work into smaller features before execution

**Date:** 2026-02-04

**Status:** Accepted

**Decision Makers:** Alexandre Pezzotta

**Context:**
Avoiding multiple execution formats (dev-tasks vs optional ticket wrappers) is easiest when each feature is small enough to execute as a single work item.

**Problem Statement:**
How do we eliminate conditional handling of oversized work items while keeping the workflow uniform?

**Options Considered:**

#### Option 1: Split oversized work into multiple work items at execution time

**Pros:**

- Keeps feature list unchanged

**Cons:**

- Increases execution-time branching and ambiguity
- Encourages multiple formats and handoff complexity

**Estimated effort:** Ongoing overhead per large feature

#### Option 2: Split oversized features before execution

**Pros:**

- Uniform execution workflow
- No conditional handling at execution time
- Clearer, smaller feature scopes

**Cons:**

- Requires earlier planning effort

**Estimated effort:** Moderate upfront planning

**Decision:**
We chose **Option 2: Split oversized features before execution**.

**Rationale:**
This keeps execution uniform and avoids handling multiple work-item formats during implementation.

**Implications:**

- Features must be sized to a single work item.
- Oversized features are split during PRD/feature definition.

**Success Criteria:**

- Execution workflow requires no conditional handling for oversized work.
- Feature scopes stay consistently small and actionable.

**Review Date:** 2026-03-04

**Actual Outcome:** _Pending_

### [DEC-008] - Remove ticket wrappers and ticket-generation workflow

**Date:** 2026-02-04

**Status:** Accepted

**Decision Makers:** Alexandre Pezzotta

**Context:**
With `dev-tasks.md` as the execution source of truth and `make feature` replacing `make ticket`, ticket wrappers and ticket-generation add no value.

**Problem Statement:**
Should we keep `TASK-###.md` wrappers and the `feature-tasks-to-tickets` workflow when they are no longer used by execution tooling?

**Options Considered:**

#### Option 1: Keep ticket wrappers for legacy compatibility

**Pros:**

- Preserves historical workflow

**Cons:**

- Adds unused artifacts
- Increases maintenance overhead

**Estimated effort:** Ongoing overhead

#### Option 2: Remove ticket wrappers and ticket-generation workflow

**Pros:**

- Simplifies documentation and execution flow
- Removes unused artifacts

**Cons:**

- Requires updating references in docs/templates

**Estimated effort:** Low to moderate

**Decision:**
We chose **Option 2: Remove ticket wrappers and ticket-generation workflow**.

**Rationale:**
Ticket wrappers are no longer used by the execution path and introduce unnecessary complexity.

**Implications:**

- `feature-tasks-to-tickets` is removed from docs and tooling guidance.
- `TASK-###.md` is no longer part of the workflow.
- `pc-ticket`/`ticket-bootstrap` tooling is removed in favor of `pc-feature`.

**Success Criteria:**

- No workflow references require ticket wrappers.
- Execution relies only on `dev-tasks.md`.

**Review Date:** 2026-03-04

**Actual Outcome:** _Pending_

### [DEC-009] - Enforce role-scoped worktree logs and auto-collect into main

**Date:** 2026-02-04

**Status:** Accepted

**Decision Makers:** Alexandre Pezzotta

**Context:**
`make feature` now orchestrates planner/patcher/tester/reporter in separate worktrees, but changes are scattered and unclear to merge.

**Problem Statement:**
How do we prevent cross-role file edits, ensure a single reviewable commit, and clean up worktrees automatically?

**Options Considered:**

#### Option 1: Manual merge and manual worktree cleanup

**Pros:**

- Simple to implement

**Cons:**

- Error-prone, inconsistent
- Leaves stray worktrees/branches

**Estimated effort:** Low upfront, high ongoing

#### Option 2: Enforce role-scoped logs + automated collector into `main`

**Pros:**

- Deterministic, audit-friendly
- Keeps `main` as the single source of truth
- Single commit for review

**Cons:**

- Requires tooling updates
- Strict scope enforcement can block some workflows

**Estimated effort:** Moderate

**Decision:**
We chose **Option 2: Enforce role-scoped logs + automated collector into `main`**.

**Rationale:**
Clear ownership boundaries and automated consolidation reduce integration overhead and keep reviews focused.

**Implications:**

- Planner/tester/reporter can only write their feature log files.
- Patcher must not touch those files.
- Worktrees are tracked in `feature-worktrees.json` and removed after success.
- All role changes are squashed into one commit on `main`.

**Success Criteria:**

- `make feature` ends with one commit on `main`.
- No out-of-scope edits from non-patcher roles.
- Worktrees are cleaned up automatically.

**Review Date:** 2026-03-04

**Actual Outcome:** _Pending_

### [DEC-004] - Codex-first workflow upgrades (plan/patch/test/report + orchestration)

**Date:** 2026-02-02

**Status:** Accepted

**Decision Makers:** Alexandre Pezzotta

**Context:**
Solo dev needs fewer context mistakes, lower token waste, and predictable guardrails when using Codex across template and project repos.

**Problem Statement:**
How do we standardize execution to reduce drift, keep outputs clean, and enable parallel roles without contaminating workspaces?

**Options Considered:**

#### Option 1: Keep current workflow guidance

**Pros:**

- Minimal doc changes

**Cons:**

- Inconsistent execution, higher risk of context drift and noisy outputs

#### Option 2: Codify strict plan/patch/test/report + orchestration + offload

**Pros:**

- Deterministic workflow and clearer gates
- Lower token waste via output offload
- Parallel roles via worktrees

**Cons:**

- Slightly more process overhead

**Decision:**
Adopt **Option 2** across process and context docs.

**Rationale:**
The added structure is lightweight but materially improves repeatability, quality gates, and context hygiene for solo, multi-role workflows.

**Implications:**

- Plan → Patch → Test → Report is mandatory for tickets.
- Worktrees are the default for parallel roles.
- Large outputs are offloaded via `pp`.

**Success Criteria:**

- Fewer context mistakes between template and project repos.
- Reduced token usage from large outputs.
- Consistent, repeatable outcomes across sessions.

**Review Date:** 2026-03-02

**Actual Outcome:** _Pending_

### [DEC-005] - Enforce output offload gating compliance

**Date:** 2026-02-03

**Status:** Accepted

**Decision Makers:** Alexandre Pezzotta

**Context:**
The Execute ticket workflow and PO loop already define Plan → Patch → Test → Report, but the new docs regression checks require every gate to mention the offload workflow and the decision to enforce it.

**Problem Statement:**
How do we ensure noisy/megasized outputs always go through `tools/offload-proxy/pp`, that gating decisions reference recorded compliance, and that ticket logs reflect the enforced workflow?

**Options Considered:**

#### Option 1: Leave offload enforcement implicit

**Description:** Trust authors to mention offload handling where convenient and keep the decision log quiet unless there is a major policy change.

**Pros:**

- Minimal documentation work

**Cons:**

- Regression tests will keep failing because the workflow is not explicitly documented at each gate.
- Compliance decisions remain scattered and hard to audit.

**Estimated effort:** Minimal documentation edits, but insufficient.

#### Option 2: Explicitly tie offload enforcement to ticket execution gates and record the decision

**Description:** Update the ticket protocol, PO loop, and decision log so every gate references `tools/offload-proxy/pp` and the decision to enforce it, making compliance auditable before progressing.

**Pros:**

- Tests pass because the mandated wording is now in place.
- Decision log provides an authoritative audit trail for offload enforcement.
- Implementers and the PO loop share a single source of truth about how offload violations are handled.

**Cons:**

- Requires precise doc updates and a decision log entry, but the scope is limited to process documentation.

**Estimated effort:** A few targeted documentation edits plus the log entry.

**Decision:**
We chose **Option 2**: enforce the offload workflow at every gate with `tools/offload-proxy/pp` and explicitly link the compliance decision to the ticket execution protocol.

**Rationale:**
The regression tests make it clear that only explicit wording counts, so we need a documented decision and workflow mention to prevent repeated failures and to keep the PO loop in sync with compliance checks.

**Implications:**

- The PO loop now routes offload violations through `docs/03-logs/decision-log.md` before allowing the next step.
- Enforce the output offload workflow with tools/offload-proxy/pp at each gate and capture compliance decisions in docs/03-logs/decision-log.md.
- Documented the decision to enforce output offload via tools/offload-proxy/pp and link it to work item execution workflow gates.

**Success Criteria:**

- Tests that sweep the workflow docs now pass because the gating and offload phrases exist.
- PO loop and ticket protocol reference `tools/offload-proxy/pp` and the decision log entry before moving forward.

**Review Date:** 2026-03-03

**Actual Outcome:** _Pending_

### [DEC-006] - Orchestrator gating traceability

**Date:** 2026-02-04

**Status:** Accepted

**Decision Makers:** Alexandre Pezzotta

**Context:**
The orchestrator/sub-agent workflow now enforces gate handoff checks at every step, and the regression tests require these transitions to be recorded before the PO loop advances.

**Problem Statement:**
How do we make gate handoffs traceable so that the PO loop, automation, and documentation remain synchronized with the orchestrator’s control flow?

**Options Considered:**

#### Option 1: Keep gating traceability implicit in the workflow docs

**Description:** Trust implementers and the PO loop to remember to log the gate handoffs without a dedicated callout.

**Pros:**

- Minimal documentation work

**Cons:**

- Tests and reviewers will continue to fail because the exact wording linking gates to the logs is missing.
- It’s impossible to audit whether the orchestrator actually logged each transition.

#### Option 2: Explicitly record every gate handoff in the decision and validation logs before the PO loop continues and cite the approach in the process docs

**Description:** Update the human orchestration workflow, execution protocol, and regression expectations so they all point to `docs/03-logs/decision-log.md` and `docs/03-logs/validation-log.md` as the gate artifacts.

**Pros:**

- Ensures the regression tests can find the required phrases.
- Creates an auditable trail of each orchestrator gate handoff.
- Keeps implementers and reviewers aligned around the same traceability chain.

**Cons:**

- Requires small doc updates and an entry in the decision log.

**Decision:**
We chose **Option 2** to record every gate handoff in the decision and validation logs before the PO loop continues so the orchestrator’s traceability obligations stay explicit.

**Rationale:**
The orchestration docs and tests explicitly complain when the gate log references are missing, so documenting and enforcing the logs prevents repeated failures and makes the gate ownership visible to the PO loop.

**Implications:**

- The human orchestration workflow and ticket execution protocol now point to the gate logs before progressing.
- Each gate handoff is noted in `docs/03-logs/decision-log.md` and `docs/03-logs/validation-log.md`.
- Regression tests that look for the gate-to-log language now have deterministic, documented references.

**Success Criteria:**

- The orchestrator gating docs mention `docs/03-logs/decision-log.md` and `docs/03-logs/validation-log.md` before the PO loop advances.
- Tests no longer fail due to missing gate handoff traceability language.

**Review Date:** 2026-03-04

**Actual Outcome:** _Pending_

### [DEC-002] - Force early LSP override load via shell env + add ping diagnostics

**Date:** 2026-01-31

**Status:** Implemented

**Decision Makers:** Alexandre Pezzotta

**Context:**
Taplo (and previously YAML) sometimes reported `workspace/configuration` not handled before Serena’s log initialization, indicating the override env from `.codex.toml` was applied too late.

**Problem Statement:**
How do we ensure LSP overrides load before any language server startup, and how do we verify config handling without restarting?

**Options Considered:**

#### Option 1: Keep only `.codex.toml` env

**Pros:**

- Centralized per-project config

**Cons:**

- Loads after Codex starts; too late for earliest LSP startup messages

#### Option 2: Export override env in shell startup

**Pros:**

- Applies before Codex launches
- Eliminates early-start race

**Cons:**

- Global to shell sessions

#### Option 3: Add import banner and manual ping diagnostics

**Pros:**

- Confirms early-load behavior
- Allows in-session verification

**Cons:**

- Adds minor diagnostic code

**Decision:**
We chose **Option 2 + Option 3**: export override env in shell startup, and add an opt-in import banner + ping mechanism.

**Rationale:**
The failure happens before `.codex.toml` applies, so shell env is the earliest reliable injection point. Diagnostics allow validation without restart.

**Implications:**

- Override must be present in shell env for earliest LSP startup
- Use ping files to verify config handler behavior on demand

**Success Criteria:**

- No `workspace/configuration not handled` errors on startup
- Ping logs confirm handler execution in-session

**Review Date:** 2026-02-14

**Actual Outcome:** _Pending_

### [DEC-001] - Choice of Frontend Framework

**Date:** 2025-01-10

**Status:** Accepted

**Decision Makers:** Engineering team, CTO

**Context:**
Starting a new web application. Need to choose a frontend framework that will support rapid development, good performance, and easy maintenance over the next 3-5 years.

**Problem Statement:**
Which frontend framework should we use for the new application?

**Options Considered:**

#### Option 1: React

**Description:** Use React with TypeScript, Vite for build tooling, and React Router

**Pros:**

- Largest ecosystem and community
- Team has most experience with React
- Extensive library of components and tools
- Great TypeScript support
- Backed by Meta, stable long-term

**Cons:**

- More boilerplate than some alternatives
- Need to make many tool choices (routing, state management, etc.)
- Bundle sizes can be large

**Estimated effort:** Low (team familiar)

#### Option 2: Vue 3

**Description:** Use Vue 3 with Composition API and TypeScript

**Pros:**

- More opinionated, fewer decisions to make
- Excellent documentation
- Good performance
- Built-in routing and state management

**Cons:**

- Team less familiar (learning curve)
- Smaller ecosystem than React
- Less corporate backing

**Estimated effort:** Medium (learning curve)

#### Option 3: Svelte

**Description:** Use SvelteKit for full-stack application

**Pros:**

- Best performance (compile-time optimization)
- Smallest bundle sizes
- Less boilerplate, more concise code
- Growing ecosystem

**Cons:**

- Smallest ecosystem of the three
- Team has no experience
- Fewer component libraries available
- Less proven in production at scale

**Estimated effort:** High (learning curve + ecosystem)

**Decision:**
We chose **Option 1: React**

**Rationale:**

- **Team velocity:** Team is already proficient, allowing faster development
- **Hiring:** Easier to find React developers
- **Ecosystem:** Need specific libraries (react-three-fiber, recharts) that don't have equivalents in other frameworks
- **Risk:** Lower risk than betting on team learning new framework under deadline
- **Trade-off:** Accepting larger bundle sizes for speed of development

While Svelte is technically superior in performance, the team expertise and ecosystem advantages of React outweigh the performance gains for our use case.

**Implications:**

- Use React 18 with TypeScript
- Use Vite for build tooling (faster than webpack)
- Adopt React Router v6 for routing
- Use Zustand for state management (lighter than Redux)
- Budget for bundle size optimization later

**Success Criteria:**

- Team can build features without blockers
- Can hire React developers easily
- Application performance meets targets (< 3s load time)

**Review Date:** 2026-01-10 (or when starting next major project)

**Actual Outcome:** _[To be filled after 6 months]_

---

### [DEC-002] - Database Choice

**Date:** 2025-01-12

**Status:** Accepted

**Decision Makers:** Backend team lead, CTO

**Context:**
Need to choose a database for the application. Data model is relational with some document-like structures. Expected scale is 100K users in first year, 1M in three years.

**Problem Statement:**
Which database should we use?

**Options Considered:**

#### Option 1: PostgreSQL

**Pros:**

- Excellent for relational data
- JSONB support for flexible schemas
- Strong ACID guarantees
- Great tooling and extensions
- Team familiar with SQL

**Cons:**

- Vertical scaling limits eventually
- More complex clustering than some alternatives

#### Option 2: MongoDB

**Pros:**

- Flexible schema
- Horizontal scaling built-in
- Good for rapid iteration
- JSON-native

**Cons:**

- Weaker consistency guarantees
- Team less familiar
- Requires learning new query language
- Harder to enforce data integrity

**Decision:**
We chose **Option 1: PostgreSQL**

**Rationale:**

- Data model is fundamentally relational (users, projects, permissions)
- Need strong consistency for billing and permissions
- JSONB gives us flexibility where needed
- Team SQL expertise reduces risk
- Can scale to our target size easily
- Better tooling for migrations and backups

**Implications:**

- Use PostgreSQL 15+
- Use Prisma as ORM for type safety
- Plan for read replicas at scale
- Use JSONB for configuration and metadata fields

**Success Criteria:**

- Query performance < 100ms for 95th percentile
- Can handle 1000 concurrent users
- Easy to maintain and debug

**Review Date:** 2026-06-01

**Actual Outcome:** _[To be filled]_

---

### [DEC-003] - Authentication Strategy

**Date:** 2025-01-14

**Status:** Proposed

**Decision Makers:** Security team, backend lead

**Context:**
Need to implement user authentication. Must support email/password and social logins. May need enterprise SSO in future.

**Problem Statement:**
Should we build authentication ourselves or use a service?

**Options Considered:**

#### Option 1: Build Custom (JWT + OAuth)

**Pros:**

- Full control
- No third-party costs
- Can customize completely

**Cons:**

- Security risk if we get it wrong
- Significant development time
- Ongoing maintenance burden
- Hard to add features like MFA, SSO

**Estimated effort:** 3-4 weeks

#### Option 2: Use Auth0 / Okta

**Pros:**

- Battle-tested security
- Built-in features (MFA, SSO, etc.)
- Quick to implement
- Compliance certifications

**Cons:**

- Monthly costs ($200-1000/month)
- Vendor lock-in
- Less customization
- Dependency on third party

**Estimated effort:** 1 week

#### Option 3: Use Supabase Auth

**Pros:**

- Open source, can self-host later
- Good developer experience
- Includes database (PostgreSQL)
- Lower cost than Auth0

**Cons:**

- Newer, less proven than Auth0
- Smaller ecosystem
- Tighter coupling with Supabase

**Estimated effort:** 1 week

**Decision:**
We chose **Option 2: Auth0**

**Rationale:**

- **Security:** Authentication is too critical to risk getting wrong
- **Time to market:** 2-3 weeks saved vs building custom
- **Features:** Will need MFA and SSO within a year
- **Compliance:** Auth0's certifications help with enterprise sales
- **Cost:** $500/month acceptable given engineering time saved
- **Flexibility:** Can migrate to custom later if needed (using standard protocols)

**Implications:**

- Integrate Auth0 SDK in frontend
- Use Auth0 middleware in backend
- Plan for webhook handling (user events)
- Budget for Auth0 costs

**Success Criteria:**

- Users can sign up and login within 1 week
- Support email/password and Google OAuth
- 99.9% uptime on auth

**Review Date:** 2025-07-01

**Actual Outcome:** _[To be filled]_

---

## Decision Categories

### Technical Architecture

| ID      | Decision           | Date       | Status   |
| ------- | ------------------ | ---------- | -------- |
| DEC-001 | Frontend framework | 2025-01-10 | Accepted |
| DEC-002 | Database choice    | 2025-01-12 | Accepted |

### Product Strategy

| ID        | Decision        | Date       | Status   |
| --------- | --------------- | ---------- | -------- |
| [DEC-XXX] | [Decision name] | YYYY-MM-DD | [Status] |

### Process & Workflow

| ID        | Decision        | Date       | Status   |
| --------- | --------------- | ---------- | -------- |
| [DEC-XXX] | [Decision name] | YYYY-MM-DD | [Status] |

---

## Superseded Decisions

When a decision is reversed or replaced, document it here:

### [DEC-XXX] - [Original Decision]

**Originally decided:** [Date]
**Superseded by:** [DEC-XXX] on [Date]
**Reason for change:** [Why we changed our minds]
**Learning:** [What we learned from this change]

---

## Decision Review Schedule

| Decision ID | Next Review Date | Owner            |
| ----------- | ---------------- | ---------------- |
| DEC-001     | 2026-01-10       | Engineering Lead |
| DEC-002     | 2026-06-01       | Backend Lead     |

---

## Related Documents

- [Implementation Log](implementation-log.md) - Code changes
- [Insights](insights.md) - Learnings from decisions
- [Tech Design docs](../02-features/) - Feature-level decisions
