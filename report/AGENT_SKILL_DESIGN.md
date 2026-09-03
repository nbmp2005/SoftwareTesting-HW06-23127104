# AI-Driven EShop API Test Generator – Agent Skill Design

## 1. Goal and scope

The generator accepts an EShop requirement/API specification and one selected feature, then produces traceable candidate API test cases plus coverage models. It assists generation and review; it does not replace human audit or fabricate execution evidence.

Primary implementation: [`.agents/skills/eshop-api-test-generator/SKILL.md`](../.agents/skills/eshop-api-test-generator/SKILL.md). Supporting skills close the loop from implementation and real execution evidence to the required reports.

## 2. Design alternatives

| Alternative | Advantages | Limitations | Decision |
| :--- | :--- | :--- | :--- |
| Prompt-only `SKILL.md` | Fast and simple | Entry file becomes long; weaker routing | Not selected |
| Skill + focused references | Progressive disclosure, maintainable, easy to demo | Output still needs human review | **Selected** |
| Skill + parser/export scripts | More deterministic and automatable | More implementation/testing effort; Markdown specs may be irregular | Future extension |

## 3. Architecture decisions for the student's self-drawn diagram

You must draw the submitted diagram yourself. Use these student-owned design blocks only as a checklist; do not submit an AI-rendered diagram:

1. Inputs: requirement spec, API spec, selected feature, target count.
2. Contract extractor: endpoints, actors, parameters, rules, schemas, ambiguities.
3. Coverage modelers: partition/boundary, decision/state/CRUD, security, schema.
4. Candidate generator: stable IDs and concrete scenarios.
5. Quality gates: completeness, uniqueness, traceability, no fabricated evidence.
6. Outputs: raw AI cases, coverage matrix, assumptions, human-review checklist.
7. Human gate: VALID/INVALID/INCOMPLETE, correction, ≥5 own cases.
8. Downstream, outside generator: Postman/Newman execution and bug triage.

Suggested drawing procedure: draw these blocks manually in diagrams.net/PowerPoint/paper, choose the arrows and feedback loop yourself, and export PNG. **Submission gap:** no self-drawn diagram file is currently present in the repository.

## 4. Pseudocode

```text
FUNCTION generate_api_tests(requirements, api_spec, feature, target_count = 35):
    ASSERT feature is explicitly selected

    contract = extract_contract(requirements, api_spec, feature)
    ambiguities = find_missing_or_conflicting_rules(contract)
    assumptions = record_explicit_assumptions(ambiguities)

    parameter_model = build_partitions_and_boundaries(contract.inputs)
    behavior_model = SELECT by feature shape:
        conditional -> build_decision_table(contract.rules)
        stateful    -> build_transition_matrix(contract.states, actors)
        CRUD        -> build_crud_lifecycle(contract.resources)

    security_model = map_applicable_security_requirements(contract)
    schema_model = derive_success_error_and_forbidden_fields(contract)

    candidates = []
    FOR coverage_item IN union(parameter_model, behavior_model,
                               security_model, schema_model):
        candidates += create_concrete_candidate(coverage_item,
                                                source = "AI",
                                                execution = "NOT RUN",
                                                audit = EMPTY)

    candidates = remove_semantic_duplicates(candidates)
    gaps = compute_uncovered_items(all_models, candidates)
    WHILE gaps is not empty OR meaningful_count(candidates) < target_count:
        new_cases = create_cases_for_meaningful_gaps(gaps)
        IF new_cases is empty:
            BREAK AND report inability to reach target without padding
        candidates += new_cases
        gaps = compute_uncovered_items(all_models, candidates)

    validate_unique_ids_and_required_fields(candidates)
    RETURN contract, all_models, candidates,
           traceability_matrix(all_models, candidates),
           assumptions, human_review_checklist
```

## 5. Skill file structure

```text
.agents/skills/eshop-api-test-generator/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── eshop-rules.md
    ├── output-schema.md
    └── quality-gates.md

.agents/skills/hw06-deliverable-sync/
├── SKILL.md
└── references/
    ├── artifact-map.md
    └── consistency-rules.md

.agents/skills/newman-evidence-reconciler/
├── SKILL.md
└── references/result-mapping.md

.agents/skills/postman-script-writer/
├── SKILL.md
└── references/assertion-patterns.md

.agents/skills/bug-report-writer/
├── SKILL.md
└── references/triage-matrix.md

.agents/skills/ai-audit-logger/
├── SKILL.md
└── references/audit-entry-protocol.md
```

The generator owns contract/coverage/candidate design. `postman-script-writer` handles reviewed assertions, `newman-evidence-reconciler` imports real run results, `bug-report-writer` triages confirmed requirement violations, `hw06-deliverable-sync` reconciles report consumers, and `ai-audit-logger` records the interaction. References are loaded only for the relevant scope.

The entrypoint files intentionally remain compact. Fragile rules are placed in focused references: audit field provenance and secret handling, bug triage lifecycle, assertion patterns, Newman result mapping, and cross-report counting/idempotency. This gives the skill suite more operational depth without forcing every invocation to load unrelated instructions.

### 5.1 Close-out contract

Every material task follows: update source artifact → validate it → synchronize affected reports → append one AI audit entry. The synchronization map prevents design counts from being confused with execution results and prohibits inferred timestamps, commits, screenshots, URLs, grades and bugs.

### 5.2 Supporting skill responsibilities

| Skill | Owns | Required close-out |
| :--- | :--- | :--- |
| `eshop-api-test-generator` | Contract, coverage models, AI candidate cases | Sync design metrics, then audit log |
| `postman-script-writer` | Reviewed Postman assertions and TC mapping | Sync implementation references, then audit log |
| `newman-evidence-reconciler` | Real run parsing, TC result mapping, preliminary failure classification | Sync execution metrics, then audit log |
| `bug-report-writer` | Evidence-based bug triage/report | Sync genuine-bug metrics, then audit log |
| `hw06-deliverable-sync` | Cross-report consistency from source artifacts | No duplicate audit entry when called internally |
| `ai-audit-logger` | Verbatim prompt, real timestamp, factual output summary | Update AI declaration only when task categories change |

## 6. Validation plan

### Structural validation

```powershell
python "C:\Users\cpshc\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".agents\skills\eshop-api-test-generator"
```

On 2026-08-30, all six skill directories passed `quick_validate.py` with Python UTF-8 mode enabled. This establishes frontmatter/structure validity only; behavioral evidence must still come from the demonstrations and real artifacts described below.

The hardening review also verified that every skill package contains at least 100 Markdown instruction/reference lines while keeping each entrypoint focused, all six `openai.yaml` files parse, all local skill links resolve, and the FR-02/FR-10/FR-15 template header/separator/sample rows have consistent columns. The review removed contradictory rules around prompt truncation/redaction, mandatory Newman metadata, bug evidence lifecycle and brittle row counting.

### Behavioral demonstration

1. Invoke `$eshop-api-test-generator` for exactly one of FR-02/FR-10/FR-15.
2. Supply the tested requirement and API specification versions.
3. Confirm output includes contract, models, ≥35 meaningful candidates, traceability and human-review checklist.
4. Check no case is self-labeled VALID and no execution result is fabricated.
5. Audit a sample manually and record improvements.
6. Record a demo video; include prompt, generated files and validation output.

## 7. Evaluation criteria

| Criterion | Measure | Actual result/evidence |
| :--- | :--- | :--- |
| Requirement traceability | % cases with valid FR/SEC trace | `[ ]` |
| Completeness | Covered model items / total model items | `[ ]` |
| Executability | % sample cases with sufficient setup/data/oracle | `[ ]` |
| Hallucination control | Unsupported rules/evidence claims | `[ ]` |
| Duplicate rate | Semantic duplicates / generated cases | `[ ]` |
| Human correction rate | INVALID + INCOMPLETE / generated | `[ ]` |

## 8. Limitations and future improvements

The model can misread ambiguous prose, create combinatorial duplicates, assume unspecified HTTP codes and overlook test-data orchestration. A future version may add a deterministic OpenAPI parser, pairwise generator, CSV/Postman exporter and validator tests. These additions should not remove the mandatory human audit gate.
