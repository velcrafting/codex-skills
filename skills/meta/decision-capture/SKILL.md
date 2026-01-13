---
name: decision-capture
description: Capture non-trivial decisions as a proposed entry for a repo's decision log (e.g., DECISIONS.md). Use when work involves meaningful tradeoffs.
---
# Decision Capture

## Goal
Prevent silent drift by turning meaningful choices into explicit, ratifiable decisions.

## Non-negotiables
- Read-only. Do not edit files automatically.
- Do not claim a decision is accepted. Only propose.
- Keep it concrete and short.

## When to use
- Architecture choices, domain boundaries, data model changes, risk invariant changes, migrations, irreversible moves.
- Any time the plan depends on a major assumption or includes “choose one of X”.

## Output (follow exactly)

# Proposed Decision

## Title
<Short, specific title>

## Context
<What problem forced this choice?>

## Decision
<What we will do>

## Alternatives considered
- A1: <alternative> (why not)
- A2: <alternative> (why not)

## Consequences
- Positive:
- Negative:
- Risks:

## Enforcement / follow-through
- Boundaries:
- Validation:
- Docs impacted:

## Review
- Needs ratification: <yes/no>
- Review after: <YYYY-MM-DD or "n/a">

## Append targets
- Decision log file: <e.g., DECISIONS.md path>
- Review queue file (if any): <e.g., REVIEW_QUEUE.md or "n/a">
