---
name: sync-root-from-context
description: Read docs/00-context and docs/01-product/prd.md, then update live root files (bootstrapped from tools/templates/root/) to match the project.
---

# Sync Root Files From Context

Use this skill when the project context or PRD changes and the live root files
need to reflect the real project (not the generic templates).

## Inputs to read

1. `docs/00-context/` (vision, system map, users, assumptions, context boundaries)
2. `docs/01-product/prd.md`

## Files to update (live root)

These files are copied into other repos from `tools/templates/root/`, but the
live versions in this repo must be updated to match this project:

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

## Workflow

1. Read the context and PRD. Summarize the project purpose, scope, platforms,
   and key workflows in 5-10 bullets.
2. Update the live root files to reflect the actual project:
   - `AGENTS.md`: describe this repo and its docs system accurately; keep
     rules aligned with docs/04-process.
   - `.codex.toml`: keep existing approval policy unless docs or the user
     explicitly request a change; adjust trust level/defaults only when
     supported by context.
   - `.serena/project.yml`: set `project_name`, `initial_prompt`, and
     `languages` based on this repo’s stack and files. Ensure the list is
     unique (no duplicates) before saving.
   - `Makefile`: keep commands aligned with actual tools and tests present.
   - `.pre-commit-config.yaml`: include hooks for the languages/tools in
     `docs/00-context/` and the repo; remove hooks for unused stacks.
   - `.editorconfig`: include the language sections needed for this repo.
   - `.githooks/pre-commit`: run the correct pre-commit stage.
   - `.githooks/pre-push`: run the correct pre-push stage (tests).
   - `LICENSE`: ensure the copyright holder/year match this repo.
   - `.gitignore` and `.serena/.gitignore`: reflect real ignored artifacts.
   - `pp.yml`: ensure offload rules match repo tooling.
3. If any file can’t be safely inferred from docs, ask a targeted question
   before editing.
4. Validate edits before saving:
   - `.codex.toml`: verify `approval_policy` unchanged unless explicitly requested.
   - `.serena/project.yml`: re-check `languages` for duplicates.
5. Keep diffs small and focused; do not change `tools/templates/root/*` here.

## Output checklist

- All live root files reflect the project context and PRD.
- No changes to template files unless explicitly asked.
- Brief summary of edits and any assumptions made.
