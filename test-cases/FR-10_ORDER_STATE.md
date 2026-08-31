# FR-10 – Order State Machine Test Design

## 1. Source and generation status

| Item | Value |
| :--- | :--- |
| Requirement source | `docs/hw6.md` §6, especially FR-10 state-transition requirement |
| API source | `docs/api_specification.md` §4.6 and §6.2 |
| API source SHA-256 | `488CBCB790099BA9CBB34C7C80BA04C6AEC9E9EBB598F031FFA575737547B139` |
| Generated set | 47 unique AI candidates (`FR10-AI-001`–`FR10-AI-047`) |
| Human extension set | 5 student-authored cases (`FR10-H-001`–`FR10-H-005`), refined with explicit contract assumptions |
| Lifecycle | Raw AI output awaiting student audit; audit fields are intentionally blank |
| Execution | All cases are `NOT RUN`; no Postman/Newman evidence is claimed |

## 2. Contract inventory

| Area | Contract used for this design |
| :--- | :--- |
| Actors | Authenticated admin; authenticated owning user; authenticated non-owner; unauthenticated/invalid-token caller |
| Admin transition API | `PUT /api/admin/orders/:id/status`, JSON body `{"status":"<target>"}`; valid admin role required |
| User cancellation API | `PUT /api/orders/:id/cancel`; bearer token required; ownership is treated as required to prevent IDOR |
| States | `pending`, `confirmed`, `shipping`, `delivered`, `canceled` |
| Allowed path | `pending → confirmed → shipping → delivered`; cancellation `pending → canceled` and `confirmed → canceled` |
| Final states | `delivered` and `canceled`; all outgoing transitions are rejected |
| State integrity | Every rejected request must leave the order and unrelated orders unchanged |
| Required headers | `Authorization: Bearer <fixture-token>` and `X-Student-Id: 23127104`; JSON admin requests also use `Content-Type: application/json` |
| Response contract | Exact success/error status and response schemas are omitted by the API spec; temporary assumptions below make candidates implementable only after student/spec-owner confirmation |

## 3. Ambiguities and working assumptions

| ID | Ambiguity | Working assumption used in candidates | Student decision required |
| :--- | :--- | :--- | :--- |
| `ASM-FR10-01` | API spec says cancellation is allowed when an order is “chưa giao”, which could include `shipping`; the explicit FR-10 rule says users cannot cancel `shipping`. | The more specific state rule wins: owner cancellation is allowed only from `pending`/`confirmed`. | Confirm intended cancellation states. |
| `ASM-FR10-02` | Success status/body are unspecified. | Successful transition/cancellation returns `200`, JSON containing the same order `id` and new `status`, with no password/token/internal fields. | Confirm exact status and schema. |
| `ASM-FR10-03` | Invalid-transition status/body are unspecified. | Return `409` with a non-sensitive JSON error; persist no state change. | Confirm whether implementation contract should use `400` or `409`. |
| `ASM-FR10-04` | Validation/not-found status/body are unspecified. | Malformed/missing/unknown status or malformed ID → `400`; absent order → `404`; JSON error; no mutation. | Confirm framework-specific validation contract. |
| `ASM-FR10-05` | Authentication/authorization error schema is unspecified. | Missing/invalid token → `401`; authenticated wrong role/non-owner → `403`; JSON error without order details. | Confirm exact auth status/schema and ownership rule. |
| `ASM-FR10-06` | Concurrent transition serialization is unspecified. | Results must match one legal serial order: cancel-first means one commit and final `canceled`; confirm-first may allow the subsequent legal `confirmed→canceled`, so two commits and final `canceled` are also valid. No lost update, hybrid state or duplicate event is allowed. | Confirm concurrency policy and fixture capability. |
| `ASM-FR10-07` | The status enum lists lowercase literals but does not say whether case/outer whitespace are normalized. | Treat the wire contract as a strict enum: `CONFIRMED` and ` confirmed ` are invalid and each returns `400` without mutation. | Confirm strict matching versus normalization. |
| `ASM-FR10-08` | Duplicate JSON object names have parser-dependent behavior and no API policy is specified. | Reject a body containing duplicate `status` keys with `400` before business logic; do not choose first/last silently. | Confirm parser/gateway policy before marking the case final executable. |
| `ASM-FR10-09` | Unsupported-method status is not specified. | A syntactically valid `PATCH` to the PUT-only status route returns `405 Method Not Allowed` and performs no mutation. | Confirm whether the deployed router intentionally returns `404` instead. |

Candidates that depend on these assumptions count as generated AI candidates, but are not claimed as final executable until the student confirms or corrects the oracle during human audit.

## 4. State and decision models

### 4.1 Full admin current × target matrix

`A` = allow; `R` = reject with state unchanged.

| Current \ Target | pending | confirmed | shipping | delivered | canceled |
| :--- | :---: | :---: | :---: | :---: | :---: |
| pending | R (`001`) | A (`002`) | R (`003`) | R (`004`) | A (`005`) |
| confirmed | R (`006`) | R (`007`) | A (`008`) | R (`009`) | A (`010`) |
| shipping | R (`011`) | R (`012`) | R (`013`) | A (`014`) | R (`015`) |
| delivered | R (`016`) | R (`017`) | R (`018`) | R (`019`) | R (`020`) |
| canceled | R (`021`) | R (`022`) | R (`023`) | R (`024`) | R (`025`) |

### 4.2 User cancellation decision table

| Auth | Ownership | Current state | Expected | TC IDs |
| :--- | :--- | :--- | :--- | :--- |
| Valid user | Owner | pending/confirmed | Allow cancellation | `026`, `027` |
| Valid user | Owner | shipping/delivered/canceled | Reject; unchanged | `028`–`030` |
| Valid user | Non-owner | pending/confirmed | Reject without revealing order details | `031`, `032` |
| Missing/invalid token | Any | pending | Reject authentication; unchanged | `033`, `034` |

## 5. Fixtures and isolation

- `ADM-A`: admin account with a valid fixture token; `USR-A`: owner; `USR-B`: non-owner. Tokens are runtime variables, never committed credentials.
- `O-P`, `O-CF`, `O-S`, `O-D`, `O-X`: dedicated orders in `pending`, `confirmed`, `shipping`, `delivered`, `canceled`; `O-U` is an unrelated sentinel order.
- Before each case, restore the named order snapshot and record `O-U`'s status/version. After the request, verify the target state and that `O-U` is unchanged, then restore the fixture snapshot.
- Concurrency cases require a database reset/seed mechanism and synchronized requests; they remain `NOT RUN` until that harness exists.

## 6. AI-generated candidate cases

| TC ID | Source | Req | Technique | Priority | Actor/current state | Request/data | Expected status/body/post-state | Setup/cleanup | Audit label | Audit reason | Correction/final ID | Execution/evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FR10-AI-001` | `AI` | FR-10; FR-18; API §6.2 | ST, self-transition | P1 | `ADM-A`; `O-P=pending` | `PUT /api/admin/orders/O-P/status`; target `pending`; required headers | `409` per ASM-03; JSON error; `O-P` remains `pending`, `O-U` unchanged | Restore `O-P/O-U` snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-002` | `AI` | FR-10; FR-18; API §6.2 | ST, valid edge | P0 | `ADM-A`; `O-P=pending` | Same admin API; target `confirmed` | `200` per ASM-02; body `id=O-P,status=confirmed`, no sensitive fields; only `O-P→confirmed` | Restore `O-P/O-U` snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-003` | `AI` | FR-10; FR-18; API §6.2 | ST, skip | P0 | `ADM-A`; `O-P=pending` | Admin API; target `shipping` | `409` per ASM-03; error; `O-P` stays `pending`, `O-U` unchanged | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-004` | `AI` | FR-10; FR-18; API §6.2 | ST, skip | P0 | `ADM-A`; `O-P=pending` | Admin API; target `delivered` | `409` per ASM-03; error; no state/version change | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-005` | `AI` | FR-10; FR-18; API §6.2 | ST, valid cancel | P0 | `ADM-A`; `O-P=pending` | Admin API; target `canceled` | `200` per ASM-02; body identifies `O-P,canceled`; only `O-P→canceled` | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-006` | `AI` | FR-10; FR-18; API §6.2 | ST, backward | P0 | `ADM-A`; `O-CF=confirmed` | Admin API; target `pending` | `409`; error; `O-CF` remains `confirmed`, sentinel unchanged | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-007` | `AI` | FR-10; FR-18; API §6.2 | ST, self-transition | P1 | `ADM-A`; `O-CF=confirmed` | Admin API; target `confirmed` | `409`; error; no mutation | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-008` | `AI` | FR-10; FR-18; API §6.2 | ST, valid edge | P0 | `ADM-A`; `O-CF=confirmed` | Admin API; target `shipping` | `200`; body `id=O-CF,status=shipping`; only `O-CF→shipping` | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-009` | `AI` | FR-10; FR-18; API §6.2 | ST, skip | P0 | `ADM-A`; `O-CF=confirmed` | Admin API; target `delivered` | `409`; error; `O-CF` stays `confirmed` | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-010` | `AI` | FR-10; FR-18; API §6.2 | ST, valid cancel | P0 | `ADM-A`; `O-CF=confirmed` | Admin API; target `canceled` | `200`; body `id=O-CF,status=canceled`; only target changes | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-011` | `AI` | FR-10; FR-18; API §6.2 | ST, backward | P0 | `ADM-A`; `O-S=shipping` | Admin API; target `pending` | `409`; error; `O-S` remains `shipping` | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-012` | `AI` | FR-10; FR-18; API §6.2 | ST, backward | P0 | `ADM-A`; `O-S=shipping` | Admin API; target `confirmed` | `409`; error; no mutation | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-013` | `AI` | FR-10; FR-18; API §6.2 | ST, self-transition | P1 | `ADM-A`; `O-S=shipping` | Admin API; target `shipping` | `409`; error; no mutation | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-014` | `AI` | FR-10; FR-18; API §6.2 | ST, valid edge | P0 | `ADM-A`; `O-S=shipping` | Admin API; target `delivered` | `200`; body `id=O-S,status=delivered`; only target changes | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-015` | `AI` | FR-10; FR-18; API §6.2 | ST, forbidden cancel | P0 | `ADM-A`; `O-S=shipping` | Admin API; target `canceled` | `409`; error; `O-S` remains `shipping` | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-016` | `AI` | FR-10; FR-18; API §6.2 | ST, final state | P0 | `ADM-A`; `O-D=delivered` | Admin API; target `pending` | `409`; error; `O-D` remains `delivered` | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-017` | `AI` | FR-10; FR-18; API §6.2 | ST, final state | P0 | `ADM-A`; `O-D=delivered` | Admin API; target `confirmed` | `409`; error; no mutation | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-018` | `AI` | FR-10; FR-18; API §6.2 | ST, final state | P0 | `ADM-A`; `O-D=delivered` | Admin API; target `shipping` | `409`; error; no mutation | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-019` | `AI` | FR-10; FR-18; API §6.2 | ST, final self | P1 | `ADM-A`; `O-D=delivered` | Admin API; target `delivered` | `409`; error; no new event/version or mutation | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-020` | `AI` | FR-10; FR-18; API §6.2 | ST, final state | P0 | `ADM-A`; `O-D=delivered` | Admin API; target `canceled` | `409`; error; remains `delivered` | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-021` | `AI` | FR-10; FR-18; API §6.2 | ST, final state | P0 | `ADM-A`; `O-X=canceled` | Admin API; target `pending` | `409`; error; `O-X` remains `canceled` | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-022` | `AI` | FR-10; FR-18; API §6.2 | ST, final state | P0 | `ADM-A`; `O-X=canceled` | Admin API; target `confirmed` | `409`; error; no mutation | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-023` | `AI` | FR-10; FR-18; API §6.2 | ST, final state | P0 | `ADM-A`; `O-X=canceled` | Admin API; target `shipping` | `409`; error; no mutation | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-024` | `AI` | FR-10; FR-18; API §6.2 | ST, final state | P0 | `ADM-A`; `O-X=canceled` | Admin API; target `delivered` | `409`; error; remains `canceled` | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-025` | `AI` | FR-10; FR-18; API §6.2 | ST, final self | P1 | `ADM-A`; `O-X=canceled` | Admin API; target `canceled` | `409`; error; no duplicate cancellation event/version | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-026` | `AI` | FR-10; API §4.6 | ST, valid cancel | P0 | `USR-A` owns `O-P=pending` | `PUT /api/orders/O-P/cancel`; user token + student header | `200` per ASM-01/02; body `O-P,canceled`; only owned order changes | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-027` | `AI` | FR-10; API §4.6 | ST, valid cancel | P0 | `USR-A` owns `O-CF=confirmed` | User cancel API for `O-CF` | `200`; body `O-CF,canceled`; only target changes | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-028` | `AI` | FR-10; API §4.6 | ST, forbidden cancel | P0 | `USR-A` owns `O-S=shipping` | User cancel API for `O-S` | `409` per ASM-01/03; error; remains `shipping` | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-029` | `AI` | FR-10; API §4.6 | ST, final state | P0 | `USR-A` owns `O-D=delivered` | User cancel API for `O-D` | `409`; error; remains `delivered` | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-030` | `AI` | FR-10; API §4.6 | ST, final state | P0 | `USR-A` owns `O-X=canceled` | User cancel API for `O-X` | `409`; error; no duplicate cancellation side effect | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-031` | `AI` | FR-10; SEC-02; API §4.6 | Security, IDOR | P0 | `USR-B` does not own `O-P=pending` | User cancel API for `O-P` using `USR-B` token | `403` per ASM-05; generic error without order data; `O-P` unchanged | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-032` | `AI` | FR-10; SEC-02; API §4.6 | Security, IDOR | P0 | `USR-B` does not own `O-CF=confirmed` | User cancel API for `O-CF` using `USR-B` token | `403`; non-enumerating error; `O-CF` unchanged | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-033` | `AI` | FR-10; SEC-02; API §4.6 | Security, auth | P0 | No authenticated actor; `O-P=pending` | User cancel API with no `Authorization` header | `401` per ASM-05; generic JSON error; order unchanged | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-034` | `AI` | FR-10; SEC-02; API §4.6 | Security, auth | P0 | Invalid/expired fixture token; `O-P=pending` | User cancel API with `Bearer invalid.fixture.token` | `401`; no order details; state unchanged | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-035` | `AI` | FR-10; FR-12; SEC-03; API §6.2 | Security, role escalation | P0 | Authenticated `USR-A`; `O-P=pending` | Admin API target `confirmed` with normal-user token | `403` per ASM-05; no admin data; state unchanged | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-036` | `AI` | FR-10; FR-12; SEC-02/03; API §6.2 | Security, auth | P0 | No token; `O-P=pending` | Admin API target `confirmed`, no Authorization | `401`; generic error; no mutation | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-037` | `AI` | FR-10; FR-12; SEC-02/03; API §6.2 | Security, auth | P0 | Invalid/expired token; `O-P=pending` | Admin API target `confirmed` with invalid bearer | `401`; generic error; no mutation | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-038` | `AI` | FR-10; FR-18; API §6.2 | EP, resource ID | P1 | `ADM-A`; ID `999999999` absent | Admin API target `confirmed` | `404` per ASM-04; JSON error; no order or sentinel changes | Preserve seed; verify absent ID |  |  |  | `NOT RUN` |
| `FR10-AI-039` | `AI` | FR-10; FR-18; API §6.2 | EP, resource ID | P1 | `ADM-A`; malformed ID `abc` | `PUT /api/admin/orders/abc/status`; target `confirmed` | `400` per ASM-04; JSON error; no mutation | Verify all fixtures unchanged |  |  |  | `NOT RUN` |
| `FR10-AI-040` | `AI` | FR-10; API §4.6 | EP, resource ID | P1 | `USR-A`; ID `999999999` absent | `PUT /api/orders/999999999/cancel` | `404` per ASM-04; generic error consistent with ownership policy; no mutation | Preserve seed |  |  |  | `NOT RUN` |
| `FR10-AI-041` | `AI` | FR-10; FR-18; API §6.2 | EP, required field | P0 | `ADM-A`; `O-P=pending` | Admin API with body `{}` | `400` per ASM-04; validation error names no sensitive data; state unchanged | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-042` | `AI` | FR-10; FR-18; API §6.2 | EP, null | P1 | `ADM-A`; `O-P=pending` | Admin API body `{"status":null}` | `400`; schema/validation error; no mutation | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-043` | `AI` | FR-10; FR-18; API §6.2 | EP, enum | P0 | `ADM-A`; `O-P=pending` | Admin API body `{"status":"refunded"}` | `400`; allowed-domain validation error; no mutation | Restore snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-044` | `AI` | FR-10; ASM-FR10-06 | Concurrency, atomicity | P0 | `ADM-A` and owning `USR-A`; one `O-P=pending` | Synchronize admin `pending→confirmed` and user cancel requests | Responses/state match a legal serial order per ASM-06: cancel-first gives one commit; confirm-first may give two legal commits; final `canceled`, no lost/hybrid/duplicate mutation, sentinel unchanged | Dedicated order, barrier, DB snapshot restore |  |  |  | `NOT RUN` |
| `FR10-AI-045` | `AI` | FR-10; FR-18; API §6.2 | Replay, idempotency | P1 | `ADM-A`; `O-S=shipping` | Send identical `shipping→delivered` request twice sequentially | First `200`; second `409` per ASM-02/03; final `delivered`; only one transition side effect/version increment | Dedicated order; restore snapshot |  |  |  | `NOT RUN` |
| `FR10-AI-046` | `AI` | FR-10; SEC-05; API §6.2 | Security, injection | P0 | `ADM-A`; sentinel fixtures recorded | `PUT /api/admin/orders/1%20OR%201=1/status`; target `confirmed` | `400` per ASM-04; generic error; no order changes and no multi-row update; behavioral probe does not prove parameterization | Restore/compare all fixture snapshots |  |  |  | `NOT RUN` |
| `FR10-AI-047` | `AI` | FR-10; SEC-05; API §6.2 | Security, injection | P0 | `ADM-A`; `O-P=pending` | Admin API body `{"status":"confirmed' OR '1'='1"}` | `400` per ASM-04; no SQL/internal detail; no state or multi-row mutation; behavioral probe only | Restore/compare target and sentinel |  |  |  | `NOT RUN` |

## 7. Human-added cases

The student explicitly supplied these five extensions. AI refinement only made the requests and oracles deterministic, corrected requirement traces, and removed unsupported bug conclusions; authorship remains `HUMAN`.

| TC ID | Source | Req | Technique | Priority | Preconditions | Request/data | Expected status/body/post-state | Setup/cleanup | Why AI missed | Execution/evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FR10-H-001` | `HUMAN` | FR-10; FR-18; API §6.2; ASM-FR10-09 | Protocol, method tampering | P1 | `ADM-A`; `O-P=pending`; target/sentinel snapshots recorded | Send `PATCH /api/admin/orders/O-P/status` with required headers and `{"status":"confirmed"}`; do not combine it with a separate GET scenario | `405` per ASM-09; JSON/non-sensitive protocol error; `O-P` remains `pending`, sentinel unchanged | Restore `O-P/O-U` snapshots | The original AI set followed the specified `PUT` verb and modeled state/actor combinations, but did not add an unsupported-method partition. The omission came from protocol behavior not being requested in the initial coverage model. | `NOT RUN` |
| `FR10-H-002` | `HUMAN` | FR-10; FR-18; API §6.2; ASM-FR10-07 | EP, near-valid enum | P0 | `ADM-A`; reset `O-P=pending` before each data row | Run the admin API once with `{"status":"CONFIRMED"}` and once with `{"status":" confirmed "}`; exact literals are two data rows of one strict-enum scenario | Each request returns `400` per ASM-07; validation error contains no internal detail; persisted status remains exactly `pending`, sentinel unchanged | Restore snapshots between both data rows | `FR10-AI-043` covered a clearly out-of-domain value (`refunded`) but not near-valid lexical variants. The initial EP model omitted case and outer-whitespace partitions because normalization behavior is absent from the spec. | `NOT RUN` |
| `FR10-H-003` | `HUMAN` | FR-10; FR-18; API §6.2; ASM-FR10-08 | Robustness, JSON parameter pollution | P0 | `ADM-A`; `O-P=pending`; raw body sending must preserve duplicate names | Send raw JSON bytes `{"status":"canceled","status":"confirmed"}` to the admin API with JSON content type | `400` per ASM-08 before transition logic; generic validation error; no transition/audit event and target/sentinel unchanged | Use a client that preserves duplicate keys; restore snapshots | The AI matrix represented `status` as one scalar target, so it did not model malformed serialization with duplicate object names. This is a parser-layer partition outside the original current×target decision table. | `NOT RUN` |
| `FR10-H-004` | `HUMAN` | FR-10; FR-18; API §6.2; ASM-FR10-03/06 | Concurrency, admin-vs-admin race | P0 | Two authenticated admin sessions; one dedicated `O-CF=confirmed`; synchronized barrier available | Concurrently send `confirmed→shipping` and `confirmed→canceled` for the same order | Exactly one request returns `200` and the other `409` under ASM-03/06; final state is the winner's `shipping` or `canceled`; responses match that serial order, with no lost/hybrid/duplicate transition and sentinel unchanged | Dedicated order, barrier and deterministic DB snapshot restore | `FR10-AI-044` tested admin-confirm versus user-cancel from `pending`; it did not generalize concurrency to two mutually exclusive admin transitions sharing the same source state. This human case closes that combinatorial gap. | `NOT RUN` |
| `FR10-H-005` | `HUMAN` | FR-10; FR-18; API §6.2; ASM-FR10-02; FR-04 context | Security, nested-data leakage, schema | P1 | `ADM-A`; `O-P=pending` belongs to `USR-A`, whose fixture has email, phone, shipping address, password hash and reset/auth metadata | Send valid `pending→confirmed`; inspect the complete response recursively, including any nested `user/customer` object | `200` per ASM-02; body identifies `O-P` with `status=confirmed`; no password/password hash, reset token, auth token or internal credential metadata; under the minimal-schema assumption, no full nested profile object; only `O-P` changes | Restore `O-P/O-U` and `USR-A` fixture snapshots | The AI cases already forbade sensitive fields generically, so this is not a wholly missed security dimension. The human contribution makes the probe concrete by seeding a related user with sensitive values and checking nested ORM serialization across FR-04/FR-10. `SEC-01/SEC-04` were removed because password storage and UI escaping are not the direct API oracle here. | `NOT RUN` |

## 8. Coverage matrix

| Modeled item | TC IDs | Status/gap |
| :--- | :--- | :--- |
| All 25 admin current × target cells | `FR10-AI-001`–`025` | Covered; HTTP oracle awaits ASM-02/03 confirmation |
| All 5 owner-cancel current states | `FR10-AI-026`–`030` | Covered; cancellation wording conflict is ASM-01 |
| Ownership/IDOR | `FR10-AI-031`, `032` | Covered under working ownership assumption ASM-05 |
| Missing/invalid authentication | `FR10-AI-033`, `034`, `036`, `037` | Covered for both API families |
| Admin role enforcement | `FR10-AI-035` | Covered |
| Existing/nonexistent/malformed resource IDs | Existing: `001`–`037`, `041`–`047`; absent/malformed: `038`–`040`, `046` | Covered representative EP; numeric max is unspecified |
| Required status and enum partitions | `FR10-AI-041`–`043`, `047` | Missing, null, outside enum, injection string covered |
| Rejected transition state integrity | `001`, `003`, `004`, `006`, `007`, `009`, `011`–`013`, `015`–`025`, `028`–`043`, `046`, `047` | Covered with target and sentinel assertions |
| Replay and competing transitions | `FR10-AI-044`, `045` | Designed; requires deterministic concurrency/reset harness |
| Success/error schema and sensitive-field exclusion | Success: `002`, `005`, `008`, `010`, `014`, `026`, `027`, `045`; errors: all rejection cases | Covered as contract assumptions ASM-02–05 |
| SEC-02 / SEC-03 / IDOR | `FR10-AI-031`–`037` | Covered by API behavior |
| SEC-05 behavioral injection | `FR10-AI-046`, `047` | Covered behaviorally; code review is needed to prove parameterized queries |
| SEC-01 | None | Not applicable: no password storage/response is in FR-10; sensitive-field absence is still asserted |
| SEC-04 | None | API responses can be inspected, but safe UI rendering requires UI evidence outside this API design |
| SEC-06 / SEC-07 | None | No upload/rate-limit contract is present for these order-transition endpoints |
| `X-Student-Id` | All cases | Included in design; screenshot/runtime evidence remains pending and is not fabricated |
| Unsupported HTTP method | `FR10-H-001` | Human extension; exact router status depends on ASM-09 |
| Near-valid enum formatting | `FR10-H-002` | Human extension; strictness depends on ASM-07 |
| Duplicate JSON keys | `FR10-H-003` | Human extension; strict rejection depends on ASM-08 |
| Admin-vs-admin race | `FR10-H-004` | Human extension; deterministic concurrency harness still required |
| Fixture-backed nested leakage | `FR10-H-005` | Human extension strengthening the generic schema/sensitive-field assertion |

## 9. Postman implementation mapping

| Scope | Collection mapping | Iteration-data mapping | Status/limitation |
| :--- | :--- | :--- | :--- |
| All 52 TC IDs | Folder `FR-10 Order State Machine` → request `FR-10 Mutation Router (Data-Driven)` | One row per TC in `FR10_data.csv`; scripts read `tcId`, method, path, body, auth and oracle via `pm.iterationData.get()` | Structurally implemented; assumptions `ASM-FR10-01`–`09` still require review |
| Persisted state/no side effect | Request `FR-10 Persisted State Verification (Data-Driven)` | `verifyOrderId` + `expectedState` | Requires admin list response to expose an order array and deterministic fixture reset |
| Replay/near-valid second request | `FR10-AI-045`, `FR10-H-002` in Mutation Router | `secondaryBody` + `secondaryExpectedStatus` | Executed through an explicit `pm.sendRequest` callback; not yet run |
| Concurrency | `FR10-AI-044`, `FR10-H-004` in Mutation Router | `racePath1/2`, bodies, auth modes and allowed status pairs | Two asynchronous `pm.sendRequest` calls; reliable race timing still depends on runner/SUT and a barrier-capable fixture |
| Secrets/fixtures | Empty collection variables `fr10AdminToken`, `fr10UserAToken`, `fr10UserBToken`, five state-specific order IDs and a sentinel | Runtime values must be supplied locally | No token/current secret value is committed |

The implementation is a runnable mapping scaffold, not execution evidence. Before Newman, the student must provide tokens/fixture IDs, restore each named state before every CSV iteration, confirm unresolved HTTP/schema assumptions and capture real `X-Student-Id` evidence.

## 10. Quality-gate result

- Structural count: 47 unique AI IDs plus 5 unique HUMAN IDs; all 52 rows have `Execution/evidence=NOT RUN`.
- Full state closure: 25/25 admin matrix cells and 5/5 owner-cancel states are mapped.
- No audit label, correction, execution result, bug, screenshot, URL or commit SHA was invented.
- Remaining gaps: nine contract decisions (`ASM-FR10-01`–`09`), deterministic fixture/reset implementation, runtime environment values, reliable duplicate-key/race transport, real execution evidence and human audit of the 47 AI candidates.

**Generation status: COMPLETE.** The ≥35 AI-candidate target is met with 47 semantically distinct scenarios. This does not mean the human-audit, implementation or execution stages are complete.
