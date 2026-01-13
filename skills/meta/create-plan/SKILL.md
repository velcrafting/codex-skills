---
name: create-plan
description: Create a concise, executable plan for a coding task. Use when the user explicitly asks for a plan or when work is clearly multi-step.
metadata:
  short-description: Plan generator
  mode: read-only
  read-only: true
  idempotent: true
---

# Create Plan

## Goal
Turn a user prompt (or spec) into a single actionable plan the user can execute against, with:
- clear scope boundaries
- ordered, atomic steps
- explicit validation commands
- known risks and open questions

The output should be executable without additional interpretation.

---

## Non-negotiables
- Operate in read-only mode: do not write or update files.
- Ask at most 1–2 clarifying questions only if truly blocking.
- If unsure but not blocked, state assumptions and proceed.
- Prefer repo-local truth over guesses (docs, config, profile).
- Do not invent commands. Use profile values, discovered tooling, or mark as `unknown`.

---

## Inputs
- User request / spec / acceptance criteria (if provided)
- Repo context (README, ARCHITECTURE, AGENTS, CALIBRATION, ROADMAP if present)
- Repo profile (authoritative if present): `<repo>/REPO_PROFILE.json`
- Global reference profile (fallback reference only): `~/.codex/repo_profile.json`

---

## Outputs
- A single plan document following the required format exactly.

---

## Profile resolution order
1) If `<repo>/REPO_PROFILE.json` exists: treat it as authoritative for:
   - stack shape
   - paths (frontend_root/backend_root)
   - commands (lint/typecheck/test/build)
   - quality bar (required_checks)
2) Else if `~/.codex/repo_profile.json` exists: treat it as a reference template for defaults only.
3) Else: proceed with minimal assumptions and record unknowns explicitly.

Never silently merge profiles. If they conflict, prefer repo-local and record the conflict as a risk.

---

## Minimal workflow

### 1) Scan context quickly (read-only)
- Read README and obvious docs:
  - README, docs/, CONTRIBUTING, ARCHITECTURE, AGENTS, CALIBRATION, ROADMAP
- Identify likely touched areas/files.
- Determine stack shape (frontend/backend/monorepo) from repo structure and/or profile.
- Determine canonical validation commands:
  - Prefer `<repo>/REPO_PROFILE.json` commands if present.
  - If missing, infer only if trivial (e.g., package.json scripts present).
  - Otherwise mark validation commands as `unknown` and list as Open questions.
- Identify constraints:
  - language/framework, deployment shape, CI gates, risk posture

If `<repo>/REPO_PROFILE.json` exists, treat its commands and paths as authoritative.

---

### 2) Plan the work
- Keep steps atomic and ordered: discovery → changes → validation → rollout.
- 6–10 action items by default.
- Verb-first actions: Add…, Refactor…, Verify…, Ship….
- Include at least one tests/validation step.
- Include at least one edge case/risk step when applicable.
- When useful, annotate steps with the relevant skill name in parentheses:
  - Example: `[ ] Add endpoint contract (api/contract-update)`
  - Keep this lightweight; do not turn the plan into a registry dump.

If a repo profile exists, prefer steps that respect its boundaries and conventions.

---

### 3) Document unknowns
- If unknowns remain, keep them in Open questions (max 3).
- If unknowns are truly blocking, ask 1–2 clarifying questions (max).
- If commands are unknown, do not guess. Record the missing command as an Open question.

---

## Validation requirements
Validation section must contain:
- runnable commands from `<repo>/REPO_PROFILE.json` when present, OR
- explicit placeholders:
  - `unknown (needs repo command)` if missing
  - `none (repo does not use this)` if not applicable

Prefer including at least:
- one fast check (lint/typecheck)
- one correctness check (tests)

---

## Output (follow exactly)

# Plan

<1–3 sentences: what we’re doing, why, and the high-level approach.>

## Scope
- In:
- Out:

## Action items
[ ] <Step 1>
[ ] <Step 2>
[ ] <Step 3>
[ ] <Step 4>
[ ] <Step 5>
[ ] <Step 6>

## Validation
- <Command or validation step 1>
- <Command or validation step 2>

## Edge cases / risks
- <Risk 1>
- <Risk 2>

## Open questions
- <Question 1>
- <Question 2>
- <Question 3>
