---
name: client-generation
description: Generate or update typed API clients from canonical contracts.
metadata:
  short-description: Typed API clients
  layer: api
  mode: write
  idempotent: true
---

# Skill: api/client-generation

## Purpose
Produce or refresh API clients so consumers:
- use typed, validated calls
- stay aligned with contracts
- do not hand-roll request logic

---

## Inputs
- Canonical API contract source
- Target language(s) or framework(s)
- Repo profile (preferred): `<repo>/REPO_PROFILE.json`

---

## Outputs
- Generated client code OR
- Updated handwritten client wrappers (repo standard)
- Regenerated artifacts committed if repo policy allows

---

## Non-goals
- Changing API behavior
- Writing UI or domain logic
- Editing generated code manually

---

## Workflow
1) Identify contract source and generator/tooling.
2) Regenerate clients deterministically.
3) Update import paths or version pins if needed.
4) Verify consumers compile/typecheck.

---

## Checks
- Generated clients compile
- No manual edits inside generated output
- Consumers pass typecheck

---

## Failure modes
- Generator output unstable → pin version or snapshot output.
- Contract invalid → block and return to `api/contract-update`.

---

## Telemetry
Log:
- skill: `api/client-generation`
- languages
- artifacts_written
- outcome
