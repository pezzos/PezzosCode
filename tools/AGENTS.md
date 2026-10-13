# Tools Guide

Use this subtree for bounded developer tooling, not product logic.

Primary entrypoints:

- `git_precommit`: deterministic hook runner, batching, and autofix escalation.
- `codex-autofix`: bounded Codex fallback for staged deterministic failures.
- `scope-guard`: enforces allowed-path safety for write-enabled autofix flows.
- `offload-proxy/pp`: explicit heavy-output proxy when large command output should not
  be replayed into Codex.

Navigation rules:

- For pre-commit or autofix context, start with `git_precommit`, then read
  `codex-autofix` only if the fallback prompt or scope rules matter.
- For scope violations, jump directly to `scope-guard`.
- Do not browse tooling files outside the current failure path.
