# SolidLSP Override for Serena

## Purpose

Provide a local SolidLSP override used by Serena, with wiring configured via
`.codex.toml`.

## Structure / Map

- `solidlsp/` - Vendored SolidLSP source.
- `.codex.toml` - Sets `mcp_servers.serena.env.PYTHONPATH` to this folder.

## Workflow

To refresh the vendor copy:

1. Replace `solidlsp/` with a new snapshot.
2. Re-apply any local patches as needed.

## Related Docs

- `.codex.toml`
