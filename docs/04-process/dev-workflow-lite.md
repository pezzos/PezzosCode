# Dev Workflow (Lite)

1. Frame
- Clarify context, constraints, and acceptance criteria.

2. Plan
- Convert scope into orchestrator slices with validation commands.

3. Dispatch
- Orchestrator delegates to native Codex roles.

4. Validate
- Run deterministic checks.
- Use scoped Codex autofix fallback when needed.
- Keep review gate orchestrator-owned.

5. Finalize
- Orchestrator accepts or revises.
- Orchestrator updates logs after acceptance.
- Report executed commands and outcomes.
