# System Map

## What is Actually Built & Running

<!-- A living map of the current system architecture and deployment -->

## System Overview

```
┌──────────────┐   bootstrap/update   ┌──────────────────────┐
│  User (PO)   │────────────────────▶│  Target Project Repo  │
└──────────────┘                      │  (bootstrapped docs, │
          │                           │   tools)             │
          │ execute tickets           └──────────────────────┘
          ▼
┌────────────────────────┐
│ PezzosCode Tooling Repo │
│ (templates + tools)     │
└────────────────────────┘
```

<!-- Replace with your actual architecture diagram -->

## Components

### Template + Docs System

- **Technology:** Markdown docs + templates.
- **Entry Points:** `docs/` (templates live in `tools/templates/docs`) and root templates in `tools/templates/root`.
- **Key Files/Modules:**
  - `docs/00-context/`: vision, users, assumptions, system map.
  - `docs/01-product/`: PRD.
  - `docs/02-features/`: feature folders + dev-tasks (execution log in dev-tasks.md).
  - `docs/03-logs/`: decisions, implementation notes, validation.
  - `docs/04-process/`: process rules and workflow.

### Tools (CLI scripts)

- **Technology:** Bash + Python.
- **Entry Points:** `tools/bootstrap-into`, `tools/pc-feature`, `tools/pc-commit`, `tools/pc-template-sync`.
- **Key Files/Modules:**
  - `tools/bootstrap-into`: copy templates into target repo and reapply updates safely.
  - `tools/pc-feature`: execute work item workflow end-to-end.
  - `tools/pc-commit`: validate and commit changes.
  - `tools/pc-template-sync`: keep template/living docs aligned.
  - `tools/offload-proxy/pp`: offload noisy command output to `.offload/`.

### Skills (Codex helpers)

- **Technology:** Markdown skill files in global `~/.codex/skills/`.
- **Entry Points:** `build-prd-from-context`, `reconcile-readmes`, `sync-root-files-from-docs`, `refresh-context-docs`, `update-project-logs`, `execute-approved-plan-safely`, etc.

### External Services

- **Codex CLI:** Executes prompts for tests/implementation/merge tasks.
- **Git:** Version control and change tracking.
- **Make:** Standard entry point for tests/CI.
- **Language runtimes:** Python, Node/TS, Rust, Go as needed per project.

## Data Flow

### Critical User Flows

1. **Bootstrap a project**
   - User action: run bootstrap/update command.
   - System flow: tools/bootstrap-into → target repo docs/tools/root files.
   - Data touched: template files, docs, tools, root templates.

2. **Execute approved work items**
   - User action: execute work items from `dev-tasks.md` in the bootstrapped repo.
   - System flow: tools/pc-feature → Codex CLI → tests/CI → logs.
   - Data touched: dev-tasks, execution logs, docs/logs, git changes.
   - Execution pattern: Plan → Patch → Test → Report.
   - Output hygiene: noisy command output is offloaded to `.offload/`.
   - Role sessions share one feature worktree by default (planner/plan-reviewer/patcher/tester/reporter) with role-scoped logs.

3. **Post-MVP hardening loop**
   - User action: report friction/errors/token waste and request optimization.
   - System flow: context update → feature/task selection → tools/skills simplification or hardening → validation/logging.
   - Data touched: `docs/00-context/`, `docs/02-features/`, `docs/03-logs/`, tools/scripts, skill inventory.

## Deployment

### Environments

| Environment | Purpose              | URL | Status    |
| ----------- | -------------------- | --- | --------- |
| Local       | Personal development | n/a | 🟢 Active |

### Build & Deploy Process

1. Run `tools/bootstrap-into` to seed or refresh a target repo.
2. Run ticket workflow commands to execute and validate work locally.
3. Capture improvements in context/features/logs and reapply in future projects.

## Configuration

### Environment Variables

None required; depends on target project.

### Feature Flags

None.

## Dependencies

### Runtime Dependencies

- Git - repo management and diffing.
- Codex CLI - AI execution.
- Make - test/CI entry points.
- Language runtimes - Python/Node/Rust/Go depending on repo.
- `tools/offload-proxy/pp` - output offload wrapper for noisy commands.

### Build Dependencies

- None beyond runtime dependencies.

## Monitoring & Observability

### Logs

- **Locations:**
  - `docs/03-logs/` for decisions, implementation notes, bugs, validations.
  - `logs/<WORK_ITEM_ID>/<step>.log` for CI/tests/precommit/feature/ticket runs.
- **Format:** Prefix each stdout line with `[WI-...][agent][step]` and include timestamps.
- **Behavior:** Tail-friendly, minimal verbosity; noisy command output is offloaded.

### Metrics

- **Tool:** none (manual).
- **Key Metrics:** successful bootstrap/update; successful ticket execution with minimal manual intervention; workflow failures per work item; token usage trend per work item.

### Alerts

- **Tool:** none.
- **Critical Alerts:** script failures logged with work item id, agent, step; human gate required for improvement proposals.

## Known Issues & Debt

- [ ] Keep tools idempotent across reruns to avoid state corruption.
- [ ] Remove unused skills and redundant script paths without breaking execution.
- [ ] Keep automation aggressive enough to reduce toil without masking critical failures.

---

**Last Updated:** 2026-02-14
**Updated By:** Alexandre Pezzotta
