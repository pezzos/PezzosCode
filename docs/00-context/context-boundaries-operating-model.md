# Context Boundaries and Operating Model

## Purpose

Define the operational boundaries and usage expectations for PezzosCode.
Prevent scope creep by stating explicit non-goals and post-MVP limits.
Provide guardrails that keep the workflow aligned with a simple, robust, AI-first process.

## Scope Boundaries

- Local CLI tool only; manual execution, no daemon or cron.
- Target platform is macOS (primary); no Windows support.
- Bootstraps new projects or updates existing repos with templates.
- Enables AI-driven execution of features/tickets with minimal manual setup.
- Serves one user only and is intentionally tuned to that user's tools/habits.
- Git is built into the workflow; tools operate inside repo boundaries.
- Idempotent, repeatable runs are required to avoid rework and token waste.

## Non-Goals

- Automatic background sync or scheduled runs.
- Cloud services, remote state, or multi-user collaboration.
- Generic support for multiple development styles or broad team configurability.
- UI (web or desktop) in this project.
- Windows support.
- Extra configuration or complexity beyond essentials.

## Anti-Patterns (Failure Modes)

- Turning PezzosCode into a background agent, daemon, or scheduler.
- Adding cloud sync, remote state, or SaaS concepts.
- Generalizing the workflow for audiences beyond the primary user.
- Adding UI layers beyond basic CLI output.
- Adding Windows support.
- Adding features that increase complexity without clear user benefit.
- Weakening idempotency/guardrails to “move faster.”

## Operating Model

- User runs the CLI to bootstrap or update a project, then uses CLI commands to drive AI execution.
- MVP baseline is complete and in use; ongoing work is optimization/hardening only.
- Human gates are required for HIGH-risk work; approvals are explicit and prompted.
- The workflow loops: context → PRD → features → ticket → execute → repeat.
- Each ticket follows Plan → Patch → Test → Report.
- Execution roles run in a single feature worktree by default; role scope is enforced by owned files/logs.
- Planner and patcher iterate based on plan-reviewer/tester/reporter feedback until issues are resolved.
- If requirements are unclear, stop and ask before continuing.
- The system must recover from errors and allow safe re-runs.
- Prefer tool-assisted workflows (Serena, hooks, scripts) over ad-hoc AI output.
- Offload large outputs to reduce token usage.
- Treat AI as a developer: provide the tools and guardrails it needs to work autonomously.
- Prefer auto-fix and auto-recovery for deterministic failures before requesting human input.
- Deterministic steps are executed by scripts via a shared runner library.
- Logs are structured, timestamped, and written to predictable per-work-item locations.
- PRD → features updates are incremental; never delete or recreate completed features.
- Plan validation is handled by a dedicated Plan Reviewer role before patching.
- Learning loops propose improvements after failures and require human approval to apply.
- Use a single worktree per feature; do not maintain `feature-worktrees.json`.

## Product Stance

- Simplicity and robustness > feature breadth.
- AI should work without manual setup per project.
- Automation that removes user toil > additional feature surface area.
- Idempotency and recoverability are non-negotiable.
- Minimal prompts and minimal friction.
- Checks and linting should run via local hooks or scripts, not manual AI steps.
- Keep dependencies minimal; add tools only when they materially reduce manual work or tokens.
- Favor script delegation over LLM steps when outcomes are deterministic.
- Prefer minimal, tail-friendly logs over verbose, unstructured output.

## MVP Definition of Done

- [x] One command can bootstrap a project with the PezzosCode template.
- [x] The user can execute approved tickets with AI and minimal manual work.
- [x] The workflow is stable, idempotent, and recoverable after failures.
- [x] The tool works on macOS for Python/TS/Node/Rust/Go projects.
- [x] MVP is complete even if no new features are added.

## Explicit Stop Condition

- MVP baseline is considered complete.
- Further work is limited to workflow hardening: reduce errors, reduce tokens, and remove unused complexity.
- Do not expand product scope (new platforms, multi-user, UI, cloud, generic style support) without an explicit new product decision.

## If you are unsure

- Stop and ask for clarification rather than guessing.
- Do not expand scope beyond stated boundaries.
- If a change helps generic users but not the primary user, reject it by default.
- Do not invent features, automation paths, or future use cases.
- Do not weaken guardrails or idempotency to “move faster.”

## High-Risk Approval

- When a ticket is HIGH risk, the CLI must present the risk summary and prompt for approval.
- The prompt should be explicit (e.g., "Do you approve the HIGH-risk ticket? (y/n)").
- Approval can be recorded as `approval: "granted"` in ticket frontmatter.
