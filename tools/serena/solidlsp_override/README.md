# Serena SolidLSP Override

## Purpose

- Hold the repo-local SolidLSP override used by Serena.
- Support the LSP override strategy documented in `docs/03-logs/decision-log.md` (DEC-002).

## Structure / Map

- `solidlsp/` - Local SolidLSP override source.
- `solidlsp/language_servers/elixir_tools/` - Elixir-specific language-server integration.

## Workflow

1. Keep Serena override wiring aligned with `.codex.toml`.
2. Keep local changes minimal when refreshing override files.

## Related Docs

- `.codex.toml`
- `docs/03-logs/decision-log.md` (DEC-002)
