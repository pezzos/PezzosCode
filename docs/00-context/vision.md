# Vision

## WHY does this product exist?

<!-- Describe the core problem this product solves and the value it provides -->

**Problem:**

- Bootstrapping or updating a project for AI-assisted delivery is still costly when workflow assumptions are not pre-wired.
- The product serves one user only (single developer/PO), so every extra prompt or manual input is avoidable toil.
- Generic support for many development styles adds complexity that this project does not need.
- Deterministic failures (template drift, lint/format, staging, retries) still create rework when not auto-fixed.
- Noisy output and unnecessary LLM steps waste tokens and slow down execution.
- Now that MVP is working across other projects, unused skills and over-complex paths become maintenance debt.

**Vision:**

- One command bootstraps or updates a project that follows the PezzosCode process.
- After bootstrap/update, the user works with AI with almost no manual work beyond describing features/tasks.
- The AI is treated as a developer: the repo ships the tools and hooks it needs to be autonomous and productive.
- Commands stay simple and memorable while the workflow gets more robust and token-efficient.
- Deterministic issues are auto-fixed by scripts/AI before asking the human for input.
- Work is orchestrated with clear roles (orchestrator, planner, plan-reviewer, patcher, tester, reporter) and clean workspaces.
- Large outputs are offloaded, keeping AI context focused and deterministic.
- Deterministic workflow steps are delegated to scripts with a shared runner and consistent metadata.
- Execution is observable: structured logs, timestamps, and tail-friendly output are standard.
- PRD → features updates are incremental, with strict template/project boundaries to prevent regressions.
- Learning loops propose improvements after failures, gated by human approval.
- Plans are validated by a dedicated Plan Reviewer role before code changes.
- Post-MVP work stays focused on reducing errors, reducing tokens, and removing unused complexity.

## WHAT exists RIGHT NOW?

<!-- Current state of the product/system -->

**Product Boundaries:**

- In scope: personal CLI tooling/templates to bootstrap/update and run the PezzosCode process on macOS.
- Out of scope: UI, cloud services, multi-user support, Windows support, and generic support for other development styles.
- The project is intentionally opinionated for one user's tools/habits; no attempt is made to fit all teams.

**Current Capabilities:**

- Bootstrap or update a project with templates and run a guided workflow with AI assistance.
- Tools support ticket execution, preflight, and documentation flow.
- Targeted for macOS and projects using Python, TypeScript/Node, Rust, or Go.
- MVP baseline is already used in other projects; current effort is workflow hardening.

**Key Metrics:**

- One-command bootstrap/update works consistently across projects.
- AI implements approved features/tasks with near-zero manual intervention.
- Workflow errors and rerun failures trend downward over time.
- Token usage per completed work item trends downward without reducing quality.

## Anchor Points

<!-- The unchanging truths that guide all decisions -->

**Product Principles:**

- Simple and robust: fewer knobs, fewer failure modes.
- AI‑first, low setup: AI can operate without manual wiring in each project.
- Opinionated over configurable: optimize for one user's workflow, tools, and habits.
- Idempotent and recoverable: safe reruns, skip completed work, handle errors gracefully.
- Minimal dependencies: only essential tools to keep setup and maintenance light.
- Token‑efficient workflow: prefer hooks and tools over verbose AI instructions.
- Predictable execution: Plan → Patch → Test → Report for every ticket.
- Parallelizable: use separate role sessions with a single feature worktree by default; add extra worktrees only when necessary.
- Script-first for deterministic tasks, AI for judgment-heavy steps.
- Observability-first: structured logs and traceable runs.
- Learning loops with human gates to reduce repeated failures.

**Target Users:**

- Primary persona: Single developer/PO using Codex to drive the workflow.
- Secondary persona: None (single‑user focus).
- What they need most: one command bootstrap, minimal manual work, predictable AI workflow.

**Strategic Constraints:**

- macOS‑first, CLI‑only, no Windows support.
- No cloud or multi‑user features; focus on essentials.
- Personal use, prioritize robustness over feature breadth.
- Do not generalize for external development styles; reduce toil for the primary user first.
