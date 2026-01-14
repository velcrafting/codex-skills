---
name: ui-refactor-extract
description: Refactor UI code without behavior change (extract/rename/reorganize) while preserving public APIs and adding evidence via tests or inspection.
metadata:
  short-description: UI refactor, no behavior change
  layer: frontend
  mode: write
  idempotent: false
---

# Skill: frontend/ui-refactor-extract

## Purpose
Improve UI maintainability without changing behavior by:
- extracting subcomponents
- renaming for clarity
- reorganizing file structure within existing conventions
- reducing component complexity (“god component” prevention)

Behavior must remain stable. This skill requires evidence.

---

## Inputs
- Target component(s)/route(s)
- Refactor intent (why, what pain)
- Public API constraints (props, exports, routes)
- Repo conventions (from `REPO_PROFILE.json` if present)

---

## Outputs
- Refactored UI modules with smaller components
- Updated imports/exports as needed
- Evidence of no behavior change:
  - tests updated/added OR
  - deterministic before/after inspection notes if tests are unavailable

---

## Non-goals
- Adding new features
- Visual redesign
- Changing data contracts
- Sweeping refactors outside the touched surface

---

## Workflow
1) Identify the smallest extraction that reduces complexity meaningfully.
2) Preserve public APIs:
   - keep existing props stable unless explicitly requested
   - keep exports stable or update all call sites
3) Extract subcomponents:
   - prefer pure, presentational components
   - pass minimal props
4) Keep behavior stable:
   - no logic changes unless required for extraction correctness
5) Add/adjust tests:
   - ensure at least one test asserts expected render/interaction
6) Run validations from profile.

---

## Checks
- No behavior change intended or introduced
- Public API compatibility preserved (props/exports/import paths)
- Typecheck/lint/tests pass if configured
- Component complexity reduced (clearer boundaries, fewer responsibilities)

---

## Failure modes
- Refactor drifts into feature work → stop and propose separate skill invocation.
- Extraction reveals hidden state coupling → recommend `frontend/state-modeling`.
- Tests unavailable → provide deterministic inspection steps and keep diff minimal.

---

## Telemetry
Log:
- skill: `frontend/ui-refactor-extract`
- refactor_type: `extract | rename | reorganize`
- evidence: `tests | inspection`
- files_touched
- outcome: `success | partial | blocked`
