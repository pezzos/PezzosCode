---
name: implement-plan-safe
description: Execute an already proposed and approved implementation plan from the current chat context when the user asks with short commands like "Implement", "Please implement this plan", or "Ok for this plan, implement with no side effects". Use only when a concrete plan already exists in the conversation and the user is asking to execute it now.
---

# Implement Plan Safe

## Overview

Execute the approved plan from the current chat context end-to-end. Keep execution deterministic, scoped, and explicitly side-effect aware.

## Input Contract

This is a chat-only skill with no CLI arguments.

Accept short trigger requests such as:

- `Implement`
- `Please implement this plan`
- `Ok for this plan, implement with no side effects`

Precondition:

- A concrete implementation plan is already present in recent chat context.

If the plan is missing or ambiguous, ask one focused question and stop.

## Workflow

1. Parse the latest approved plan from chat context.
2. Confirm constraints and assumptions from the plan (scope, files, tests, safety constraints).
3. Execute the work directly (do not restate the plan unless clarification is required).
4. Validate with targeted tests/checks defined by the plan.
5. Report outcomes with changed files, commands run, test results, and unresolved risks.

## No-Side-Effect Guardrails

- Do not run destructive git/file operations unless explicitly requested in the current turn.
- Do not run `make feature`, `pc-feature`, or `tools/pc-feature` without explicit user approval in the current turn.
- Prefer minimal diffs and scoped edits.
- If a safety conflict appears, stop and ask one focused question before proceeding.

## Output Contract

Return:

1. Execution summary
2. Files changed
3. Commands run and key results
4. Validation results
5. Remaining risks or follow-ups
