# Investigation Rubric

## Expected-vs-Actual Source Priority

Derive expected behavior from these sources, in order:

1. `docs/04-process/*`
2. `docs/02-features/*`
3. `docs/01-product/*`
4. `docs/00-context/*`
5. other relevant project docs

## Root-Cause and Fix Option Requirements

- Rank root-cause hypotheses by concrete evidence from provided evidence:
  - `output` when available (preferred),
  - otherwise `issue` + any provided `context`.
- If `output` is missing, explicitly call out lowered confidence and assumptions.
- Propose at least three durable options:
  - direct implementation fix,
  - prevention/guardrail fix (tests/checks/process),
  - workflow/operational fix.
- For each option include:
  - why it addresses the likely cause,
  - durability across future runs,
  - key risks/tradeoffs,
  - whether it is deterministic.

## Docs Conflict Handling

If docs conflict or remain ambiguous:

1. Cite conflicting sources.
2. Explain confidence impact.
3. Propose doc-improvement action.
4. Ask user decision when conflict changes fix choice.

## Output Sections (in order)

1. Issue Summary
2. Root Cause Hypotheses
3. Expected vs Actual
4. Permanent Fix Options
5. Future Auto-Fix Proposals (recommendation-only)
6. Open Questions (only when needed for a decision)
