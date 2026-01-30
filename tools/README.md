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

## `tools/pc-ticket`

Purpose: Orchestrate the Ticket Execution Protocol (TDD + gates + docs + commit)
with Codex as the primary and secondary agent.

Usage:

```bash
tools/pc-ticket F=01 T=001
```

Configuration:

```text
tools/pc-ticket-config.json
```

## `tools/bootstrap-into`

Purpose: Copy the docs system, skills, and tooling into a target repo. Prompts
per file to overwrite, merge with Codex, or skip. Adds a marker comment so
future runs skip already-bootstrapped files, even if they differ.
The merge option requires the `codex` CLI.

Usage:

```bash
tools/bootstrap-into <target-repo-path>
tools/bootstrap-into --self
```

Behavior:
- Templates live in `tools/templates/docs` and are the source of truth.
- The script updates only syncable template/guidance files.
- Real content is never overwritten after bootstrap.
- `tools/bootstrap-into` itself is not synced into other repos.

## `tools/markdown-lint`

Purpose: Lint Markdown files for line endings, trailing whitespace, and missing
trailing newlines.

Usage:

```bash
tools/markdown-lint
```
