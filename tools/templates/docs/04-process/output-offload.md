# Output Offload (pp)

`pp` is a lightweight wrapper for commands that can generate large outputs. It
captures the full output to disk when it exceeds a threshold and only prints a
small preview plus a pointer id.

## Usage

```bash
tools/offload-proxy/pp <command> [args...]
```

Examples:

```bash
tools/offload-proxy/pp rg --files
tools/offload-proxy/pp git diff
```

When output exceeds the threshold (or the command is on the always-offload
list), the full output is stored in:

```
.offload/<hash>.txt
```

`pp` will only print:

- The pointer id
- The head/tail preview

## Policy

- Do not paste large command outputs into prompts.
- Use `pp` for noisy commands and share the pointer id.
- Retrieve output by id using `pp` to keep context small.

Example retrieval:

```bash
tools/offload-proxy/pp sed -n '1,120p' .offload/<id>.txt
```

## Recommended Patterns

- Wrap noisy commands: `rg`, `git diff`, long `cat`, or build logs.
- Share the pointer id when discussing large outputs.
- Add frequently noisy commands to the always-offload list in `pp.yml`.
- Prefer offloading over pasting large outputs into prompts to reduce token usage.

## Configuration (pp.yml)

`pp` reads `pp.yml` from the repo root (or `$PP_CONFIG` if set).

```yaml
threshold_lines: 200
head_lines: 20
tail_lines: 20
always_offload:
  - git diff
  - rg
```

Notes:

- `threshold_lines` triggers offload when output exceeds this line count.
- `always_offload` matches the command prefix (start of the command line).
