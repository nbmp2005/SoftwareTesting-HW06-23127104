# Cross-report consistency rules

Read this reference when calculating metrics, resolving discrepancies or changing checklist state.

## Metric state model

| State | Required evidence | May update |
| :--- | :--- | :--- |
| Planned/generated | Structured TC records with unique IDs and source | AI-generated/human-added/design coverage |
| Audited | Student-confirmed label and reason/correction | VALID/INVALID/INCOMPLETE counts |
| Final executable | Accepted/corrected TC record with complete executable fields | Final count |
| Implemented | Collection/data mapping exists for the TC | Implementation coverage, not execution |
| Executed | Real run maps to the TC | Executed and TC result |
| Genuine bug | Confirmed requirement violation after triage | Bug count/classification |
| Submission-complete bug | Confirmed bug plus GitHub Issue and screenshot | Final evidence checklist |

## Counting rules

- Use explicit TC records and stable IDs. Never count Markdown table separator/header rows.
- Do not infer rejected/merged state from strikethrough alone unless the repository explicitly defines that convention. Prefer an audit/status field or a documented mapping.
- `AI-generated` includes retained raw AI cases, even those later rejected. `Final executable` excludes rejected/merged cases.
- `Human-added` requires explicit student authorship/confirmation; AI suggestions cannot be relabeled human.
- Audit labels apply only to AI-generated cases. When audit is complete: `AI-generated = VALID + INVALID + INCOMPLETE`.
- Follow the repository's stated execution equation. For the current checklist, `Executed = Passed + Failed + Skipped`; keep `Blocked` separate unless the report explicitly combines it.
- Totals equal the sum of FR-02, FR-10 and FR-15. Never use placeholder strings such as `[≥35]` in arithmetic.

## Conflict handling

| Conflict | Action |
| :--- | :--- |
| Design count differs across reports | Recount source TC records and patch consumers |
| Newman has extra unmapped executions | Preserve design counts; mark execution totals partial and list orphan executions |
| Reports claim execution but no artifact exists | Do not invent evidence; flag discrepancy and preserve user-authored claim for review |
| Checked checklist item lacks evidence | Flag `Missing evidence`; do not silently untick a user-confirmed item |
| Two artifacts describe different runs | Keep separate run IDs/metadata; do not combine silently |
| Consumer has manual analysis text | Patch only metrics/links affected; preserve analysis unless contradicted by evidence |

## Idempotency and completion

A successful sync is idempotent: a second run on unchanged source artifacts produces no file changes. Handoff must list sources, consumers changed, old→new metrics, unresolved discrepancies and fields intentionally left pending.
