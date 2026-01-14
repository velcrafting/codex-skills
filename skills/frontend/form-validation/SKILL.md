---
name: form-validation
description: Add input validation rules and UX patterns for forms (client-side validation, errors, submit gating) consistent with repo conventions.
metadata:
  short-description: Form validation + UX
  layer: frontend
  mode: write
  idempotent: false
---

# Skill: frontend/form-validation

## Purpose
Implement consistent form validation and error UX:
- validation rules (required, format, ranges)
- error messaging and accessibility
- submit gating (disabled states, preventing double submit)
- server error handling and mapping where applicable

---

## Inputs
- Form location (route/component)
- Fields and constraints (required/optional, format, min/max)
- Submit behavior (create/update, optimistic allowed yes/no)
- Error handling expectations (inline vs toast vs summary)
- Repo profile (preferred): `<repo>/REPO_PROFILE.json` (form library, patterns)

---

## Outputs
- Validation rules aligned with repo conventions (schema-based or imperative)
- Error UI:
  - field-level errors
  - form-level errors (submit failures)
- Submit safety:
  - disable while submitting
  - prevent duplicate submissions
- Optional: tests for validation behavior (recommended)

---

## Non-goals
- Changing backend contracts
- Implementing domain rules that must be enforced server-side (only mirror client-side)
- Redesigning the form UI

---

## Workflow
1) Identify repo form pattern:
   - native, react-hook-form, formik, custom, schema validator
2) Implement validation:
   - prefer schema validation when repo uses it
   - keep rules close to field definitions
3) Wire error UX:
   - show field error near input
   - show submit error in a consistent location
4) Ensure accessibility:
   - label associations
   - aria-describedby for error text when appropriate
5) Ensure submit safety:
   - disable submit while pending
   - guard against double submit
6) Map server errors:
   - field errors vs global errors
   - do not leak raw server messages if unsafe
7) Run validations from profile and add tests if repo expects them.

---

## Checks
- Invalid inputs prevented or clearly errored
- All interactive fields have labels and accessible error text
- Submit cannot be double-fired
- Error states are deterministic (no flicker, no stale errors)
- Typecheck/lint/tests pass if configured

---

## Failure modes
- Validation source-of-truth unclear → recommend `shared/schema-types` and mirror rules.
- Conflicting UX patterns → follow existing repo standard and document deviation.
- Server error mapping unknown → handle as global error and log for follow-up.

---

## Telemetry
Log:
- skill: `frontend/form-validation`
- fields_count
- validation_style: `schema | imperative | library`
- tests_added: `yes | no`
- files_touched
- outcome: `success | partial | blocked`
