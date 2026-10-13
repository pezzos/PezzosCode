# AGENTS.md

This repository is docs-first and orchestrator-first.

## Source of truth

- `docs/AGENTS.md`
- `docs/README.md`
- `docs/00-context/*`
- `docs/01-product/*`
- `docs/02-work-items/backlog.md`
- `docs/03-logs/*`
- `docs/04-process/*`
- `.orchestrator/profile-catalog.json`
- `.orchestrator/native-role-manifest.json`
- `.orchestrator/skills-catalog.json`
- `.codex/config.toml`
- `.codex/agents/*`
- `prompts/specialists/*`
- `.agents/skills/README.md`

## Autonomy model

- Human defines context and validates implementation kickoff.
- Orchestrator executes the implementation loop autonomously after kickoff.
- Native Codex roles run within explicit scope and contracts.
- Logical specialist profiles map directly to native Codex roles.
- No mandatory human checkpoint between dispatch/revise/complete.

## Operating rules

- Keep diffs focused and minimal.
- Always list executed commands and summarize results.
- Ask for missing context instead of guessing.
- No mandatory ticket system.
- Follow: Context -> Product Formalization -> Root/README Sync (if needed) -> Approved Execution -> Validate -> Finalize.
- Prefer canonical global skills for context/product/root/readme/log workflows.
- Coder agents do not edit `docs/03-logs/*`.

## Safety and quality

- Deterministic checks run first.
- Codex fallback auto-fix is allowed on scoped files only.
- Out-of-scope edits are blocked by `tools/scope-guard`.
- Use `tools/offload-proxy/pp` for heavy command output.

## Risk authority

- Human approval is required only for destructive/high-risk actions.
