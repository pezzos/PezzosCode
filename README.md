[![CI](https://github.com/pezzos/PezzosCode/actions/workflows/ci.yml/badge.svg)](https://github.com/pezzos/PezzosCode/actions/workflows/ci.yml)

# PezzosCode bootstrap

> A simple, reusable bootstrap for starting new projects or upgrading existing ones with a docs system, skills, and lightweight tools.

## Purpose

This repo is a template kit for human + LLM development:

- A structured docs system in `docs/` for vision, requirements, features, and logs.
- A small set of tools in `tools/` for linting and workflow helpers.
- Reusable skills in `.codex/skills/` for repeatable tasks.
- A ready-to-copy `AGENTS.md` for AI usage rules.

## Structure

```
/docs
├── 00-context/              # WHY & WHAT EXISTS NOW
│   ├── vision.md            # Product purpose & principles
│   ├── assumptions.md       # Risks & unknowns
│   └── system-map.md        # Current system state
│
├── 01-product/              # WHAT TO BUILD
│   └── prd.md               # Product requirements
│
├── 02-features/             # HOW TO BUILD IT
│   └── feature-<name>/
│       ├── feature-spec.md  # User intent & acceptance
│       ├── tech-design.md   # Architecture & approach
│       ├── dev-tasks.md     # Implementation tasks
│       └── test-plan.md     # Testing strategy
│
├── 03-logs/                 # MEMORY (the magic)
│   ├── implementation-log.md # Code changes & why
│   ├── decision-log.md       # Key decisions
│   ├── bug-log.md            # Bugs & fixes
│   ├── validation-log.md     # Post-ship reality
│   └── insights.md           # Learnings
│
└── 04-process/              # HOW TO WORK
    ├── dev-workflow.md       # Daily workflow
    ├── definition-of-done.md # Quality standards
    └── llm-prompts.md        # Prompts for AI
```

See **[docs/README.md](docs/README.md)** for complete documentation.

## What Makes This Different

### 1. Logs Over Perfect Docs

Chronological logs never go stale. We capture reality as it happens, not aspirational documentation that becomes outdated.

### 2. Built for AI Collaboration

Clear structure and templates that LLMs can understand and fill out. Every feature has the context an AI needs to help you effectively.

### 3. Learning Built-In

Track what you expected vs what actually happened. Extract insights. Get smarter with every feature you ship.

### 4. Just-in-Time Documentation

Don't document everything upfront. Document before (specs), during (decisions), and after (outcomes). Only what matters, when it matters.

## Quick Start

### 1. Bootstrap a new project from this repo

Option A: clone and start fresh.

```bash
git clone https://github.com/pezzos/PezzosCode my-new-project
cd my-new-project
rm -rf .git
git init
```

Then customize:

- Update `docs/00-context/vision.md`
- Update `docs/00-context/system-map.md`
- Update `docs/00-context/users.md`
- Update `docs/01-product/prd.md`

Option B: use this repo as a GitHub template and clone your new repo.

### 2. Improve an existing project by adding the kit

Use the helper script to copy the docs, skills, tools, and workflow files. The
script prompts per existing file to overwrite, merge with Codex, or skip. It
also appends a small marker comment to files it updates; if the marker is
present, future runs skip that file even if it differs:

```bash
./tools/bootstrap-into /path/to/your/existing-project
```

This will bring in:

- `docs/`
- `.codex/skills/`
- `tools/`
- `AGENTS.md`
- `Makefile`

### 3. Fill Out Your Context (30 minutes)

Start with these four files:

1. **`docs/00-context/vision.md`** - Why your product exists
2. **`docs/00-context/system-map.md`** - What's running right now
3. **`docs/00-context/users.md`** - Who the product is for
4. **`docs/01-product/prd.md`** - What you're building

### 4. Build Your First Feature

Create a feature folder:

```bash
mkdir docs/02-features/your-feature-name
cp -r docs/02-features/feature-template/* docs/02-features/your-feature-name/
```

Fill out:

- `feature-spec.md` - What and why
- `tech-design.md` - How you'll build it
- `dev-tasks.md` - Task breakdown
- `test-plan.md` - How you'll validate it

### 5. Ship and Learn

After shipping, update:

- `docs/03-logs/implementation-log.md` - What you built
- `docs/03-logs/validation-log.md` - What actually happened
- `docs/03-logs/insights.md` - What you learned

## How to Run Codex Here

1. Read `AGENTS.md` for repo-specific rules.
2. Work from the repo root.
3. Use a per-repo config by running:

```bash
codex -C .
```

If you use profiles or overrides, add them to `.codex.toml`.

## Workflow Ticket

Use this template to keep work scoped and traceable:

```
Title:
Goal:
Context (docs/ links):
Scope (in/out):
Acceptance criteria:
Tests:
Logs to update:
```

## Philosophy

### Documentation is Memory

Most teams forget why they made decisions. This system captures the **context**, **reality**, and **learning** at every step.

### Logs Are Eternal

Perfect docs go stale. Chronological logs of what happened are forever useful.

### AI-Native Structure

Templates LLMs can fill out. Context for every feature. Prompts that work. Built for human-AI collaboration from day one.

### Single Source of Truth

Every type of information has ONE place. No duplication, no confusion.

## Who This Is For

- **Solo developers** working with AI assistants
- **Small teams** who need structure without bureaucracy
- **Startups** moving fast but wanting to capture learnings
- **Anyone** building with LLMs

## Examples

### Shipping a Feature

1. **Plan** - Fill out feature spec, tech design, tasks (1-2 hours)
2. **Build** - Work through tasks, log decisions (days/weeks)
3. **Ship** - Deploy, update system map (1 hour)
4. **Validate** - Track metrics, update logs (ongoing)

### Fixing a Bug

1. Document in bug log
2. Fix and test
3. Update implementation log
4. Update bug log with root cause

### Making a Decision

1. Document options in decision log
2. Choose and explain rationale
3. Implement
4. Review outcome later

## Get Started in 5 Minutes

Don't overthink it. Start small:

**Day 1:** Create vision.md - Clarify your thinking

**Day 2:** Map your current system - Find gaps

**Day 3:** Write a PRD for next feature - Save hours of confusion

**Day 4:** Log what you built - Future you will thank you

**Day 5+:** Track outcomes and extract insights - This is where magic happens

## Contributing

This is a template meant to be customized. Fork it, make it yours, share improvements.

Found something that works well? Open an issue or PR to help others.

## License

MIT License - Use freely, modify as needed, share improvements.

---

Start using PezzosCode bootstrap today.

[⭐ Star this repo](https://github.com/pezzos/PezzosCode) | [📖 Full Documentation](docs/README.md) | [🐛 Issues](https://github.com/pezzos/PezzosCode/issues)
