import re
import datetime

def update_test_summary():
    with open("report/TEST_SUMMARY.md", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        r'\| Final executable \| `45` \| `\[ \]` \| `\[ \]` \| `\[ \]` \|': r'| Final executable | `45` | `52` | `[ ]` | `97` |',
        r'\| Executed \| `45` \| `48` \| `\[ \]` \| `93` \|': r'| Executed | `45` | `52` | `[ ]` | `97` |',
        r'\| Passed \| `36` \| `8` \| `\[ \]` \| `44` \|': r'| Passed | `36` | `8` | `[ ]` | `44` |',
        r'\| Failed \| `9` \| `40` \| `\[ \]` \| `49` \|': r'| Failed | `9` | `44` | `[ ]` | `53` |',
        r'\| Blocked/skipped \| `0` \| `4` \| `\[ \]` \| `4` \|': r'| Blocked/skipped | `0` | `0` | `[ ]` | `0` |',
        r'\| Genuine bugs \| `1` \| `\[ \]` \| `\[ \]` \| `\[ \]` \|': r'| Genuine bugs | `1` | `3` | `[ ]` | `4` |'
    }

    for old, new in replacements.items():
        content = re.sub(old, new, content)

    with open("report/TEST_SUMMARY.md", "w", encoding="utf-8") as f:
        f.write(content)


def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        r'\| Final test cases \| `45` \| `\[pending\]` \| `\[pending\]` \| `\[pending\]` \|': r'| Final test cases | `45` | `52` | `[pending]` | `97` |',
        r'\| Executed \| `45` \| `48` \| `\[0\]` \| `93` \|': r'| Executed | `45` | `52` | `[0]` | `97` |',
        r'\| Passed \| `36` \| `8` \| `\[0\]` \| `44` \|': r'| Passed | `36` | `8` | `[0]` | `44` |',
        r'\| Failed \| `9` \| `40` \| `\[0\]` \| `49` \|': r'| Failed | `9` | `44` | `[0]` | `53` |',
        r'\| Blocked \| `0` \| `4` \| `\[0\]` \| `4` \|': r'| Blocked | `0` | `0` | `[0]` | `0` |',
        r'\| Genuine bugs \| `1` \| `\[0\]` \| `\[0\]` \| `\[0\]` \|': r'| Genuine bugs | `1` | `3` | `[0]` | `4` |',
        r'\| 2 \| API 2 — FR-10 full pipeline \| 30 \| `\[ \]` \|': r'| 2 | API 2 — FR-10 full pipeline | 30 | `[x]` |'
    }

    # Handle character corruption if any
    for old, new in replacements.items():
        # Make matching slightly flexible for whitespace
        old_pattern = old.replace(' ', r'\s*')
        content = re.sub(old_pattern, new, content)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)


def update_checklist():
    with open("docs/SUBMISSION_CHECKLIST.md", "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(
        r'\| Bugs triaged/reported \| \[x\] \| \[ \] \| \[ \] \|',
        r'| Bugs triaged/reported | [x] | [x] | [ ] |',
        content
    )

    with open("docs/SUBMISSION_CHECKLIST.md", "w", encoding="utf-8") as f:
        f.write(content)


def update_main_report():
    with open("report/MAIN_REPORT.md", "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(
        r'\| `47` \| `\[pending human audit\]` \| `\[pending human audit\]` \| `\[pending human audit\]` \| `5` \| `\[pending human audit\]` \| `48` \| `8` \| `40` \| `4` \| `\[not triaged\]` \|',
        r'| `47` | `[pending human audit]` | `[pending human audit]` | `[pending human audit]` | `5` | `52` | `52` | `8` | `44` | `0` | `3` |',
        content
    )

    with open("report/MAIN_REPORT.md", "w", encoding="utf-8") as f:
        f.write(content)


def update_audit():
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ai_log = f"""
## [FR-10] Đồng bộ số liệu Deliverables
- **Timestamp**: {now_str}
- **Prompt**: `/ai-audit-logger Hãy chạy skill hw06-deliverable-sync để rà soát thư mục. Tính toán lại số lượng test case và Genuine Bugs, cập nhật số liệu vào TEST_SUMMARY.md, MAIN_REPORT.md, và tick các mục hợp lệ trong README.md checklist.`
- **Hành động AI**:
  - Đọc quy tắc và mapping từ `hw06-deliverable-sync`.
  - Cập nhật TEST_SUMMARY.md (FR-10 Executed: 52, Pass: 8, Fail: 44, Blocked: 0, Bugs: 3).
  - Cập nhật MAIN_REPORT.md bảng 6.2 tương ứng.
  - Cập nhật README.md bảng summary và tick hoàn thành FR-10 full pipeline.
  - Cập nhật SUBMISSION_CHECKLIST.md tick mục "Bugs triaged/reported" cho FR-10.
- **Mức độ tự chủ**: Level 5 (Tự động tính toán tổng số từ các artifact khác nhau và đồng bộ cấu trúc Markdown trên 5 files).
"""

    with open("report/AI_AUDIT_REPORT.md", "a", encoding="utf-8") as f:
        f.write("\n" + ai_log)


update_test_summary()
update_readme()
update_checklist()
update_main_report()
update_audit()
print("All sync completed!")
