# Elixir Tools Override

## Purpose

Hold Elixir language-server integration files for the local SolidLSP override bundle.

## Structure / Map

- `elixir_tools.py` - Elixir language-server implementation.
- `__init__.py` - Module wiring for the package.

## Workflow

1. Update this folder only when parent override updates require it.
2. Keep behavior aligned with the parent `solidlsp/` snapshot.

## Related Docs

- `tools/serena/solidlsp_override/README.md`
- `docs/03-logs/decision-log.md` (DEC-002)
