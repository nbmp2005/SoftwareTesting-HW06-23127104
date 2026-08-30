# FR-02 – Login & Account Lockout Test Design

## 1. Sources and contract snapshot

| Source | Version/evidence | FR-02 facts used |
| :--- | :--- | :--- |
| `docs/api_specification.md` | SHA-256 `488CBCB790099BA9CBB34C7C80BA04C6AEC9E9EBB598F031FFA575737547B139` | Base URL `http://localhost:3000`; `POST /api/login`; JSON fields `email`, `password`; success `200` with JWT `token` and `user` |
| `.agents/skills/eshop-api-test-generator/references/eshop-rules.md` | Workspace rule snapshot | Failed login increments exactly 1; lock from 3 consecutive failures for 30 seconds; generic/non-revealing errors; success resets failures |
| `docs/hw6.md` §6 | HW06-AI assignment | ≥35 AI cases/API; parameter partitions, security, schema; every executed request must carry `X-Student-Id` |

### 1.1 Contract inventory

| Item | Contract |
| :--- | :--- |
| Endpoint | `POST /api/login` |
| Default headers | `Content-Type: application/json`; `X-Student-Id: {{studentId}}` |
| Body | `{"email":"{{fr02EmailA}}","password":"{{fr02PasswordA}}"}` |
| Success | `200`; JSON contains `token` as a JWT string and `user` as an object |
| Failure/state rules | Each wrong credential attempt for an existing unlocked account increments exactly 1; third consecutive failure locks for 30 seconds; locked account cannot authenticate; successful login resets consecutive failures |
| Security | Error must not expose whether email/password caused failure; SQL input must not bypass authentication; response must not expose password/hash/reset/lock internals |
| Supporting verification | A returned token is sent as `Authorization: Bearer <token>` to `GET /api/users/me` |

### 1.2 Named fixtures and reset protocol

- `U-A`, `U-B`, `U-C`: isolated active users with known non-secret test credentials stored as Postman variables; default snapshot is `attempts=0`, `locked_until=NULL`.
- `WRONG-1`, `WRONG-2`, `WRONG-3`: distinct wrong strings that never equal a fixture password.
- Before and after every stateful case, restore the named user to its snapshot using the deterministic seed/reset procedure. The concrete command/path remains pending implementation and must be filled before execution.
- Timing cases measure from the recorded third-failure response time. Prefer a controllable clock/DB fixture; otherwise record actual timestamps and scheduling tolerance.
- All cases retain `X-Student-Id: {{studentId}}`. No negative case intentionally omits this mandatory assignment header.

### 1.3 Ambiguities and working assumptions

| ID | Missing/conflicting detail | Design treatment |
| :--- | :--- | :--- |
| `ASM-FR02-01` | Exact HTTP status for invalid credentials, validation failure and locked account is unspecified | Expect a non-2xx `4xx`; resolve exact code before final Postman oracle |
| `ASM-FR02-02` | Error response schema/message is unspecified | Require a generic non-sensitive failure with no `token`/authenticated `user`; exact fields/message pending |
| `ASM-FR02-03` | Backend email format/type validation is not explicit | Robustness candidates expect safe `4xx` rejection; student must confirm oracle against authoritative clarification |
| `ASM-FR02-04` | Counter behavior for malformed requests, unknown email and requests while already locked is unspecified | Do not assert a counter change for those cases; assert only no authentication/no leakage |
| `ASM-FR02-05` | Exact JWT claims and top-level extra success fields are unspecified | Validate JWT syntax, decodable header/payload, `token` and `user`; do not invent required claims or forbid unrelated fields |
| `ASM-FR02-06` | Exact 30-second scheduler boundary/tolerance is unspecified | Keep 29/30/31-second cases; exact `t=30` execution needs controlled clock or documented tolerance |
| `ASM-FR02-07` | Unsupported media-type/method status is unspecified | Expect safe `4xx`; exact `400/404/405/415` pending |

## 2. Coverage inventory

| Dimension | Partitions/boundaries | Planned TC IDs |
| :--- | :--- | :--- |
| Valid login/token/schema | Fresh login, JWT syntax/usability, success schema, sensitive-field exclusion | `FR02-AI-001`–`005` |
| Attempt counter/reset | `0→1`, `1→2`, `2→3`, reset after success/expiry, account isolation, concurrency | `FR02-AI-006`–`010`, `014`–`020` |
| Lock timing | Immediate, 29s, exactly 30s, 31s | `FR02-AI-008`–`013`, `019`–`020` |
| Email partitions | Missing/null/empty/whitespace; malformed strings; wrong JSON types; unknown account; SQLi | `FR02-AI-021`–`033`, `049`–`050` |
| Password partitions | Missing/null/empty/whitespace; wrong JSON types; long/Unicode/SQLi strings | `FR02-AI-027`–`044`, plus `006`–`020` |
| Protocol and error schema | Empty/malformed body, media type, method, enumeration parity | `FR02-AI-035`–`049` |
| Security requirements | SEC-02 token usability; SEC-05 behavioral injection; response leakage/enumeration | `FR02-AI-004`, `005`, `017`, `044`, `049`, `050` |

## 3. Decision table

| Rule | Account exists | Locked now | Password correct | Expected action |
| :--- | :---: | :---: | :---: | :--- |
| R1 | Y | N | Y | `200`; token + user; reset consecutive failures |
| R2 | Y | N | N | Generic `4xx`; increment exactly 1; lock when new count reaches 3 |
| R3 | Y | Y | Y/N | Generic `4xx`; no token; remain locked until duration expires |
| R4 | N | N/A | Y/N | Generic `4xx`; no account-existence disclosure |
| R5 | Invalid request shape | N/A | N/A | Safe `4xx`; no token/session; no server error |

## 4. AI-generated candidate cases

Audit columns are intentionally blank for student review. All results remain `NOT RUN`.

| TC ID | Source | Req | Technique | Priority | Preconditions | Request/data | Expected status/body/post-state | Cleanup | Audit label | Audit reason | Correction/final ID | Execution/evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FR02-AI-001` | `AI` | FR-02; API 1.2 | EP, DT | P0 | `U-A` clean/unlocked | Default login with `{{fr02EmailA}}`, `{{fr02PasswordA}}` | `200`; JSON has non-empty `token` string and `user` object; authenticated; attempts reset to 0 | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-002` | `AI` | FR-02; API 1.2 | Schema | P0 | `U-A` clean/unlocked | Default valid login | `200`; body is JSON; `token` type string; `user` type object; no error payload per ASM-FR02-05 | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-003` | `AI` | FR-02; API 1.2 | Schema, Security | P1 | `U-A` clean/unlocked | Default valid login; decode returned token locally | Token has three dot-separated JWT segments; header/payload decode as JSON; do not require unspecified claims | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-004` | `AI` | FR-02; SEC-02; API 2.1 | Security, Integration | P0 | Complete valid login for `U-A` | Send returned token to `GET /api/users/me` as Bearer token with student header | Protected request authenticates as `U-A`; no other user's profile returned | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-005` | `AI` | FR-02; SEC-01 | Security, Schema | P0 | `U-A` clean/unlocked | Default valid login | `200`; response contains no `password`, password hash, reset token/OTP, failure counter or lock timestamp at any inspected user-object level | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-006` | `AI` | FR-02-R2 | DT, State | P0 | `U-A` attempts=0/unlocked | Login with `WRONG-1` | Generic `4xx` per ASM-01/02; no token; attempts `0→1`; not locked | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-007` | `AI` | FR-02-R2 | DT, State | P0 | `U-A` attempts=1/unlocked | Login with `WRONG-2` | Generic `4xx`; no token; attempts `1→2`; not locked | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-008` | `AI` | FR-02-R2,R3 | BVA, State | P0 | `U-A` attempts=2/unlocked | Login with `WRONG-3` | Generic `4xx`; attempts `2→3`; account becomes locked for 30 seconds; no token | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-009` | `AI` | FR-02-R3,R4 | State, DT | P0 | Lock `U-A` by three consecutive failures | Immediately login with correct password | Generic `4xx`; no token/user authentication; remains locked | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-010` | `AI` | FR-02-R3,R4 | State, DT | P1 | `U-A` currently locked | Immediately login with another wrong password | Generic `4xx`; no token; remains locked; counter change not asserted per ASM-FR02-04 | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-011` | `AI` | FR-02-R4 | BVA, State | P0 | `U-A` locked at recorded `t0` | Correct login at `t0+29s` | Generic `4xx`; no token; still locked | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-012` | `AI` | FR-02-R4 | BVA, State | P0 | Controlled clock; `U-A` locked at `t0` | Correct login at exactly `t0+30s` | Lock has expired and login succeeds `200`; token/user returned; attempts reset; execution tolerance follows ASM-FR02-06 | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-013` | `AI` | FR-02-R4 | BVA, State | P0 | `U-A` locked at recorded `t0` | Correct login at `t0+31s` | `200`; token/user returned; unlocked; attempts reset to 0 | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-014` | `AI` | FR-02-R1,R2 | State, Sequence | P0 | `U-A` clean | Wrong once → correct → wrong twice → correct | First success resets counter; two later failures do not lock; final correct login succeeds; each wrong increments exactly 1 | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-015` | `AI` | FR-02-R1,R2 | State, Sequence | P0 | `U-A` clean | Wrong twice → correct → wrong once | Success after two failures resets; later wrong attempt is new count 1 and account is not locked | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-016` | `AI` | FR-02-R2,R3 | State, Isolation | P0 | `U-A` and `U-B` clean | Lock `U-A`; login correctly as `U-B` | `U-A` locked; `U-B` succeeds `200`; counters/lock state are account-isolated | Restore both snapshots |  |  |  | `NOT RUN` |
| `FR02-AI-017` | `AI` | FR-02-R4 | Security, Isolation | P1 | `U-A` clean; unknown email fixture exists in no account | Submit same unknown email with three wrong passwords; then valid login `U-A` | Unknown requests return generic failures; no existence leak; `U-A` remains unaffected and succeeds | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-018` | `AI` | FR-02-R2 | Concurrency, State | P1 | `U-C` attempts=0; two synchronized clients | Send two wrong-password requests concurrently | Both fail without token; each failure contributes exactly 1; final attempts=2; account not yet locked | Restore `U-C` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-019` | `AI` | FR-02-R2,R3 | Concurrency, BVA | P0 | `U-C` attempts=1; two synchronized clients | Send two wrong-password requests concurrently | Both fail; final attempts=3; account locked; no lost update permits a subsequent immediate correct login | Restore `U-C` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-020` | `AI` | FR-02-R1,R4 | State, Sequence | P0 | `U-A` locked; wait/control to `t0+31s` | Correct login after expiry, then one wrong login | Correct login succeeds and resets; following wrong is count 1, not immediate re-lock | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-021` | `AI` | API 1.2; HW06 partition | EP, Negative | P1 | `U-A` clean | Body contains password only; email omitted | Safe generic `4xx` per ASM-01/03; no token/session; no 5xx | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-022` | `AI` | API 1.2; HW06 partition | EP, Negative | P1 | `U-A` clean | `email:null`, correct password | Safe generic `4xx`; no token/session; no 5xx | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-023` | `AI` | API 1.2; HW06 partition | EP, Negative | P1 | `U-A` clean | `email:""`, correct password | Safe generic `4xx`; no token/session | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-024` | `AI` | FR-02 email; HW06 partition | EP, Negative | P1 | `U-A` clean | `email:"user.example.com"`, correct password | Safe generic `4xx` under ASM-FR02-03; no token/session | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-025` | `AI` | FR-02-R4 | EP, Security | P0 | Unknown syntactically valid email | Login unknown email with `WRONG-1` | Generic `4xx`; no token; response does not reveal account absence | No account state to clean |  |  |  | `NOT RUN` |
| `FR02-AI-026` | `AI` | API 1.2 | Type partition | P1 | `U-A` clean | `email:{"value":"{{fr02EmailA}}"}`, correct password | Safe `4xx`; object is not accepted as email; no 5xx/token | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-027` | `AI` | API 1.2 | EP, Negative | P1 | `U-A` clean | Body contains email only; password omitted | Safe generic `4xx`; no token/session; no 5xx | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-028` | `AI` | API 1.2 | EP, Negative | P1 | `U-A` clean | Registered email; `password:null` | Safe generic `4xx`; no token/session; counter side effect pending ASM-FR02-04 | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-029` | `AI` | API 1.2; FR-02-R2 | EP, Negative | P1 | `U-A` clean | Registered email; `password:""` | Generic `4xx`; no token; if treated as credential failure, counter increments exactly 1 | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-030` | `AI` | API 1.2; FR-02-R2 | EP, Negative | P1 | `U-A` clean | Registered email; `password:"   "` | Generic `4xx`; no token; if treated as credential failure, counter increments exactly 1 | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-031` | `AI` | API 1.2 | Type partition | P1 | `U-A` clean | Registered email; `password:{"value":"WRONG-1"}` | Safe `4xx`; object rejected; no token/session | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-032` | `AI` | FR-02-R2 | Robustness, Boundary | P1 | `U-A` clean | Registered email; wrong password of 10,000 `A` characters | Generic `4xx`; bounded handling/no 5xx; no token; one credential failure at most | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-033` | `AI` | FR-02-R2 | Unicode, EP | P1 | `U-A` clean | Registered email; wrong Unicode password `SaiMậtKhẩu🔒1!` | Generic `4xx`; no encoding crash/token; one credential failure | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-034` | `AI` | SEC-05; FR-02-R2 | Security, Injection | P0 | `U-A` clean | Registered email; password `' OR '1'='1' --` | Generic `4xx`; no authentication/bypass/SQL error leakage; stored data unchanged | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-035` | `AI` | API 1.2 | Protocol, Negative | P1 | No state precondition | POST with `{}` and default headers | Safe generic `4xx`; no token/session; no 5xx | None |  |  |  | `NOT RUN` |
| `FR02-AI-036` | `AI` | API 1.2 | Protocol, Robustness | P1 | No state precondition | POST malformed JSON `{"email":` with JSON content type | Safe `4xx` under ASM-FR02-07; no stack trace/token/session | None |  |  |  | `NOT RUN` |
| `FR02-AI-037` | `AI` | API 1.2 | Protocol | P2 | `U-A` clean | POST valid JSON as `Content-Type:text/plain`; keep student header | Safe `4xx` under ASM-FR02-07; request not authenticated; exact media-type status pending | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-038` | `AI` | API 1.2 | Protocol, Method | P2 | No state precondition | `GET /api/login` with student header | Non-success `4xx` under ASM-FR02-07; no token/session; no state change | None |  |  |  | `NOT RUN` |
| `FR02-AI-039` | `AI` | FR-02-R4 | Security, Differential | P0 | `U-A` clean; unknown email available | Compare one wrong-password login for `U-A` with one login for unknown email | Both generic failures have equivalent status class/schema and no cause-specific/account-existence detail; no token | Restore `U-A` snapshot |  |  |  | `NOT RUN` |
| `FR02-AI-040` | `AI` | SEC-05; FR-02-R4 | Security, Injection | P0 | `U-A` clean | Email `' OR 1=1 --`; password arbitrary wrong string | Generic `4xx`; no authentication/SQL error/account dump; `U-A` state/data unchanged | Restore `U-A` snapshot |  |  |  | `NOT RUN` |

## 5. Human-added cases

The student must add at least five cases after auditing the AI candidates. No HUMAN case is pre-populated by the agent.

| TC ID | Source | Req | Technique | Priority | Preconditions | Request/data | Expected status/body/post-state | Cleanup | Why AI missed | Execution/evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |

## 6. Coverage closure

| Requirement/rule | Covered IDs | Gap/justification |
| :--- | :--- | :--- |
| Valid login `200`, token and user | `FR02-AI-001`–`005` | Exact JWT claims/top-level optional fields unspecified (`ASM-FR02-05`) |
| Wrong attempt increments exactly 1 | `FR02-AI-006`–`008`, `014`–`020`, `036`–`037`, `042`–`044` | Direct post-state needs fixture/DB probe; malformed-request counter behavior intentionally not assumed |
| Lock begins at third consecutive failure | `FR02-AI-008`–`010`, `016`, `019` | Complete at design level |
| Lock duration is 30 seconds | `FR02-AI-011`–`013`, `020` | Exact `t=30` needs controlled clock/tolerance resolution (`ASM-FR02-06`) |
| Success resets failures | `FR02-AI-001`, `014`, `015`, `020` | Complete at design level; requires deterministic state reset/probe at execution |
| Input partitions/types | `FR02-AI-021`–`044` | Backend validation status/schema unresolved (`ASM-FR02-01`–`04`) |
| No enumeration/sensitive disclosure | `FR02-AI-005`, `017`, `031`, `049` | Timing side-channel is not asserted because tolerance/environment oracle is unspecified |
| SQL injection behavioral coverage | `FR02-AI-034`, `050` | Passing cases cannot prove source code uses parameterized queries; code review is separate |
| Success/error schema | `FR02-AI-002`, `005`, `021`–`050` | Exact error schema/message unspecified (`ASM-FR02-02`) |
| `X-Student-Id` requirement | All `FR02-AI-001`–`050` | Actual console screenshot must be produced by student during execution |
| SEC-01 password not plaintext | `FR02-AI-005` covers response exposure only | Storage-at-rest requirement needs DB/code evidence; login API alone cannot prove it |

## 7. Generator handoff

- Status: `COMPLETE` for candidate generation; `PARTIAL` for final executable suite until human audit and ambiguities are resolved.
- AI-generated candidates: **40**. Human-added: **0**. Audit decisions: **pending**. Execution: **NOT RUN**.
- Student next actions: resolve `ASM-FR02-01`–`07`, label every AI row VALID/INVALID/INCOMPLETE with reasons, correct invalid/incomplete rows, add ≥5 genuinely student-authored cases, then implement and execute in Postman/Newman.
