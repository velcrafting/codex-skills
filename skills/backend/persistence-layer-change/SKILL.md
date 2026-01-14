---
name: persistence-layer-change
description: Implement schema/migration changes and update data access patterns safely.
metadata:
  short-description: Schema + migration + safe access updates
  layer: backend
  mode: write
  idempotent: false
---

# Skill: backend/persistence-layer-change

## Purpose
Change persistence safely by managing:
- schema changes (tables/columns/indexes)
- migrations
- updated read/write paths
- compatibility and rollout strategy

This skill is responsible for preventing data loss and breaking changes.

---

## Inputs
- Desired schema change (add/alter/remove)
- Backward compatibility needs:
  - can deploy in one step or requires multi-step rollout
- Data access layers involved (ORM/query builder/raw SQL)
- Repo profile (preferred): `<repo>/REPO_PROFILE.json`

---

## Outputs
- Migration(s) or schema change artifact(s)
- Updated data access code to use new schema
- Tests updated or added
- Notes on rollout if multi-step needed (in comments or docs if repo standard)

---

## Non-goals
- Business logic changes unrelated to the schema
- Endpoint wiring (unless required for compilation)
- Rewriting the persistence layer wholesale

---

## Workflow
1) Identify existing migration mechanism and conventions.
2) Choose safe change strategy:
   - additive change first (preferred)
   - dual-write or backfill if required
   - destructive change only with explicit migration plan
3) Implement migration with deterministic up/down behavior when supported.
4) Update data access paths:
   - reads tolerate both states during rollout if needed
   - writes remain consistent
5) Add/adjust indexes carefully (avoid accidental perf regressions).
6) Add tests:
   - migration applies
   - reads/writes work
7) Run required validations from profile.

---

## Checks
- Migration applies cleanly in a fresh environment (as supported by repo)
- No destructive change without explicit plan
- Tests pass (and cover at least one new access path)
- Typecheck/lint pass if configured
- Performance hazards considered (indexes, N+1, full scans)

---

## Failure modes
- Migration framework missing → stop and recommend establishing it before change.
- Destructive change requested → require staged plan and rollback notes.
- Unknown production constraints → recommend conservative additive migration first.

---

## Telemetry
Log:
- skill: `backend/persistence-layer-change`
- migration_type: `additive | staged | destructive`
- artifacts_written: migration file(s)
- files_touched
- outcome: `success | partial | blocked`
