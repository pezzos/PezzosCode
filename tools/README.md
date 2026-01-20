# Tools

Helper utilities for working in this repo or bootstrapping it into another
project.

## `tools/pc-commit`

Purpose: Run `make check`, enforce an allowlist of changed paths, and guide
standardized commit messages.

Usage:

```bash
tools/pc-commit [options]
```

## `tools/bootstrap-into`

Purpose: Copy the docs system, skills, and tooling into a target repo. Prompts
per file to overwrite, merge with Codex, or skip. Adds a marker comment so
future runs skip already-bootstrapped files, even if they differ.
The merge option requires the `codex` CLI.

Usage:

```bash
tools/bootstrap-into <target-repo-path>
```

## `tools/markdown-lint`

Purpose: Lint Markdown files for line endings, trailing whitespace, and missing
trailing newlines.

Usage:

```bash
tools/markdown-lint
```
