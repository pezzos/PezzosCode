# Planner Allowed Tests Update Prompt

Allowed Tests must list specific, meaningful unittest/pytest commands that exist.
Do not use `make ci`, `make feature`, `pc-feature`, placeholders, or narrative text.
Do not edit any files.
Do not run commands.
Do not update `docs/03-logs/*`.
Return ONLY the Allowed Tests section body as bulleted commands.
Each bullet must contain exactly one command wrapped in backticks.
If no valid command is available, return an empty response.

Work Item ID: {work_item_id}
Issues: {issues}
