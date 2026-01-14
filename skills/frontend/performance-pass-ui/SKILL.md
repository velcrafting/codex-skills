---
name: performance-pass-ui
description: Identify and reduce avoidable UI performance regressions (render churn, heavy computations, oversized bundles) without behavior change.
metadata:
  short-description: UI perf pass
  layer: frontend
  mode: write
  idempotent: true
---

# Skill: frontend/performance-pass-ui

## Purpose
Improve UI performance by removing obvious regressions and hotspots:
- unnecessary rerenders
- expensive derived computations on render
- unbounded lists or heavy DOM
- avoidable bundle bloat and lazy-load misses

This is a focused pass. It should not change user-facing behavior.

---

## Inputs
- Target UI surface (route/component)
- Reported symptom (slow render, jank, laggy typing, long TTI) if known
- Repo profile (preferred): `<repo>/REPO_PROFILE.json` (framework/tooling/commands)
- Existing instrumentation (React DevTools Profiler, performance marks, logs) if present

---

## Outputs
- Minimal code changes improving performance
- Notes in code comments where tradeoffs exist (why memoization, why virtualization, etc.)
- Optional: small measurement note in PR summary (before/after) if measurement is available

---

## Non-goals
- Visual redesign
- Refactoring purely for style
- Introducing new dependencies unless repo standard
- Premature micro-optimizations without evidence

---

## Workflow
1) Establish baseline:
   - reproduce issue or identify likely hot path
   - prefer measurable evidence (profiler, devtools, timing marks)
2) Identify top offenders:
   - rerender cascades (props identity churn)
   - heavy computations in render
   - large lists without virtualization
   - excessive re-fetch or revalidation loops
3) Apply smallest effective fix:
   - memoize derived values (`useMemo`) only when computation is non-trivial
   - stabilize callbacks (`useCallback`) only when it prevents churn
   - split components to reduce rerender surface
   - add list virtualization if large lists
   - add lazy loading for heavy routes/components if repo uses it
4) Verify behavior unchanged:
   - same UI output and interaction
5) Run validations from profile.

---

## Checks
- No user-visible behavior change (same UI states and interactions)
- Typecheck/lint pass if configured
- Performance improvement is plausible and localized:
  - fewer renders in hot path OR
  - reduced work per render OR
  - reduced payload/deferral of heavy components
- No new infinite loops (effects, memo deps, query invalidations)

---

## Failure modes
- No evidence of perf issue → add minimal measurement first or decline changes.
- Memoization causes stale UI → fix dependencies or remove optimization.
- Optimization increases complexity too much → revert and propose a safer alternative.
- Large list performance issues → recommend virtualization; if not allowed, limit rendered rows.

---

## Telemetry
Log:
- skill: `frontend/performance-pass-ui`
- target: `<route/component>`
- techniques: `memo | split | virtualization | lazy-load | effect-fix | other`
- files_touched
- outcome: `success | partial | blocked`
