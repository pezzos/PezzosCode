# Users

## Purpose

<!-- Describe who uses the product and why it matters to them. -->

PezzosCode is built for a single developer/PO who wants a reliable, AI-first workflow
to bootstrap/update projects and execute features with near-zero manual input.

## Primary Users

### Persona: Developer/PO (single user)

- **Who they are:** A solo builder running multiple projects with one personal workflow, toolset, and habits.
- **Goals:** Bootstrap/update projects fast; describe intent once; let AI execute and auto-fix deterministic issues.
- **Pain points:** Manual prompts interrupt flow; repetitive fixups add toil; token-heavy runs cost time and context.
- **Context of use:** macOS CLI, frequent use across new and existing repos.
- **Success looks like:** One-command bootstrap/update + AI executes approved tasks with almost no human input.
- **Non-goals:** UI-driven workflows, multi-user coordination, heavy configuration, or support for other dev styles.

## Secondary Users

None. Single-user focus.

## Edge Users

None. This product is intentionally single-user.

## Key User Journeys

1. **Bootstrap or refresh a project**
   - **Trigger:** Need to start a new project or update an existing repo with latest workflow.
   - **Steps:** Run bootstrap/update command; verify sync; continue with context/features.
   - **Success outcome:** Project is ready for AI execution with minimal manual adjustments.
   - **Failure risks:** Template conflicts; missing dependencies; non-idempotent reruns.

2. **Execute approved work with AI**
   - **Trigger:** Features/tasks are defined and approved.
   - **Steps:** Run execution command; AI performs Plan → Patch → Test → Report; deterministic issues auto-fix.
   - **Success outcome:** Features implemented with near-zero manual intervention.
   - **Failure risks:** Workflow breaks on errors; approvals not respected; token waste from avoidable LLM steps.

3. **Post-MVP workflow hardening**
   - **Trigger:** Errors, token spikes, or repeated manual interventions are observed.
   - **Steps:** Capture friction; prioritize hardening task; simplify/remove unused parts; validate and log.
   - **Success outcome:** Fewer failures, fewer prompts, lower token usage.
   - **Failure risks:** Over-optimization hides needed diagnostics; useful capabilities removed by mistake.

## Accessibility & Inclusion

<!-- Needs that affect UI/UX and user review behavior. -->

- [x] CLI-only workflow.
- [x] Minimal prompts; avoid unnecessary interactions.
- [x] macOS-first environment.

## Glossary

<!-- Terms users use, not internal jargon. -->

- **Bootstrap:** Copy the PezzosCode template and set up a project to run the workflow.
- **Refresh/Update:** Reapply template/tooling changes into an existing project safely.
- **Execute Ticket:** Run the ticket protocol end-to-end with AI assistance.
- **Toil:** Any avoidable human input or repetitive manual fixup in the workflow.
- **Auto-fix:** Deterministic script/AI correction that runs before asking the user to intervene.
