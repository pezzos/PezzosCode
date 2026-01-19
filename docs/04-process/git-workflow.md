# Git Workflow

> Simple and pragmatic workflow for working alone or evolving towards branches.

---

## "Simple Solo" Mode (default)

-  **Single branch:** `main`
-  **Atomic commits:** one commit = one clear intention, a limited scope
-  **1 ticket = 1 commit** (unless explicitly stated)

### Steps

1. **Synchronize `main`**
   - `git pull --rebase`
2. **Work in small chunks**
   - Modify, test locally
   - `git add -p` for a clean commit
3. **Check and commit**
   - `scripts/pc-commit` (checks status, runs `make check`, suggests message)
4. **Push**
   - `git push`

### Commit Format

`type(scope): summary`

Allowed types: `feat`, `fix`, `docs`, `chore`.

Examples:
-  `feat(auth): add token refresh`
-  `fix(ui): avoid null crash`
-  `docs(process): add git workflow`

---

## Commit Template

The `.gitmessage` file provides a commit skeleton.

Installation: see `docs/04-process/gitmessage-install.md`.

---

## Commit Script

`scripts/pc-commit`:
-  checks that the git status is clean except for expected files
-  runs `make check`
-  suggests a formatted commit message
-  supports `--dry-run`

Examples:
```bash
scripts/pc-commit --allow docs/04-process/git-workflow.md
scripts/pc-commit --allow docs/04-process --dry-run
```

---

## Appendix: "branch/worktree" option (later)

Use if you need parallel work or major changes.

### Branches
```bash
git switch -c feat/my-feature
```

### Worktrees
```bash
git worktree add ../PezzosCode-my-feature -b feat/my-feature
```

Return to simple mode once the work is completed.