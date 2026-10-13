# Orchestration Model

## Why this model

This repository is designed for AI-agent execution with minimal human interruption.
The human role is to define context and answer high-impact questions; the orchestrator handles implementation loops and specialist routing autonomously.

## Roles and ownership

- Human: context definition, kickoff approval, exceptional risk arbitration, final answers to blocking questions.
- Orchestrator: decomposition, native-role selection, review, acceptance, logs.
- Native Codex role: scoped implementation, review, analysis, draft, or testing work.
- Autofix: scoped quality-fix fallback in hooks.

## Canonical skill hierarchy

- `orchestrator-governance` owns routing, ownership, and guardrails.
- `execute-approved-plan-safely` is the default entrypoint once a plan is approved.
- `orchestrator-agent-loop` defines low-level native-role orchestration conventions.

## Native role model

- Canonical specialist profiles live in `.orchestrator/profile-catalog.json`.
- Canonical native-role metadata lives in `.orchestrator/native-role-manifest.json`.
- Native Codex role declarations live in `.codex/config.toml` and `.codex/agents/*.toml`.
- Repo-local specialist prompts live in `prompts/specialists/`.
- Same-document multi-role reviews stay sequential to avoid collisions.
- Parallel homogeneous work should use `spawn_agents_on_csv`.

## Default execution policy

1. Context is defined or refreshed (`refresh-context-docs`).
2. Product docs are formalized or reviewed with the right specialist panel (`build-prd-from-context` / `review-product-docs-with-specialists`).
3. Root operational files or README files are synchronized when docs imply drift (`sync-root-files-from-docs` / `reconcile-readmes`).
4. Approved plans are executed through orchestrated native-role delegation (`execute-approved-plan-safely`).
5. Orchestrator reviews outputs and either accepts or requests revision.
6. Orchestrator finalizes and updates logs (`update-project-logs`).

No manual approval checkpoint is required between steps 4-6 by default.

## Escalation policy

Escalate to human only when:

- destructive/high-risk action is required,
- policy/security boundary is violated,
- blocker remains unresolved after configured retries,
- a specialist review yields blocking questions that require product judgment.

## Quality policy

- Deterministic checks first.
- Specialist review when context/product docs are incomplete or risky.
- Root/README sync only when documentation changes justify it.
- Codex autofix fallback second (scoped and guarded).
- One retry by default, then fail closed.
