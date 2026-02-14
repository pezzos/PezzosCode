---
name: workflow-hardening-top5
description: Analyze docs/possible-improvements.md and propose up to five prioritized workflow-hardening recommendations focused on reliability, failure prevention, and low-risk rollout. Use when the user asks for process/workflow improvement ideas in chat and does not want feature expansion implementation.
---

# Workflow Hardening Top5

## Overview

Return high-value workflow/process hardening recommendations from the project backlog. Keep output read-only and chat-only.

## Input Contract

When triggered, read:

`docs/possible-improvements.md`

If the file is missing or empty, report that clearly and stop.

## Selection Rules

1. Extract candidate improvements from proposal entries.
2. Deduplicate candidates by root workflow problem.
3. Keep only workflow hardening ideas:
   - process reliability
   - validation gates
   - guardrails against repeated failures
   - scope control and closeout quality
4. Exclude:
   - product feature additions
   - UX/UI feature expansion
   - speculative ideas not grounded in the file evidence
5. Prioritize candidates by:
   - recurrence (how often the failure pattern appears)
   - impact (how much instability/rework it causes)
   - prevention value (ability to stop issue classes early)
   - implementation safety (can be rolled out with minimal blast radius)

## Output Size Rule

- Return at most 5 recommendations.
- Return fewer than 5 when there is not enough strong evidence.
- Never pad with weak or duplicated ideas to reach 5.

## Guardrails

- Do not edit files.
- Do not run patch/apply commands.
- Do not auto-approve or auto-implement any proposal.
- Do not include feature-roadmap additions.
- Keep recommendations reversible and low-risk by default.

## Output Format

Return a numbered list with one block per recommendation:

1. **Improvement**
2. **Why implement now**
3. **Benefits**
4. **Risks / trade-offs**
5. **No-side-effect rollout**
   - start with a narrow pilot or dry-run
   - define explicit success/failure checks
   - include rollback/disable path
6. **Evidence**
   - cite proposal identifiers/work-item references from `possible-improvements.md`

If fewer than 5 are returned, add a short final note:

`Returned <N> recommendation(s) because only <N> met the evidence and priority threshold.`
