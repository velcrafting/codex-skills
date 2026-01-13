---
name: cartographer
description: Generate a deterministic project map (Tree.txt + docs/PROJECT_MAP.md) for a repo. Use only when explicitly invoked.
metadata:
  short-description: Repo map generator
  mode: write
  idempotent: true
---

# Cartographer

## Goal
Produce a **durable, reviewable map of the repo** that helps humans and agents understand structure quickly, without inventing architecture or behavior.

Primary outputs:
- `Tree.txt` (curated, deterministic tree)
- `docs/PROJECT_MAP.md` (index linking key artifacts)

This skill **maps what exists**. It does not decide how the system should work.

---

## Non-negotiables
- Do not write outputs into `.codex/` (runtime only).
- Do not modify application code.
- Prefer deterministic output (stable ordering, stable excludes).
- Do not invent architecture, intent, or rules.
- If artifacts already exist, update them in place with minimal diff.

---

## Inputs
- Target repo root (explicit or inferred)
- Default exclude rules (defined in script)
- Optional flags passed to the script:
  - `--tree`
  - `--map`
  - `--all`
  - `--max-depth <n>`

---

## Outputs
- `<repo>/Tree.txt`
- `<repo>/docs/PROJECT_MAP.md`

Optional (future extensions, not required):
- `<repo>/docs/diagrams/system/*`
- Colocated `*.state-machine.md`

---

## When to use
- After significant repo growth or restructuring
- When onboarding new contributors or agents
- Before or after cross-cutting refactors
- Prior to publishing or reviewing governance artifacts

Do **not** use as a substitute for:
- ARCHITECTURE.md
- system diagrams
- decision records

---

## Workflow

### 1) Preconditions (read-only)
- Identify repo root.
- Confirm the repo is not `.codex/` itself.
- Check whether `docs/` exists (create only if needed for outputs).

---

### 2) Run the cartographer script
Execute from repo root or with an explicit path:

```sh
python3 scripts/project_ops/cartographer.py --all
