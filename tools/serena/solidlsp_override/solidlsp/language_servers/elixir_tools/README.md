# Elixir Language Server Integration

## Purpose

Provide Elixir language support via the official Expert language server.

## Structure / Map

- `elixir_tools.py` - Main integration class (`ElixirTools`).
- Language id: `"elixir"`.
- Command: `expert --stdio`.

## Workflow

Prerequisites:
- Elixir installed and available in `PATH`.
- Expert available (auto-downloads if missing).

Project notes:
- Expert performs best after `mix compile`.
- `asdf` versions are respected when `.tool-versions` is present.

Testing:
```bash
pytest test/solidlsp/elixir/ -m elixir
```

## Related Docs

- https://github.com/elixir-lang/expert
