# Context Boundaries and Operating Model

## Purpose
Define the operational boundaries and usage expectations for PezzosSystem (ConfVault).
Prevent scope creep by stating explicit non-goals and MVP stop conditions.
Provide guardrails that keep the PRD aligned with an intentional, manual workflow.

## Scope Boundaries
- Local CLI tool only; manual execution, no daemon or cron.
- Target platforms are macOS and Linux; no Windows support.
- Collects only explicitly selected config files declared by the user.
- No automatic discovery, inference, or background decision-making.
- Secrets detection is mandatory and blocks committing by default.
- Versions are stored in Git with per-file metadata to support restore.

## Non-Goals
- Automatic background sync or scheduled runs.
- Cloud backup, remote storage, or multi-user collaboration.
- Full system backups or file system snapshots.
- Secret rotation, key management, or vault services.
- UI (web or desktop).
- Windows support.

## Operating Model
- User intentionally runs the CLI to collect specific config files.
- The tool performs secret detection and sanitization before any commit attempt.
- If a secret is detected, the default behavior is to block committing.
- The user is expected to review sanitized output and metadata.
- Git history is the source of truth; the tool does not manage Git workflows.
- Restore is an explicit, user-triggered action based on metadata.

## MVP Definition of Done
- [ ] Manual CLI flow can collect selected config files on macOS and Linux.
- [ ] Secret detection blocks committing by default.
- [ ] Sanitized outputs are versioned in Git with per-file metadata.
- [ ] Restore works reliably from metadata-defined versions.
- [ ] No secrets can be pushed accidentally using the default workflow.
- [ ] MVP is considered complete even if no further features are added.

## If you are unsure
- Prefer failing safely over proceeding with partial information.
- Ask for clarification rather than guessing.
- Do not expand scope beyond the stated boundaries.
- Do not invent features, automation paths, or future use cases.

<!-- PezzosCode bootstrap -->
