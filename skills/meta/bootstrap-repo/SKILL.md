---
name: bootstrap-repo
description: Bootstrap or refresh a repo scaffold (governance docs, .codex folder, Tree.txt). Use only when explicitly invoked.
---
# Bootstrap Repo

## Goal
Create or refresh a standard repo scaffold quickly and predictably:
- AGENTS.md
- ARCHITECTURE.md
- CALIBRATION.md
- DECISIONS.md
- SUGGESTIONS.md
- REVIEW_QUEUE.md
- ROADMAP.md
- Tree.txt
- .codex/SKILLS.md

## Non-negotiables
- Do not create duplicate files (no foo_copy.md, foo 2.md).
- If a file exists, modify it in place.
- Keep this bootstrap fast: bounded questions, template-driven outputs.
- Prefer defaults when user is unsure.

## Workflow

### 1) Quick discovery (read-only)
Perform a fast scan of the target repo:

- Identify repo root
- Detect existing scaffold files
- Detect stack hints:
  - `package.json`, `pnpm-lock.yaml`, `yarn.lock`
  - `pyproject.toml`, `requirements.txt`, `poetry.lock`
  - `Makefile`, CI configs
- Detect test / lint / build commands if trivially discoverable
- Detect frontend/backend roots if obvious (`frontend/`, `backend/`, `src/`)

Do **not** recurse deeply. This is heuristic, not forensic.

### 2) Bounded setup questions (multiple-choice)
Ask 8–12 questions max. Multiple-choice + recommended defaults.
Allow a fast-path: user can reply `defaults` to accept all recommended options.

Use this exact question format:

```text
1) Repo identity?
a) New repo scaffold
b) Existing repo refresh (recommended if files exist)

2) Stack shape?
a) Python backend
b) Node/Next frontend
c) Monorepo (Python + Node) (recommended if both exist)
d) Other

3) Primary objective for the next 2–4 weeks?
a) Ship new feature/domain (recommended)
b) Stabilize reliability
c) Refactor/cleanup
d) Mixed

4) Risk posture?
a) Risk-off / safety-first (recommended)
b) Balanced
c) Move fast

5) Change discipline?
a) No drive-by refactors (recommended)
b) Refactor allowed when touching code

6) Test posture?
a) Run relevant tests by default (recommended)
b) Only run tests on request

7) Decision rigor?
a) Propose decisions for non-trivial tradeoffs (recommended)
b) Keep decisions informal

8) Roadmap format?
a) Milestones + checkpoints (recommended)
b) Simple task list

9) Repo boundaries?
a) Prefer domain modules; avoid god files (recommended)
b) Flexible

10) Skills usage?
a) Use skills when relevant, never block progress (recommended)
b) Strict: must use skills if applicable

11) README handling?
a) Create README if missing (recommended)
b) Always refresh README (only if you want it overwritten)
c) Do not create/modify README

If answers are incomplete, proceed with recommended defaults and list assumptions.

### Template source

- Use templates from: `~/.codex/templates/repo-scaffold/`
- If a specialized profile is later added (e.g., TradingBot-style), select the corresponding template folder.
- If the template folder is missing or incomplete, fall back to minimal inline templates embedded in this skill.
- Templates must be applied deterministically:
  - Do not invent structure outside the template.
  - Only fill documented placeholders (mission, risk posture, quality bar, boundaries).

---

### 3) Template application
- Select templates from `~/.codex/templates/`
- If a specialized template set exists (e.g. domain-specific), use it
- Otherwise fall back to the generic templates

Template rules:
- Apply deterministically
- Only fill documented placeholders (mission, posture, boundaries, quality bar)
- Do not invent new sections beyond the template

---

### 4) Generate or update scaffold (write changes)
- Create missing files from templates
- Update existing files in place to align with chosen options
- Ensure `.codex/telemetry/` exists (repo-local)
- Create or refresh `.codex/SKILLS.md` (repo-local skills note)
- Generate `Tree.txt` excluding:
  - `.git`, `.venv`, `node_modules`, `.next`, `dist`, `build`
  - `.pytest_cache`, `.mypy_cache`, `__pycache__`, `.DS_Store`
  - `.codex/log`, `.codex/sessions`

---

### 5) Optional: minimal repo profile inference
If stack inference is **high confidence**, create a **minimal** `REPO_PROFILE.json` in repo root:

- language(s)
- frontend/backend presence
- obvious command hooks if detected

If confidence is low, skip and defer to `$personalize-repo`.

Never overwrite an existing profile without explicit approval.

---

### 6) Completion report
Output a short report (8–14 lines) including:
- Files created or updated
- Assumptions used (if any)
- Whether a repo profile was created or deferred
- Next recommended step:
  - If intent is fuzzy: `$intake-interview`
  - If structure needs tailoring: `$personalize-repo`
  - If intent is clear: `$create-plan`

Do **not** print full file contents.

---

## Checks
- Repo contains the expected scaffold files
- No duplicate files created
- Tree.txt renders cleanly and excludes junk paths
- `.codex/telemetry/` exists in repo

---

## Failure modes
- Existing files diverge heavily from templates → modify minimally, do not rewrite wholesale
- Stack inference ambiguous → skip profile creation and defer
- User answers contradictory → apply recommended defaults and record assumptions

---

## Notes
This skill establishes **structure and discipline**, not product direction.
It should always make the repo easier for subsequent skills to reason about.