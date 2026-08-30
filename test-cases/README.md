# Test Case Authoring Guide

Excel là artifact bắt buộc; các file Markdown trong thư mục này là nguồn review/traceability có thể chuyển sang Excel. Giữ cùng ID và field giữa Markdown, Excel, Postman và Newman.

## Canonical fields

| Field | Meaning |
| :--- | :--- |
| TC ID | Stable ID: `FR02-AI-001`, `FR10-H-001` |
| Source | `AI` hoặc `HUMAN` |
| Requirement | FR/SEC/API rule |
| Technique | EP/BVA/DT/ST/Security/Schema/CRUD |
| Priority | P0/P1/P2 |
| Preconditions | Exact data, account, role and state |
| Request/data | Method, URL, headers, body/data row |
| Expected | Status, schema, body and post-state |
| Cleanup | How to restore isolation |
| AI audit | VALID/INVALID/INCOMPLETE + reason/correction |
| Execution | PASS/FAIL/BLOCKED/NOT RUN + evidence |

## Lifecycle and counting

- AI candidate IDs use `FRxx-AI-nnn` and `Source=AI`; student extensions use `FRxx-H-nnn` and `Source=HUMAN` only after explicit student authorship/confirmation.
- Preserve every raw AI candidate for audit. Use `Correction/final ID` to map an INVALID/INCOMPLETE candidate to its corrected case instead of silently replacing history.
- Count unique TC records, not assertions or Markdown table rows. Separator/header/placeholder rows do not count.
- `AI-generated` includes retained AI candidates; `Final executable` excludes rejected/merged/unresolved candidates and includes accepted corrections plus accepted HUMAN cases.
- A design row remains `NOT RUN` until a real Postman/Newman artifact maps to its TC ID.
- HUMAN rows require a concrete `Why AI missed` analysis; AI suggestions cannot be relabeled as student-authored cases.

Do not delete invalid AI cases; preserve them in the audit/raw sheet and link to corrected final case. Human-added cases use `H` in the ID and must include `Why AI missed`.
