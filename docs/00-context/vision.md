# Vision

## WHY does this product exist?

<!-- Describe the core problem this product solves and the value it provides -->

**Problem:**
- Bootstrapping a new project with an AI‑first workflow is time‑consuming and inconsistent without a stable template.
- The primary user (single developer/PO) wants to describe problems/features and let AI implement them with minimal manual setup.
- Without a standardized process, work becomes brittle, repetitive, and error‑prone.

**Vision:**
- One command bootstraps a project that follows the PezzosCode process.
- After bootstrapping, the user can work with AI with almost no manual work beyond describing features/tasks.
- Commands are simple, memorable, and the workflow is robust and easy to use.

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

**Target Users:**
- Primary persona: Single developer/PO using Codex to drive the workflow.
- Secondary persona: None (single‑user focus).
- What they need most: one command bootstrap, minimal manual work, predictable AI workflow.

**Strategic Constraints:**
- macOS‑first, CLI‑only, no Windows support.
- No cloud or multi‑user features; focus on essentials.
- Personal use, prioritize robustness over feature breadth.
