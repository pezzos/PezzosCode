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

### [DEC-074] - Add dedicated Codex profiles for prepare-features Architect/UX/PM roles

**Date:** 2026-02-18

**Status:** Implemented

**Decision:**
Define dedicated `.codex.toml` profiles for prepare roles (`Architect`, `UXUI`, `ProductManager`) in both live and template config files, and route `tools/pc-prepare-features` default role execution to those profile names.

**Rationale:**
Prepare-features role prompts are semantically distinct from Planner/PlanReviewer duties. Dedicated profile names improve role clarity, allow future tuning without cross-role coupling, and align prepare role identity with existing named-role profile conventions.

**Implications:**

- `pc-prepare-features` defaults are now:
  - Architect step -> `Architect`
  - UX step -> `UXUI`
  - Product Manager gate -> `ProductManager`
- Existing environment overrides (`PREPARE_ARCHITECT_PROFILE`, `PREPARE_UX_PROFILE`, `PREPARE_PM_PROFILE`) remain supported.
- Template-generated repos inherit the same prepare-role profile set.

### [DEC-073] - Carry PM retry context into Architect/UX prepare-role prompts

**Date:** 2026-02-18

**Status:** Implemented

**Decision:**
Update `tools/pc-prepare-features` and prepare-role prompts so PM retry iterations pass explicit carry-forward context to Architect/UX: previous design draft, previous UX draft, prior PM feedback issues, and iteration index.

**Rationale:**
The retry loop reran Architect/UX, but role prompts did not include prior artifacts or PM findings. That made retries behave like fresh generation and increased repeated generic output/block cycles.

**Implications:**

- Architect/UX retries are now instructed to revise prior drafts instead of restarting from blank.
- PM findings from the last blocked iteration are fed into both roles as structured JSON.
- First iteration behavior remains unchanged (empty prior context).

### [DEC-072] - Make prepare-features semantic and role-driven; keep process-feature generation opt-in

**Date:** 2026-02-18

**Status:** Implemented

**Decision:**
Update `tools/pc-prepare-features` to execute Architect/UX/PM roles via dedicated prompt files and block generation unless PM semantic criteria pass (or explicit PM waiver is chosen). Also change process-feature handling so `## Process Features` is excluded by default and included only with `--include-process-features` / `INCLUDE_PROCESS_FEATURES=1`.

**Rationale:**
Structural heading checks alone were insufficient and allowed generic tooling-centric artifacts to pass PM review. Explicit semantic gating and project-specific role outputs reduce false approvals. Process/governance checklist items should not silently inflate executable feature scope.

**Implications:**

- `make prepare-features` now depends on prompt contracts for Architect/UX/PM role outputs.
- PM approval is fail-closed on semantic issues (generic markers, missing feature-specific context, contradictory PM decision payloads).
- Teams can still include process features, but must opt in explicitly.

### [DEC-071] - Treat prepare/review state/report artifacts as workflow-level contracts in live and template docs

**Date:** 2026-02-16

**Status:** Implemented

**Decision:**
Document `docs/03-logs/prepare-features-state.json` and `docs/03-logs/review-features-report.json` as required outputs in:

- live workflow/docs (`docs/04-process/human-orchestration-workflow.md`, `docs/README.md`, `tools/README.md`),
- template workflow/docs (`tools/templates/docs/04-process/human-orchestration-workflow.md`, `tools/templates/docs/README.md`),

and enforce references via `tests/test_docs_logs.py`.

**Rationale:**
Phase 3/4 added machine-readable runtime artifacts. Without explicit docs and tests, template/live drift can hide these outputs from operators and future bootstrap repos.

**Implications:**

- Operators now have explicit artifact expectations for prepare/review runs.
- Template repos inherit the same artifact contract as the source repository.
- `make feature` runtime remains unaffected.

### [DEC-070] - Persist prepare/review orchestration outcomes as machine-readable artifacts

**Date:** 2026-02-16

**Status:** Implemented

**Decision:**
Add deterministic runtime artifacts for the global orchestration commands:

- `docs/03-logs/prepare-features-state.json` from `tools/pc-prepare-features`
- `docs/03-logs/review-features-report.json` from `tools/pc-review-features`

and support prefix-based decision override aliases in `pc-prepare-features` (for example `PM-BLOCK:2`).

**Rationale:**
As prepare/review loops grow, terminal output alone is not enough for debugging reruns or auditing gate decisions. Machine-readable artifacts preserve dependency/PM outcomes and review findings in a stable, automatable format.

**Implications:**

- PM-gate retries/waivers/blocks are now traceable across runs.
- Review findings are available both inline in feature docs and in one aggregated report.
- `make feature` runtime remains unchanged.

### [DEC-069] - Split global preparation/review from work-item execution and enforce dependency-aware feature ordering

**Date:** 2026-02-16

**Status:** Implemented

**Decision:**
Introduce two new orchestration commands outside `make feature` runtime:

- `make prepare-features` (`Architect -> UX -> dependency planner -> PM gate -> feature generation`)
- `make review-features` (`Security Reviewer -> Product Manager` findings pass)

and make `tools/prd-to-features` consume `docs/02-features/feature-order.json` when present.

**Rationale:**
Architecture/UX alignment, dependency ordering, and pre-execution risk findings must happen before feature execution starts. Keeping these responsibilities outside `make feature` avoids runtime-role scope creep and preserves existing gate contracts.

**Implications:**

- `make feature` control-flow (`Orchestrator -> Planner -> Plan Reviewer -> Patcher -> Tester -> Reporter`) remains unchanged.
- Feature generation now has an explicit dependency-order artifact and deterministic ambiguity/cycle resolution path.
- Post-generation findings are injected into machine-managed sections of feature docs, giving patcher actionable backlog items without manual pre-editing.

### [DEC-068] - Treat feature-template `dev-tasks.md` pair as required in template-sync enforcement

**Date:** 2026-02-16

**Status:** Implemented

**Decision:**
Make `tools/pc-template-sync` enforce `docs/02-features/feature-template/dev-tasks.md` and `tools/templates/docs/02-features/feature-template/dev-tasks.md` as a required pair even if one side is missing from template discovery globs.

**Rationale:**
This pair is a hard dependency of `devtasks-schema-check` coherence guard. If template-source copy drift escapes sync detection, consumer repos fail pre-commit with no local migration path.

**Implications:**

- Required one-sided-missing pair drift is now handled deterministically by `tools/pc-template-sync --apply`.
- Both-sides-missing remains fail-closed and requires manual restoration from a known-good revision.
- Schema-check remediation now explicitly distinguishes missing template-source copy from legacy entry migration needs.

### [DEC-067] - Add explicit schema/runtime/template compatibility marker for dev-tasks feedback outcomes

**Date:** 2026-02-16

**Status:** Implemented

**Decision:**
Introduce a deterministic compatibility contract (`feedback-outcome-v1`) across:

- `tools/pc-devtasks-schema-check` (expected marker/version),
- `tools/pc-feature` (runtime marker declaration),
- live and template-source `docs/02-features/feature-template/dev-tasks.md` (marker + feedback outcome fields).

**Rationale:**
Consumer repositories can sync only schema checks while lagging runtime/template artifacts, causing deterministic pre-commit failures that are hard to diagnose. A shared marker plus guard fails early with explicit remediation.

**Implications:**

- Schema checks now surface tooling/template drift before work-item semantic validation.
- Template feedback sections are contractually required to include `Outcome` fields.
- Consumer sync paths are clearer: update tooling/templates together, then run migration backfill.

### [DEC-066] - Confirm post-MVP strategy: hardening and simplification only

**Date:** 2026-02-14

**Status:** Implemented

**Decision:**
Treat MVP as achieved and constrain next work to workflow hardening only: reduce human toil, reduce error rate, reduce token consumption, and remove unused complexity (skills/code paths).

**Rationale:**
The product is now working in other projects, and the user explicitly confirmed it is personal/single-user and not intended to support broader development styles.

**Implications:**

- Context docs now state a post-MVP optimization phase instead of open-ended feature expansion.
- New expected features prioritize automation/autofix, token efficiency, and pruning.
- Requests that generalize for multi-user or broad style compatibility remain out of scope unless a new product decision is made.

### [DEC-065] - Enforce CI-level skill metadata contracts and explicit invocation for high-impact skill workflows

**Date:** 2026-02-14

**Status:** Implemented

**Decision:**
Adopt a two-part hardening baseline for local skills:

1. enforce metadata/interface quality with a dedicated CI checker (`tools/pc-skills-metadata-check`), and
2. require explicit invocation (`policy.allow_implicit_invocation: false`) for high-impact mutating skills.

**Rationale:**
Batch-A improvements raised metadata quality, but there was no deterministic gate preventing future drift. Additionally, mutating skills (plan execution, feature generation, root sync, etc.) are safer when invoked explicitly rather than implicitly.

**Implications:**

- `make test`/`make ci` now fail-closed for malformed skill metadata and prompt-token drift.
- High-impact mutating skills are less likely to auto-trigger unexpectedly.
- Skill maintenance now includes deterministic script helpers and reference-driven progressive disclosure.

### [DEC-064] - Standardize skill interface metadata and portable prompts

**Date:** 2026-02-14

**Status:** Implemented

**Decision:**
Apply a repository-wide baseline for local Codex skills: every skill must have explicit trigger-oriented `description` metadata, an `agents/openai.yaml` interface block, `default_prompt` that references the `$skill-name` token, and no user-specific absolute paths in skill metadata/instructions.

**Rationale:**
Recent skill behavior showed drift risk from uneven metadata quality (trigger ambiguity, stale prompts, and hardcoded paths). A single baseline improves deterministic activation, explicit invocation, and portability.

**Implications:**

- Skill discovery and auto-activation become more predictable.
- UI skill chips/prompts are consistent across all local skills.
- Skills remain portable across machines/worktrees without local path rewrites.

### [DEC-063] - Align skills-check with Codex Skills directory contract

**Date:** 2026-02-13

**Status:** Implemented

**Decision:**
Update `skills-check` (live + template `Makefile`) to allow documented skill directories: optional `scripts/`, `references/`, `assets/`, and `agents/openai.yaml`. Keep fail-closed behavior for any unexpected top-level files/subdirectories and unexpected contents under `agents/`.

**Rationale:**
The previous gate rejected `agents/`, but Codex Skills documentation allows `agents/openai.yaml` and skill scaffolding creates it by default. The old rule caused deterministic false failures at final CI gates.

**Implications:**

- `make test`/`make ci` no longer fail on valid `agents/openai.yaml` layout.
- Skill layout policy remains strict and deterministic (unknown paths still blocked).
- Live/template parity is preserved to avoid bootstrap drift.

### [DEC-047] - Add chat-only shorthand skill for approved plan execution

**Date:** 2026-02-13

**Status:** Implemented

**Decision:**
Add a new local skill `implement-plan-safe` to trigger execution when the user sends short commands like `Implement`, provided an approved plan already exists in recent chat context.

**Rationale:**
The command flow is repetitive: user approves a plan, then asks for implementation with safety constraints. A dedicated chat-only skill reduces prompt overhead while preserving explicit safety rules and deterministic execution behavior.

**Implications:**

- Faster user invocation for plan execution.
- Mandatory guardrail behavior remains explicit in one reusable skill.
- Missing/ambiguous plan context now produces one focused clarifying question instead of speculative execution.

### [DEC-045] - Precommit template-sync uses deterministic copy autofix with Codex-only conflict escalation

**Date:** 2026-02-12

**Status:** Implemented

**Decision:**
Run `tools/pc-template-sync --apply --stage` in precommit and apply deterministic copy rules for non-conflicting drift, while failing dual-edited pairs for Codex-assisted semantic merge.

**Rationale:**
Most template/living mismatches are mechanical synchronization tasks and should not block commits. True dual-edit divergence can encode intent on both sides and requires semantic resolution rather than blind overwrite.

**Implications:**

- One-side-changed and neither-side-changed mismatches are auto-fixed by copy and staged.
- Both-sides-changed mismatches remain blocked with explicit remediation instructions.
- `tools/pc-precommit` now re-evaluates staged-file scope when hooks stage additional files.

### [DEC-044] - Close feature 17 on `main` and mark feature docs completed

**Date:** 2026-02-12

**Status:** Implemented

**Decision:**
Complete feature 17 by fully merging `feature-17-resume-in-progress-tickets-patcher` into `main`, then set F-17 core doc statuses to `Completed`.

**Rationale:**
The active worktree branch had additional delivery commits beyond prior merges. Closing on `main` removes split-brain execution context and keeps documentation aligned with delivered state.

**Implications:**

- `main` becomes the single source for feature 17 continuation/follow-up work.
- Feature status metadata now reflects completion in spec/design/test/tasks docs.
- Historical execution details remain preserved in role logs and execution entries.

### [DEC-043] - Repair pending resume sections from role artifacts before blocking

**Date:** 2026-02-12

**Status:** Implemented

**Decision:**
On resume startup, attempt deterministic reconciliation of pending execution sections (`Patch`, `Test Results`, `Reporter Review`) from existing tester/reporter role artifacts before raising a contradictory-state block.

**Rationale:**
Observed restarts could fail even when valid role artifacts existed, due to stale pending placeholders in `dev-tasks.md`. Repair-first removes avoidable manual cleanup while retaining fail-closed behavior when evidence remains inconsistent.

**Implications:**

- Resume now supports policy gating via `RESUME_CONTRADICTION_POLICY` with a kill-switch back to strict block mode.
- Repair writes are constrained to planner-owned execution sections and only when placeholders are pending.
- Tester/reporter outcomes can be inferred from role artifacts when feedback sections are empty, preserving correct planner restart routing.

### [DEC-042] - Enforce explicit role-loop control-flow contract

**Date:** 2026-02-11

**Status:** Implemented

**Decision:**
Define one required runtime order (`Orchestrator → Planner → Plan Reviewer → Patcher → Tester → Reporter → Orchestrator`) and deterministic restart rules (reviewer `BLOCK`, tester `FAIL`, and reporter `FAIL` all restart at Planner; only reporter `PASS` returns control to final Orchestrator gates).

**Rationale:**
Retry loops were under-specified across process docs and prompts, which risked inconsistent reruns and weak handoff context. A single contract keeps retries predictable and auditable.

**Implications:**

- Role outputs must include actionable failure context for restart passes.
- No-op restart passes must be recorded explicitly in iteration logs.
- Restarts should reuse existing artifacts/logs when safe instead of reinitializing work from scratch.

### [DEC-018] - Interactive HIGH-risk approval gate for `pc-feature`

**Date:** 2026-02-06

**Status:** Implemented

**Decision:**
Use an interactive approval prompt when a work item is classified HIGH risk, instead of always requiring a separate PO-file update/restart loop.

**Rationale:**
This keeps the safety gate while reducing workflow friction. For unattended/non-interactive runs, safety remains fail-closed by default unless `APPROVE_HIGH_RISK=1` is explicitly set.

**Implications:**

- Interactive runs can continue in the same `make feature` session after explicit approval.
- Non-interactive automation still blocks high-risk work unless opt-in override is provided.

### [DEC-017] - Observability-first workflow hardening

**Date:** 2026-02-05

**Status:** Approved

**Decision Makers:** Alexandre Pezzotta

**Context:**
Token burn, limited observability, and inconsistent role behavior were causing regressions and slow debugging.

**Problem Statement:**
How do we reduce deterministic token burn and improve traceability without expanding scope or adding new infrastructure?

**Options Considered:**

#### Option 1: Keep ad-hoc LLM-driven execution

**Description:** Rely on manual prompts and unstructured outputs.

**Pros:**

- Minimal tooling changes

**Cons:**

- Continued token waste
- Hard-to-debug failures
- Inconsistent role behavior

**Estimated effort:** Low

#### Option 2: Standardize runner + structured logs + role prompts (chosen)

**Description:** Introduce a shared runner, structured logs, incremental PRD → features, plan review, and human-gated improvement proposals.

**Pros:**

- Deterministic execution for repeatable steps
- Tail-friendly, timestamped logs
- Clear role boundaries and plan validation

**Cons:**

- Requires updates across docs/tools

**Estimated effort:** Moderate

**Decision:**
Adopt Option 2 and make observability-first, script-driven execution the default.

**Consequences:**

- Logs live at `logs/<WI>/<step>.log` with standard prefixes.
- Plan Reviewer is required before patching.
- PRD → features is incremental; Done features are not regenerated.
- Single worktree per feature; no `feature-worktrees.json`.

### [DEC-018] - Increment work item IDs per feature

**Date:** 2026-02-06

**Status:** Approved

**Decision Makers:** Alexandre Pezzotta

**Context:**
Work item IDs reset per day, which makes it harder to track sequential work on a single feature across multiple days.

**Problem Statement:**
Should work item IDs increment per day or per feature?

**Options Considered:**

#### Option 1: Increment per day (status quo)

**Description:** Reset the sequence daily (e.g., `WI-YYYYMMDD-01` each day).

**Pros:**

- Simple and date-scoped

**Cons:**

- Harder to follow sequential work within a feature across days
- Creates duplicate sequence numbers for a feature

**Estimated effort:** Low

#### Option 2: Increment per feature (chosen)

**Description:** Use the next sequence number for the feature regardless of date; keep the current date in the ID.

**Pros:**

- Monotonic sequencing within a feature
- Easier to audit and reference work items

**Cons:**

- Sequence number no longer resets daily

**Estimated effort:** Low

**Decision:**
Adopt per-feature sequencing for work item IDs.

**Consequences:**

- `pc-feature` generates the next WI by scanning existing feature entries.
- Templates and docs describe the per-feature sequencing rule.

### [DEC-016] - Defer global log updates until feature completion

**Date:** 2026-02-05

**Status:** Implemented

**Decision Makers:** Alexandre Pezzotta

**Context:**
Global logs were being updated during execution, which produced premature entries and contributed to role-scope conflicts.

**Problem Statement:**
When should global decision/implementation/validation logs be updated during a feature run?

**Options Considered:**

#### Option 1: Update global logs during each gate

**Description:** Append entries as soon as a gate completes.

**Pros:**

- Immediate traceability

**Cons:**

- Premature entries when a run later fails
- More role-scope conflicts in shared worktrees

**Estimated effort:** Low

#### Option 2: Update global logs only after completion (chosen)

**Description:** Defer global log updates until gates pass and the feature completes; use reporter summaries.

**Pros:**

- Logs reflect completed work only
- Keeps role logs feature-scoped until done

**Cons:**

- Less incremental visibility during execution

**Estimated effort:** Low

**Decision:**
Adopt Option 2 and update global logs only after completion using reporter-provided summaries.

**Consequences:**

- Global logs reflect completed features only.
- Role logs remain the source for in-progress execution details.

### [DEC-015] - Keep dev-tasks planner-only; move tester/reporter output to role logs

**Date:** 2026-02-05

**Status:** Implemented

**Decision Makers:** Alexandre Pezzotta

**Context:**
`pc-feature` was writing tester/reporter output into `dev-tasks.md`, which conflicted with role scope enforcement and blurred task ownership.

**Problem Statement:**
How should we keep `dev-tasks.md` as the planner-owned task source of truth while still recording test and review output?

**Options Considered:**

#### Option 1: Allow tester/reporter edits to dev-tasks

**Description:** Expand role scope so tester/reporter can write test and review sections in `dev-tasks.md`.

**Pros:**

- Keeps execution log centralized

**Cons:**

- Weakens role isolation
- Causes scope violations if logs are out of sync

**Estimated effort:** Low

#### Option 2: Move tester/reporter output to role logs (chosen)

**Description:** Keep `dev-tasks.md` planner-only and record tester output in `validation-log.md` and reporter output in `reporter-log.md`.

**Pros:**

- Clear ownership boundaries
- Avoids role-scope violations

**Cons:**

- Execution log information is split across files

**Estimated effort:** Low

**Decision:**
Adopt Option 2 and keep `dev-tasks.md` planner-only, with tester/reporter output recorded in their role logs.

**Consequences:**

- `dev-tasks.md` no longer mirrors tester/reporter sections.
- Reviewers should consult role logs for execution results.

### [DEC-014] - Extract JSON payloads for preflight parsing

**Date:** 2026-02-05

**Status:** Implemented

**Decision Makers:** Alexandre Pezzotta

**Context:**
The preflight JSON response sometimes includes extra prose, causing parsing failures and halting `pc-feature`.

**Problem Statement:**
How do we make preflight JSON parsing resilient to non-JSON prefixes/suffixes while still enforcing structured output?

**Options Considered:**

#### Option 1: Retry on parse failure with a stricter prompt

**Description:** Add a second prompt when JSON parsing fails.

**Pros:**

- Keeps strict JSON format

**Cons:**

- Adds another model call

**Estimated effort:** Low

#### Option 2: Extract JSON payload from the response

**Description:** Parse only the content between the first `{` and last `}` before JSON decoding.

**Pros:**

- Handles stray prose without extra calls
- Simple and deterministic

**Cons:**

- Could accept unintended JSON if multiple objects are present

**Estimated effort:** Low

**Decision:**
We chose **Option 2: Extract JSON payload from the response**, plus a stricter prompt.

**Rationale:**
It reduces failure modes with minimal overhead while still instructing the model to output JSON only.

**Implications:**

- `pc-feature` strips non-JSON prefixes/suffixes before parsing.
- Prompt explicitly forbids prose or markdown.

**Success Criteria:**

- Preflight JSON parsing no longer fails due to stray prose.

**Review Date:** 2026-03-01

**Actual Outcome:** _Pending_

### [DEC-013] - Enforce Allowed Tests allowlist and forbid recursive feature runs

**Date:** 2026-02-05

**Status:** Implemented

**Decision Makers:** Alexandre Pezzotta

**Context:**
Tester steps were running `make feature F=<id>` recursively, causing unsafe worktree mutations, sandbox failures, and runaway token usage.

**Problem Statement:**
How do we keep tests scoped to patcher changes and prevent recursive feature execution?

**Options Considered:**

#### Option 1: Allow Tester to choose tests

**Description:** Keep the Tester autonomous to decide what to run.

**Pros:**

- Minimal process friction

**Cons:**

- Recursion risk (`make feature`), uncontrolled worktree changes
- Inconsistent test scope

**Estimated effort:** Low

#### Option 2: Explicit Allowed Tests allowlist in dev-tasks

**Description:** Planner/Patcher lists exact test commands; Tester runs only those.

**Pros:**

- Scoped, predictable tests
- Blocks recursive `make feature`/`pc-feature`

**Cons:**

- Requires explicit test planning

**Estimated effort:** Medium

#### Option 3: Hardcoded test suite per feature

**Description:** Each feature defines a fixed test suite in code/config.

**Pros:**

- Repeatable and enforceable

**Cons:**

- Additional config overhead
- Less flexible during discovery

**Estimated effort:** Medium-high

**Decision:**
We chose **Option 2: Explicit Allowed Tests allowlist in dev-tasks**.

**Rationale:**
It keeps tests scoped to patcher changes while preventing recursive feature execution and sandbox violations.

**Implications:**

- `pc-feature` requires Allowed Tests and blocks `make feature`/`pc-feature` as tests.
- Planner/Patcher must define specific, non-recursive tests before Tester runs.

**Success Criteria:**

- `make feature F=<id>` no longer triggers recursive runs.
- Tester only executes allowlisted, scoped tests.

**Review Date:** 2026-03-01

**Actual Outcome:** _Pending_

### [DEC-012] - Role-scoped formatting and auto-clean worktrees in pc-feature

**Date:** 2026-02-05

**Status:** Implemented

**Decision Makers:** Alexandre Pezzotta

**Context:**
`pc-feature` runs multiple role steps in a shared worktree. Role logs were being modified by the patcher or by formatting side effects, triggering role-scope enforcement failures.

**Problem Statement:**
How do we prevent cross-role edits and formatting side effects while keeping the same formatting behavior as pre-commit?

**Options Considered:**

#### Option 1: Disable formatting during role steps

**Description:** Skip formatting entirely and rely on final pre-commit to normalize files.

**Pros:**

- Minimal work during role steps

**Cons:**

- Formatting happens late and can touch role logs during commit
- Reintroduces cross-role edits at the end

**Estimated effort:** Low

#### Option 2: Role-scoped pre-commit formatting with hook skips

**Description:** Run `pre-commit run --files` on each role’s changed files and skip hooks that do not accept filenames.

**Pros:**

- Same formatting tools as pre-commit
- Formatting limited to role-owned files
- Prevents end-of-workflow formatting surprises

**Cons:**

- Requires careful skip list
- Depends on `pre-commit` being available locally

**Estimated effort:** Medium

#### Option 3: Custom formatter per file type

**Description:** Reimplement formatting with direct calls to individual tools by file type.

**Pros:**

- Full control of scope
- No pre-commit dependency

**Cons:**

- Diverges from pre-commit configuration
- Higher maintenance burden

**Estimated effort:** Medium-high

**Decision:**
We chose **Option 2: Role-scoped pre-commit formatting with hook skips**.

**Rationale:**
It keeps formatting aligned with the pre-commit toolchain while limiting changes to each role’s files, preventing role-log violations and late-stage diffs.

**Implications:**

- `pc-feature` runs `pre-commit run --files` per role and skips hooks that don’t accept file arguments.
- Dirty worktrees are detected early and can be deleted/recreated after user confirmation.

**Success Criteria:**

- `make feature F=<id>` completes without role-scope errors on role logs.
- Formatting no longer modifies role logs outside their owning role.

**Review Date:** 2026-03-01

**Actual Outcome:** _Pending_

### [DEC-011] - Use repo-local CODEX_HOME for scripted Codex exec

**Date:** 2026-02-04

**Status:** Implemented

**Decision Makers:** Alexandre Pezzotta

**Context:**
Codex CLI runs from scripted tooling (pre-commit hooks and feature automation) fail when Codex attempts to write sessions outside the repo sandbox.

**Problem Statement:**
How do we allow Codex CLI to persist session data without requiring access to the user's home directory?

**Options Considered:**

#### Option 1: Allow home directory writes

**Description:** Permit Codex to write to `~/.codex` by granting broader permissions.

**Pros:**

- Minimal tooling changes
- Matches Codex defaults

**Cons:**

- Requires expanded permissions outside the repo
- Less deterministic for sandboxed runs

**Estimated effort:** Low

#### Option 2: Use repo-local CODEX_HOME

**Description:** Set `CODEX_HOME` to the repo-local `.codex` directory for scripted runs.

**Pros:**

- Works within sandboxed environments
- Keeps Codex state scoped to the repo

**Cons:**

- Requires updating tooling scripts

**Estimated effort:** Low

**Decision:**
We chose **Option 2: Use repo-local CODEX_HOME**

**Rationale:**
It keeps automation self-contained while unblocking Codex exec in hooks and scripts.

**Implications:**

- Scripted Codex calls set `CODEX_HOME` to `.codex`.
- Repo templates include the profile defaults to align sub-agent behavior.

**Success Criteria:**

- `codex exec` succeeds in scripted hooks without home directory access.

**Review Date:** 2026-03-01

**Actual Outcome:** Implemented; validation pending real pre-commit runs.

### [DEC-010] - Enforce template/living sync via pre-commit

**Date:** 2026-02-04

**Status:** Implemented

**Decision Makers:** Alexandre Pezzotta

**Context:**
Template files and their live counterparts can drift, leading to mismatched process docs and hooks.

**Problem Statement:**
How do we ensure template files and living files stay synchronized without manual reminders?

**Options Considered:**

#### Option 1: Manual checklist reminders

**Description:** Rely on humans/Codex reminders to update both sides.

**Pros:**

- No tooling changes
- Lowest implementation effort

**Cons:**

- Drift is easy to miss
- Enforcement is inconsistent

**Estimated effort:** Low

#### Option 2: Pre-commit gate with Codex-assisted autofix

**Description:** Diff template vs living files on pre-commit; if only one side changed, run Codex to update the other.

**Pros:**

- Automated enforcement at commit time
- Keeps templates and living docs aligned

**Cons:**

- Requires Codex CLI availability for autofix
- Hook can fail when mismatches are unrelated

**Estimated effort:** Medium

**Decision:**
We chose **Option 2: Pre-commit gate with Codex-assisted autofix**

**Rationale:**
This enforces sync at the earliest safe gate while minimizing manual overhead.

**Implications:**

- Pre-commit runs a new template sync hook.
- One-sided changes auto-propagate; unrelated mismatches fail fast.

**Success Criteria:**

- Template and living files stay aligned in normal workflows.
- No repeated manual reminders needed.

**Review Date:** 2026-03-01

**Actual Outcome:** Implemented; awaiting validation from real pre-commit runs.

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
- Single worktree per feature; no `feature-worktrees.json` tracking file.
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

### DEC-019 - Treat repeated reviewer/reporter churn as policy conflict and stop early

- **Date:** 2026-02-06
- **Status:** Accepted
- **Context:** `pc-feature` could exhaust loop attempts while repeatedly revising plans/reports without progressing patch/test state.
- **Decision:**
  - Lock a run-level risk policy baseline after preflight.
  - Use attempt-scoped reporter diff baseline.
  - Detect repeated identical reporter FAIL signatures and explicit policy contradictions, then fail fast with a clear error.
  - Add timestamped attempt/step/status timeline notes to the work item iteration log.
- **Consequences:**
  - Faster failure for non-progress loops.
  - Better diagnostics for where and why execution stopped.

### DEC-020 - Exclude volatile workflow artifacts from patcher branch replay

- **Date:** 2026-02-06
- **Status:** Accepted
- **Context:** `pc-feature` final collection replays `patcher` branch changes onto `main`. Repeated executions accumulate volatile artifacts (role logs, global logs, run logs, and local execution-trace edits) that can diverge from `main` and trigger `git apply --3way` conflicts.
- **Decision:**
  - Filter patcher branch replay to durable implementation paths only.
  - Exclude `dev-tasks.md`, role-scoped logs, `docs/03-logs/*.md`, and `logs/` artifacts from branch replay.
  - Keep final commit scope explicit by adding `dev-tasks.md` and global logs from `main` at final staging, rather than replaying their branch versions.
- **Consequences:**
  - Final collection becomes resilient to repeated-run log churn.
  - Runtime `logs/WI-*` files are no longer implicitly allowed via branch diff drift.

### DEC-021 - Treat high-risk approval as persisted state, not inferred risk

- **Date:** 2026-02-06
- **Status:** Accepted
- **Context:** Resumed work items with `Risk level: HIGH` could still carry `Notes: Awaiting PO Approval`. The workflow inferred approval from risk level when building policy basis, which could trigger a false `plan-reviewer policy conflict` abort.
- **Decision:**
  - Persist explicit approval marker in Notes when high-risk gate is approved.
  - On resume, re-run high-risk approval gate when marker is missing.
  - Build plan-reviewer policy basis from actual approval state.
  - Route first policy contradiction through planner correction and fail only on repeated contradiction.
- **Consequences:**
  - Retries no longer fail immediately due stale high-risk notes.
  - High-risk gating behavior remains explicit and auditable across reruns.

### DEC-022 - Runtime `logs/` artifacts are ephemeral for pc-feature finalization

- **Date:** 2026-02-06
- **Status:** Accepted
- **Context:** `pc-feature` produces execution logs under `logs/WI-*` while running. These runtime artifacts caused false blockers in final scoped staging and `tools/pc-commit` disallowed-change checks.
- **Decision:**
  - Treat `logs/` as ignored ephemeral paths for scoped final staging checks.
  - Pass ephemeral allow paths (including `logs`) to final `tools/pc-commit` invocation.
  - Reset ephemeral paths from index before final staging so they cannot be committed accidentally.
- **Consequences:**
  - Runtime logs no longer block `make feature F=<id>` finalization.
  - Feature completion is based on implementation/doc deliverables, not transient run artifacts.

### DEC-023 - Reviewer BLOCK rounds must not consume execution attempt budget

- **Date:** 2026-02-06
- **Status:** Accepted
- **Context:** Repeated plan-reviewer BLOCK responses exhausted `MAX_LOOPS` and caused `pc-feature: max iteration attempts reached` before meaningful patch/test execution.
- **Decision:**
  - Track execution attempts and reviewer BLOCK rounds with separate counters.
  - Increment execution attempts only after reviewer `APPROVE`.
  - Add `MAX_REVIEWER_BLOCKS` cap with a specific failure message for unresolved reviewer churn.
- **Consequences:**
  - Plan-quality loops no longer starve patch/test execution attempts.
  - Failure mode is explicit when reviewer feedback cannot converge.

### DEC-024 - Tighten `pc-feature` execution isolation and test-command scope

- **Date:** 2026-02-07
- **Status:** Accepted
- **Context:** Workflow safety gaps remained around broad escalation (`pp` prefix), stale worktree reuse, global cleanup side effects, and overly permissive Allowed Tests command parsing.
- **Decision:**
  - Scope cleanup to the current feature patcher worktree/branch only.
  - Evaluate escalation allowlist against unwrapped `tools/offload-proxy/pp` commands, not the wrapper itself.
  - Enforce behind-`main` freshness checks for existing patcher worktrees.
  - Keep role logs lazy-created; remove startup pre-creation.
  - Re-run HIGH-risk approval on resume when approval marker is missing.
  - Record technical collection conflicts as technical notes (not PO approval state).
  - Filter branch replay to durable implementation paths only.
  - Restrict Allowed Tests to explicit `unittest`/`pytest` command forms.
  - Add early root dirty-scope guard and immediate post-reviewer read-only enforcement.
  - Enforce anti-hardcode plan requirements (fixtures/seed/invariants/contracts) before patching.
- **Consequences:**
  - Lower risk of cross-worktree/branch deletion and escalation abuse.
  - Higher determinism for reruns and test execution scope.
  - Earlier, clearer failures when scope or policy constraints are violated.

### DEC-025 - Templates mirror living workflow docs

- **Date:** 2026-02-07
- **Status:** Accepted
- **Context:** Pre-commit template sync detected drift between workflow docs and their templates.
- **Decision:**
  - Treat the living workflow docs in `docs/04-process/` as the source of truth.
  - Update templates to match the living docs when drift is detected.
- **Consequences:**
  - Template sync remains deterministic and prevents policy divergence.

### DEC-026 - Feature execution runtime artifacts are worktree-local

- **Date:** 2026-02-08
- **Status:** Accepted
- **Context:** `pc-feature` role execution occurred in the patcher worktree, but key runtime artifacts (`dev-tasks.md` and `logs/WI-*`) were still written/read from `main`, causing stale reviewer context and untracked artifact failures.
- **Decision:**
  - Treat the patcher worktree as the runtime source-of-truth for feature execution artifacts.
  - Resolve and validate `dev-tasks.md`, planner/tester/reporter logs, and `logs/<WI>/...` inside the active worktree.
  - Require actionable failure context on reviewer/tester FAIL outcomes so retries can converge (`File/Path`, `Check`, `Evidence`, `Expected fix`).
  - Keep strict `MAX_LOOPS` cap and no-op iteration logging as mandatory safety rails.
- **Consequences:**
  - Reporter/planner loops consume current iteration artifacts, not stale `main` files.
  - Runtime logs no longer pollute `main` during execution.
  - Retry loops have deterministic remediation context and fail with clearer diagnostics when exhausted.

### DEC-027 - Enforce deterministic plan policy before patcher execution

- **Date:** 2026-02-08
- **Status:** Accepted
- **Context:** Planner output can still contain forbidden instructions (role-scoped files/global logs/forbidden commands). If reviewer misses this, patcher fails later with role-scope errors and wastes loop budget.
- **Decision:**
  - Add orchestrator-side plan policy validation before patcher execution.
  - Treat violations as `BLOCK` and route back to planner with actionable required changes.
  - Expand patcher role-scope checks to block role-scoped files across all feature folders, not just current feature.
- **Consequences:**
  - Invalid plans are stopped deterministically before patching.
  - Feature-id/context mismatches become visible earlier.
  - Failure mode shifts from late patcher guard crashes to actionable planner revision loops.

### DEC-028 - Plan-reviewer read-only guard is delta-based

- **Date:** 2026-02-08
- **Status:** Accepted
- **Context:** Reviewer guard previously failed on any dirty worktree path, including orchestrator/planner writes made before reviewer execution (notably planner no-op notes in `dev-tasks.md`).
- **Decision:**
  - Capture pre-review dirty snapshot and compare against post-review snapshot.
  - Treat only reviewer-introduced dirty deltas as violations.
  - Move planner no-op note write to after reviewer verification.
  - Add pre-review hygiene checkpoint (`AUTO_REVIEWER_HYGIENE`) to auto-clean planner-owned pre-existing dirt and block unexpected paths.
- **Consequences:**
- Prevents false attribution of planner/orchestrator edits to reviewer.
- Preserves strict read-only enforcement for real reviewer modifications.
- Improves failure diagnostics and loop traceability for reruns.

### DEC-029 - Restore auto-resume with strict startup state gating

- **Date:** 2026-02-08
- **Status:** Accepted
- **Context:** Resume behavior is required for in-progress features, but previous simplification toward pristine-only startup removed reliable resume while recent failures showed dirty/stale/parallel-state hazards.
- **Decision:**
  - Reintroduce automatic resume by default via `RESUME_MODE=auto`.
  - Add explicit startup modes: `auto`, `prompt`, `fresh`.
  - Treat stale behind-`main` feature worktrees as hard failures in `auto` mode.
  - Allow resume only when dirty state is runtime-scoped; block non-runtime dirty files.
  - Auto-checkpoint dirty `dev-tasks.md` when a resumable work item exists.
  - Enforce single active feature across patcher worktrees.
- **Consequences:**
  - In-progress feature reruns resume without manual prompts in the common case.
  - Startup failures become deterministic and actionable for stale/unsafe states.
  - Parallel active feature attempts are blocked to preserve single-feature execution guarantees.

### DEC-030 - Adopt WIP-first startup resume for active feature worktrees

- **Date:** 2026-02-08
- **Status:** Accepted
- **Context:** Single-user, single-feature workflow requires preserving existing work-in-progress in the feature worktree. Strict startup cleanliness and startup checkout cleanup caused avoidable friction and perceived data-loss risk.
- **Decision:**
  - Treat any existing dirty state in the active feature worktree as valid WIP at startup.
  - Replace startup dirty-path blocking/cleanup with a startup checkpoint commit over all dirty non-ignored paths in the feature worktree.
  - Preserve startup state in `RESUME_MODE=auto`/`prompt`; keep destructive recreation only in `RESUME_MODE=fresh`.
  - Downgrade root pre-start dirty-path gate from hard fail to warning.
- **Consequences:**
  - `make feature` reliably continues in-progress work without startup resets/checkouts.
  - Startup behavior aligns with single-user operational model and reduces interruption cost.
  - End-of-flow scoped commit guards remain in place for final collection safety.

### DEC-031 - Promote Plan Reviewer to a first-class orchestrator step

- **Date:** 2026-02-09
- **Status:** Accepted
- **Context:** Feature 12 failures showed ambiguous planner/reviewer state transitions, non-deterministic reviewer loops, and incomplete step-level traceability across planner review decisions.
- **Decision:**
  - Treat Plan Reviewer as a dedicated role step with its own role-scoped log artifact (`plan-reviewer-log.md`).
  - Require step-boundary commit checkpoints for role transitions, including explicit commit traceability for review decisions.
  - Run deterministic plan-policy checks before LLM reviewer gating to prevent repetitive LLM-only block loops.
  - Require planner revisions to be self-contained and merge-safe when feedback loops return partial/delta plans.
  - Standardize tester/reporter feedback contracts so planner/patcher retries receive consistent remediation context.
- **Consequences:**
  - Planner/Plan Reviewer/Patcher transitions are auditable and less prone to dirty-state attribution errors.
  - Invalid plans are blocked earlier with deterministic reasons before patcher execution.
  - Feedback-loop convergence is more reliable due to stronger plan/validation/report contracts.

### DEC-032 - Enforce Plan Contract v1 and bounded reviewer/planner retry controls

- **Date:** 2026-02-09
- **Status:** Accepted
- **Context:** Feature 12 showed repeated reviewer BLOCK cycles where stale forbidden paths persisted in plan text due append-style revised-plan merging, while loop counters were ambiguous (`attempt` remained constant) and planner revision retries lacked an explicit dedicated cap.
- **Decision:**
  - Standardize planner output to **Plan Contract v1** sections (`Approach`, `Files to change`, `Risks`, `Tests (anti-hardcode coverage required)`) and align reviewer prompts to the same contract.
  - Treat revised plans as full replacements (no append merge fallback) to avoid stale policy violations lingering in active plan state.
  - Keep policy checks section-aware (`Files to change` primary scope) with full-plan fallback scanning as a safety net.
  - Add independent retry controls for reviewer/planner loop:
    - reviewer cap (`MAX_REVIEWER_BLOCKS`, exact-trigger semantics),
    - planner revision cap (`MAX_PLANNER_REVISIONS`),
    - stagnation guard (`MAX_STAGNANT_REVIEWER_BLOCKS`) for repeated unresolved policy signatures.
  - Emit explicit loop counters in iteration log notes for diagnosability.
- **Consequences:**
  - Repeated BLOCK cycles terminate deterministically with actionable terminal reasons.
  - Planner/reviewer handoffs become easier to debug from logs.
  - Contract drift risk is reduced through prompt + protocol alignment.

### DEC-033 - Reporter global-log is a JSON signal; orchestrator owns global log writes

- **Date:** 2026-02-09
- **Status:** Accepted
- **Context:** `pc-feature` could fail after successful gates when reporter returned clarification text instead of JSON for global-log summaries. Reporter role scope requires reporting, while orchestrator owns final updates to `docs/03-logs/*`.
- **Decision:**
  - Keep reporter global-log step as read-only signal generation (JSON only, no file edits).
  - Add one strict JSON-repair retry when reporter global-log payload parsing fails.
  - If payload remains invalid, continue with deterministic orchestrator-generated global-log lines derived from `work_item_id` and `requires_global_logs`.
  - Preserve orchestrator as the only writer for global log files.
- **Consequences:**
  - `make feature` no longer hard-fails at the final reporter global-log parse step.
  - Global reporting remains present by default via deterministic fallback lines.
  - Role-scope boundaries remain explicit: reporter reports, orchestrator writes.

### DEC-034 - Add pre-patch policy recheck and planner reroute for patcher scope violations

- **Date:** 2026-02-09
- **Status:** Accepted
- **Context:** Feature 13 resume/retry flow still allowed a late terminal abort (`patcher edited role-scoped files`) when plan drift reintroduced forbidden paths after earlier review steps.
- **Decision:**
  - Re-run deterministic `plan_policy_violations(...)` immediately before patcher execution.
  - If pre-patch policy check fails, do not invoke patcher; route to planner revision with explicit remediation.
  - If patcher still produces role-scoped/global-log edits, restore patcher dirt and route back to planner revision instead of immediate terminal abort.
  - Keep existing terminal role-scope guards as final safety nets.
- **Consequences:**
  - Resume/retry loops fail earlier and more deterministically on policy drift.
  - Planner receives actionable remediation context instead of a hard-stop path.
  - Patcher scope enforcement remains strict while becoming recoverable within loop limits.

### DEC-035 - Remove change-budget workflow control and keep legacy entry compatibility

- **Date:** 2026-02-09
- **Status:** Accepted
- **Context:** The change-budget fields (`max_files`, `max_new_modules`) were no longer acting as a real control in `pc-feature` because planning loops could still revise scope and proceed. Keeping budget wording in runtime contracts created misleading governance.
- **Decision:**
  - Remove change-budget logic from runtime risk classification and generated execution-entry content.
  - Keep deterministic HIGH-risk triggers for security-sensitive paths/flags and cross-cutting refactors.
  - Keep compatibility for existing execution logs by supporting both section titles: `Files to Change` and legacy `Files to Change + Change Budget`.
  - Align process/template/worklog docs and feature 14-16 changelogs with the new baseline wording.
- **Consequences:**
  - New work items no longer display or evaluate change-budget fields.
  - Existing historical/in-progress entries remain readable and updatable without manual migration.
  - Scope governance remains via explicit risks, review loops, and deterministic policy checks instead of soft budget numbers.

### DEC-036 - Reframe F-15 around useful compact logs for continuous improvement

- **Date:** 2026-02-09
- **Status:** Accepted
- **Context:** Feature 15 wording captured offload audit and compaction mechanics but did not explicitly cover validation-log compaction, compact-output usefulness requirements, or a deterministic derived-output location.
- **Decision:**
  - Keep Feature 15 focused on offload audit + log compaction.
  - Expand compaction scope to `decision-log`, `implementation-log`, and `validation-log`.
  - Require a compact-output usefulness contract (source/date/work-item/outcome/evidence references).
  - Keep compaction non-destructive by writing derived artifacts under `docs/03-logs/compacted/` and preserving canonical logs.
- **Consequences:**
  - Feature 15 now aligns directly with the continuous workflow-improvement objective.
  - Compaction outputs become auditable and actionable instead of only shorter text.
  - Test/implementation scope is clearer for future execution.

- WI-20260209-01: Process docs changed; orchestrator retained ownership of deferred docs/03-logs updates.

### DEC-037 - Treat forbidden plan commands by command context and add deterministic plan/test policy checks

- **Date:** 2026-02-09
- **Status:** Accepted
- **Context:** Plan-review logs showed repeated `BLOCK` decisions from three recurring causes: false positives when `tools/pc-feature` appeared as a file path, missing explicit ownership for `docs/03-logs/*` updates, and plan Tests commands drifting from Allowed Tests.
- **Decision:**
  - Evaluate forbidden plan commands in command context and avoid treating file-path entries in `Files to change` as executable commands.
  - Keep deterministic blocking for role/global log paths.
  - Require explicit global-log handoff wording only when plans touch process/global-log docs.
  - Require concrete plan test commands to be listed in Allowed Tests.
  - Align AGENTS/process docs and planner/reviewer prompts with this policy.
- **Consequences:**
  - Reduced false-positive blocks while preserving policy safety.
  - Earlier deterministic remediation for real plan-policy gaps.
  - More stable planner/reviewer loop behavior with clearer required changes.

### DEC-038 - Orchestrator-owned aggregation for workflow improvement proposals

- **Date:** 2026-02-09
- **Status:** Accepted
- **Context:** `docs/possible-improvements.md` was updated during role steps in the shared worktree, causing planner/reporter scope violations and unstable `make feature` runs.
- **Decision:**
  - Keep role feedback as the proposal source.
  - Make `docs/possible-improvements.md` orchestrator-owned only.
  - Queue proposals during the run and flush them at orchestrator checkpoints.
  - Deduplicate queued proposals by signature and merge richer context before writing.
  - Keep role/patcher plans from targeting `docs/possible-improvements.md` directly.
- **Consequences:**
  - Continuous-improvement signals are preserved across retries without widening role write scope.
  - Proposal registry updates are clearer and deterministic.
  - Scope violations from role edits to the global proposal registry are prevented.

### DEC-039 - Non-planner role commits auto-reset planner-owned `dev-tasks.md`

- **Date:** 2026-02-10
- **Status:** Accepted
- **Context:** Feature execution could terminate near completion with `tester edited out-of-scope files: .../dev-tasks.md` even when tester/reporter flow otherwise passed, due to planner-owned `dev-tasks.md` remaining dirty at non-planner commit boundaries in shared/resumed worktrees.
- **Decision:**
  - Keep planner ownership of `dev-tasks.md` unchanged.
  - Before role-scope enforcement in `commit_role_step(...)`, auto-reset `dev-tasks.md` for non-planner roles (`tester`, `reporter`, `plan-reviewer`).
  - Keep strict terminal guards for patcher/global-log scope unchanged.
- **Consequences:**
  - Reduces false terminal aborts from incidental `dev-tasks.md` dirt at tester/reporter/plan-reviewer commit boundaries.
  - Preserves role ownership and deterministic scope enforcement semantics.

### DEC-040 - Make patcher-branch collection resilient with conflict auto-skip and explicit diagnostics

- **Date:** 2026-02-10
- **Status:** Accepted
- **Context:** Final collection could abort with a generic `conflict detected while collecting worktrees` error even when tester/reporter outcomes were PASS. The failure stopped integration and did not clearly identify conflicting paths.
- **Decision:**
  - Keep `git apply --3way` collection strategy.
  - Add diagnostics-first collection in `apply_branch_diff(...)` (precheck + conflict path extraction).
  - During collection of patcher branch into main, auto-retry non-conflicting paths and fall back to per-path apply when needed.
  - If conflicts remain, auto-skip conflicting paths, emit explicit warning logs listing those paths, append an Iteration Log note, and continue workflow to final gates.
- **Consequences:**
  - Reduced run-breaking behavior from localized collection conflicts.
  - Better operator visibility into exactly which paths conflicted during `collecting patcher branch into main`.
  - Non-conflicting changes have a higher chance of being integrated in the same run without manual patch replay.

### DEC-041 - Compaction must prefer freshest dated entries and emit LLM-optimized derived artifacts

- **Date:** 2026-02-10
- **Status:** Accepted
- **Context:** Canonical logs in `docs/03-logs/*.md` had recent entries that were not present in compacted artifacts. The previous compaction parser depended on strict heading shape and first-in-file selection, so compacted views could become stale and expensive to use in LLM prompts.
- **Decision:**
  - Parse compaction sections with log-specific heading handling, including mixed `##`/`###` validation headings.
  - Sort extracted entries by parsed date (newest first) before truncation.
  - Deduplicate by deterministic keys (`DEC-*` identity for decisions; normalized summary/work-item/evidence fingerprint for implementation/validation), with optional semantic-map canonicalization via `docs/03-logs/compacted/semantic-map.json`.
  - Emit two derived output contracts per log: full compact JSON and token-optimized LLM JSON (`*.llm.json`), plus a `compaction-report.json` with freshness and token metrics.
- **Consequences:**
  - Compacted logs stay aligned with latest canonical entries (`freshness_lag_days=0` target).
  - Prompt token usage is reduced for repeated log-context retrieval.
  - Canonical logs remain non-destructive source-of-truth while derived compact artifacts become the default retrieval surface for LLM workflows.

### DEC-043 - Align context/product docs to the canonical execution protocol

- **Date:** 2026-02-11
- **Status:** Accepted
- **Context:** Process/workflow updates (single feature worktree semantics, explicit planner/plan-reviewer/patcher/tester/reporter roles, role-log ownership, and final `make ci` gating) were implemented in protocol docs, but context/product docs still contained mixed legacy wording and ambiguous guidance.
- **Decision:**
  - Keep `docs/04-process/ticket-execution-protocol.md` as the authoritative execution spec.
  - Sync `docs/00-context/*` and `docs/01-product/prd.md` terminology to the current role model and single-worktree default.
  - Update `docs/04-process/dev-workflow.md` to remove conflicting execution details and defer to protocol semantics where conflicts exist.
  - Clarify in `docs/04-process/definition-of-done.md` that deployment/staging/team-notification checklists are conditional for downstream deployed products.
- **Consequences:**
  - Reduces process drift across context/product/process docs.
  - Makes execution ownership and gate semantics easier to apply consistently during `make feature` runs.
  - Keeps this repo's local-tooling DoD coherent without removing reusable downstream guidance.

### DEC-044 - Stage reliability and workflow-validation work as expected features first

- **Date:** 2026-02-11
- **Status:** Accepted
- **Context:** Most current feature set is already implemented, but two follow-up needs were identified: stronger recovery when template/living files drift during autofix/pre-commit, and a repeatable end-to-end workflow test path. These should be planned without prematurely creating full feature folders.
- **Decision:**
  - Add two new entries to `docs/00-context/expected-features.md`:
    - workflow hardening for template-drift and autofix recovery;
    - end-to-end workflow smoke testing via a synthetic/fake feature.
  - Keep scope at expected-features planning level only for now (no `docs/02-features/<feature>/` scaffolding yet).
- **Consequences:**
  - Captures the next roadmap priorities in the canonical intake document.
  - Preserves incremental planning workflow and avoids creating partial feature specs before kickoff.

### DEC-045 - Mirror new expected features and protocol guardrails directly in the PRD

- **Date:** 2026-02-11
- **Status:** Accepted
- **Context:** `docs/00-context/expected-features.md` now includes two additional reliability/testing features, and protocol docs in `docs/04-process/` contain stricter execution constraints (Allowed Tests policy, explicit high-risk gate behavior, final CI gate limits, precommit log-scope rules) that were only partially reflected in `docs/01-product/prd.md`.
- **Decision:**
  - Update `docs/01-product/prd.md` to include the missing expected features in Process Features.
  - Add matching FR entries for resume behavior, commit gating, and template-drift/autofix hardening, plus a synthetic-feature smoke-test requirement.
  - Expand the PRD Workflow/Process Requirements bullets to match current protocol guardrails.
  - Bump PRD metadata version/date and add a corresponding changelog row.
- **Consequences:**
  - PRD remains a current source of truth for both product scope and execution constraints.
  - Context→PRD mapping stays deterministic when running context-to-product updates.

### DEC-046 - Generate dedicated feature folders for missing PRD P0/P1 process features

- **Date:** 2026-02-11
- **Status:** Accepted
- **Context:** After PRD v0.5 alignment, four P0/P1 process features were not represented as dedicated folders under `docs/02-features/`, while incremental mode requires adding only missing features without touching existing folders.
- **Decision:**
  - Create new feature folders `17` through `20` for:
    - resume in-progress tickets,
    - commit gated by completed ticket docs,
    - template drift hardening + autofix recovery,
    - synthetic feature workflow smoke test.
  - Keep existing folders `01`-`16` unchanged (no regeneration, no renumbering, no deletion).
  - Populate the template core documents (`feature-spec.md`, `tech-design.md`, `dev-tasks.md`, `test-plan.md`) with CLI-focused content and maintain template role-log stubs.
- **Consequences:**
  - PRD-to-features coverage now includes newly introduced P0/P1 process features.
  - Incremental/additive behavior is preserved for existing projects.

### DEC-047 - Run final CI gates on patcher candidate before collecting into main

- **Date:** 2026-02-11
- **Status:** Accepted
- **Context:** `make feature` could collect patcher changes into `main` and only then run final `make ci`. When final CI failed, users were left with partially collected/staged `main` changes despite a failed workflow.
- **Decision:**
  - Execute final `make ci` attempts in the patcher worktree candidate (`cwd=patcher_path`) before any collection into `main`.
  - Run scoped autofix against explicit candidate paths in the patcher worktree and commit patcher autofix deltas before retrying CI.
  - Collect patcher branch changes into `main` only after final gates pass.
- **Consequences:**
  - Final gate failures no longer write partial collection side effects to `main`.
  - Final gate behavior remains deterministic with the same two-attempt CI policy.
  - Patcher autofix output is validated and versioned before collection.

### DEC-048 - Enforce fail-closed reporter handoff completeness and compacted-output gates

- **Date:** 2026-02-12
- **Status:** Accepted
- **Context:** Recent WI retries showed passing tests could still lead to reporter failures because execution-record placeholders remained (`Patch`, `Test Results`, `Reporter Review`, top execution fields), and compacted output expectations drifted from actual artifact paths.
- **Decision:**
  - Enforce strict Allowed Tests commands as explicit, existing unittest/pytest targets.
  - Add pre-reporter completeness checks that block reporter review when execution placeholders or required metadata are still incomplete.
  - Add post-reporter checks that block reporter `PASS` when required compacted outputs are missing or traceability evidence is absent.
  - Keep compacted-output path resolution centralized via the shared compaction resolver and apply it consistently in handoff checks.
  - Remove implemented items from `docs/possible-improvements.md` and keep unresolved proposals only.
- **Consequences:**
  - Reporter outcomes are now fail-closed on incomplete execution records.
  - Retry loops shift from late/manual corrections to deterministic, earlier feedback.
  - Compaction/output expectations are validated directly against declared WI scope.

### DEC-049 - Treat finalization-owned reporter findings as non-blocking and preserve runtime reconciliation

- **Date:** 2026-02-12
- **Status:** Accepted
- **Context:** Feature-18 runs hit `max reporter retry attempts reached` while tester was PASS because reporter commits reset planner-owned `dev-tasks.md` before scope check, discarding runtime reconciliation. Reporter also flagged `Commit`/`Final Report` placeholders that are only completed after final gates.
- **Decision:**
  - Keep planner ownership of `dev-tasks.md` intact, but reorder reporter-step writes so reporter role-log commits occur before runtime reconciliation writes to `dev-tasks.md`.
  - Add a strict classifier for reporter `FAIL` outputs:
    - normalize to non-blocking `PASS` only when failure evidence is finalization-owned (`Commit`, `Final Report`, final `Gates` placeholders),
    - preserve fail-closed behavior for handoff issues (`Reporter Review`, `Test Results`, traceability/completed-output gaps).
  - Update reporter prompt guidance to explicitly state that `Commit`/`Final Report`/final `Gates` completion is post-reporter.
- **Consequences:**
  - Prevents non-actionable reporter retry loops from consuming attempt budget.
  - Preserves deterministic fail-closed checks for real handoff completeness defects.
  - Keeps role boundaries unchanged while removing a self-inflicted reset path in reporter retries.

### DEC-050 - Add opt-in stale-worktree sync resume mode

- **Date:** 2026-02-12
- **Status:** Accepted
- **Context:** `make feature` in `RESUME_MODE=auto` fails if an existing patcher worktree is behind `main`. This protects strict main-freeze policy but blocks users who intentionally want to keep in-progress feature work and continue after main moved.
- **Decision:**
  - Add `RESUME_MODE=sync` as an explicit opt-in startup mode.
  - For stale existing patcher worktrees, `sync` checkpoints dirty startup state and runs `git merge --no-edit refs/heads/main` in the patcher worktree before resume.
  - If merge fails, stop with manual conflict-resolution instructions.
  - Keep `RESUME_MODE=auto` and `RESUME_MODE=prompt` stale behavior unchanged.
  - Refresh `Main head locked:` after successful stale sync so resume can proceed deterministically.
- **Consequences:**
  - Users can continue in-progress features after main advances without recreating worktrees.
  - Default strict behavior remains fail-closed unless sync mode is explicitly selected.
  - Conflict resolution remains human-owned when automatic merge cannot be completed.

### DEC-051 - Provide explicit feature-help entrypoints instead of relying on `make feature --help`

- **Date:** 2026-02-12
- **Status:** Accepted
- **Context:** Operators requested inline help for an increasingly complex `make feature` command, especially around `RESUME_MODE` policies. GNU Make consumes `--help` itself, so `make feature --help` cannot be routed to feature orchestration help text.
- **Decision:**
  - Add explicit help entrypoints: `make feature-help`, `make feature HELP=1`, and `tools/pc-feature --help`.
  - Keep GNU Make semantics unchanged and document why `make feature --help` is not interceptable.
- **Consequences:**
  - Help is now local, deterministic, and does not depend on guessing env vars.
  - Operator UX improves without introducing non-standard Make behavior.

### DEC-052 - Use patcher-safe candidate filtering for final-gate scoped autofix

- **Date:** 2026-02-12
- **Status:** Accepted
- **Context:** Final-gate scoped autofix reused collection candidate paths (`collect_branch_merge_paths`), which intentionally include runtime feature docs (`dev-tasks.md`, role logs). When those paths were passed to patcher autofix and mutated by pre-commit, `commit_role_step` failed with `patcher edited role-scoped files`.
- **Decision:**
  - Add a dedicated helper for final-gate autofix candidate selection that filters patcher-forbidden paths using existing scope rules.
  - Emit explicit diagnostics whenever role-scoped/global-log candidates are skipped from autofix input.
  - Keep final collection into `main` on the existing candidate selector so workflow collection semantics remain unchanged.
- **Consequences:**
  - Prevents recurring late patcher scope aborts caused by planner-owned docs entering autofix.
  - Preserves existing branch collection behavior and avoids side effects on final commit content.

### DEC-053 - Keep Python tooling 3.9-safe and scope final autofix checks to touched deltas

- **Date:** 2026-02-12
- **Status:** Accepted
- **Context:** Feature-18 runs failed in two ways: local/system Python 3.9 crashed on `tools/markdown-lint` annotations (`list[str] | None`), and final-gate scoped autofix falsely aborted because pre-existing planner-owned dirty files (`dev-tasks.md`) were treated as new out-of-scope mutations.
- **Decision:**
  - Add `from __future__ import annotations` to Python tool scripts that use `| None` annotations (`tools/markdown-lint`, `tools/pc-allowed-tests-check`).
  - Keep scoped-autofix fail-closed semantics, but evaluate out-of-scope changes by pre/post dirty snapshot delta so only files touched during autofix are considered violations.
  - Add regression coverage for both compatibility and autofix-delta behavior, including a system-Python-3.9 execution check for `tools/markdown-lint`.
- **Consequences:**
  - Pre-commit markdown checks no longer crash under Python 3.9 environments.
  - Final-gate scoped autofix no longer false-fails on pre-existing out-of-scope dirty files.
  - Real out-of-scope mutations during autofix still fail deterministically.

### DEC-054 - Decouple `--allow` policy scope from literal git staging pathspecs in `pc-commit`

- **Date:** 2026-02-12
- **Status:** Accepted
- **Context:** Final feature commits could fail with `fatal: pathspec '.tmp' did not match any files` because `pc-feature` passes runtime allow prefixes (for scope checks) and `pc-commit` previously reused those raw allow values as literal `git add` pathspecs.
- **Decision:**
  - Keep `--allow` as the policy boundary for changed-path validation.
  - Stage only changed paths discovered from `git status --porcelain` that satisfy allow rules.
  - Do not stage raw allow values directly.
  - Surface concise `pc-commit` failure detail in final workflow event reasons for faster diagnosis.
- **Consequences:**
  - Missing runtime prefixes (like `.tmp`) no longer cause false-negative final commit failures.
  - Commit scope enforcement remains fail-closed via allow-rule validation.
  - Future debugging of commit-step failures becomes deterministic from workflow status/history output.

### DEC-055 - Commit evidence gate must target active WI and prefer actionable failure detail

- **Date:** 2026-02-12
- **Status:** Accepted
- **Context:** Feature execution produced false commit-gate failures by validating stale WI blocks when `dev-tasks.md` entries were not ordered by append position. Commit failure reasons also captured noisy first output lines, and shell quoting in remediation text produced `command not found` side errors.
- **Decision:**
  - `pc-feature` passes the active `work_item_id` to `tools/pc-commit`.
  - `pc-commit` validates that explicit WI when provided.
  - Fallback behavior (no explicit WI) selects newest WI by parsed WI id, not by file position.
  - Commit evidence gate runs before expensive checks and again after checks for fail-fast + fail-closed behavior.
  - Failure detail extraction prioritizes high-signal markers (`Commit evidence gate failed`, `fatal`, traceback/error) instead of first-line output.
  - Remediation output uses literal quoting only (no shell command substitution).
- **Consequences:**
  - Active work-item commit gating is deterministic even when execution log entries are reordered.
  - Commit failure summaries in workflow history are materially more diagnostic.
  - Failing commit-gate runs waste less execution time.

- WI-20260212-04: Process docs changed; orchestrator retained ownership of deferred docs/03-logs updates.

### DEC-056 - Share commit-evidence validator and add deterministic finalization repair/sync

- **Date:** 2026-02-13
- **Status:** Accepted
- **Context:** Commit-gate diagnostics diverged between `pc-feature` and `pc-commit`, and top-field parsing in `pc-commit` could misclassify blank values by consuming next-line labels. Finalization could also validate stale main `dev-tasks.md` content after patcher-side commit/report updates.
- **Decision:**
  - Introduce `lib/commit_evidence_gate.py` as the single source of truth for commit-evidence rules and required-field diagnostics.
  - Update `pc-commit` to use the shared validator.
  - Update `pc-feature` to use the shared validator, run one deterministic evidence-repair pass from tester/reporter artifacts, and normalize stale non-completed top `Outcome` to `pass` only when final-gate evidence is completed.
  - Sync finalized patcher `dev-tasks.md` into main worktree immediately before final staging/commit.
- **Consequences:**
  - Eliminates parser drift and misleading multiline status errors.
  - Makes final commit gate behavior deterministic on the same finalized artifact content that is staged.
  - Reduces late commit failures caused by stale placeholders/top fields while preserving fail-closed behavior for genuinely missing evidence.

### DEC-057 - Let `RESUME_MODE=sync` reconcile lock drift without requiring stale-start detection

- **Date:** 2026-02-13
- **Status:** Accepted
- **Context:** `RESUME_MODE=sync` was documented as explicit drift reconciliation, but implementation refreshed `Main head locked:` only when startup had already detected a stale (`behind main`) patcher worktree in the same run. Lock mismatches could still fail in sync mode when the branch was not classified stale at startup.
- **Decision:**
  - On locked-main mismatch, treat `RESUME_MODE=sync` as explicit consent to reconcile drift.
  - Re-evaluate behind-state at lock-check time; if behind, checkpoint dirty startup state and merge `refs/heads/main` before refreshing lock.
  - If not behind, refresh the lock note directly in sync mode.
  - Keep `auto`/`prompt` fail-closed and include behind-state guidance in the failure message.
- **Consequences:**
  - Sync mode now matches operator intent: explicit reconciliation instead of conditional partial behavior.
  - Strict default policy remains unchanged for non-sync modes.
  - Drift diagnostics are more actionable when runs are blocked.

### DEC-058 - Reconcile stale section outcomes from role artifacts before commit gate

- **Date:** 2026-02-13
- **Status:** Accepted
- **Context:** Commit auto-repair could leave `Outcome: needs replan` even after successful reruns when `Reporter Review`/`Test Results` sections were non-pending but stale, because section reconciliation only ran for pending placeholders while role logs already carried newer PASS artifacts.
- **Decision:**
  - Add deterministic section-outcome reconciliation in `pc-feature` commit repair using latest tester/reporter artifacts, even when sections are non-pending.
  - Prefer artifact outcomes over stale section outcomes when deriving top `Outcome` during commit repair.
  - Emit explicit terminal reporter workflow events (`DONE`/`FAIL`) in the non-skip reporter path so workflow status does not remain open-ended.
- **Consequences:**
  - Reduces false commit-gate failures caused by stale execution-log section outcomes.
  - Keeps fail-closed behavior when artifacts and gate evidence still do not support completion.
  - Workflow status telemetry remains consistent across skip and non-skip reporter paths.

- WI-20260213-05: Process docs changed; orchestrator retained ownership of deferred docs/03-logs updates.

### DEC-059 - Keep `investigate` as a chat-only, plan-only skill with no autonomous fixes

- **Date:** 2026-02-13
- **Status:** Accepted
- **Context:** A reusable output-investigation skill was needed for frequent manual Codex runs, but the user explicitly constrained scope to analysis and recommendations only.
- **Decision:**
  - Implement `investigate` as a chat-first skill with inline inputs (`command` + `output`) and no CLI execution contract.
  - Require deterministic analysis flow: issue detection, root-cause hypotheses, docs-based expected-vs-actual comparison, and multiple permanent fix options.
  - Enforce docs-conflict surfacing and docs-improvement recommendations whenever source expectations disagree.
  - Enforce decision gating: ask the user questions when a decision is required; do not autonomously choose a fix path.
  - Restrict auto-fix to future-facing recommendations only; no file edits, hook changes, or command execution in the current run.
- **Consequences:**
  - Standardizes repeated diagnosis prompts into one reusable skill while keeping execution non-destructive.
  - Preserves human control for ambiguous or policy-impacting remediation choices.
  - Leaves room for future automation design without introducing implicit process changes now.

### DEC-060 - Create `workflow-hardening-top5` as a read-only prioritization skill with max-5 output

- **Date:** 2026-02-13
- **Status:** Accepted
- **Context:** The project needed a reusable chat-only skill to turn `docs/possible-improvements.md` into high-value workflow hardening recommendations. The user required prioritization with a strict upper limit of five items and allowed fewer than five when evidence is insufficient.
- **Decision:**
  - Add a dedicated skill at `.codex/skills/workflow-hardening-top5`.
  - Restrict scope to workflow/process robustness, stability, and issue prevention; exclude feature expansion.
  - Enforce output size as `<= 5` recommendations with evidence-based filtering and deduplication.
  - Require each recommendation to include why-now rationale, benefits, risks/trade-offs, and no-side-effect rollout guidance.
  - Keep execution non-destructive: no file edits, no patch/apply actions, no auto-implementation.
- **Consequences:**
  - Recommendation quality and consistency improve across repeated chats.
  - Human decision authority remains intact because the skill is analysis-only.
  - The skill may intentionally return fewer than five items when confidence or evidence is limited.

### DEC-061 - Keep Allowed Tests hardening deterministic (template + validation), skip runtime auto-fix

- **Date:** 2026-02-13
- **Status:** Accepted
- **Context:** Feature 19 failed on invalid Allowed Tests target drift (`tests.test_pc_precommit` missing). Auto-fix ideas were evaluated but carry non-negligible risk of selecting semantically wrong tests or masking documentation drift.
- **Decision:**
  - Update feature and template Allowed Tests guidance to require explicit existing unittest/pytest commands and validation through `tools/pc-allowed-tests-check`.
  - Add deterministic template-schema enforcement in `tools/pc-devtasks-schema-check` so future feature templates keep the required Allowed Tests guidance markers.
  - Do not implement runtime Allowed Tests auto-rewrite/suggestion logic at this stage.
- **Consequences:**
  - Future feature skeletons inherit a stricter and clearer Allowed Tests contract.
  - Validation shifts left (template/schema time) without changing `pc-feature` execution semantics.
  - Residual risk from risky auto-fix heuristics is intentionally avoided.

### DEC-062 - Auto-sanitize preflight scope and auto-repair repeated reviewer policy blocks

- **Date:** 2026-02-13
- **Status:** Accepted
- **Context:** Reviewer blocks repeatedly surfaced forbidden plan paths copied from preflight `files_to_change` context (role/global logs), causing stagnation loops before patching.
- **Decision:**
  - Auto-sanitize preflight `files_to_change` to patcher-allowed paths only.
  - Convert forbidden role/global-log targets into explicit reporter/orchestrator handoff notes in preflight docs updates.
  - Keep strict plan policy checks but focus path checks on `Files to change` plus explicit write-intent lines.
  - Add deterministic planner auto-rewrite for forbidden `Files to change` entries and policy-diff diagnostics.
  - On repeated identical reviewer-policy signatures, inject a deterministic recovery plan template before stagnation termination.
- **Consequences:**
  - Reduces repeated reviewer `BLOCK` loops caused by forbidden-path echo from preflight context.
  - Preserves fail-closed behavior when policy issues remain unresolved after deterministic recovery.
  - Improves operator visibility with explicit policy-diff and auto-fix notes in iteration logs.

### DEC-063 - Resume planner stability and plan-policy parser hardening

- **Date:** 2026-02-13
- **Status:** Accepted
- **Context:** Feature 19 reproduced planner/reviewer loops where malformed non-contract plan content and command-policy false positives blocked convergence. Resume after tester `FAIL` could trigger full plan regeneration even when a valid plan already existed.
- **Decision:**
  - On resume after tester `FAIL`, force planner-create only when the `Plan` section is incomplete; otherwise keep and revise existing plan.
  - Enforce planner-create output validation before writing `#### Plan`: required contract sections, anti-hardcode coverage (when enforced), and policy checks.
  - Harden command-policy parsing to avoid false positives from path-like tokens (for example `tools/pc-hooks-run`) while still blocking explicit `tools/pc-feature` command intent.
  - Extend deterministic policy auto-rewrite so malformed non-contract plans can be rehydrated to a compliant `Plan Contract v1` template.
  - Keep prompt task naming deterministic and add separator fallback (`_`/`-`) only when one variant is missing, avoiding ambiguous dual-file resolution.
- **Consequences:**
  - Reduces non-converging planner/reviewer loops caused by malformed plan bodies and parser false positives.
  - Keeps fail-closed behavior for real policy violations while reducing noisy false command blocks.
  - Improves resume determinism without altering orchestration authority boundaries.

### DEC-064 - Harden planner-create contract intake with deterministic rejection artifacts and terminal failure state

- **Date:** 2026-02-13
- **Status:** Accepted
- **Context:** Workflow smoke run `WI-20260213-01` failed at planner-create quality gate while leaving partial planner side effects and non-terminal runtime state, reducing diagnostics quality and recovery determinism.
- **Decision:**
  - Normalize list/indent heading prefixes when matching `Plan Contract v1` section labels so semantically-correct section headings are accepted even with markdown bullets/indentation.
  - On planner-create quality failure, write deterministic diagnostics and raw planner payload to `logs/<WI>/planner-create-rejection.md`.
  - Emit explicit terminal workflow events for both planner and feature with `state=FAILED` when planner-create quality checks fail.
  - Revert unexpected planner-create side effects in `dev-tasks.md` before exiting so rejected output cannot persist as active plan content.
  - Align planner create/update prompt examples (live + template copies) to canonical heading-at-column-1 contract formatting.
- **Consequences:**
  - Improves planner-create diagnostics and workflow state correctness without relaxing fail-closed quality gates.
  - Reduces false negatives caused by superficial markdown heading formatting variance.
  - Preserves deterministic rollback behavior for rejected planner-create output.

- WI-20260213-01: Process docs changed; orchestrator retained ownership of deferred docs/03-logs updates.

### DEC-065 - Relax `investigate` input contract to support description-only incidents

- **Date:** 2026-02-14
- **Status:** Accepted
- **Context:** The existing `investigate` skill required both `command` and full `output`, which blocked valid investigations when command output was unavailable or unhelpful (for example, command succeeds but generated artifacts are wrong).
- **Decision:**
  - Keep CLI-evidence mode as the preferred path: `command + output`.
  - Add description-only mode: `issue=<plain-language description>`.
  - Accept free-text invocation and normalize it to `issue=<...>`.
  - Require a clarifying question only when both `output` and `issue` are missing.
  - Align the rubric and agent metadata so evidence ranking supports `output` when present or `issue/context` when output is absent.
- **Consequences:**
- Investigation workflow remains backward compatible for existing `command/output` usage.
- Users can now diagnose outcome failures without pasting large CLI output.
- Recommendations remain evidence-ranked, with explicit confidence/assumption handling when output is missing.

### DEC-066 - Make PRD-to-features hydrate-only by default (no skeleton mode)

- **Date:** 2026-02-14
- **Status:** Accepted
- **Context:** Running `prd-to-features` in bootstrapped repos produced many
  new feature folders containing unadapted template content, which did not meet
  feature documentation quality expectations.
- **Decision:**
  - Enforce hydrate-only behavior as the default and only mode for
    `tools/prd-to-features`.
  - Generate feature-specific content for core docs during feature creation.
  - For existing non-done folders, update only missing files and
    placeholder/incomplete core docs (no destructive overwrite of authored
    docs).
  - Read implementation/decision logs to skip features explicitly marked
    completed, rejected, or deferred.
  - Update skill/rule documentation to explicitly reject skeleton-only outputs.
- **Consequences:**
  - New features generated from PRD are immediately usable and contextualized.
  - Incremental safety remains intact while eliminating template-only drift.
- Existing authored feature docs are preserved unless clearly template-like or
  incomplete.

### DEC-067 - Legacy bootstrap resume compatibility without weakening commit status gate

- **Date:** 2026-02-14
- **Status:** Accepted
- **Context:** Some bootstrapped repositories contain legacy summary-only work
  item entries (`Outcome: pass`, missing `####` sections). Startup resume in
  `pc-feature` hard-fails on missing sections, but commit gates intentionally
  require normalized `Outcome: completed`.
- **Decision:**
  - Keep commit-evidence strictness unchanged (`Outcome: completed` remains the
    only accepted completed status at commit gate).
  - Add startup compatibility in `pc-feature` to treat legacy bootstrap
    summary-only entries as non-resumable and start a fresh work item.
  - Add deterministic startup section auto-repair for resumable entries missing
    required section headers.
  - Add dedicated migration utility for legacy bootstrap entries.
- **Consequences:**
  - Freshly bootstrapped legacy repos no longer crash on first `make feature`.
- Commit policy remains fail-closed and consistent with protocol/docs.
- Teams can migrate legacy docs explicitly without forcing destructive rewrites.

### DEC-068 - Bootstrap target repos as living-runtime assets (including prompts) without shipping `tools/templates`

- **Date:** 2026-02-14
- **Status:** Accepted
- **Context:** Downstream bootstrapped repos failed at planner startup because `pc-feature` requires runtime prompts from `prompts/*.md`, while `bootstrap-into` copied template assets and tooling but did not materialize prompts as living files. The target repo also carried `tools/templates/*` despite a living-file deployment intent.
- **Decision:**
  - Update `bootstrap-into` to deploy `tools/templates/prompts/*.md` as living files into `prompts/*.md`.
  - Stop copying `tools/templates/*` into downstream target repos during bootstrap.
  - Treat `prompts/*` as sync-managed bootstrap assets for reapply behavior.
  - Keep source-repo prompt/template parity guardrails by extending `pc-template-sync` and template-sync hook triggers to include prompt paths.
  - Update process docs/remediation text to support both template-enabled repos and living-only bootstrapped repos.
- **Consequences:**
- Fresh bootstraps are runtime-ready for `pc-feature` without additional prompt-file recovery.
- Target repos become lighter and avoid stale template directories.
- Source repo retains explicit parity controls for managed templates and prompts.

### DEC-069 - Treat reporter sandbox/index-lock commit failures as non-blocking and centralize role commits via script

- **Date:** 2026-02-14
- **Status:** Accepted
- **Context:** Reporter runs in bootstrapped/downstream environments can emit `Outcome: FAIL` solely because commit operations are blocked by sandbox git index lock permissions (`.git/index.lock`), creating false-negative reporter failures and retry-loop exhaustion.
- **Decision:**
  - Route role commits through a dedicated script (`tools/pc-role-commit`) invoked by `pc-feature` instead of inline `git add`/`git commit` calls.
  - Classify reporter FAIL feedback that is limited to sandbox/index-lock commit restrictions as environment-only and auto-normalize it to PASS.
  - Keep fail-closed behavior for real reporter scope/handoff gaps by requiring no actionable scope markers for the environment-lock normalization path.
  - Update reporter prompt contracts (live + template) to prohibit direct `git commit` commands and make commit ownership explicit.
- **Consequences:**
  - Reporter retry loops no longer fail on non-actionable environment commit restrictions.
  - Role-commit behavior is deterministic and script-owned, improving consistency across repos and runtimes.
  - Genuine reporter completeness failures remain blocking.

### DEC-070 - Treat metadata-drift-only reporter failures as non-blocking with opt-in deterministic reconciliation writes

- **Date:** 2026-02-15
- **Status:** Accepted
- **Context:** In bootstrapped/downstream repos, reporter can return `Outcome: FAIL` due to stale machine-owned execution-summary metadata (for example `Outcome: needs replan`, stale `Test Results`, stale `Docs/logs updated`) even when tester evidence is current and scope checks are otherwise complete.
- **Decision:**
  - Add a dedicated reporter-failure classifier for metadata-drift-only failures and normalize this class to reporter `PASS` (non-blocking).
  - Introduce `AUTO_REPAIR_RUNTIME_METADATA` modes: `off`, `warn`, `apply`, with default `warn`.
  - Keep `warn` as no-side-effect preview-only behavior; allow deterministic writes only in explicit `apply` mode.
  - Restrict runtime metadata apply writes to an allowlist of machine-owned fields/sections and block apply when non-allowlisted updates would be required.
  - Emit deterministic runtime metadata reconciliation ledger notes in execution logs for traceability.
- **Consequences:**
  - Reporter retry loops no longer exhaust on non-actionable stale execution metadata.
  - Default behavior remains low-risk and side-effect constrained.
  - Operators retain explicit control to persist reconciliation updates when desired.

### DEC-071 - Remove hard PyYAML runtime dependency from skills metadata check and enforce no-site-packages execution

- **Date:** 2026-02-15
- **Status:** Accepted
- **Context:** Cross-repo `make feature F=01` runs in a consumer worktree failed deterministically at `tools/pc-skills-metadata-check` with `ModuleNotFoundError: No module named 'yaml'` (incident evidence offload ids `84871f42fee0a40815efe8bdcc30043b3e3de57cf2d949b065dfc65a22becfa3` and `30ea6a8cd205348489fa4f415110d6b39fcf12d4eafbc546f9d58e3b82a1f01f`).
- **Decision:**
  - Add a stdlib-backed YAML fallback parser in `tools/pc-skills-metadata-check` so skill metadata validation no longer hard-crashes when `PyYAML` is unavailable.
  - Keep `PyYAML` as preferred parser when present; fallback parser is used only when `yaml` cannot be imported.
  - Run `skills-metadata-check` via `python3 -S` in live/template `Makefile` targets to make dependency regressions deterministic in local and CI runs.
  - Add explicit regression coverage that executes the tool with `python3 -S`.
- **Consequences:**
  - Bootstrapped/consumer repos no longer fail on missing site-packages for this check.
- CI now fails fast if a future change reintroduces hard third-party dependency assumptions.
- YAML parsing is intentionally constrained to the skill metadata schema in fallback mode.

### DEC-072 - Align dev-tasks schema/migration checks with resume tester-outcome invariant

- **Date:** 2026-02-15
- **Status:** Accepted
- **Context:** Consumer work items could contain complete `Test Results` with no
  parsed tester outcome in `Tester Feedback`, which passes
  `pc-devtasks-schema-check` but deterministically blocks `pc-feature` resume
  (`missing critical artifact: test results exist without tester feedback`).
- **Decision:**
  - Add a semantic invariant check in `tools/pc-devtasks-schema-check` that
    fails when `Test Results` is complete and `Tester Feedback` lacks an
    `Outcome`.
  - Extend `tools/pc-devtasks-migrate-legacy` to auto-repair this mismatch by
    upserting `Tester Feedback` outcome, derived deterministically from
    `Test Results` evidence (explicit outcome first, then exit-code/pass-fail
    inference, fallback `SKIPPED`).
  - Keep `pc-feature` resume fail-closed invariant behavior unchanged.
- **Consequences:**
  - Schema validation now catches this contradiction before runtime resume.
  - Legacy repos get a deterministic migration path without manual section edits.
  - Resume contract remains strict and consistent across tools.

### DEC-073 - Treat machine-owned status-parity contradictions as metadata-drift-only reporter failures

- **Date:** 2026-02-15
- **Status:** Accepted
- **Context:** `make feature F=02` could terminate with `pc-feature: max reporter retry attempts reached` when reporter feedback described stale machine-owned execution metadata using wording variants that did not match existing metadata-drift markers.
- **Decision:**
  - Extend reporter metadata-drift classification in `tools/pc-feature` with structural contradiction detection based on machine-owned field references + status-state contradictions (stale/mismatch/parity drift), not only fixed phrases.
  - Keep fail-closed behavior for actionable scope gaps by expanding blocking markers (`pending placeholders`, `still pending`, `missing an outcome line`).
  - Continue deterministic runtime metadata reconciliation in the metadata-drift normalization path before retry escalation.
- **Consequences:**
  - Reporter wording variants that describe machine-owned status contradictions are normalized to PASS consistently.
  - Actionable handoff/scope issues remain `scope_gap` and continue through Planner rework.
  - Reporter retry loops no longer exhaust on metadata-only contradiction phrasing.
