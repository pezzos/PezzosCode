# AGENTS.md

This folder contains the documentation system for AI-assisted development.

Start here:

- `docs/README.md` explains the structure and how to use it.

Find the right document by topic:

- Product vision, boundaries, and system state: `docs/00-context/`
- Context boundaries and operating model: `docs/00-context/context-boundaries-operating-model.md`
- Requirements and success criteria: `docs/01-product/`
- Feature-specific work: `docs/02-features/`
- Decisions, bugs, validation, and learnings: `docs/03-logs/`
- Workflow and standards: `docs/04-process/` (use `docs/04-process/ticket-execution-protocol.md` for ticket implementation)
- PO loop: `docs/04-process/human-orchestration-workflow.md`

Ticket implementation entrypoint:

- Run `make feature F=<feature-id>` to bootstrap and execute autonomously by default.
- Manual mode: `make feature MANUAL=1 F=<feature-id>`.
- If HIGH RISK, stop after Preflight and set status to "Awaiting PO Approval".

Operational rules:

- Codex MUST use Serena for symbol-aware navigation and edits when available.
- Codex MUST use `tools/offload-proxy/pp` for commands that can produce large output (e.g., `rg`, `sed` on large ranges, tests, or logs).
- Codex MUST update `docs/03-logs/*.md` to record decisions, implementation changes, bugs, validations, and insights. If no log entry is needed, explicitly state why in the response.

If you are unsure where to look, read `docs/README.md` first.
