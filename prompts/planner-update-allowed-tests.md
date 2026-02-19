# Planner Allowed Tests Update Prompt

Allowed Tests must list specific, meaningful repo-supported test/validation commands.
Do not use `make ci`, `make feature`, `pc-feature`, placeholders, or narrative text.
Use commands that can be copied verbatim into the Plan `Tests` section.
Prefer commands that match the current repo capability (language/tooling stack), for example:

- `python3 -m unittest tests/test_pc_feature.py`
- `python3 -m unittest discover -s tests -p "test_*.py"`
- `python3 -m pytest tests/test_pc_feature.py -q`
- `npm test`
- `npm run test:unit`
- `go test ./...`
- `cargo test`
- `make test`
- `tools/pc-devtasks-schema-check`
  If Issues mention missing dotted unittest selectors (for example `tests.test_x.Class`), rewrite to a file-path or discover command.
  If Issues mention touched test files missing explicit coverage, include commands that explicitly reference every missing touched test file or module marker.
  Prepatch validation checks command syntax/contract only; postpatch validation checks target existence/execution.
  Do not edit any files.
  Do not run commands.
  Do not update `docs/03-logs/*`.
  Return ONLY the Allowed Tests section body as bulleted commands.
  Each bullet must contain exactly one command wrapped in backticks.
  If no valid command is available, return an empty response.

Work Item ID: {work_item_id}
Issues: {issues}
