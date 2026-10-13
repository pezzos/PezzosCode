# Contracts

## 1) Native Role Output (JSON Required)

Delegated native roles must return one JSON object with schema version `coder_output_v1`.

Required fields:
- `schema_version`
- `task_id`
- `status`
- `summary`
- `changed_files`
- `tests`
- `next_step`

Optional fields:
- `profile`
- `task_kind`
- `proposed_file_scope`
- `out_of_scope_changes`
- `errors`
- `risks`
- `findings`
- `questions_for_user`
- `recommended_followup_profiles`
- `suggested_doc_targets`

## 2) Routing Contract

- `.orchestrator/profile-catalog.json` = logical profile metadata
- `.orchestrator/native-role-manifest.json` = machine-readable role manifest
- `.codex/config.toml` and `.codex/agents/*.toml` = executable role registry

## 3) Parallelism Contract

- Same-document multi-role review remains sequential.
- Independent exploration or review work may run in parallel.
- Homogeneous independent work items may use `spawn_agents_on_csv`.
- Overlapping write scopes require orchestrator arbitration before acceptance.
