---
name: investigate
description: Thoroughly investigate command output passed inline, identify issue and root-cause hypotheses, compare actual behavior with expected behavior defined in project docs/processes, and propose multiple permanent fixes plus future auto-fix recommendations. Use when the user provides a command and output text and wants analysis-only guidance with no code edits.
---

# Investigate

## Overview

Investigate one run deeply and return durable fix strategies for future runs. Keep output in chat only.

## Input Contract

Accept a single-line, inline input:

`Investigate "command=<command text>" "output=<full raw output text>"`

If command or output is missing, ask one focused clarifying question and stop.

## Steps

1. Parse command and output exactly as provided.
2. Identify the primary issue and any secondary issues.
3. Build root-cause hypotheses ranked by evidence from the output.
4. Derive expected behavior from project documentation in this priority order:
   - `docs/04-process/*`
   - `docs/02-features/*`
   - `docs/01-product/*`
   - `docs/00-context/*`
   - other relevant project docs
5. Compare expected vs actual behavior with concise evidence references.
6. Propose multiple permanent fix options (minimum three), covering:
   - direct implementation fix
   - prevention/guardrail fix (tests/checks/process)
   - workflow/operational fix
7. For each fix option, include:
   - why it addresses the likely root cause
   - how it remains durable in future runs or different contexts
   - key risks/tradeoffs
   - whether the fix is deterministic
8. Propose future auto-fix ideas only as recommendations. Do not execute or apply them now.
9. If any real decision is required, ask focused question(s) and do not choose a path autonomously.

## Docs Conflict Handling

If docs conflict or remain ambiguous:

1. Cite the conflicting sources.
2. Explain how the conflict affects diagnosis confidence or fix selection.
3. Propose a docs-improvement action to prevent repeated ambiguity.
4. Ask the user for a decision when the conflict changes the chosen fix path.

## Guardrails

- Do not edit files.
- Do not run fix commands.
- Do not install or modify hooks.
- Do not change `pre-commit` or `make feature` behavior in this run.
- Keep analysis and recommendations chat-only.

## Output Format

Return these sections in order:

1. Issue Summary
2. Root Cause Hypotheses
3. Expected vs Actual
4. Permanent Fix Options
5. Future Auto-Fix Proposals (recommendation-only)
6. Open Questions (only when a decision is required)
