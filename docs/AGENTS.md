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

Ticket implementation entrypoint:
- Run `make ticket T=<id>` before executing a ticket.
- If HIGH RISK, stop after Preflight and set status to "Awaiting PO Approval".

If you are unsure where to look, read `docs/README.md` first.
