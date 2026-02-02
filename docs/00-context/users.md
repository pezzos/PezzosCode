# Users

## Purpose

<!-- Describe who uses the product and why it matters to them. -->

PezzosCode is built for a single developer/PO who wants a reliable, AI-first workflow
to bootstrap projects and execute features with minimal manual effort.

## Primary Users

### Persona: Developer/PO (single user)

- **Who they are:** Entrepreneur building multiple projects for self and clients, using Codex as the main executor.
- **Goals:** Bootstrap projects fast; describe features and let AI implement them with minimal manual setup.
- **Pain points:** AI workflows need manual setup; small errors derail flow; inconsistent process adherence.
- **Context of use:** macOS CLI, frequent use across new and existing repos.
- **Success looks like:** One-command bootstrap + AI executes approved tasks without manual intervention.
- **Non-goals:** UI-driven workflows, multi-user coordination, or heavy configuration.

## Secondary Users

None. Single-user focus.

## Edge Users

<!-- Rare but important users, admins, partners, etc. -->

### Persona: [Name or Role]

- **Who they are:** [short description]
- **Goals:** [what they want to achieve]
- **Pain points:** [what makes their job hard today]
- **Context of use:** [environment, device, frequency]
- **Success looks like:** [outcome they care about]
- **Non-goals:** [what they do not need]

## Key User Journeys

1. **Bootstrap a project**
   - **Trigger:** Need to start a new project or retrofit an existing repo.
   - **Steps:** Run bootstrap command; confirm template files; start describing context.
   - **Success outcome:** Project has PezzosCode structure ready for AI execution.
   - **Failure risks:** Template conflicts; missing dependencies; non-idempotent reruns.

2. **Execute approved work with AI**
   - **Trigger:** Features/tasks are defined and approved.
   - **Steps:** Run execution command; AI writes tests and implementation; review output.
   - **Success outcome:** Features implemented with minimal manual work.
   - **Failure risks:** Workflow breaks on errors; approvals not respected; token waste.

## Accessibility & Inclusion

<!-- Needs that affect UI/UX and user review behavior. -->

- [x] CLI-only workflow.
- [x] Minimal prompts; avoid unnecessary interactions.
- [x] macOS-first environment.

## Glossary

<!-- Terms users use, not internal jargon. -->

- **Bootstrap:** Copy the PezzosCode template and set up a project to run the workflow.
- **Execute Ticket:** Run the ticket protocol end-to-end with AI assistance.
