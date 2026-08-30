# Newman result mapping rules

Read this reference before calculating execution metrics or writing TC-level results.

## Evidence tiers

| Tier | Examples | Permitted use |
| :--- | :--- | :--- |
| A — machine-readable run | Newman JSON/JUnit with executions/assertions | TC mapping, counts, assertion failures, run metadata present in artifact |
| B — complete CLI/HTML report | Full console output or HTML report for one identified run | Counts and metadata visible in that report; record lower confidence for TC mapping |
| C — partial log/screenshot | Selected request or failure evidence | Support one observation only; never derive full-suite totals |
| D — user recollection/planned result | “It should pass” or manually typed totals without artifact | Do not use as execution evidence |

Collection path, command, commit, host and timestamps are desirable metadata, not universal parse preconditions. Extract only what the artifact actually contains and mark missing fields pending.

## Mapping identity precedence

1. Explicit TC ID in iteration data or execution metadata.
2. TC ID embedded in request name.
3. Unique mapping table from request + iteration key to TC ID.
4. No reliable identity: classify as unmapped; do not guess from execution order.

## TC result algorithm

For each uniquely mapped TC:

- `PASS`: request completed and every assertion assigned to that TC passed.
- `FAIL`: at least one assigned assertion failed because observed behavior violated its implemented oracle.
- `BLOCKED`: request/setup did not reach the point where the intended behavior could be evaluated, such as network, authentication setup or fixture failure.
- `SKIPPED`: runner explicitly skipped the TC/request/iteration.
- `UNVERIFIED`: request ran but there is no assertion set sufficient to evaluate the TC oracle.

Do not report `UNVERIFIED` as pass. A malformed assertion can make the Newman run fail while the classification is `Test bug`, not product bug.

## Aggregation rules

- Count unique mapped TC IDs, not request events or assertions.
- If one TC appears multiple times intentionally, report executions separately and define how the summary collapses retries; default final status is the last clean rerun only when the report identifies it as the authoritative rerun.
- Never merge results from different commits/environments into one run summary without labeling the aggregation.
- Preserve raw artifacts unchanged. Report transformations and mappings in Markdown/test-case records.
- If mapping coverage is incomplete, update only confidently mapped cases and label overall totals partial.

## Failure classification cues

| Evidence pattern | Preliminary class | Required next check |
| :--- | :--- | :--- |
| Assertion expected value conflicts with cited spec | Test bug | Correct assertion and rerun |
| DNS/refused connection/setup request failure | Environment/setup | Restore environment and rerun affected cases |
| Expected behavior is not specified | Spec ambiguity | Record Q&A; do not file product bug |
| Stable actual result contradicts exact rule | Product-bug candidate | Reproduce independently, then use bug triage matrix |
| Authentication setup fails and downstream cases cascade | Blocked cascade | Do not count every downstream failure as a product bug |
| JSON parse assertion fails because response is unexpected HTML | Could be product or environment | Inspect status/content type and server evidence before classification |

Classification remains preliminary until requirement, test implementation and reproduction evidence are reviewed.

## Run-level consistency checks

- Assign a stable run ID or artifact path and keep start/end metadata together.
- Confirm the feature/collection represented by the artifact before applying per-feature totals.
- Report mapping coverage as `mapped unique TC IDs / unique executable records expected`.
- List duplicate IDs, missing design IDs and orphan executions separately.
- Ensure pass + fail + skipped follows the repository convention for executed; keep blocked/unverified visible rather than hiding them in pass/fail.
- Confirm the result path written to each TC points to the same authoritative run used in the summary.
- Do not overwrite a newer authoritative run with an older artifact.
- Keep intentional CI failing-run evidence separate from genuine product failures and link the restoring run/commit only when real.
- Handoff must distinguish authoritative totals, partial totals and observations supported only by Tier C evidence.
- A second reconciliation of the same unchanged artifact must not duplicate evidence links or alter counts.
