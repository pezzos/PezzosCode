# AGENTS.md

Purpose of this folder:

- Define how we work, quality gates, and AI prompting standards.

Key files:

- `docs/04-process/dev-workflow.md`: human + LLM workflow, including the template bootstrapping flow from context → PRD → features.
- `docs/04-process/definition-of-done.md`: completion criteria.
- `docs/04-process/llm-prompts.md`: prompt templates and guidance.
- `docs/04-process/ticket-template.md`: ticket format with PRD traceability, change budget, and docs update checklist.
- `docs/04-process/ticket-execution-protocol.md`: canonical ticket implementation workflow (TDD + gates).
- `docs/04-process/human-orchestration-workflow.md`: canonical PO loop for bootstrapping and iterating features.

Ticket entrypoint:

- Run `make feature F=<feature-id>` to bootstrap and execute autonomously by default.
- Manual mode: `make feature MANUAL=1 F=<feature-id>`.
- If HIGH RISK, stop after Preflight and set status to "Awaiting PO Approval".
