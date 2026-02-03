# Ticket Execution Protocol (TDD + Gates)

> **Canonical implementation workflow for agents**
>
> For any ticket implementation, this protocol is mandatory. It supersedes generic workflow guidance for execution.

---

## Scope Control (No Scope Creep)

- Follow Context Boundaries and Non-Goals: `docs/00-context/context-boundaries-operating-model.md`.
- Do not add features, automation, or optimizations beyond the ticket.
- If requirements are unclear, stop and ask the PO.
- Ticket-specific Definition of Done must be stated before coding.

## End-to-End Workflow

1. **Ticket Ingestion**
   - Run `make ticket T=<id> [F=<feature-id>]` to bootstrap and execute autonomously by default.
   - Manual mode (no autonomous TDD/implementation): `make ticket MANUAL=1 T=<id> [F=<feature-id>]`.
   - Example (one command): `make ticket F=01 T=102`.
   - Open the ticket file: `docs/02-features/<feature>/TASK-XXX.md`.
   - Confirm scope, success criteria, and change budget.
   - Complexity flag: `complexity: "simple" | "complex"` in ticket frontmatter.
   - Complex tickets run an orchestrated flow with explicit tester/reviewer feedback steps.
   - Tooling must be idempotent: reruns should not corrupt state or report success when a step fails.

2. **Resuming a Ticket (Automatic)**
   - If a worklog already exists, `make ticket` resumes automatically.
   - Preflight is skipped if the **Preflight Report** section is already filled.
   - TDD generation is skipped if the **TDD Plan** section is already filled.
   - Tests and CI are always re-run on resume.
   - Commit is skipped if a commit message is already recorded in the worklog.

3. **Preflight Report (Mandatory)**
   - Produce the Preflight Report exactly in the format below.

4. **Risk Classification**
   - Classify the ticket as LOW or HIGH risk using the deterministic rules below.

5. **Approval Gate (HIGH Risk Only)**
   - If HIGH, stop after Preflight and request PO approval.
   - No implementation work until approval is explicitly granted.
   - Set ticket status to **Awaiting PO Approval** in frontmatter.

6. **Plan → Patch → Test → Report**
   - Plan: approach, files, risks, tests, and ticket-specific DoD.
   - Patch: make the smallest diff that satisfies the ticket (TDD where applicable).
   - Test: run agreed checks and record results.
   - Report: summarize what changed, commands run, and outcomes.

7. **Feedback Loop (Implementer ↔ Tester ↔ Reviewer)**
   - Tester records failures in the **Tester Feedback** section.
   - Reviewer records issues in the **Reviewer Feedback** section.
   - Implementer updates the patch and logs the loop in **Iteration Log**.
   - Repeat until feedback is resolved.

8. **TDD Cycle (when applicable)**
   - Write tests first.
   - Run tests and confirm they fail for the right reason.
   - Implement minimal code changes to pass tests.
   - Re-run tests and confirm they pass.

9. **Docs Sync (Mandatory)**
   - Update required docs/logs per ticket template.
   - Record a gating summary in docs/03-logs/implementation-log.md and validation findings in docs/03-logs/validation-log.md for the Execute ticket workflow so the logs mirror the implemented sequence.

10. **Gates**

- Run `make ci` and ensure it passes.
- Automated runs may attempt to auto-fix failing tests/CI up to the configured limit.
- Autofix prompt template: `docs/04-process/ci-autofix-prompt.md`.

11. **Commit**

- 1 ticket = 1 commit.
- Follow commit rules in `docs/04-process/git-workflow.md`.
- Use `tools/pc-commit` to enforce convention and checks.
- Before commit, the ticket doc is auto-updated (DoD checkboxes, Tests Run, Report Final) and must be complete.

12. **AI Tooling (preferred)**

- Use Serena for code navigation and symbol-aware edits when available.
- Offload large outputs using `tools/offload-proxy/pp` to reduce token usage.

---

## Risk Classification (Deterministic)

HIGH RISK if any of the following apply:

- Changes touch `sanitizer/`, `detectors/`, `restore/`, `git_ops/`, or `metadata/`.
- Changes modify secret-blocking or fail-close behavior.
- Changes affect restore apply semantics or permissions.
- Secret scanning dependencies/policies are added or modified.
- Change budget exceeded (>10 files OR >2 new modules OR cross-cutting refactor impacting 3+ modules).

Otherwise, LOW RISK.

---

## Preflight Report (Mandatory Format)

```
Ticket ID:
PRD reference / feature mapping:
Risk level: LOW | HIGH (triggers: ...)
Scope summary (in/out):
Non-goals reminder:
Files to change:
Change budget:
TDD plan: tests to write first
Ticket DoD (explicit):
Doc updates planned:
```

---

## Final Report (Mandatory Format)

```
What changed (files):
Tests written (names) + results:
Docs/logs updated checklist:
make ci results:
Commands run (use `pp` for noisy output):
Commit message:
```

---

## References

- Dev workflow (background only): `docs/04-process/dev-workflow.md`
- Definition of Done: `docs/04-process/definition-of-done.md`
- Git workflow: `docs/04-process/git-workflow.md`
- Ticket template: `docs/04-process/ticket-template.md`
- Context boundaries: `docs/00-context/context-boundaries-operating-model.md`
