# Skill: frontend/component-scaffold

## Purpose
Create a new UI component consistent with repo conventions (structure, typing, styling, exports).

## Inputs
- Component name + location
- Brief description of responsibility
- Any required props (names + types if known)
- Repo profile (REPO_PROFILE.json) if present

## Outputs
- New component file(s)
- Export wiring (index barrel or equivalent) if repo uses it
- Minimal usage example (story/demo/test) only if repo profile requires it

## Config
- If REPO_PROFILE.json exists, follow its stack, paths, and conventions.
- If missing, ask the minimum questions needed (framework, file conventions, export pattern).

## Non-goals
- Do not introduce business rules.
- Do not add unrelated refactors.

## Checks
- Run required checks from REPO_PROFILE.json if available (typecheck at minimum).
- Ensure component renders without runtime errors (smoke-level).

## Failure modes
- Wrong file placement or naming: re-align with repo conventions.
- Missing exports: add wiring consistent with repo patterns.
