# Skills Telemetry

Telemetry is append-only JSONL that records what happened during a run.
Each line is one skill invocation.

## Locations
- Repo log: .codex/telemetry/skills.telemetry.jsonl
- Global log (optional): ~/.codex/telemetry/skills.telemetry.jsonl

## JSONL schema (v1)

Required fields:
- schema_version: "1"
- ts_utc: ISO-8601 UTC timestamp
- repo: repository name or path slug
- git_head: current commit SHA (or "unknown")
- run_id: stable id for a single Codex run
- skill_id: "group/skill-name"
- intent: short sentence describing the task
- inputs: object, safe summary only (no secrets)
- outputs: object
  - files_changed: array of repo-relative paths
  - commands_ran: array of strings
- checks: object
  - attempted: array of strings (typecheck, tests, lint, build)
  - passed: array of strings
  - failed: array of strings
- outcome: "success" | "partial" | "fail"
- duration_ms: number
- followups: array of strings (optional)

Safety rules:
- Never log secrets, tokens, raw env vars, customer data, or full API responses.
- Prefer counts and file paths over payload contents.
- Truncate long strings to 500 chars.

Example record:
{"schema_version":"1","ts_utc":"2026-01-09T14:21:11Z","repo":"tradingbot","git_head":"abc1234","run_id":"run_20260109_1420_01","skill_id":"backend/endpoint-scaffold","intent":"Add POST /api/orders/conditional","inputs":{"method":"POST","path":"/api/orders/conditional"},"outputs":{"files_changed":["backend/app/api/orders/conditional.py"],"commands_ran":["pytest -q"]},"checks":{"attempted":["tests"],"passed":["tests"],"failed":[]},"outcome":"success","duration_ms":84213}
