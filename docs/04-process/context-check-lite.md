# Context Check Lite

## Purpose

Run a minimal deterministic gate before broad task dispatch.

## Validated files

- `docs/00-context/vision.md`
- `docs/00-context/users.md`
- `docs/00-context/system-map.md`
- `docs/00-context/context-boundaries-operating-model.md`
- `docs/00-context/expected-features.md`
- `docs/01-product/prd.md`

## Validation rules

- Required files exist.
- Required files are non-empty.
- No unresolved placeholders (`[TODO]`, `[TBD]`, `<TODO>`, `<TBD>`).

## Output

- Report: `docs/03-logs/context-check-lite.json`
- Decision: `PASS` or `BLOCK`

## Ownership

- Orchestrator runs and interprets this gate.
- Coder sessions consume results but do not update the report.
