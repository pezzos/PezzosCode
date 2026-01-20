# Context Boundaries and Operating Model

## Purpose
Define the operational boundaries and usage expectations for PezzosSystem (ConfVault).
Prevent scope creep by stating explicit non-goals and MVP stop conditions.
Provide guardrails that keep the PRD aligned with the intended manual workflow.

## Scope Boundaries
- Local CLI tool only; manual execution, no daemon or cron.
- Target platforms are macOS and Linux; no Windows support.
- Collects only explicitly selected config files.
- Secrets detection is mandatory and blocks committing by default.
- Versions are stored in Git with metadata to support restore.

## Non-Goals
- Automatic background sync or scheduled runs.
- Cloud backup, remote storage, or multi-user collaboration.
- Full system backups or file system snapshots.
- Secret rotation, key management, or vault services.
- Windows support.

## Operating Model
- User runs the CLI manually to select and collect specific config files.
- Tool scans for secrets and sanitizes output before any commit attempt.
- If a secret is detected, the default behavior is to block committing.
- User reviews sanitized output and metadata before committing to Git.
- Restore is performed by selecting a saved version via metadata.

## MVP Definition of Done
- [ ] Manual CLI flow can collect selected config files on macOS and Linux.
- [ ] Secret detection blocks committing by default.
- [ ] Sanitized outputs are versioned in Git with metadata.
- [ ] Restore works from metadata-defined versions.
- [ ] Non-goals and scope boundaries are explicitly documented in the PRD.

## If you are unsure
- Prefer failing safely over proceeding with partial information.
- Ask for clarification rather than guessing.
- Do not expand scope beyond the stated boundaries.
- Do not invent features or automation paths.
