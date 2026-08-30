# Test-case output schema

The repository source format is Markdown tables. CSV/Excel may be exported later, but must preserve the same records and IDs.

| Field | Requirement |
| :--- | :--- |
| `TC ID` | Stable and unique, e.g. `FR10-AI-001` |
| `Source` | `AI` for agent-generated candidates; `HUMAN` only after the student explicitly authors/confirms an extension |
| `Requirement trace` | Exact FR/SEC/API rule IDs |
| `Technique` | EP, BVA, DT, ST, CRUD, Security, Schema, etc. |
| `Priority` | P0/P1/P2 with risk-based meaning |
| `Preconditions` | Actor, role, data ownership and current state |
| `Request` | Method, path, relevant headers/body/query/path fields |
| `Concrete data` | Literal or named fixture values, never vague “invalid value” |
| `Expected status` | Exact when specified; otherwise mark assumption |
| `Expected body/schema` | Required/forbidden fields, types and business values |
| `Expected post-state` | Persistence and forbidden side effects |
| `Cleanup` | Deterministic isolation/reset method |
| `AI audit label` | Blank for new AI candidates; later student decision: VALID/INVALID/INCOMPLETE. Not applicable to HUMAN rows |
| `AI audit reason/correction` | Blank until student review; preserve the raw candidate and point to corrected/final ID when needed |
| `Execution result/evidence` | `NOT RUN` for new design; later PASS/FAIL/BLOCKED/SKIPPED plus real artifact reference |

Keep a separate coverage matrix mapping every modeled item to one or more TC IDs. One case may cover multiple dimensions, but do not count assertions as separate test cases unless they represent independently executable scenarios.

## Record invariants

- `TC ID` and `Source` agree: `FRxx-AI-nnn` → AI, `FRxx-H-nnn` → HUMAN.
- IDs are never reused after rejection; correction history maps raw ID to final ID.
- A row with unresolved ambiguity, vague data or missing oracle is not final executable.
- Expected status may be marked as an explicit assumption only when the spec omits it; cite the ambiguity instead of presenting it as a rule.
- `Execution result/evidence` never changes from `NOT RUN` without real run evidence mapped to that TC ID.
- A HUMAN case includes `Why AI missed`; an AI candidate does not manufacture this explanation.

## Repository table layout

AI candidate tables must include:

```text
TC ID | Source | Req | Technique | Priority | Preconditions | Request/data |
Expected status/body/post-state | Cleanup | Audit label | Audit reason |
Correction/final ID | Execution/evidence
```

Human-extension tables must include:

```text
TC ID | Source | Req | Technique | Priority | Preconditions | Request/data |
Expected status/body/post-state | Cleanup | Why AI missed | Execution/evidence
```

Feature-specific context, such as `Actor/current state`, may replace the generic Preconditions label but not the information requirement.
