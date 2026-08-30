# FR-10 – Order State Machine Test Design

## Transition model

Allowed transitions from the requirement:

| Current | Requested | Actor | Expected |
| :--- | :--- | :--- | :--- |
| pending | confirmed | Admin | Allow |
| pending | canceled | User/Admin | Allow |
| confirmed | shipping | Admin | Allow |
| confirmed | canceled | User/Admin | Allow |
| shipping | delivered | Admin | Allow |
| all other combinations | any | User/Admin | Reject; state unchanged |

Build a full `5 current states × 5 requested states` admin matrix plus user-cancel rows. Explicitly include self, backward, skip and both final states.

## Coverage inventory

| Dimension | Coverage | Planned TC IDs |
| :--- | :--- | :--- |
| Valid transitions | Every allowed edge | `[IDs]` |
| Invalid transitions | Every disallowed edge or justified representative set | `[IDs]` |
| Actors | admin, owning user, other user, unauthenticated | `[IDs]` |
| Resource ID | existing own/other; nonexistent; malformed/boundary | `[IDs]` |
| State integrity | rejected request leaves state unchanged | `[IDs]` |
| Robustness | replay/idempotency; concurrent requests if feasible | `[IDs]` |
| Schema/security | success/error shape; SEC-02/03; IDOR | `[IDs]` |

## AI-generated cases

| TC ID | Source | Req | Technique | Priority | Actor/current state | Request/data | Expected status/body/post-state | Setup/cleanup | Audit label | Audit reason | Correction/final ID | Execution/evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FR10-AI-001` | `AI` | `[FR/SEC]` | `[ST/Security/etc.]` | `[P]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[VALID/INVALID/INCOMPLETE]` | `[ ]` | `[ ]` | `NOT RUN` |

## Human-added cases

| TC ID | Source | Req | Technique | Priority | Preconditions | Request/data | Expected status/body/post-state | Setup/cleanup | Why AI missed | Execution/evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FR10-H-001` | `HUMAN` | `[ ]` | `[ ]` | `[P]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[actual analysis]` | `NOT RUN` |

## Transition coverage closure

| Current state | Admin targets covered | User cancel covered | State-integrity assertion | Gaps |
| :--- | :--- | :--- | :--- | :--- |
| pending | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| confirmed | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| shipping | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| delivered | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| canceled | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
