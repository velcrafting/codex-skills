---
name: domain-logic-module
description: Add or refactor domain rules into a testable module boundary with explicit invariants.
metadata:
  short-description: Domain rules + invariants + tests
  layer: backend
  mode: write
  idempotent: false
---

# Skill: backend/domain-logic-module

## Purpose
Create or refactor domain logic so that business rules live in:
- a testable module boundary
- with explicit invariants
- and deterministic error behavior

This skill prevents domain rules from leaking into controllers, jobs, or adapters.

---

## Inputs
- Domain concept to implement or change (1–3 sentences)
- Invariants that must always hold (must/must-not list)
- Entry points that will call this module:
  - endpoint handler / job / integration adapter
- Repo profile (preferred): `<repo>/REPO_PROFILE.json`

---

## Outputs
- Domain module(s) with:
  - clear inputs/outputs
  - explicit invariants
  - deterministic error returns
- Unit tests that cover:
  - happy path
  - invariant violations
  - at least one edge case

---

## Non-goals
- Wiring endpoints (use `backend/endpoint-scaffold`)
- Schema/migrations (use `backend/persistence-layer-change`)
- External API IO concerns (use `backend/integration-adapter`)
- UI logic

---

## Workflow
1) Locate the correct domain boundary (existing module/folder pattern wins).
2) Define the public API of the module:
   - function(s) or class with explicit types
3) Encode invariants explicitly:
   - validate preconditions
   - validate postconditions where meaningful
4) Define error behavior:
   - typed error codes (align with `shared/error-taxonomy` if present)
   - avoid throwing raw exceptions across boundaries unless repo standard
5) Write unit tests focused on rules, not wiring.
6) Ensure callers orchestrate and do not re-implement rules.
7) Run required validations from profile.

---

## Checks
- Invariants are explicit and enforced
- Errors are deterministic and mapped cleanly
- Callers become thinner after extraction
- Unit tests cover:
  - happy path
  - at least 2 invariant failures
  - edge case
- Typecheck/lint pass if configured

---

## Failure modes
- Invariants unclear or contested → recommend `$decision-capture` before encoding.
- Rule sprawl across multiple modules → propose consolidation (but do not refactor widely).
- Tests hard to write due to coupling → extract dependencies and inject interfaces.

---

## Telemetry
Log:
- skill: `backend/domain-logic-module`
- domain_area: `<short label>`
- invariants_added_or_changed: count
- tests_added: count
- files_touched
- outcome: `success | partial | blocked`
