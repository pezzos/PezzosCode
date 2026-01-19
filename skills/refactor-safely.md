Goal
Improve code structure without changing behavior.

Inputs
- Target files or modules.
- Rationale for refactor (readability, maintainability, performance).

Steps
1) Read current behavior and tests.
2) Identify safe refactor boundaries and invariants.
3) Make small, reversible changes with clear checkpoints.
4) Run tests after each checkpoint.
5) Summarize improvements and any risks.

Commands
- `rg -n "<symbol-or-file>"`
- Test command (ask if not documented).

Output
- Cleaner code with identical behavior.

DoD
- All existing tests pass.
- No observable behavior change.
