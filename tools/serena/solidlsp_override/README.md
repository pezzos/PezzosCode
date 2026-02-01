# SolidLSP Override for Serena

## Purpose

Provide a stable local override of SolidLSP (cached snapshot from 2026-01-26)
with a small Taplo/TOML fix, so Serena behavior does not drift with cache
updates.

## Structure / Map

- `solidlsp/` - Vendored SolidLSP snapshot.
- `solidlsp/language_servers/taplo_server.py` - Taplo `workspace/configuration` fix.
- `.codex.toml` - Sets `mcp_servers.serena.env.PYTHONPATH` to this folder.

## Workflow

To refresh the vendor copy:
1. Replace `solidlsp/` with a new snapshot.
2. Re-apply the Taplo patch in `taplo_server.py`.

## Related Docs

- `.codex.toml`
