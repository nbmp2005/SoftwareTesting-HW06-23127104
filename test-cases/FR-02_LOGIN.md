# FR-02 – Login & Account Lockout Test Design

## Coverage inventory

| Dimension | Partitions/boundaries to cover | Planned TC IDs |
| :--- | :--- | :--- |
| Email | registered/unregistered; valid/invalid format; missing/null/empty/whitespace; case/normalization; injection payload | `[IDs]` |
| Password | correct/wrong; missing/null/empty; Unicode/long input; injection payload | `[IDs]` |
| Attempt counter | 0→1, 1→2, 2→3; success resets; independent accounts | `[IDs]` |
| Lock timing | immediately locked; 29s; 30s; 31s; retry behavior | `[IDs]` |
| Token/response | JWT exists/valid claims; no sensitive fields; error consistency; schema | `[IDs]` |
| Protocol | content type; malformed JSON; method/path; `X-Student-Id` | `[IDs]` |

## Decision table

| Rule | Account exists | Locked now | Password correct | Expected action |
| :--- | :---: | :---: | :---: | :--- |
| R1 | Y | N | Y | Success; token; reset attempts |
| R2 | Y | N | N | Reject; increment exactly 1; lock if new count ≥3 |
| R3 | Y | Y | Y/N | Reject as locked; do not authenticate |
| R4 | N | N/A | Y/N | Generic reject; no account disclosure |

## AI-generated cases

Paste ≥35 raw AI-generated rows. Preserve wording sufficiently to audit it.

| TC ID | Source | Req | Technique | Priority | Preconditions | Request/data | Expected status/body/post-state | Cleanup | Audit label | Audit reason | Correction/final ID | Execution/evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FR02-AI-001` | `AI` | `[FR/SEC]` | `[EP/BVA/DT/etc.]` | `[P]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[VALID/INVALID/INCOMPLETE]` | `[specific reason]` | `[ ]` | `NOT RUN` |

## Human-added cases

| TC ID | Source | Req | Technique | Priority | Preconditions | Request/data | Expected status/body/post-state | Cleanup | Why AI missed | Execution/evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FR02-H-001` | `HUMAN` | `[ ]` | `[ ]` | `[P]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[actual analysis]` | `NOT RUN` |

## Coverage closure

| Requirement/rule | Covered IDs | Gap/justification |
| :--- | :--- | :--- |
| Wrong attempt increments exactly 1 | `[ ]` | `[ ]` |
| Lock begins at third consecutive failure | `[ ]` | `[ ]` |
| Lock duration is 30 seconds | `[ ]` | `[ ]` |
| Successful login returns JWT and resets failures | `[ ]` | `[ ]` |
| No sensitive information disclosure | `[ ]` | `[ ]` |
