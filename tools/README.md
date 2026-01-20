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

Purpose: Copy the documentation system and core tooling into a target repo.

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
