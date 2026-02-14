# Root File Checklist

## Live Root Files to Update

- `AGENTS.md`
- `.codex.toml`
- `.editorconfig`
- `.gitignore`
- `.gitmessage`
- `LICENSE`
- `Makefile`
- `pp.yml`
- `.pre-commit-config.yaml`
- `.serena/project.yml`
- `.serena/.gitignore`
- `.githooks/pre-commit`
- `.githooks/pre-push`

## Per-File Expectations

- `AGENTS.md`: align repository rules and docs references with current process docs.
- `.codex.toml`: keep `approval_policy` unchanged unless explicitly requested.
- `.serena/project.yml`: align `project_name`, `initial_prompt`, and unique `languages`.
- `Makefile`: keep commands aligned with current tools/tests.
- `.pre-commit-config.yaml`: keep hooks aligned with active stack.
- `.editorconfig`: keep language sections aligned with repo contents.
- `.githooks/pre-commit`: run the correct pre-commit stage.
- `.githooks/pre-push`: run the correct pre-push stage.
- `LICENSE`: keep holder/year accurate.
- `.gitignore` and `.serena/.gitignore`: reflect real generated artifacts.
- `pp.yml`: align offload behavior with current tooling.

## Validation Checklist

- Confirm `.codex.toml` `approval_policy` is unchanged unless explicitly requested.
- Confirm `.serena/project.yml` has no duplicate language entries.
- Confirm no edits were made under `tools/templates/root/` unless explicitly requested.

## Output Checklist

- All required live root files reflect context + PRD.
- No unintended template edits.
- Assumptions/gaps are explicitly called out.
