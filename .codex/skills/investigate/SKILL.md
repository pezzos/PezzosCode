---
name: investigate
description: Perform analysis-only investigation of failing outcomes using inline command output or a plain issue description, produce evidence-ranked root-cause hypotheses, compare expected vs actual behavior from project docs, and propose durable fix options. Use when the user asks to "investigate" a failing run and explicitly wants diagnosis without file edits.
---

# Investigate

## Overview

Investigate one run deeply and return durable, evidence-ranked fix strategies.
Keep output in chat only.

## Input Contract

Accept a single-line, inline input in one of these forms:

1. CLI-evidence mode (preferred):
   `Investigate "command=<command text>" "output=<full raw output text>"`

2. Description-only mode (when CLI output is unavailable):
   `Investigate "issue=<plain-language issue description>"`

Also accept free-text input such as:
`$investigate <issue description>`
Treat free text as `issue=<...>`.

Optional in either mode:

- `"command=<command text>"`
- `"context=<environment/run details>"`

If both `output` and `issue` are missing, ask one focused clarifying question and stop.

## Detailed Rubric

Use `references/investigation-rubric.md` for:

- expected-vs-actual source priority,
- fix-option scoring dimensions,
- docs-conflict handling,
- required output section order.

## Steps

1. Parse provided evidence fields (`command`, `output`, `issue`, `context`) exactly as provided, and normalize free text to `issue`.
2. Identify the primary issue and any secondary issues.
3. Build root-cause hypotheses ranked by available evidence:
   - prioritize `output` evidence when present,
   - otherwise use `issue` + `context` evidence and mark assumptions explicitly.
4. Apply the rubric in `references/investigation-rubric.md`.
5. Ask focused question(s) only when a real decision is required.

## Guardrails

- Do not edit files.
- Do not run fix commands.
- Do not install or modify hooks.
- Do not change `pre-commit` or `make feature` behavior in this run.
- Keep analysis and recommendations chat-only.
