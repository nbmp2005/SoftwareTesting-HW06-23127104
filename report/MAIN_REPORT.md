# HW06 – AI-Assisted API Testing Report

## 1. Student and submission information

| Field | Value |
| :--- | :--- |
| Student name | `[FULL_NAME]` |
| Student ID | `[STUDENT_ID]` |
| Class | `[CLASS]` |
| SUT repository | `https://github.com/ttbhanh/eshop-sut` |
| Tested fork/repository | `[PUBLIC_GITHUB_URL]` |
| Tested commit | `[SUT_COMMIT_SHA]` |
| Test environment | `[OS, Node, Postman, Newman versions]` |
| Execution date | `[ISO_TIMESTAMP]` |

## 2. AI declaration

I use AI tools for requirement extraction, test-design assistance, coverage analysis, Postman assertion assistance, execution-evidence reconciliation, bug-report drafting, documentation synchronization, and Agent Skill design. Every AI-generated test case remains subject to student review. The full interaction record is provided in [AI_AUDIT_REPORT.md](AI_AUDIT_REPORT.md).

## 3. Scope and API selection

| API | Pool | Feature | In-scope endpoints | Why selected |
| :--- | :--- | :--- | :--- | :--- |
| API 1 | A | FR-02 Login & account lockout | `POST /api/login`; supporting security probes at `/api/users/me`, `/api/forgot-password`, `/api/reset-password` | Boundary, decision-table, authentication, timed state and cross-feature bypass risk |
| API 2 | B | FR-10 Order state machine | `PUT /api/admin/orders/:id/status`; `PUT /api/orders/:id/cancel`; supporting reads/setup | Full transition and actor matrix |
| API 3 | C | FR-15 Product CRUD | `GET/POST/PUT/DELETE /api/products[/:id]` | CRUD, field validation, authorization, isolation |

Group uniqueness confirmation: `[WHO CONFIRMED, WHEN, EVIDENCE LINK/PATH]`.

### 3.1 Sources of truth

- Assignment: `docs/hw6.md`.
- SUT requirements: `[LINK TO TESTED VERSION README.md]`.
- API specification: `[LINK TO TESTED VERSION api_specification.md]`.
- Applicable requirements: FR-02, FR-10, FR-12, FR-15 and SEC-01–SEC-07 as mapped below.

### 3.2 Assumptions and ambiguities

| ID | Ambiguity | Working assumption | Resolution/evidence |
| :--- | :--- | :--- | :--- |
| ASM-01 | `[e.g. exact error status not specified]` | `[assumption]` | `[lecturer/spec/code decision]` |

## 4. Test approach

### 4.1 Techniques

Equivalence partitioning and boundary value analysis were applied to every input parameter. Decision tables were used for FR-02, state-transition testing for FR-10, and CRUD lifecycle/isolation testing for FR-15. All three APIs include authentication/authorization, injection/input-handling and response-schema checks where applicable.

### 4.2 AI collaboration pipeline

For each API: contract extraction → partition/state/security/schema modelling → AI case generation → human audit (`VALID/INVALID/INCOMPLETE`) → correction → human extension → implementation → execution → bug triage. Prompts and outputs are traceable in the AI Audit appendix.

### 4.3 Test-case fields

Each test case contains ID, source, requirement trace, technique, priority, preconditions, request, data, expected status/body/schema/post-state, cleanup, AI audit label/reason, execution result and evidence.

## 5. FR-02 – Login & account lockout

### 5.1 Contract and coverage model

| Item | Detail |
| :--- | :--- |
| Endpoint | `POST /api/login` |
| Inputs | `email`, `password`; headers including `Content-Type`, `X-Student-Id` |
| Main rules | Wrong attempt increments exactly 1; locked from 3 consecutive failures; lock 30 seconds; success returns JWT and resets failures |
| Security focus | SEC-01, SEC-02, SEC-05; forged JWT rejection, enumeration, sensitive response fields and lock-bypass interactions |
| Data/reset strategy | Dedicated `U-A/U-B/U-C` fixture snapshots; deterministic seed/reset command still pending implementation |

Decision table and detailed cases: [FR-02 test design](../test-cases/FR-02_LOGIN.md). Excel sheet: `[PATH/LINK]`.

### 5.2 AI generation result

| Generated | Partition | Boundary | Decision/state | Security | Schema |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `40` | `14` | `7` | `15` | `7` | `4` |

Counts are non-exclusive by technique. Prompt/output reference: `AI_AUDIT_REPORT.md` Interaction 005; Interaction 004 records the interrupted first attempt. Seven ambiguities (`ASM-FR02-01`–`07`) remain explicit in the test design.

### 5.3 Human audit and corrections

| VALID | INVALID | INCOMPLETE | Corrected | Rejected/merged |
| ---: | ---: | ---: | ---: | ---: |
| `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |

Human audit has not started. No VALID/INVALID/INCOMPLETE decision or correction is claimed yet.

### 5.4 Human extensions

Human-added count is `5`: `FR02-H-001`–`005`, explicitly supplied by the student and refined for deterministic oracles in `AI_AUDIT_REPORT.md` Interaction 008. They cover JWT `alg=none` forgery, password-reset interaction with an active login lock, email case-normalization of the failure counter, attempts injected during the 30-second lock and forgot-password enumeration parity. `H-002`–`H-005` retain explicit working assumptions because the source contract does not fully specify cross-feature lock/reset, normalization, sliding-window or unknown-email behavior. The documented `resetToken` success field is not independently classified as a defect.

Postman implementation status: the collection has a data-driven `Login` request plus an `FR-02 Human Extensions` folder. Dedicated scripts implement the forged-JWT rejection probe (`H-001`), password-reset setup requests (`H-002`) and ordered forgot-password differential comparison (`H-005`); `H-003/H-004` map to state/timing sequences through `Login`. Iteration files, deterministic fixture reset and controlled timing remain pending, so implementation is still partial and no execution is claimed.

### 5.5 Execution and findings

| Final | Executed | Passed | Failed | Blocked/skipped | Bugs |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `45` | `45` | `36` | `9` | `0` | `1` |

Evidence: `[NEWMAN SECTION/SCREENSHOT/COMMIT]`. Findings: `[summary]`.

## 6. FR-10 – Order state machine

### 6.1 Contract and coverage model

| Item | Detail |
| :--- | :--- |
| Admin transition | `PUT /api/admin/orders/:id/status` |
| User cancellation | `PUT /api/orders/:id/cancel` |
| States | `pending`, `confirmed`, `shipping`, `delivered`, `canceled` |
| Final states | `delivered`, `canceled` |
| Actor rule | User cancels only pending/confirmed; admin follows state machine |
| Security focus | SEC-02, SEC-03, IDOR/ownership |
| Fixture strategy | Named fixtures `O-P/O-CF/O-S/O-D/O-X` plus unrelated sentinel `O-U`; deterministic seed/reset implementation remains pending |

Transition matrix and detailed cases: [FR-10 test design](../test-cases/FR-10_ORDER_STATE.md).

### 6.2 AI generation, audit, extension and execution

| Generated | VALID | INVALID | INCOMPLETE | Human-added | Final | Pass | Fail | Bugs |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `47` | `[pending human audit]` | `[pending human audit]` | `[pending human audit]` | `5` | `[pending human audit]` | `[not run]` | `[not run]` | `[not triaged]` |

Prompt/output references: `AI_AUDIT_REPORT.md` Interactions 012–014. The 47-case AI set covers the complete admin/user state model plus security, schema and robustness probes. The student then supplied five HUMAN extensions (`FR10-H-001`–`005`), refined to cover unsupported method, near-valid enum formatting, duplicate JSON keys, admin-vs-admin concurrency and fixture-backed nested-data leakage. All 52 IDs are mapped by `FR10_data.csv` into folder `FR-10 Order State Machine`: a dynamic mutation router plus an independent persisted-state verification request. Replay/variant and race rows use traceable `pm.sendRequest` assertions. Implementation remains conditional on local tokens, deterministic fixture reset and confirmation of `ASM-FR10-01`–`09`; no AI-candidate audit, execution or bug evidence is claimed.

## 7. FR-15 – Product CRUD

### 7.1 Contract and coverage model

| Item | Detail |
| :--- | :--- |
| Endpoints | `GET /api/products`, `GET /api/products/:id`, `POST /api/products`, `PUT /api/products/:id`, `DELETE /api/products/:id` |
| Required constraints | name required/max 255; price required/>0; existing category required |
| Isolation rule | Updating one product must not change other products |
| Access rule | Mutating product APIs require valid admin role (FR-12) |
| Security focus | SEC-02, SEC-03, SEC-04, SEC-05 |
| Cleanup strategy | Unique `HW06-*` names, tracked returned IDs, target/sentinel snapshots and deterministic restore/delete |

CRUD/partition matrix and cases: [FR-15 test design](../test-cases/FR-15_PRODUCT_CRUD.md).

### 7.2 AI generation, audit, extension and execution

| Generated | VALID | INVALID | INCOMPLETE | Human-added | Final | Pass | Fail | Bugs |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `50` | `[pending human audit]` | `[pending human audit]` | `[pending human audit]` | `0` | `[pending human audit]` | `[not run]` | `[not run]` | `[not triaged]` |

Prompt/output reference: `AI_AUDIT_REPORT.md` Interaction 015. The 50 AI candidates cover CRUD lifecycle, list/detail/search, every request field and boundary, referential integrity, partial/full update isolation, auth/role enforcement across all mutation endpoints, schema/sensitive-field checks, SQL injection, stored-XSS API behavior, mass assignment and concurrent updates. Eight explicit ambiguities (`ASM-FR15-01`–`08`) separate locally omitted status/schema/domain/update rules from the source contract. No human audit, human extension, Postman implementation, execution or bug evidence is claimed.

## 8. Postman and Newman

### 8.1 Features used

Chỉ giữ các dòng thực sự đã sử dụng và dẫn evidence.

| Feature | Use | Evidence |
| :--- | :--- | :--- |
| Workspace | `[description]` | `[URL/screenshot]` |
| Collection/folders | FR-02 `Login` + human support; FR-10 `FR-10 Order State Machine` with mutation and persisted-state requests | `HW06_Eshop.postman_collection.json` |
| Collection/environment variables | `baseUrl`; empty `studentId`; empty FR-10 token/order/sentinel placeholders supplied only at runtime | `HW06_Eshop.postman_collection.json` |
| Pre-request script | Iteration-driven method/path/body/auth routing; every FR-10 request binds `X-Student-Id` to `{{studentId}}` | `HW06_Eshop.postman_collection.json` |
| Test scripts | TC-ID trace, exact status/body-state, credential-field scan, replay/variant callbacks, concurrency status-pair and independent persisted-state assertions | `HW06_Eshop.postman_collection.json` |
| Data-driven run | FR-02 supports 45 IDs; FR-10 maps 52/52 IDs through 52 rows, but fixture setup and real run evidence remain pending | `FR02_data.csv`; `FR10_data.csv`; `HW06_Eshop.postman_collection.json` |
| Mock server | `[description or N/A]` | `[evidence]` |
| Monitor | `[description or N/A]` | `[evidence]` |
| Newman reporter | CLI + HTML/JUnit | `[artifact]` |

### 8.2 Command and environment

```text
[EXACT NEWMAN COMMAND EXECUTED]
```

Header evidence: `[REAL SCREENSHOT PATH]`. HTML report: `[PATH/LINK]`. No secrets are included in exported artifacts.

## 9. Bugs

Summary is maintained in [BUG_REPORT.md](BUG_REPORT.md). Do not count a failed test as a bug until it has been reproduced and traced to a violated requirement.

## 10. CI/CD

See [CICD_REPORT.md](CICD_REPORT.md) for pipeline configuration, passing/failing commits, run links and screenshots.

## 11. AI-driven test generator

The reusable generator and its supporting close-out skills are documented in [AGENT_SKILL_DESIGN.md](AGENT_SKILL_DESIGN.md). Each package uses a focused entrypoint plus routed references for audit provenance, test schema/quality gates, Postman assertions, Newman result mapping, bug triage and report consistency. The workflow synchronizes report consumers from real source artifacts and records AI interactions while preserving the mandatory human audit and evidence gates. Structural/link/schema validation passed for all six packages; behavioral demonstration evidence remains a separate student task. The submitted diagram is self-drawn by the student.

## 12. Overall test summary and conclusion

See [TEST_SUMMARY.md](TEST_SUMMARY.md). Discuss risk-based conclusions, uncovered scope, environment limitations and release recommendation: `[CONCLUSION]`.

## Appendices

- [AI Critique](AI_CRITIQUE.md)
- [AI Audit Report](AI_AUDIT_REPORT.md)
- [Git Commit Log](GIT_COMMIT_LOG.md)
