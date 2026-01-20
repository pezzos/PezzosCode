---
name: prepare-commit
description: Prepare a clean, scoped commit by reviewing diffs, confirming tests/lint, updating logs, and staging intended files. Use when a user asks to get changes ready for commit or requests a commit prep checklist.
---

# Prepare Commit

## Overview
Review changes, confirm quality checks, and stage the intended files for a clean commit.

## Inputs
- List of files changed.
- Short commit intent.

## Steps
1) Review diffs for scope and correctness.
2) Confirm tests/lint status or ask which commands to run.
3) Ensure relevant logs are updated per the Definition of Done.
4) Draft a clear, scoped commit message.
5) Stage only the intended files.

## Commands
- `git status -sb`
- `git diff`
- `git add <paths>`

## Output
- Staged changes ready for commit with a clear message.

## DoD
- Changes are scoped and reviewed.
- Tests/lint status is recorded or requested.
