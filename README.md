# HW06 – AI API Testing

> Sinh viên: `[HỌ VÀ TÊN]`  
> MSSV: `[STUDENT_ID]`  
> Repository công khai: `[GITHUB_REPOSITORY_URL]`  
> Video demo Agent Skill: `[YOUTUBE_URL hoặc N/A]`

Repository này chứa hồ sơ thực hiện HW06 cho ba feature đã chọn:

| Pool | Feature | API family chính | Trạng thái |
| :--- | :--- | :--- | :--- |
| A | FR-02 – Login & account lockout | `POST /api/login` + supporting auth probes | 40 AI candidates + 5 human extensions; Postman implementation partial; chờ AI audit, iteration/setup và execution |
| B | FR-10 – Order state machine | `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel` | 47 AI + 5 human; Postman/CSV mapped 52/52; chờ fixture reset, human audit và execution |
| C | FR-15 – Product CRUD | `GET/POST/PUT/DELETE /api/products[/:id]` | 50 AI candidates; chờ human audit, human extensions, Postman implementation và execution |

Lựa chọn này hợp lệ vì lấy đúng một feature từ mỗi Pool A, B, C. Trước khi bắt đầu, phải xác nhận bộ ba không trùng với thành viên khác trong nhóm.

## Test summary

Chỉ điền số liệu từ kết quả thực tế; không suy đoán hoặc sao chép số liệu mẫu.

| Chỉ số | FR-02 | FR-10 | FR-15 | Tổng |
| :--- | ---: | ---: | ---: | ---: |
| AI-generated test cases | `40` | `47` | `50` | `137` |
| Human-added test cases | `5` | `5` | `0` | `10` |
| Final test cases | `45` | `[pending]` | `[pending]` | `[pending]` |
| Executed | `45` | `[0]` | `[0]` | `[0]` |
| Passed | `36` | `[0]` | `[0]` | `[0]` |
| Failed | `9` | `[0]` | `[0]` | `[0]` |
| Genuine bugs | `1` | `[0]` | `[0]` | `[0]` |

## Self-assessment

| No. | Criteria | Grade | Self-Assessed Grade | Evidence |
| :--- | :--- | ---: | ---: | :--- |
| 1 | API 1 – FR-02 full pipeline | 30 | `[ ]` | [Main report](report/MAIN_REPORT.md#5-fr-02--login--account-lockout) |
| 2 | API 2 – FR-10 full pipeline | 30 | `[ ]` | [Main report](report/MAIN_REPORT.md#6-fr-10--order-state-machine) |
| 3 | API 3 – FR-15 full pipeline | 30 | `[ ]` | [Main report](report/MAIN_REPORT.md#7-fr-15--product-crud) |
| 4 | Agent Skill – AI-driven test generator | 10 | `[ ]` | [Skill design](report/AGENT_SKILL_DESIGN.md) |
| **Total** | | **100** | **`[000]`** | |

## Document map

- [Kiến thức nền](docs/FOUNDATION.md)
- [Kế hoạch và hướng dẫn từng task](docs/TASK_GUIDE.md)
- [Checklist bằng chứng và đóng gói](docs/SUBMISSION_CHECKLIST.md)
- [Main report](report/MAIN_REPORT.md)
- [Test summary](report/TEST_SUMMARY.md)
- [Bug report](report/BUG_REPORT.md)
- [CI/CD report](report/CICD_REPORT.md)
- [Agent Skill design](report/AGENT_SKILL_DESIGN.md)
- [AI Critique](report/AI_CRITIQUE.md)
- [AI Audit Report](report/AI_AUDIT_REPORT.md)
- [Git commit log](report/GIT_COMMIT_LOG.md)

## Agent Skill workflow

Các skill trong `.agents/skills/` được tổ chức theo pipeline và phải cập nhật artifact trong repository, không chỉ trả nội dung để copy:

1. `eshop-api-test-generator` tạo test design có traceability cho một feature.
2. `postman-script-writer` triển khai assertion khi test case đã có oracle được review.
3. `newman-evidence-reconciler` nhập kết quả chạy thật và phân loại failure.
4. `bug-report-writer` chỉ ghi genuine bug sau triage và reproduction.
5. `hw06-deliverable-sync` đồng bộ source artifact sang main report, test summary, README và checklist.
6. `ai-audit-logger` ghi interaction hiện tại bằng prompt nguyên văn và timestamp thật.

Mọi skill phải giữ nguyên các field chưa có evidence; không được tự điền số execution, SHA, URL, screenshot, timestamp cũ hoặc kết quả giả.

Độ chặt chẽ được đo trên toàn bộ skill package (`SKILL.md` + focused references), không bằng số dòng của entrypoint. Entrypoint giữ routing/invariants; decision tables và quy tắc chi tiết nằm trong `references/` để agent chỉ tải đúng phần cần dùng.

## Required non-Markdown artifacts

Các file sau chỉ được thêm sau khi có dữ liệu/chứng cứ thật: Postman collection JSON, environment JSON đã loại secret, data files, Newman HTML, Excel test cases và summary, screenshots, sơ đồ tự vẽ PNG, PDF của report/audit/critique, và pipeline YAML.

Tên file nộp cuối: `[STUDENT_ID]_HW06_AI_API_[SELF_ASSESSED_GRADE_3_DIGITS].zip`.
