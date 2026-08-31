# Test Summary Report

## Execution metadata

| Field | Value |
| :--- | :--- |
| Execution ID | FR-10: `FR10-20260831T163646594Z`; other run IDs pending |
| Start/end time | FR-10: `2026-08-31T16:36:46.594Z`–`2026-08-31T16:36:54.546Z` |
| SUT commit | `[SHA]` |
| Collection/environment | `HW06_Eshop.postman_collection.json`; `FR02_data.csv`; `FR10_data.csv`; runtime environment with secrets remains uncommitted |
| Newman report | FR-10 Tier A: `newman-report-FR10.json`, SHA-256 `1BAFF84BD829F0BCAC5D6BE2FF72673441CEFF7B8136A913E285D196991691F3`; FR-02: `newman-report-FR02.json` |

## Metrics

| Metric | FR-02 | FR-10 | FR-15 | Total |
| :--- | ---: | ---: | ---: | ---: |
| AI-generated | `40` | `47` | `50` | `137` |
| AI VALID | `[pending human audit]` | `[ ]` | `[ ]` | `[pending]` |
| AI INVALID | `[pending human audit]` | `[ ]` | `[ ]` | `[pending]` |
| AI INCOMPLETE | `[pending human audit]` | `[ ]` | `[ ]` | `[pending]` |
| Human-added | `5` | `5` | `0` | `10` |
| Final executable | `45` | `52` | `[ ]` | `97` |
| Executed | `45` | `52` | `[ ]` | `97` |
| Passed | `36` | `8` | `[ ]` | `44` |
| Failed | `9` | `44` | `[ ]` | `53` |
| Blocked/skipped | `0` | `0` | `[ ]` | `0` |
| Genuine bugs | `1` | `3` | `[ ]` | `4` |

## Coverage

| Coverage dimension | Planned | Covered | Gaps and rationale |
| :--- | ---: | ---: | :--- |
| Requirements/rules | `[ ]` | `[ ]` | `[ ]` |
| Input partitions/boundaries | `[ ]` | `[ ]` | `[ ]` |
| Valid/invalid transitions | `[ ]` | `[ ]` | `[ ]` |
| Applicable SEC requirements | `[ ]` | `[ ]` | `[ ]` |
| Response schemas | `[ ]` | `[ ]` | `[ ]` |

## Failure classification

| TC ID | Result | Classification (`Product bug/Test bug/Environment/Spec ambiguity`) | Bug ID/action |
| :--- | :--- | :--- | :--- |
| FR-10: `AI-001,003,004,006,007,009,011–013,015–023,025,029,030,034,037`; `H-001,H-003` | `FAIL` | Spec ambiguity: chiefly `409`/`400`, auth status, router and duplicate-key policy | Confirm `ASM-FR10-03/05/08/09`, correct oracle if needed, rerun |
| FR-10: `AI-002,005,008,010,014,026,027,045`; `H-005` | `FAIL` | Test script/response-schema ambiguity | Reconcile body-status oracle with actual response schema, then rerun |
| FR-10: `AI-024,028,031,032,035` | `FAIL` | Product-bug candidate: final-state/cancel/ownership/role behavior | Independently reproduce and triage before assigning bug IDs |
| FR-10: `H-004` | `FAIL` | Concurrency/spec-policy ambiguity | Confirm serialization policy and reproduce with deterministic barrier |
| FR-10: `AI-038–040,046` | `BLOCKED` | Environment/setup: verification fixture ID unresolved | Repair `verifyOrderId`/sentinel data and rerun; do not count as product failure |

## Exit assessment

- Release/test conclusion: `[PASS / PASS WITH RISKS / FAIL / BLOCKED]`.
- Residual risks: `[list]`.
- Recommended next tests: `[list]`.
