---
name: orchestrator-agent-loop
description: Native-role delegation/review/finalization conventions for orchestrators. Use when the orchestrator must split work into sub-agents, choose between sequential and parallel execution, and arbitrate structured outputs.
---

# Orchestrator Agent Loop

## Loop Procedure

1. Prepare scoped jobs with `task_id`, `scope`, `task_kind`, and target role.
2. Check `.orchestrator/native-role-manifest.json` and `.codex/config.toml`.
3. Launch native Codex sub-agents.
4. Use `spawn_agents_on_csv` only for independent homogeneous rows.
5. Keep overlapping write scopes sequential.
6. Review `coder_output_v1` payloads and arbitrate revisions.
7. Finalize accepted work and update logs through the orchestrator.

## Hard Rules

- Do not treat legacy session/dispatch scripts as the nominal runtime.
- Do not allow same-document multi-role write work in parallel.
- Do not drop the structured JSON contract when delegating.
