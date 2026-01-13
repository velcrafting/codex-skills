You are executing the SKILL: system-contract-map.

Context:
This repository contains a multi-layer system with:
- Frontend
- API
- Backend
- Multiple market domains (crypto, stocks, prediction markets)
- Distinct AI/strategy logic and execution logic

Task:
Produce a system-level contract map that defines structure and expectations, not implementation detail.

Requirements:
- Identify core containers and boundaries
- Identify cross-boundary interactions
- Explicitly separate intent/decision logic from execution logic
- Document invariants that must always hold
- Do not model fine-grained state or UI logic

Outputs (write files exactly to these paths):
1. docs/diagrams/system/c4/container.mmd
2. docs/diagrams/system/sequences/<domain>-order.mmd for:
   - crypto
   - stock
   - prediction
3. docs/diagrams/system/invariants.md (append if exists)

Rules:
- Use Mermaid syntax
- Optimize for clarity and correctness, not completeness
- If assumptions are required, list them explicitly in invariants
- Do not invent features that are not implied by the repo

Begin by analyzing the repository structure and existing docs before producing artifacts.
