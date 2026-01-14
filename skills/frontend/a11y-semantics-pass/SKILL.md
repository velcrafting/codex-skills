---
name: a11y-semantics-pass
description: Improve semantics and accessibility coverage for UI changes (roles, labels, focus, keyboard, ARIA correctness).
metadata:
  short-description: A11y + semantic audit
  layer: frontend
  mode: write
  idempotent: true
---

# Skill: frontend/a11y-semantics-pass

## Purpose
Ensure UI changes meet baseline accessibility and semantic correctness by addressing:
- semantic HTML usage
- labels and names
- keyboard navigation
- focus management
- ARIA only when necessary and correct

This skill is a pass over existing UI, not feature work.

---

## Inputs
- Target UI surface (components/routes)
- Recent changeset or affected controls
- Repo profile (preferred): `<repo>/REPO_PROFILE.json` (testing/tooling hints)

---

## Outputs
- Updated markup and attributes improving accessibility
- Optional test updates (e.g., testing-library queries by role/name)
- Notes in code comments if tradeoffs are required

---

## Non-goals
- Visual redesign
- Adding new features
- Introducing new dependencies unless repo standard

---

## Workflow
1) Prefer semantic elements first (button, label, fieldset, nav, main).
2) Ensure every interactive control has an accessible name.
3) Ensure keyboard support:
   - tab order sensible
   - enter/space behavior correct
4) Manage focus for dialogs/menus/wizards:
   - focus on open
   - restore focus on close
5) Use ARIA only when needed; avoid “ARIA soup”.
6) Update tests to query by role/name where applicable.
7) Run validations from profile.

---

## Checks
- Interactive elements have accessible names
- Keyboard navigation works for primary flows
- Focus behavior is not broken for dialogs/menus
- Tests still pass; prefer role-based queries where present

---

## Failure modes
- Component library abstracts markup → apply fixes at the wrapper level or use library-supported props.
- Conflicting patterns → follow existing repo standard and document deviations.
- Unclear expected keyboard behavior → ask minimal clarifying question.

---

## Telemetry
Log:
- skill: `frontend/a11y-semantics-pass`
- files_touched
- areas: `labels | focus | keyboard | semantics | aria`
- outcome: `success | partial | blocked`