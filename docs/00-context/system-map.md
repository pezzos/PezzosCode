# System Map

## What is Actually Built & Running

<!-- A living map of the current system architecture and deployment -->

## System Overview

```
┌──────────────┐   bootstrap/update   ┌──────────────────────┐
│  User (PO)   │────────────────────▶│  Target Project Repo  │
└──────────────┘                      │  (bootstrapped docs, │
          │                           │   tools, skills)     │
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
- **Entry Points:** `tools/bootstrap-into`, `tools/pc-feature`, `tools/pc-commit`.
- **Key Files/Modules:**
  - `tools/bootstrap-into`: copy templates into target repo.
  - `tools/pc-feature`: execute work item workflow end-to-end.
  - `tools/pc-commit`: validate and commit changes.
  - `tools/offload-proxy/pp`: offload noisy command output to `.offload/`.

### Skills (Codex helpers)

- **Technology:** Markdown skill files in `.codex/skills/`.
- **Entry Points:** `context-to-product`, `prd-to-features`, `feature-status-audit`, `sync-root-from-context`, etc.

### External Services

- **Codex CLI:** Executes prompts for tests/implementation/merge tasks.
- **Git:** Version control and change tracking.
- **Make:** Standard entry point for tests/CI.
- **Language runtimes:** Python, Node/TS, Rust, Go as needed per project.

## Data Flow

### Critical User Flows

1. **Bootstrap a project**
   - User action: run bootstrap/update command.
   - System flow: tools/bootstrap-into → target repo docs/tools/skills/root files.
   - Data touched: template files, docs, tools, skills, root templates.

2. **Execute approved work items**
   - User action: execute work items from `dev-tasks.md` in the bootstrapped repo.
   - System flow: tools/pc-feature → Codex CLI → tests/CI → logs.
   - Data touched: dev-tasks, execution logs, docs/logs, git changes.
   - Execution pattern: Plan → Patch → Test → Report.
   - Output hygiene: noisy command output is offloaded to `.offload/`.
   - Parallel roles use worktrees for isolation (planner/patcher/tester/reporter).

## Deployment

### Environments

| Environment | Purpose              | URL | Status    |
| ----------- | -------------------- | --- | --------- |
| Local       | Personal development | n/a | 🟢 Active |

### Build & Deploy Process

1. Run tools/bootstrap-into to seed a target repo.
2. Use ticket workflow to execute features locally.

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

- **Location:** `docs/03-logs/`.
- **Key Events:** ticket execution, decisions, validations.

### Metrics

- **Tool:** none (manual).
- **Key Metrics:** successful bootstrap; successful ticket execution with minimal manual intervention.

### Alerts

- **Tool:** none.
- **Critical Alerts:** none (manual review).

## Known Issues & Debt

- [ ] Keep tools idempotent across reruns to avoid state corruption.

---

**Last Updated:** 2026-02-04
**Updated By:** Alexandre Pezzotta
