# AI audit entry protocol

Đọc reference này khi tạo, sửa hoặc đối soát một entry trong `report/AI_AUDIT_REPORT.md`.

## Field acquisition precedence

| Field | Preferred source | Fallback | Invalid fallback |
| :--- | :--- | :--- | :--- |
| AI tool | Runtime/product identity visible in current context | User-confirmed tool name for retrospective logs | Guessing a model/version |
| Date/time | Timestamp captured at interaction start or transcript metadata | A real timestamp captured during the same interaction, explicitly treated as session time | Current time used for an older interaction |
| Prompt | Verbatim current user message | User-supplied verbatim copy for a retrospective log | Summary, translation, HTML encoding |
| AI Output | Factual close-out summary after validation | Clearly marked partial-result summary | Planned work presented as completed |

## Exactness versus secrets

The assignment requires a verbatim prompt, but secrets must not be committed. If the prompt contains a credential:

1. Do not write the secret.
2. Replace only the sensitive value with `[REDACTED SECRET]`.
3. Add this sentence inside the Prompt block: `[Audit note: a secret value was redacted; all non-secret text is verbatim.]`
4. Tell the user the entry is necessarily not byte-for-byte identical and ask them to rotate any exposed credential.

Never silently redact ordinary text. Never omit a long prompt merely to keep the report short. Split it across fenced blocks if necessary while preserving every non-secret character.

## Interaction boundary

- One user request and the assistant work needed to fulfill it form one interaction entry.
- Internal tool calls, retries, sync steps and validations do not become separate entries.
- A later user message that changes the objective or asks for another deliverable becomes another entry.
- A correction to the assistant during an unfinished request may remain part of the same entry only when the report format can preserve both user messages verbatim; otherwise use two chronological entries.

## Duplicate and correction rules

- Treat identical `Date/time + Prompt` as a duplicate.
- Do not deduplicate merely because two prompts have similar meaning.
- Correct a historical entry only with user authorization and reliable replacement data.
- Preserve an audit note describing what was corrected; do not silently rewrite academic history.

## Output-summary checklist

The output summary should state:

- the concrete result;
- material files created or changed;
- validation actually run and its result;
- blockers or evidence not available;
- explicit non-actions when they prevent a misleading inference, such as “execution metrics were not changed.”

## Validation scenarios

| Scenario | Required behavior |
| :--- | :--- |
| Current prompt and timestamp available | Append one complete chronological entry |
| Same prompt text used on another date | Keep both entries; timestamps distinguish them |
| Exact `Date/time + Prompt` already exists | Do not append a duplicate |
| Historical prompt available but timestamp absent | Write no fabricated timestamp; request user confirmation or retain unavailable marker |
| Output validation failed | Summary must say validation failed/partial, not “completed” |
| Prompt contains a token | Redact only the token, add audit note and warn user |
| Prompt contains ordinary sensitive-looking test data | Do not silently redact unless it is genuinely a credential |
| Prompt contains triple backticks | Use a longer outer fence so Markdown remains valid |
| Skill invoked internally during a larger task | Log the parent user interaction once, not the internal invocation |
| AI task category already declared | Leave main-report declaration unchanged |

## Entry integrity checks

- Exactly one occurrence of each required label appears in the entry.
- Prompt text is inside its intended fence and cannot terminate it early.
- Chronological placement agrees with `Date/time`.
- The tool identity is a product/tool name, not an internal shell command.
- Output paths named in the summary exist or are explicitly described as pending.
- The summary does not contain unsupported pass/fail counts, URLs or SHAs.
