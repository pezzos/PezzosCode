# Context File Checklist

Use this checklist to identify missing fields and drive clarification questions.
Do not ask about fields that are already complete and unambiguous.

## 1) `docs/00-context/vision.md`

Required:

- Problem statements (who is impacted and why it matters)
- Vision outcomes (desired future state)
- Product boundaries (in scope vs out of scope)
- Current capabilities and key metrics
- Anchor principles, target users, strategic constraints

## 2) `docs/00-context/system-map.md`

Required:

- Real system overview (diagram or equivalent textual map)
- Components and technology choices
- Critical user flows and data touched
- Deployment environments and build/deploy process
- Runtime/build dependencies
- Observability/logging/metrics/alerts

## 3) `docs/00-context/context-boundaries-operating-model.md`

Required:

- Purpose and scope boundaries
- Explicit non-goals and anti-patterns
- Operating model and execution flow
- Product stance and MVP DoD
- Explicit stop condition and uncertainty handling
- HIGH-risk approval handling

## 4) `docs/00-context/users.md`

Required:

- Primary users/personas
- Secondary/edge users (or explicit "none")
- Key user journeys with trigger, steps, outcomes, risks
- Accessibility/inclusion constraints relevant to product usage
- Glossary terms used by users

## 5) `docs/00-context/assumptions.md`

Required:

- User, technical, and business assumptions
- High and medium risks with mitigation
- Unknowns (critical + important)
- Validation log entries for key assumptions and decisions

## 6) `docs/00-context/expected-features.md`

Required:

- Explicit feature candidates in normalized format
- Owner, problem, outcome, priority for each feature
- Notes/constraints where needed

## Clarification Question Style

- Ask focused questions that can be answered concretely.
- Ask for dates/scope when statements may become stale.
- Resolve contradictions explicitly before writing.
- If the user cannot answer, capture as unknown/risk instead of guessing.
