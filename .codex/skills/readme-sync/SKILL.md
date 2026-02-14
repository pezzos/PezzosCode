---
name: readme-sync
description: Reconcile all non-template README.md files, remove duplication, and keep statements concise and accurate against docs/00-context and docs/03-logs sources of truth. Use when README content drifts, repeats itself, or needs a documentation cleanup pass.
---

# README Sync

Use this skill when README files drift out of date or repeat each other. The goal
is to keep information accurate and concise with minimal duplication.

## Detailed Rules

Read `references/readme-rules.md` for scope boundaries, source-of-truth rules,
audience constraints, canonical structure, and deduplication policy.

## Workflow

1. Enumerate README files in scope.
2. Read context/log sources and apply reconciliation rules from `references/readme-rules.md`.
3. Choose canonical locations for repeated information.
4. Rewrite in-scope READMEs to concise, non-duplicated content.
5. Keep edits concise; do not expand content beyond command/script parameter explanation.
6. Use `tools/offload-proxy/pp` only for large-output reads (e.g., `rg`, `cat`);
   avoid it for filesystem writes like `mkdir`, `cp`, or `mv`.
