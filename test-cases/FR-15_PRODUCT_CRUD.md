# FR-15 – Product CRUD Test Design

## CRUD and parameter model

| Area | Partitions/boundaries | Planned TC IDs |
| :--- | :--- | :--- |
| Create | valid minimal/full; duplicate behavior if relevant; all validations | `[IDs]` |
| Read/list | existing/nonexistent ID; schema; created values persisted | `[IDs]` |
| Update | each field; 254/255/256 name; price partitions; category; isolation | `[IDs]` |
| Delete | existing/nonexistent; repeat delete; later GET; related data behavior | `[IDs]` |
| Name | missing/null/empty/whitespace; 1/254/255/256 chars; Unicode/XSS | `[IDs]` |
| Price | missing/null; negative/0/positive; string/Boolean/large/decimal assumption | `[IDs]` |
| Category | missing/null; existing/nonexistent; wrong type | `[IDs]` |
| Authorization | no token; malformed/expired; user role; admin role | `[IDs]` |
| Injection/schema | path/body SQLi; stored XSS safe rendering; response fields/types | `[IDs]` |

## AI-generated cases

| TC ID | Source | Req | Technique | Priority | Preconditions | Request/data | Expected status/body/post-state | Cleanup | Audit label | Audit reason | Correction/final ID | Execution/evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FR15-AI-001` | `AI` | `[FR/SEC]` | `[CRUD/EP/BVA/etc.]` | `[P]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[VALID/INVALID/INCOMPLETE]` | `[ ]` | `[ ]` | `NOT RUN` |

## Human-added cases

| TC ID | Source | Req | Technique | Priority | Preconditions | Request/data | Expected status/body/post-state | Cleanup | Why AI missed | Execution/evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FR15-H-001` | `HUMAN` | `[ ]` | `[ ]` | `[P]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[actual analysis]` | `NOT RUN` |

## CRUD coverage closure

| Rule/operation | Covered IDs | Gap/justification |
| :--- | :--- | :--- |
| Admin-only mutations | `[ ]` | `[ ]` |
| Name required and ≤255 | `[ ]` | `[ ]` |
| Price required and >0 | `[ ]` | `[ ]` |
| Category exists/required | `[ ]` | `[ ]` |
| Update isolation | `[ ]` | `[ ]` |
| Read/delete lifecycle | `[ ]` | `[ ]` |
