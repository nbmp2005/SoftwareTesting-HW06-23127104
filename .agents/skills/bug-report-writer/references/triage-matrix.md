# Bug triage and evidence matrix

Read this reference when classifying a failed test or changing a bug lifecycle state.

## Classification decision table

| Observation | Requirement oracle reliable? | Test/setup valid? | Reproduced? | Classification |
| :--- | :---: | :---: | :---: | :--- |
| Actual contradicts spec | Yes | Yes | Yes | Confirmed product bug |
| Actual contradicts spec | Yes | Unknown | Any | Triage pending |
| Assertion implements wrong oracle | Yes | No | Any | Test bug |
| Timeout/service unavailable/fixture failure | Any | No | Any | Environment/setup issue |
| Spec omits or conflicts on expected behavior | No | Yes | Any | Spec ambiguity / Q&A |
| Same underlying defect appears through multiple TCs | Yes | Yes | Yes | One bug mapped to multiple TC IDs |

“Reproduced” may be `1/1` when one deterministic reproduction is all that exists. Do not claim a stronger rate.

## Lifecycle and submission evidence

| State | Can appear in detailed report? | Count as genuine bug? | Can tick final bug-evidence checklist? |
| :--- | :---: | :---: | :---: |
| Triage pending | Yes, under a separate pending section | No | No |
| Confirmed, issue/screenshot pending | Yes | Yes | No |
| Confirmed, GitHub Issue and screenshot attached | Yes | Yes | Yes, if all required fields also exist |
| Rejected as test/environment/spec issue | Yes, in failure classification | No | No |

The assignment requires Markdown report + GitHub Issue + screenshot for final submission. Missing external evidence makes the deliverable incomplete; it does not retroactively turn a reproduced requirement violation into a non-bug.

## Severity guide

- **Critical:** broad authentication/authorization bypass, severe data exposure/destruction, or system-wide unavailability with no practical workaround.
- **High:** major business rule or security violation affecting important users/data.
- **Medium:** incorrect behavior with limited scope or a viable workaround.
- **Low:** minor contract/presentation issue with little operational impact.

Severity is impact; priority is scheduling. Record both when the template asks for both, and preserve the student's final judgment.

## Required detail fields

Before a confirmed entry is ready for submission, verify:

- stable unique Bug ID and concise observable title;
- exact FR/SEC/API rule plus source/version;
- severity and priority with separate rationales when both are used;
- OS/tool versions, SUT commit and base host when known;
- actor/account role, ownership, data and state preconditions;
- all related TC IDs and whether AI suggested or missed the case;
- reproducible method/path/headers/body with secret values omitted;
- requirement-based expected status/body/post-state;
- observed status/body/post-state from evidence;
- actual reproduction count, impact and workaround if any;
- Newman/Postman evidence, screenshot and public GitHub Issue status.

Missing submission-only evidence must remain visibly pending; do not insert placeholder paths that look real.

## Duplicate and closure rules

- Group failures by likely root cause and violated rule, not merely identical error text.
- One bug may list multiple TC IDs and endpoints when the same root cause is demonstrated.
- Similar symptoms with different violated rules or fixes may remain separate bugs.
- Never merge confirmed bugs solely to reduce the reported count.
- Closing a bug requires a tested fix build and retest evidence; a code change alone is not verification.
- If a bug is rejected after investigation, preserve the history and move its failure to the correct classification instead of deleting it.

## Triage handoff minimum

- State the classification and the exact evidence supporting it.
- List missing evidence separately from evidence that contradicts the bug claim.
- Identify which report metrics/checklist fields may change and which must remain unchanged.
- Route confirmed bugs to synchronization; route non-product failures only to failure classification.
