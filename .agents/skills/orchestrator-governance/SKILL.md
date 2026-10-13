---
name: orchestrator-governance
description: "Enforce an orchestrator-only workflow for software delivery. Use when coordinating tasks across native Codex roles where the orchestrator must route specialist work, documentation workflows, and delegated coding without editing application code."
---

# Orchestrator Governance

Operate as orchestrator only.
Default to autonomous delegation after initialization.

## Initialization Gate

Run these commands before any delegated work:

1. `python3 scripts/orchestrator_guard.py init`
2. `python3 scripts/orchestrator_guard.py assert`
3. `python3 scripts/orchestrator_guard.py run-status`
4. `python3 scripts/orchestrator_guard.py policy-show`

## Canonical Hierarchy

- `orchestrator-governance` = ownership, routing, and guardrails
- `execute-approved-plan-safely` = approved-plan execution entrypoint
- `orchestrator-agent-loop` = native-role orchestration conventions

## Native Role Rules

- Route work to the smallest useful native role set defined in `.codex/config.toml`.
- Use `.orchestrator/native-role-manifest.json` as the local routing manifest.
- Keep same-document multi-role reviews sequential.
- Prefer `spawn_agents_on_csv` for broad homogeneous review or audit batches.
- Keep `coder_output_v1` as the required structured output of delegated roles.

## Do Not Use

- `scripts/orchestrator_dispatch.py`
- `scripts/session_registry.py`
- bootstrap-local `coder-executor` as a canonical worker path
