---
name: investigate
description: Perform analysis-only investigation of inline command output, produce evidence-ranked root-cause hypotheses, compare expected vs actual behavior from project docs, and propose durable fix options. Use when the user asks to "investigate" a failing run and explicitly wants diagnosis without file edits.
---

# Investigate

## Overview

Investigate one run deeply and return durable, evidence-ranked fix strategies.
Keep output in chat only.

## Input Contract

Accept a single-line, inline input:

`Investigate "command=<command text>" "output=<full raw output text>"`

If command or output is missing, ask one focused clarifying question and stop.

## Detailed Rubric

Use `references/investigation-rubric.md` for:

- expected-vs-actual source priority,
- fix-option scoring dimensions,
- docs-conflict handling,
- required output section order.

## Steps

1. Parse command and output exactly as provided.
2. Identify the primary issue and any secondary issues.
3. Build root-cause hypotheses ranked by evidence from the output.
4. Apply the rubric in `references/investigation-rubric.md`.
5. Ask focused question(s) only when a real decision is required.

## Guardrails

- Do not edit files.
- Do not run fix commands.
- Do not install or modify hooks.
- Do not change `pre-commit` or `make feature` behavior in this run.
- Keep analysis and recommendations chat-only.
