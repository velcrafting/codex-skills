---
name: component-scaffold
description: Create a new UI component consistent with repo conventions (structure, typing, styling, exports).
metadata:
  short-description: New component scaffold
  layer: frontend
  mode: write
  idempotent: false
---

# Skill: frontend/component-scaffold

## Purpose
Create a new UI component consistent with repo conventions (file layout, TypeScript usage, styling system, exports, naming).

This skill is the default entry point for adding UI surfaces.

---

## Inputs
- Component name
- Target location (route, feature folder, or component library folder)
- Brief responsibility statement (1–2 sentences)
- Props: names + types (if known)
- Any dependencies on existing components or design system
- Repo profile (preferred): `<repo>/REPO_PROFILE.json`

---

## Outputs
- New component file(s)
- Export wiring (barrel/index) if the repo uses it
- Minimal usage example only if repo conventions require it (story/demo/test)

---

## Non-goals
- Implement business/domain rules
- Change API contracts
- Large refactors unrelated to the new component

---

## Workflow
1) Read repo conventions (prefer `REPO_PROFILE.json`; otherwise infer from existing nearby components).
2) Choose correct placement (nearest existing pattern wins).
3) Create the component with minimal API surface:
   - small prop surface
   - sane defaults
   - predictable rendering
4) Wire exports the way the repo already does (or do nothing if it does not).
5) Add minimal usage/example only if required by repo conventions.
6) Run required validations (from repo profile if present).

---

## Checks
- Component compiles (typecheck passes if configured)
- Component renders without runtime errors (smoke-level)
- Export wiring is correct (import path works)
- No unrelated files modified

---

## Failure modes
- Conventions unclear → use `$ask-questions-if-underspecified` (framework, file naming, export pattern).
- Wrong placement → relocate to match nearest existing pattern.
- Missing exports → add wiring consistent with repo patterns.
- Component grows too large during creation → split into subcomponents and keep the public API small.

---

## Telemetry
Log:
- skill: `frontend/component-scaffold`
- files_touched
- conventions_source: `repo_profile | inferred | user_specified`
- outcome: `success | partial | blocked`
