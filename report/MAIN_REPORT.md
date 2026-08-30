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
| API 1 | A | FR-02 Login & account lockout | `POST /api/login` | Boundary, decision-table, authentication and timed state |
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
| Security focus | SEC-01, SEC-02, SEC-05; enumeration, sensitive response fields |
| Data/reset strategy | `[isolated users/reset command]` |

Decision table and detailed cases: [FR-02 test design](../test-cases/FR-02_LOGIN.md). Excel sheet: `[PATH/LINK]`.

### 5.2 AI generation result

| Generated | Partition | Boundary | Decision/state | Security | Schema |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `[≥35]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |

Prompt/output references: `[AUDIT ENTRY IDS]`.

### 5.3 Human audit and corrections

| VALID | INVALID | INCOMPLETE | Corrected | Rejected/merged |
| ---: | ---: | ---: | ---: | ---: |
| `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |

Key corrections: `[specific examples and reasons]`.

### 5.4 Human extensions

At least five cases with rationale: `[TC IDs]`. Explain what AI missed and why: `[analysis]`.

### 5.5 Execution and findings

| Final | Executed | Passed | Failed | Blocked/skipped | Bugs |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |

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
| Fixture strategy | `[orders seeded/created in each state]` |

Transition matrix and detailed cases: [FR-10 test design](../test-cases/FR-10_ORDER_STATE.md).

### 6.2 AI generation, audit, extension and execution

| Generated | VALID | INVALID | INCOMPLETE | Human-added | Final | Pass | Fail | Bugs |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `[≥35]` | `[ ]` | `[ ]` | `[ ]` | `[≥5]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |

Prompt/output references: `[AUDIT ENTRY IDS]`. Key corrections: `[details]`. Human-missed analysis: `[details]`. Evidence: `[links/paths]`.

## 7. FR-15 – Product CRUD

### 7.1 Contract and coverage model

| Item | Detail |
| :--- | :--- |
| Endpoints | `GET /api/products`, `GET /api/products/:id`, `POST /api/products`, `PUT /api/products/:id`, `DELETE /api/products/:id` |
| Required constraints | name required/max 255; price required/>0; existing category required |
| Isolation rule | Updating one product must not change other products |
| Access rule | Mutating product APIs require valid admin role (FR-12) |
| Security focus | SEC-02, SEC-03, SEC-04, SEC-05 |
| Cleanup strategy | `[unique prefix + tracked IDs + cleanup]` |

CRUD/partition matrix and cases: [FR-15 test design](../test-cases/FR-15_PRODUCT_CRUD.md).

### 7.2 AI generation, audit, extension and execution

| Generated | VALID | INVALID | INCOMPLETE | Human-added | Final | Pass | Fail | Bugs |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `[≥35]` | `[ ]` | `[ ]` | `[ ]` | `[≥5]` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |

Prompt/output references: `[AUDIT ENTRY IDS]`. Key corrections: `[details]`. Human-missed analysis: `[details]`. Evidence: `[links/paths]`.

## 8. Postman and Newman

### 8.1 Features used

Chỉ giữ các dòng thực sự đã sử dụng và dẫn evidence.

| Feature | Use | Evidence |
| :--- | :--- | :--- |
| Workspace | `[description]` | `[URL/screenshot]` |
| Collection/folders | `[description]` | `[path]` |
| Collection/environment variables | `[description]` | `[path]` |
| Pre-request script | Add `X-Student-Id`, setup data | `[screenshot/path]` |
| Test scripts | Status/schema/business assertions | `[path]` |
| Data-driven run | Transition/partition rows | `[data path/report]` |
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
