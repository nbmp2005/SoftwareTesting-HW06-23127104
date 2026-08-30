# CI/CD API Test Report

## 1. Pipeline overview

| Field | Value |
| :--- | :--- |
| Platform | `[GitHub Actions/other]` |
| Workflow file | `[.github/workflows/api-tests.yml]` |
| Trigger | `[push/pull_request/workflow_dispatch]` |
| SUT startup | `[command/service]` |
| Database seed/reset | `[command]` |
| Test command | `[exact Newman command]` |
| Reports | `[HTML/JUnit artifact names]` |

Pipeline flow: checkout → install dependencies → seed/start SUT → wait for readiness → execute Newman → publish artifacts → preserve non-zero exit code as failed job.

## 2. Configuration explanation

Explain variable/secret handling, deterministic fixtures, readiness check, timeout, Newman version, reporter settings, artifact retention and why the job fails when an assertion fails: `[DETAILS]`.

## 3. Passing run

| Evidence | Value |
| :--- | :--- |
| Commit SHA/link | `[PASS_COMMIT_URL]` |
| Workflow run | `[PASS_RUN_URL]` |
| Result | `Passed` |
| Summary | `[requests/assertions/tests]` |
| Screenshot | `[REAL_PATH]` |
| Report artifact | `[URL/PATH]` |

Explain what this run proves and any limitations: `[ANALYSIS]`.

## 4. Intentional failing run

| Evidence | Value |
| :--- | :--- |
| Commit SHA/link | `[FAIL_COMMIT_URL]` |
| Workflow run | `[FAIL_RUN_URL]` |
| Result | `Failed as designed` |
| Intentional change | `[one assertion/test changed]` |
| Screenshot | `[REAL_PATH]` |
| Report artifact | `[URL/PATH]` |

Explain why this is a controlled quality-gate demonstration, not a product bug. Link the restoring commit: `[RESTORE_COMMIT_URL]`.

## 5. Conclusion

`[Reliability, feedback speed, residual risks and improvement actions]`.
