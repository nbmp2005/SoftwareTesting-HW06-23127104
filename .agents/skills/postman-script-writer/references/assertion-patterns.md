# Postman assertion and patching rules

Read this reference when generating assertions or modifying a collection JSON.

## Oracle-to-assertion mapping

| Oracle | Assertion strategy |
| :--- | :--- |
| Status | `pm.response.to.have.status(expected)` in a TC-labelled test |
| Content type | Assert the response header before treating the body as JSON |
| JSON validity | Parse inside a dedicated `pm.test`; parsing failure must fail that test |
| Schema | Validate required properties/types and forbidden sensitive fields; use `pm.response.to.have.jsonSchema` when supported |
| Business value | Assert exact values or requirement-defined predicates, not mere existence |
| Error contract | Assert status, stable error code/schema and only exact message text guaranteed by spec |
| Headers | Assert presence/value only when specified or security-relevant |
| Post-state | Use a follow-up request or setup/verification request with a traceable TC mapping |
| No side effect | Compare before/after state or query the resource after the rejected operation |

Postman runs sibling `pm.test` blocks independently. Do not assume a failed status test prevents later JavaScript from running. Either parse JSON inside each dependent test or use a shared parse result whose failure is asserted explicitly and whose consumers guard against `undefined` without hiding failures.

## Request and TC mapping

- One request may represent one TC, or a data-driven request may represent multiple TCs through iteration data.
- Every executable scenario needs a stable TC ID in the request name, iteration data or mapping table.
- Multiple assertions for one scenario remain one test case.
- A setup/cleanup request is not a test case unless it has its own independently traceable oracle.

## Collection patch safety

1. Identify the target by method + normalized URL path + folder/request identity; name alone is insufficient when duplicated.
2. Preserve unrelated `event`, variables, auth, headers and scripts.
3. Avoid whole-file formatting churn when a targeted edit is possible.
4. Parse the final JSON and inspect the semantic diff around the target request.
5. Never insert actual secrets or Postman current values into committed JSON.
6. A successful JSON parse proves structure only. Execution evidence still requires a real Postman/Newman run.

## HW06-specific checks

- Verify that the collection or collection-level pre-request script supplies `X-Student-Id` through a variable; never invent the student's ID.
- Do not claim header evidence until a real console/request capture exists.
- Keep TC ID visible in Newman output so `newman-evidence-reconciler` can map results deterministically.

## Negative and stateful test invariants

- A rejected mutation should assert both its error contract and the unchanged persisted state when the requirement defines no side effect.
- Authorization tests must distinguish missing/invalid authentication from authenticated wrong-role/ownership cases.
- Injection cases assert safe behavior and data integrity; one passing payload does not prove parameterized implementation.
- Schema tests cover error responses as well as success responses.
- List assertions should not depend on unstable ordering unless the contract specifies ordering.
- Time-dependent lockout assertions should record controlled timing variables/tolerance and avoid arbitrary sleeps in the test script.
- Cleanup failures should be visible and must not silently convert later fixture contamination into product failures.

## Script quality gates

Before handoff, verify:

- every generated `pm.test` name contains or can deterministically resolve to the TC ID;
- each implemented oracle traces to the test-design row/spec;
- parsing failures create a failing test rather than only a console message;
- assertions use exact types and meaningful predicates;
- no assertion relies on a variable that may be undefined without an explicit guard/failure;
- data-driven scripts read the correct iteration fields and do not leak values between iterations;
- setup variables use appropriate collection/environment scope and secrets stay in uncommitted current values;
- collection JSON parses and the semantic diff is limited to intended requests;
- implementation status may be synchronized, but execution status remains `NOT RUN` until real evidence exists.
