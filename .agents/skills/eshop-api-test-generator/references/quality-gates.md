# Quality gates

Run all applicable gates before handoff. A structural pass does not imply behavioral correctness.

## G1 — Source and contract

- Tested requirement/API-spec source and version are identified or explicitly pending.
- Every in-scope endpoint, actor, auth/header, input field, output schema and business rule appears in the contract inventory.
- Unsupported assumptions are separated from requirements.
- Conflicts and omissions have stable ambiguity IDs.

## G2 — Coverage model

- Every input has valid/invalid equivalence partitions and relevant boundary values.
- Conditional behavior has decision-rule coverage.
- Stateful features include valid and invalid transitions, actor/ownership combinations and state-unchanged assertions.
- CRUD features cover lifecycle, dependencies, isolation and cleanup.
- Each applicable SEC requirement maps to cases; non-applicable SEC rules have rationale.
- Success/error schemas and forbidden sensitive fields are covered.

## G3 — Candidate quality

- Every case has a unique stable ID, `Source=AI`, exact requirement/technique trace and risk-based priority.
- Setup, data, request, oracle, postcondition/no-side-effect and cleanup are concrete.
- No case relies on unresolved ambiguity while being counted final executable.
- Semantic duplicates have been removed; minor data changes alone do not create a new case.
- New candidates have blank audit fields and `Execution=NOT RUN`.

## G4 — Count and traceability

- Count from unique structured records, not headings, placeholders or assertions.
- Every modeled item maps to at least one TC ID or a documented gap.
- Target ≥35 is met with meaningful AI-generated cases. If not, status is `PARTIAL`, not complete.
- HUMAN cases and AI cases remain separately countable.

## G5 — Preservation and safety

- Existing student audit labels, corrections, human cases and execution evidence are preserved.
- No secrets, actual tokens/passwords, fabricated screenshots, URLs, SHAs, bugs or results appear.
- Time-dependent/concurrent cases state fixture and timing limitations.

## G6 — Close-out

- Target test-design file is valid Markdown and follows `output-schema.md`.
- `$hw06-deliverable-sync` updated only design/audit metrics supported by the records.
- `$ai-audit-logger` records one interaction after the output summary is known.
- Handoff lists counts, coverage gaps, ambiguity IDs, files changed, validation performed and student decisions still required.
