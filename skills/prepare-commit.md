Goal
Prepare changes for a clean, scoped commit that follows repo conventions.

Inputs
- List of files changed.
- Short commit intent.

Steps
1) Review diffs for scope and correctness.
2) Confirm tests/lint status or ask for commands if unknown.
3) Ensure relevant logs are updated per DoD.
4) Draft a scoped commit message.
5) Stage only the intended files.

Commands
- `git status -sb`
- `git diff`
- `git add <paths>`

Output
- Staged changes ready for commit with a clear message.

DoD
- Changes are scoped and reviewed.
- Tests/lint status recorded or requested.
