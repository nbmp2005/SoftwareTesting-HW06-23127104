# FR-15 – Product CRUD Test Design

## 1. Source, contract and lifecycle

| Item | Value |
| :--- | :--- |
| Sources | `docs/hw6.md` §6; `docs/api_specification.md` §3.1–§3.3; repository FR-15 rule set |
| API source SHA-256 | `488CBCB790099BA9CBB34C7C80BA04C6AEC9E9EBB598F031FFA575737547B139` |
| Endpoints | `GET /api/products`; `GET /api/products/:id`; admin-only `POST /api/products`, `PUT /api/products/:id`, `DELETE /api/products/:id` |
| Fields/rules | `name` required/≤255; numeric `price>0`; existing required `category_id`; optional `description`, `imageUrl`; updates must not affect other products |
| Generated set | 50 unique AI candidates (`FR15-AI-001`–`FR15-AI-050`) |
| Lifecycle | Raw AI output awaiting student audit; audit fields blank; all cases `NOT RUN` |

All requests include `X-Student-Id: 23127104`. Mutations also use JSON content type and a named runtime bearer token; no real credential is stored.

## 2. Ambiguities and working assumptions

| ID | Ambiguity | Working assumption | Decision required |
| :--- | :--- | :--- | :--- |
| `ASM-FR15-01` | Local API spec gives an example body but omits the FR-15 constraints. | Apply repository rules: name required/≤255, numeric price >0, category required/existing. | Confirm against tested SUT commit. |
| `ASM-FR15-02` | Success status/schema omitted. | GET/PUT/DELETE → `200`; POST → `201`; product JSON has numeric `id/price/category_id`, string `name`, optional string/null description/image. | Confirm exact status/schema. |
| `ASM-FR15-03` | Validation/not-found contract omitted. | Invalid body/path → `400`; absent product/category → `404`; JSON error; no mutation. | Confirm framework contract. |
| `ASM-FR15-04` | Auth error contract omitted. | Missing/invalid token → `401`; valid non-admin → `403`; generic JSON error; no mutation. | Confirm middleware behavior. |
| `ASM-FR15-05` | PUT partial/full semantics omitted. | PUT is partial; omitted fields retain existing values. | Confirm update semantics. |
| `ASM-FR15-06` | Optional-field nullability/type/URL rules omitted. | Omitted/null allowed; present description/image must be strings; URL syntax is not validated. | Confirm optional-field rules. |
| `ASM-FR15-07` | Read auth and list/search envelope omitted. | Reads are public; list/search returns an array or documented product-array envelope. | Confirm access/envelope. |
| `ASM-FR15-08` | Unknown properties and concurrency policy omitted. | Reject privileged/unknown fields with `400`; concurrent partial updates serialize, both return `200`, and the final product contains both non-conflicting changes without a lost update. | Confirm allow-list/locking. |

Candidates depending on these assumptions are not final executable until human audit confirms or corrects their oracle.

## 3. Coverage model and fixtures

| Field/area | Partitions and boundaries | TC IDs |
| :--- | :--- | :--- |
| CRUD/read/search | valid create/minimal; list/detail/search; partial/full update; delete/absent/replay | `001`–`016` |
| `name` | missing/null/empty/whitespace; 1/254/255/256 chars; Unicode | `017`–`025` |
| `price` | missing/null/negative/zero; `0.01`; decimal; numeric string | `026`–`032` |
| `category_id` | missing/null; existing 10/11; absent 999999999; string type | `001`, `002`, `011`, `033`–`036` |
| Optional fields | omitted/string/null/empty; object wrong type | `001`, `002`, `012`, `037`, `038` |
| Auth/role | missing, invalid, non-admin across create/update/delete | `039`–`045` |
| Security/isolation | SQLi path/body; stored XSS API probe; mass assignment; concurrent update | `046`–`050` |

- `ADM-A` and `USR-A` are fixture actors. `CAT-A=10`, `CAT-B=11` exist. `P-A` is the target; `P-B` is an unrelated sentinel.
- `N1="A"`, `N254="A"*254`, `N255="A"*255`, `N256="A"*256` are deterministic named strings.
- Restore snapshots before each case. Track/delete created IDs; restore updated/deleted fixtures and compare `P-B`.

## 4. AI-generated candidate cases

| TC ID | Source | Req | Technique | Priority | Preconditions | Request/data | Expected status/body/post-state | Cleanup | Audit label | Audit reason | Correction/final ID | Execution/evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FR15-AI-001` | `AI` | FR-15; FR-12; API §3.3 | CRUD, happy path | P0 | `ADM-A`; `CAT-A` exists | POST products with `{"name":"HW06-P-001","price":100000,"description":"Mô tả","imageUrl":"https://example.test/p.png","category_id":10}` | `201` per ASM-02; exact values/schema/new id; one row created; `P-B` unchanged | Delete returned ID |  |  |  | `NOT RUN` |
| `FR15-AI-002` | `AI` | FR-15; API §3.3 | CRUD, minimal | P1 | `ADM-A`; `CAT-A` | POST `{"name":"M","price":0.01,"category_id":10}` | `201`; optional fields absent/null; exact persistence | Delete returned ID |  |  |  | `NOT RUN` |
| `FR15-AI-003` | `AI` | FR-15; API §3.1 | CRUD, schema | P0 | `P-A/P-B` exist | GET product list without bearer | `200` per ASM-07; array/envelope; item types valid; no credential fields; no mutation | None |  |  |  | `NOT RUN` |
| `FR15-AI-004` | `AI` | FR-15; API §3.2 | CRUD, schema | P0 | `P-A` exists | GET product `P-A` | `200`; exact id/name/price/category, valid schema, no sensitive fields | None |  |  |  | `NOT RUN` |
| `FR15-AI-005` | `AI` | FR-15; API §3.1 | EP, search | P1 | Unique `HW06-Needle-005` exists | GET `?search=HW06-Needle-005` | `200`; includes fixture; every result matches name-search semantics; no mutation | Delete fixture |  |  |  | `NOT RUN` |
| `FR15-AI-006` | `AI` | FR-15; API §3.1 | EP, search | P2 | No matching name | GET `?search=HW06-NO-MATCH-006` | `200`; empty product collection; no mutation | None |  |  |  | `NOT RUN` |
| `FR15-AI-007` | `AI` | FR-15; API §3.2 | EP, ID | P1 | ID absent | GET product `999999999` | `404` per ASM-03; generic JSON error; unchanged repository | None |  |  |  | `NOT RUN` |
| `FR15-AI-008` | `AI` | FR-15; API §3.2 | EP, ID | P1 | Snapshots recorded | GET product `abc` | `400`; no internal detail or mutation | None |  |  |  | `NOT RUN` |
| `FR15-AI-009` | `AI` | FR-15; API §3.3 | CRUD, partial, isolation | P0 | `P-A/P-B` snapshotted | PUT `P-A` `{"name":"HW06-Renamed-009"}` | `200` per ASM-05; only name changes; omitted fields and `P-B` unchanged | Restore `P-A` |  |  |  | `NOT RUN` |
| `FR15-AI-010` | `AI` | FR-15; API §3.3 | CRUD, partial, isolation | P0 | Same | PUT `P-A` `{"price":125000.5}` | `200`; exact numeric price only; sentinel unchanged | Restore `P-A` |  |  |  | `NOT RUN` |
| `FR15-AI-011` | `AI` | FR-15; API §3.3 | CRUD, dependency | P0 | `CAT-B=11` exists | PUT `P-A` `{"category_id":11}` | `200`; category changes only; sentinel unchanged | Restore `P-A` |  |  |  | `NOT RUN` |
| `FR15-AI-012` | `AI` | FR-15; API §3.3 | CRUD, optional fields | P1 | `P-A/P-B` | PUT `P-A` `{"description":null,"imageUrl":""}` | `200` per ASM-06; exact null/empty values persist; required fields and sentinel unchanged | Restore `P-A` |  |  |  | `NOT RUN` |
| `FR15-AI-013` | `AI` | FR-15; API §3.3 | CRUD, full update | P0 | `CAT-B` exists | PUT all fields: `HW06-Full-013`, price 99000, `D13`, HTTPS image, category 11 | `200`; all values persisted; one target only; sentinel unchanged | Restore `P-A` |  |  |  | `NOT RUN` |
| `FR15-AI-014` | `AI` | FR-15; API §3.2/3.3 | CRUD, lifecycle | P0 | Disposable `P-D` | DELETE `P-D`, then GET it | DELETE `200`; subsequent GET `404`; only target removed | Recreate fixture |  |  |  | `NOT RUN` |
| `FR15-AI-015` | `AI` | FR-15; API §3.3 | CRUD, absent delete | P1 | ID absent | DELETE `999999999` | `404`; product count/sentinel unchanged | None |  |  |  | `NOT RUN` |
| `FR15-AI-016` | `AI` | FR-15; API §3.3 | CRUD, replay delete | P1 | Disposable `P-D` | DELETE same ID twice | First `200`, second `404`; one deletion only; sentinel unchanged | Recreate fixture |  |  |  | `NOT RUN` |
| `FR15-AI-017` | `AI` | FR-15; API §3.3 | EP, required name | P0 | Baseline count | POST without name; price 100, category 10 | `400`; no creation | None |  |  |  | `NOT RUN` |
| `FR15-AI-018` | `AI` | FR-15; API §3.3 | EP, null name | P0 | Same | POST `name:null` | `400`; no creation | None |  |  |  | `NOT RUN` |
| `FR15-AI-019` | `AI` | FR-15; API §3.3 | EP, empty name | P0 | Same | POST `name:""` | `400`; no creation | None |  |  |  | `NOT RUN` |
| `FR15-AI-020` | `AI` | FR-15; API §3.3 | EP, whitespace | P1 | Same | POST `name:"   "` | `400`; whitespace not persisted; no creation | None |  |  |  | `NOT RUN` |
| `FR15-AI-021` | `AI` | FR-15; API §3.3 | BVA, min name | P2 | `ADM-A`; `CAT-A` | POST `name:N1` | `201`; one-character name exact | Delete created |  |  |  | `NOT RUN` |
| `FR15-AI-022` | `AI` | FR-15; API §3.3 | BVA, 254 | P2 | Same | POST `name:N254` | `201`; stored length 254 contract units | Delete created |  |  |  | `NOT RUN` |
| `FR15-AI-023` | `AI` | FR-15; API §3.3 | BVA, max | P0 | Same | POST `name:N255` | `201`; stored length 255 | Delete created |  |  |  | `NOT RUN` |
| `FR15-AI-024` | `AI` | FR-15; API §3.3 | BVA, max+1 | P0 | Baseline count | POST `name:N256` | `400`; no truncation or creation | None |  |  |  | `NOT RUN` |
| `FR15-AI-025` | `AI` | FR-15; API §3.3 | EP, Unicode | P1 | `ADM-A`; `CAT-A` | POST name `Cà phê ☕ 商品` | `201`; Unicode round-trips and JSON remains valid | Delete created |  |  |  | `NOT RUN` |
| `FR15-AI-026` | `AI` | FR-15; API §3.3 | EP, required price | P0 | Baseline count | POST without price | `400`; no creation | None |  |  |  | `NOT RUN` |
| `FR15-AI-027` | `AI` | FR-15; API §3.3 | EP, null price | P0 | Same | POST `price:null` | `400`; no creation | None |  |  |  | `NOT RUN` |
| `FR15-AI-028` | `AI` | FR-15; API §3.3 | EP, negative price | P0 | Same | POST `price:-1` | `400`; no negative persistence | None |  |  |  | `NOT RUN` |
| `FR15-AI-029` | `AI` | FR-15; API §3.3 | BVA, zero | P0 | Same | POST `price:0` | `400`; no creation | None |  |  |  | `NOT RUN` |
| `FR15-AI-030` | `AI` | FR-15; API §3.3 | BVA, positive | P0 | `ADM-A`; `CAT-A` | POST `price:0.01` | `201`; positive numeric price equals 0.01 | Delete created |  |  |  | `NOT RUN` |
| `FR15-AI-031` | `AI` | FR-15; API §3.3 | EP, decimal | P1 | Same | POST `price:99.99` | `201`; decimal remains numeric/exact per precision contract | Delete created |  |  |  | `NOT RUN` |
| `FR15-AI-032` | `AI` | FR-15; API §3.3 | EP, wrong type | P0 | Baseline count | POST `price:"100"` | `400`; no coercion or creation | None |  |  |  | `NOT RUN` |
| `FR15-AI-033` | `AI` | FR-15; API §3.3 | EP, required category | P0 | Baseline count | POST omitting category | `400`; no creation | None |  |  |  | `NOT RUN` |
| `FR15-AI-034` | `AI` | FR-15; API §3.3 | EP, null category | P0 | Same | POST `category_id:null` | `400`; no creation | None |  |  |  | `NOT RUN` |
| `FR15-AI-035` | `AI` | FR-15; API §3.3 | EP, referential integrity | P0 | Category absent | POST `category_id:999999999` | `404`; no orphan product | None |  |  |  | `NOT RUN` |
| `FR15-AI-036` | `AI` | FR-15; API §3.3 | EP, wrong type | P1 | `CAT-A=10` | POST `category_id:"10"` | `400`; no coercion or creation | None |  |  |  | `NOT RUN` |
| `FR15-AI-037` | `AI` | FR-15; API §3.3 | EP, optional wrong type | P1 | `P-A/P-B` | PUT description object `{"text":"bad"}` | `400` per ASM-06; target/sentinel unchanged | None |  |  |  | `NOT RUN` |
| `FR15-AI-038` | `AI` | FR-15; API §3.3 | EP, optional wrong type | P1 | Same | PUT imageUrl object `{"href":"https://example.test"}` | `400`; target/sentinel unchanged | None |  |  |  | `NOT RUN` |
| `FR15-AI-039` | `AI` | FR-15; FR-12; SEC-02 | Security, auth | P0 | No token | POST valid body without Authorization | `401` per ASM-04; no creation/data leak | None |  |  |  | `NOT RUN` |
| `FR15-AI-040` | `AI` | FR-15; FR-12; SEC-03 | Security, role | P0 | `USR-A` non-admin | POST valid body with user token | `403`; no creation | None |  |  |  | `NOT RUN` |
| `FR15-AI-041` | `AI` | FR-15; FR-12; SEC-02 | Security, auth | P0 | `P-A/P-B`; no token | PUT `P-A` `{"price":1}` | `401`; both unchanged | None |  |  |  | `NOT RUN` |
| `FR15-AI-042` | `AI` | FR-15; FR-12; SEC-03 | Security, role | P0 | `USR-A`; `P-A/P-B` | PUT `P-A` `{"price":1}` | `403`; both unchanged | None |  |  |  | `NOT RUN` |
| `FR15-AI-043` | `AI` | FR-15; FR-12; SEC-02 | Security, auth | P0 | Disposable product; no token | DELETE target | `401`; product remains retrievable; sentinel unchanged | Remove fixture |  |  |  | `NOT RUN` |
| `FR15-AI-044` | `AI` | FR-15; FR-12; SEC-03 | Security, role | P0 | `USR-A`; disposable product | DELETE with user token | `403`; target remains; no side effect | Remove fixture |  |  |  | `NOT RUN` |
| `FR15-AI-045` | `AI` | FR-15; FR-12; SEC-02 | Security, invalid auth | P0 | `P-A/P-B` | PUT with `Bearer invalid.fixture.token` | `401`; target/sentinel unchanged | None |  |  |  | `NOT RUN` |
| `FR15-AI-046` | `AI` | FR-15; SEC-05; API §3.2 | Security, injection | P0 | Snapshots/count | GET product path `1%20OR%201=1` | `400`; no SQL/internal detail, multi-row disclosure or mutation; behavioral only | None |  |  |  | `NOT RUN` |
| `FR15-AI-047` | `AI` | FR-15; SEC-05; API §3.3 | Security, injection | P0 | `ADM-A`; baseline | POST name `x'); DROP TABLE products;--` with valid other fields | `201` under string-domain rule; exact literal stored; never SQL execution/internal error; other products remain readable | Delete created row |  |  |  | `NOT RUN` |
| `FR15-AI-048` | `AI` | FR-15; SEC-04; API §3.1/3.3 | Security, stored XSS | P0 | `ADM-A`; `CAT-A` | POST name `<img src=x onerror=alert(1)>`, then GET it | API returns inert JSON string without server execution/error; UI-safe rendering needs separate evidence | Delete created |  |  |  | `NOT RUN` |
| `FR15-AI-049` | `AI` | FR-15; FR-12; API §3.3 | Security, mass assignment | P0 | `ADM-A`; baseline | POST valid fields plus `id:777`, `role:"admin"`, `isAdmin:true`, forged `created_at` | `400` per ASM-08; no chosen ID/privilege/internal metadata or creation | Inspect/remove only if violation observed |  |  |  | `NOT RUN` |
| `FR15-AI-050` | `AI` | FR-15; ASM-FR15-05/08 | Concurrency, isolation | P0 | Dedicated `P-A`; `P-B`; synchronized admins | Concurrent PUTs: `{"name":"Race-A"}` and `{"price":222}` | Both `200`; final `P-A` has name `Race-A` and price `222` with other fields retained; no lost update; `P-B` unchanged | Barrier and snapshot restore |  |  |  | `NOT RUN` |

## 5. Human-added cases

No student-authored FR-15 extension has been supplied. At least five HUMAN cases with genuine “Why AI missed” analysis remain required.

| TC ID | Source | Req | Technique | Priority | Preconditions | Request/data | Expected status/body/post-state | Cleanup | Why AI missed | Execution/evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |

## 6. Coverage closure

| Modeled item | TC IDs | Status/gap |
| :--- | :--- | :--- |
| CRUD lifecycle/read/search | `001`–`016` | Covered; status/schema assumptions pending |
| All request fields and boundaries | `017`–`038` plus `001`, `002`, `009`–`013` | Covered; precision, URL and PUT semantics pending |
| Authentication/authorization | `039`–`045` | Covered across create/update/delete |
| SEC-04/05 and mass assignment | `046`–`049` | API behavioral coverage; UI/code evidence still needed |
| Isolation/concurrency | `009`–`013`, `037`, `038`, `041`–`045`, `050` | Sentinel assertions covered; race harness pending |
| Success/error schemas and credential exclusion | All cases | Covered under ASM-02–04 |
| SEC-01, SEC-06, SEC-07 | None | Not applicable: no password storage, upload or rate-limit rule in this feature |
| `X-Student-Id` | All cases | Designed; real console/request evidence pending |

## 7. Quality-gate result

- 50 unique AI IDs; all `Source=AI`; 13 columns; blank audit triplets; `Execution/evidence=NOT RUN`; no HUMAN rows.
- CRUD, every request field, BVA/EP, auth/role, schemas, isolation and applicable security are traceable without semantic padding.
- No execution result, bug, screenshot, link, SHA or credential was fabricated.
- Gaps: `ASM-FR15-01`–`08`, human audit, five human extensions, Postman/fixture/concurrency implementation and real run evidence.

**Generation status: COMPLETE.** The ≥35 target is met with 50 semantically distinct AI candidates; audit/implementation/execution are not claimed complete.
