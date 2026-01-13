---
name: intake-interview
description: Interview to extract intent, constraints, assumptions, and success criteria for a new system or major feature. Produces an Intake Brief (not a plan, not code).
metadata:
  short-description: Interview → intake brief
  mode: interview
  read-only: true
  idempotent: true
---

# Intake Interview

## Goal
Turn a messy, high-level goal into a crisp **Intake Brief** that surfaces assumptions and prevents silent drift.

This skill produces clarity, not implementation.

---

## Non-negotiables
- Operate in read-only mode. Do not modify files.
- Ask questions to eliminate high-impact ambiguity.
- Do not “smooth over” unknowns. Record them.
- Do not output a plan or propose an architecture. Output only the Intake Brief.

---

## Workflow

### 1) Minimal context scan (if in a repo)
- Skim: README, docs, AGENTS/ARCHITECTURE/ROADMAP/CALIBRATION if present.
- Check for `REPO_PROFILE.json`:
  - If present, treat it as authoritative for stack/tooling and do not re-ask those questions.
- Identify: constraints, current architecture shape, and any non-negotiables.

### 2) Interview (bounded)
Ask up to 10 questions maximum. Prefer multiple-choice. Ask only what materially affects design.

Question groups:
- Objective: what outcome, who uses it, what does success look like?
- Constraints: timeline, tech constraints, security/risk constraints, performance/reliability.
- Interfaces: inputs/outputs, integrations, APIs, data stores.
- Invariants: “must always hold true”, “must never happen”.
- Scope boundaries: what is explicitly out of scope.

Avoid tooling questions already answered by `REPO_PROFILE.json`.

### 3) Output Intake Brief (follow template exactly)

# Intake Brief

## Objective
<1–3 sentences>

## Users
- Primary:
- Secondary:
- Non-users:

## Success metrics
- <Metric 1>
- <Metric 2>

## Constraints
- Technical:
- Operational:
- Risk/safety:

## Functional requirements (v1)
- <Req 1>
- <Req 2>
- <Req 3>

## Non-functional requirements
- Performance:
- Reliability:
- Observability:

## Assumptions register
- A1: <assumption> | confidence: (low/med/high) | impact: (low/med/high)
- A2: <assumption> | confidence: (low/med/high) | impact: (low/med/high)

## Open questions
- Q1 (blocking/non-blocking):
- Q2 (blocking/non-blocking):

## Out of scope (v1)
- <Item 1>
- <Item 2>

## Recommended next step
- If repo scaffolding is missing: `$bootstrap-repo`
- If repo exists but profile/governance needs tailoring: `$personalize-repo`
- If requirements are crisp and execution is next: `$create-plan`
