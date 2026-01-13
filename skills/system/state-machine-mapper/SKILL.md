You are executing the SKILL: state-machine-mapper.

Target:
<Component or file path here>

Task:
Convert the component’s behavior into an explicit state machine.

Requirements:
- Enumerate all states, including transient and error states
- Enumerate all transitions with triggers and guards
- Do not collapse states for brevity
- Include invalid or “should not happen” paths if they are possible
- Assume asynchronous and external failures are possible unless proven otherwise

Outputs (write exactly):
- Create or overwrite:
  <target-directory>/<ComponentName>.state-machine.md

That file must include:
1. State definitions with entry/exit conditions
2. A complete transition table
3. A Mermaid state diagram
4. A Findings section listing:
   - Missing transitions
   - Ambiguous logic
   - Hidden assumptions
   - Coupling to external systems

Rules:
- Every conditional branch in code must appear in the transition table
- If behavior is unclear, mark it explicitly as ambiguous
- Do not modify source code unless explicitly instructed

Begin by reading the target component in full.
