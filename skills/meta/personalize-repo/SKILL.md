---
name: personalize-repo
description: Tailor a bootstrapped repo into a project-specific operating system by capturing intent, constraints, and preferences, then updating docs and generating a repo-local REPO_PROFILE.json. Use only when explicitly invoked.
metadata:
  short-description: Vibe check → repo OS + profile
  mode: write
  idempotent: true
---

# Personalize Repo

## Goal
Convert a generic scaffold into a project-specific operating system by capturing intent, tradeoffs, and constraints, then updating docs accordingly.

This skill also **creates or finalizes** the repo’s canonical execution contract:
- `REPO_PROFILE.json` in repo root

The global profile at `~/.codex/repo_profile.json` is a **reference template only**.

This is intentionally more open-ended than `bootstrap-repo`.

---

## Non-negotiables
- Start with questions. Do not edit files until answers are received OR the user approves proceeding with stated assumptions.
- Do not create duplicate files. Modify existing files in place.
- Keep outputs concrete: update documents, not vibes.
- Make assumptions explicit if proceeding without answers.
- Do not introduce new skills unless explicitly requested.

---

## Inputs
- Target repo root (explicit or inferred)
- Existing scaffold docs (AGENTS/ARCHITECTURE/CALIBRATION/ROADMAP etc.)
- Optional Intake Brief (from `intake-interview`)
- Global reference profile: `~/.codex/repo_profile.json` (read-only)
- Existing repo profile if present: `<repo>/REPO_PROFILE.json`

---

## Outputs
- Updated governance and architecture docs (repo root)
- Updated `.codex/SKILLS.md` (repo-local; preferred skills and routing)
- Created or updated `<repo>/REPO_PROFILE.json` (canonical for this repo)

---

## Workflow

### 1) Context scan (read-only)
- Identify repo root and top-level structure.
- Detect existing docs:
  - AGENTS.md, ARCHITECTURE.md, CALIBRATION.md, ROADMAP.md, DECISIONS.md
- Detect existing profile:
  - `<repo>/REPO_PROFILE.json` (authoritative if present)
- Note stack hints quickly (package.json, pyproject, Makefile, CI).
- If an Intake Brief exists, treat it as intent input.

Do not perform deep codebase analysis. This is personalization, not implementation.

---

### 2) Vibe check interview (open-ended, bounded)
Ask 5–8 open-ended questions. Keep each question short.
Prefer questions that drive meaningful doc customization.

Ask these (customize slightly if context makes them irrelevant):

1) What does “done” look like for this project in 30 days?
2) What kinds of mistakes are most expensive here (money, safety, reputation, time)?
3) What do you want to be strict about (non-negotiables) vs flexible about?
4) What parts of the system are allowed to be messy temporarily, and what must stay clean always?
5) What are the most likely failure modes (technical or operational)?
6) What’s your preferred working style with the agent (more questions upfront vs more iteration)?
7) What is explicitly out of scope for now, even if tempting?
8) Any conventions to enforce (folder boundaries, naming, testing, docs cadence)?

Offer fast-paths:
- User can answer briefly in bullets.
- User can say `defaults` to keep the scaffold generic.

If answers are incomplete but work is not blocked, proceed using conservative defaults and list assumptions explicitly.

---

### 3) Translate answers into doc deltas (proposal first)
Based on the answers (and Intake Brief if available), propose specific updates to:
- AGENTS.md (rules, discipline, testing posture, boundaries)
- ARCHITECTURE.md (system shape, key boundaries, integration seams)
- CALIBRATION.md (definition of done, quality bar, review criteria)
- ROADMAP.md (milestones, gates, evidence expectations)
- `.codex/SKILLS.md` (preferred skills, decision guide pointers, “when to log telemetry”)

If decisions are implied, suggest using `$decision-capture`.

Do not write yet unless answers are received OR the user approves proceeding with stated assumptions.

---

### 4) Create or finalize REPO_PROFILE.json (canonical contract)
Create or update `<repo>/REPO_PROFILE.json` so downstream skills can run deterministically.

Rules:
- If `<repo>/REPO_PROFILE.json` exists: update it deliberately (no silent rewrites).
- If it does not exist:
  - Start from the global reference template `~/.codex/repo_profile.json` if present.
  - Otherwise create a minimal profile from discovered hints and interview answers.
- Keep diffs minimal: do not reformat/reorder the profile unless required.

Minimum required fields (do not omit):
- stack.frontend / stack.backend (or "none")
- stack.language (array)
- commands.lint / commands.typecheck / commands.test / commands.build (use "none" if truly absent)
- paths.frontend_root / paths.backend_root (or "none")
- quality_bar.required_checks (array)
- conventions.package_manager if applicable

Profile quality rules:
- Prefer explicit "none" over guessing commands.
- If commands are unknown, record them as "unknown" and add an Open question in completion report.
- Never store secrets.

This file becomes authoritative for:
- `create-plan`
- all frontend/backend/api/shared skills that execute checks or generate code

---

### 5) Apply updates (write changes)
- Update docs in place.
- Keep changes minimal and aligned with stated preferences.
- If a required file is missing, create it using the existing scaffold pattern.
- Ensure no contradictions between docs and REPO_PROFILE.json.

---

### 6) Completion report (8–14 lines)
Output:
- Files changed (created/updated) and why (short clause each)
- Any new invariants/rules introduced
- Assumptions made (if any)
- REPO_PROFILE.json status (created/updated/deferred + key fields set)
- Next recommended step:
  - Usually `$create-plan`
  - Or `$decision-capture` if tradeoffs remain unresolved

Do not print full file contents.

---

## Checks
- No duplicate files created
- Core docs exist and align with preferences
- `<repo>/REPO_PROFILE.json` exists and has the minimum required fields
- `.codex/SKILLS.md` updated with repo-preferred routing

---

## Failure modes
- User answers conflict with detected stack → prefer user intent, note discrepancy.
- Repo profile commands unknown → set to "unknown" and record as open questions.
- Existing docs are heavily customized → apply minimal deltas, avoid wholesale rewrites.
- Repo profile incomplete at handoff:
  - If required commands remain `unknown`, recommend resolving them before `$create-plan`,
    OR explicitly proceed with `unknown` validations recorded in the plan.
