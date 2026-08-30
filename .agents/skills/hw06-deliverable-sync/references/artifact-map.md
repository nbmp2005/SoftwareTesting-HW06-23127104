# HW06 artifact synchronization map

Chỉ đọc các hàng liên quan tới thay đổi hiện tại.

| Change/source artifact | Required consumers | Update allowed from evidence | Never infer |
| :--- | :--- | :--- | :--- |
| `test-cases/FR-02_LOGIN.md`, `FR-10_ORDER_STATE.md`, `FR-15_PRODUCT_CRUD.md` | matching section in `report/MAIN_REPORT.md`; design rows in `report/TEST_SUMMARY.md`; summary rows in `README.md` | AI-generated/human-added/final counts, audit-label counts, technique/coverage notes, traceable TC IDs; only count records with explicit ID/Source | execution/pass/fail/bug counts |
| Postman collection/environment/data files | `report/MAIN_REPORT.md` §8 and matching feature implementation notes | paths, request/TC mapping, features demonstrably present, sanitized-variable strategy | successful execution, screenshots, host, tool versions |
| Newman CLI/JSON/HTML/JUnit evidence | `report/TEST_SUMMARY.md`; `report/MAIN_REPORT.md` feature §execution and §8; `README.md`; checklist | run metadata, executed/pass/fail/skipped, report path, real host/command if present | bug classification, missing metadata, fabricated screenshots |
| Confirmed entries in `report/BUG_REPORT.md` plus reproduction evidence | `report/TEST_SUMMARY.md`; `report/MAIN_REPORT.md` §9 and feature bug counts; `README.md`; checklist | genuine bug count, IDs, classifications, evidence paths | turning raw failures into bugs |
| CI workflow and real run evidence | `report/CICD_REPORT.md`; `report/MAIN_REPORT.md` §10; checklist; README document/evidence links | workflow path/config, real commit/run/artifact links and statuses | SHA/link/status absent from evidence |
| `.agents/skills/**` | `report/AGENT_SKILL_DESIGN.md`; `report/MAIN_REPORT.md` §11; `README.md` document map or skill inventory; relevant guide | actual architecture/file tree, validation command/result, capability boundaries | self-drawn diagram, demo URL, behavioral success not tested |
| `report/AI_AUDIT_REPORT.md` | `report/MAIN_REPORT.md` §2 and feature audit references | actual tools/tasks declared and stable entry references | missing old timestamps/prompts/output |
| Git history | `report/GIT_COMMIT_LOG.md`; main/CI references when applicable | exact command output and SHA mappings | future commits or uncommitted work |

## Counting conventions

- Count one test case per unique executable TC row/record, not per assertion.
- `AI-generated`: `Source=AI`, including later rejected cases if raw audit history is retained. Explain how rejected/merged cases affect `Final executable`.
- `Human-added`: only cases the student explicitly authored/confirmed as human extension.
- `Final executable`: accepted/corrected candidate cases plus accepted human-added cases, excluding rejected/merged cases.
- Audit totals apply only to AI-generated cases and should sum to AI-generated once human audit is complete.
- Do not mark `≥35` or `≥5` satisfied from a template placeholder.
- Use [consistency-rules.md](consistency-rules.md) for lifecycle, conflict and idempotency decisions; this file only routes sources to consumers.
