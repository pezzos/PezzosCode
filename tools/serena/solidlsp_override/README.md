# SolidLSP override for Serena

This folder vendors a frozen snapshot of SolidLSP from Serena's uv cache
(2026-01-26) to provide a stable local override for Taplo/TOML support.

Why this exists
- Serena updates may change SolidLSP behavior or clear cache copies.
- We need a durable local copy with a small Taplo LSP fix.

Patch applied
- Added a `workspace/configuration` handler in
  `solidlsp/language_servers/taplo_server.py` to satisfy Taplo 0.10.0.

Wiring
- `.codex.toml` sets `mcp_servers.serena.env.PYTHONPATH` to this folder.

If you want to refresh the vendor copy in the future:
- Replace `solidlsp/` with a new snapshot, then re-apply the Taplo patch.
