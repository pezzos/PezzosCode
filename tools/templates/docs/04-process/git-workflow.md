# Git Workflow

> Simple and pragmatic workflow for working alone or evolving towards branches.

---

## "Simple Solo" Mode (default)

- **Single branch:** `main`
- **Atomic commits:** one commit = one clear intention, a limited scope
- **1 ticket = 1 commit** (unless explicitly stated)
- **Commit convention enforced:** `type(scope): summary` via `tools/pc-commit`
- **Hooks over AI for checks:** linting and checks live in git hooks where possible

### Steps

1. **Synchronize `main`**
   - `git pull --rebase`
2. **Work in small chunks**
   - Modify, test locally
   - `git add -p` for a clean commit
3. **Check and commit**
   - `tools/pc-commit` (checks status, runs `make check`, suggests message)
4. **Push**
   - `git push`

### Commit Format

`type(scope): summary`

Allowed types: `feat`, `fix`, `docs`, `chore`.

Examples:

- `feat(auth): add token refresh`
- `fix(ui): avoid null crash`
- `docs(process): add git workflow`

---

## Commit Template

The `.gitmessage` file provides a commit skeleton.

Installation: see `docs/04-process/gitmessage-install.md`.

---

## Commit Script

`tools/pc-commit`:

- checks that the git status is clean except for expected files
- runs `make check`
- suggests a formatted commit message
- supports `--dry-run`
- enforces the commit message convention

Examples:

```bash
tools/pc-commit --allow docs/04-process/git-workflow.md
tools/pc-commit --allow docs/04-process --dry-run
```

---

## Precommit Hooks (Autofix)

- Precommit runs checks on the staged file list only.
- Deterministic fixers (ruff/black/shfmt/prettier/taplo/gofmt/rustfmt) run first; Codex runs only as a fallback when unresolved issues remain.
- If autofix modifies files, re-stage with `git add -u` and print the list of modified/re-staged files.
- Codex in precommit runs with vanilla config (no Serena MCP injection and no role profiles).
- Codex fallback is hard-scoped to the staged file list and fails if out-of-scope paths are touched.
- Precommit-only fixes must not update `docs/03-logs/*` or feature execution logs.

---

## Worktrees Policy (Parallel Sessions)

Use worktrees when you want clean isolation between changes.
Default: **single worktree per feature**; add extra worktrees only when necessary.

Naming convention:
`../<repo_name>-<feature_name>-<agent_name>`
Example: `../PezzosCode-auth-impl`, `../PezzosCode-auth-review`

Role scope (enforced by tooling):

- Planner: `docs/02-features/<feature>/planner-log.md`
- Tester: `docs/02-features/<feature>/validation-log.md`
- Reporter: `docs/02-features/<feature>/reporter-log.md`
- Patcher: anywhere except role-scoped log files

Collector behavior:

- `main` is the only merge destination and is never edited directly by role worktrees.
- Role branches are squashed into a single commit on `main` after collection.
- Worktrees and their branches are removed after successful collection.

---

## Appendix: "branch/worktree" option (later)

Use if you need parallel work or major changes.

### Branches

```bash
git switch -c feat/my-feature
```

### Worktrees

```bash
git worktree add ../PezzosCode-auth-impl -b feat/auth
git worktree add ../PezzosCode-auth-review -b feat/auth-review
```

Return to simple mode once the work is completed.
