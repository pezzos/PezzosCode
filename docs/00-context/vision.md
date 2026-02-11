# Vision

## WHY does this product exist?

<!-- Describe the core problem this product solves and the value it provides -->

**Problem:**

- Bootstrapping a new project with an AI‑first workflow is time‑consuming and inconsistent without a stable template.
- The primary user (single developer/PO) wants to describe problems/features and let AI implement them with minimal manual setup.
- Without a standardized process, work becomes brittle, repetitive, and error‑prone.
- AI needs a minimal, reliable toolchain to operate like a productive developer without constant human intervention.
- Context mistakes between template vs. project and noisy outputs cause wasted tokens and rework.
- Lack of predictable gates (plan/patch/test/report) slows iteration and increases regressions.
- Deterministic tasks are still pushed through LLMs, burning tokens that should be handled by scripts.
- Limited observability makes CI/test/precommit failures hard to diagnose and slows iteration.
- Non-incremental PRD → features updates cause regressions and confusion.
- Role prompts and plan review gates are inconsistent, creating avoidable rework.
- Learning loops for improving scripts and processes are ad hoc.

**Vision:**

- One command bootstraps a project that follows the PezzosCode process.
- After bootstrapping, the user can work with AI with almost no manual work beyond describing features/tasks.
- The AI is treated as a developer: the repo ships the tools and hooks it needs to be autonomous and productive.
- Commands are simple, memorable, and the workflow is robust, low‑token, and easy to use.
- Work is orchestrated with clear roles (orchestrator, planner, plan-reviewer, patcher, tester, reporter) and clean workspaces.
- Large outputs are offloaded, keeping AI context focused and deterministic.
- Deterministic workflow steps are delegated to scripts with a shared runner and consistent metadata.
- Execution is observable: structured logs, timestamps, and tail-friendly output are standard.
- PRD → features updates are incremental, with strict template/project boundaries to prevent regressions.
- Learning loops propose improvements after failures, gated by human approval.
- Plans are validated by a dedicated Plan Reviewer role before code changes.

## WHAT exists RIGHT NOW?

<!-- Current state of the product/system -->

**Product Boundaries:**

- In scope: CLI tooling and templates to bootstrap and run the PezzosCode process on macOS.
- Out of scope: UI, cloud services, multi‑user support, Windows support, and extra complexity beyond essentials.
- A future CLI/TUI can exist, but any UI will live in another project and only call CLI commands.

**Current Capabilities:**

- Bootstrap a project with a template and run a guided workflow with AI assistance.
- Tools support ticket execution, preflight, and documentation flow.
- Targeted for macOS and projects using Python, TypeScript/Node, Rust, or Go.

**Key Metrics:**

- Success is one‑command bootstrap + AI execution with almost no manual setup.
- AI can implement approved features/tasks without workflow failures.
- Simplicity, robustness, and idempotent reruns are the core success signals.

## Anchor Points

<!-- The unchanging truths that guide all decisions -->

**Product Principles:**

- Simple and robust: fewer knobs, fewer failure modes.
- AI‑first, low setup: AI can operate without manual wiring in each project.
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
