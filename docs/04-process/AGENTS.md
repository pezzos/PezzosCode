# AGENTS.md

Purpose of this folder:

- Define how we work, quality gates, and AI prompting standards.

Key files:

- `docs/04-process/dev-workflow.md`: human + LLM workflow, including the template bootstrapping flow from context → PRD → features.
- `docs/04-process/definition-of-done.md`: completion criteria.
- `docs/04-process/llm-prompts.md`: prompt templates and guidance.
- `docs/04-process/ticket-execution-protocol.md`: canonical work item execution workflow (TDD + gates).
- `docs/04-process/human-orchestration-workflow.md`: canonical PO loop for bootstrapping and iterating features.
- `prompts/`: role-specific prompts (planner, plan-reviewer, patcher, tester, reporter).
- `docs/possible-improvements.md`: human-gated proposals after failures; orchestrator-owned and deduplicated from role feedback.

Work item entrypoint:

- Run `make feature F=<feature-id>` to bootstrap and execute autonomously by default.
- Manual mode: `make feature MANUAL=1 F=<feature-id>`.
- If HIGH RISK, stop after Preflight and set status to "Awaiting PO Approval".
