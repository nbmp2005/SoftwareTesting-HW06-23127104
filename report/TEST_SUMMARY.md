# Test Summary Report

## Execution metadata

| Field | Value |
| :--- | :--- |
| Execution ID | FR-02: `FR02-20260902T150418757Z`; FR-10: `FR10-20260902T150434504Z`; FR-15: `FR15-20260902T150456902Z` |
| Start/end time | FR-02: `2026-09-02T15:04:18.757Z`–`2026-09-02T15:04:22.746Z`; FR-10: `2026-09-02T15:04:34.504Z`–`2026-09-02T15:04:42.887Z`; FR-15: `2026-09-02T15:04:56.902Z`–`2026-09-02T15:05:02.162Z` |
| SUT commit | Not captured in Newman artifacts; student confirmation required |
| Collection/environment | `HW06_Eshop.postman_collection.json`; `FR02_data.csv`; sanitized `FR10_data.csv`/`FR15_data.csv`; runtime JWTs remain captured in raw Newman artifacts and require rotation/sanitized publication copies |
| Newman report | Tier A: `newman-report-FR02-ai.json` (`C29A152084038D98B70D1B219BB7DDB0776D7A5079972A78BF9E18189ADF0E4A`); `newman-report-FR10.json` (`10CD5E0F2FB9789095AB4F4C6258A9B42292E29BC16126E0E722B2082BEC1D89`); `newman-report-FR15.json` (`AE21D309C08924BD1B75DA54141F8BBD15539E5B3077270FC2E27A305AE806E0`) |

## Metrics

| Metric | FR-02 | FR-10 | FR-15 | Total |
| :--- | ---: | ---: | ---: | ---: |
| AI-generated | `40` | `47` | `50` | `137` |
| AI VALID | `40` | `47` | `50` | `137` |
| AI INVALID | `0` | `0` | `0` | `0` |
| AI INCOMPLETE | `0` | `0` | `0` | `0` |
| Human-added | `5` | `5` | `5` | `15` |
| Planned records (generated + human-added) | `45` | `52` | `55` | `152` |
| Final executable after human audit | `45` | `52` | `55` | `152` |
| Executed | `45` | `48` | `55` | `148` |
| Passed | `36` | `0` | `7` | `43` |
| Failed | `9` | `48` | `48` | `105` |
| Blocked/skipped | `0` | `4` | `0` | `4` |
| Genuine bugs | `1` | `1` | `2` | `4` |

## Coverage

| Coverage dimension | Evidence | Gaps and rationale |
| :--- | :--- | :--- |
| Requirements/rules | Stable TC IDs map FR-02, FR-10 and FR-15 rules to all 152 design records | Human VALID/INVALID/INCOMPLETE audit and several assumption resolutions remain pending |
| Input partitions/boundaries | EP/BVA rows exist for all request parameters represented in the three designs | Some strict HTTP/schema expectations are assumptions rather than specification rules |
| Valid/invalid transitions | FR-10 maps the 25-cell admin matrix and owner-cancel states | Shared mutable fixtures contaminate later iterations; four verification cases are blocked |
| Applicable SEC requirements | Auth/role, sensitive-field and injection probes are implemented | FR-10 role/ownership evidence is not independent because identities/state were not reset |
| Response schemas | JSON/schema assertions executed in all three runs | The API spec omits most exact response schemas; unsupported oracles must not be reported as product bugs |

## Failure classification

| TC ID | Result | Classification (`Product bug/Test bug/Environment/Spec ambiguity`) | Bug ID/action |
| :--- | :--- | :--- | :--- |
| FR-02: `AI-001`–`005` | `FAIL` | Confirmed product bug: response exposes credential/lockout internals | `BUG-001`; [Issue #1](https://github.com/nbmp2005/SoftwareTesting-HW06-23127104/issues/1) |
| FR-02: `H-002`–`005` | `FAIL` | Mixed working-assumption/setup outcomes; not additional confirmed bugs | Review FR-02 assumptions and rerun with deterministic account state |
| FR-10: `AI-003`, `AI-004`, `AI-009`, `AI-024` | `FAIL` | Confirmed product bug: invalid state transitions accepted | `BUG-002` |
| FR-10: role/ownership and concurrency probes | `FAIL` | Triage pending: dirty shared state and duplicate user identity prevent the intended oracle | `BUG-003`/`BUG-004` are not counted; reset fixtures and rerun |
| FR-10: remaining non-blocked failures | `FAIL` | Mixed test-oracle/spec ambiguity and fixture-cascade failures | Review exact `400`/`409` and response-schema assumptions; full TC-level classification remains pending |
| FR-10: `AI-038`–`040`, `046` | `BLOCKED` | Environment/setup: verification fixture ID unresolved | Repair `verifyOrderId`/sentinel data and rerun; do not count as product failure |
| FR-15: missing/invalid fields and unauthorised mutations | `FAIL` | Confirmed product bugs | `BUG-006`, `BUG-007` |
| FR-15: `201`/full-object response assertions | `FAIL` | Spec ambiguity/test oracle; FR-15 does not define that response contract | `BUG-005` rejected; revise oracle |
| FR-15: `H-005` | `FAIL` | Test bug plus robustness observation: comma-list secondary status is parsed as `NaN` | Correct runner and rerun before triaging the observed `500` |

## Exit assessment

- Release/test conclusion: `FAIL`.
- Residual risks: four confirmed security/validation/state-management defects; four FR-10 cases remain blocked, and many failed cases still need a clean fixture-isolated rerun before final classification.
- Recommended next tests: reset state per iteration, use distinct FR-10 user identities, repair verification fixtures and `FR15-H-005`, then rerun and retest the four confirmed issues.
