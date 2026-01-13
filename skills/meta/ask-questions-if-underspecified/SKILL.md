---
name: ask-questions-if-underspecified
description: Clarify requirements before implementing. Do not use automatically, only when invoked explicitly.
metadata:
  short-description: Clarify → proceed or assume
  mode: interview
  read-only: true
  idempotent: true
---

# Ask Questions If Underspecified

## Goal
Ask the minimum set of clarifying questions needed to avoid wrong work.
Do not start implementing until must-have questions are answered, unless the user explicitly asks to proceed with assumptions.

---

## Non-negotiables
- Do not run commands or edit files while must-have unknowns remain.
- Prefer repo-local truth over guesses.
- If `REPO_PROFILE.json` exists, do not ask questions it already answers (stack, paths, commands, quality bar).
- Do not contradict repo governance (AGENTS/CALIBRATION) if present.
- Use only when explicitly invoked.

---

## Workflow

### 1) Decide whether the request is underspecified
Treat a request as underspecified if, after exploring how to perform the work, any of the following are unclear:
- Objective (what should change vs stay the same)
- Done (acceptance criteria, examples, edge cases)
- Scope (which files/components/users are in/out)
- Constraints (compatibility, performance, style, deps, time)
- Safety/reversibility (migration, rollout/rollback, risk)

Environment/tooling questions are underspecified only if `REPO_PROFILE.json` is missing.

If multiple plausible interpretations exist, assume it is underspecified.

### 2) Ask must-have questions first (keep it small)
Ask 1–5 questions in the first pass. Prefer questions that eliminate whole branches of work.

Make questions easy to answer:
- Short, numbered questions
- Multiple-choice where possible
- Suggest defaults (clearly marked)
- Provide a fast-path response (`defaults`)
- Allow compact answers like `1b 2a 3c` and restate chosen options

### 3) Pause before acting
Until must-have answers arrive:
- Do not run commands, edit files, or produce a detailed plan that depends on unknowns.
- You may do low-risk discovery only if it does not commit to a direction (inspect repo structure, read configs/docs).

If the user explicitly asks to proceed without answers:
- State assumptions as a short numbered list
- Proceed under those assumptions without further questioning

### 4) Confirm interpretation, then hand off
Once you have answers:
- Restate requirements in 1–3 sentences including constraints and success criteria
- Recommend the next skill to invoke (usually `$create-plan` or an implementation skill)

---

## Question templates
- "Before I start, I need: (1) ..., (2) ..., (3) .... If you don't care about (2), I will assume ...."
- "Which should it be? A) ... B) ... C) ... (pick one)"
- "What would you consider 'done'? For example: ..."
- "Any constraints (versions, performance, style, deps)? If none, I will target project defaults."

```text
1) Scope?
a) Minimal change (default)
b) Refactor while touching the area
c) Not sure - use default

2) Compatibility target?
a) Current project defaults (default)
b) Also support older versions: <specify>
c) Not sure - use default

Reply with: defaults (or 1a 2a)
