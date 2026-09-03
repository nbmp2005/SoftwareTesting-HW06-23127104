# HW06 – AI API Testing

> Sinh viên: `Nguyễn Bình Minh Phương`
> MSSV: `23127104`
> Repository công khai: [nbmp2005/SoftwareTesting-HW06-23127104](https://github.com/nbmp2005/SoftwareTesting-HW06-23127104)
> Video demo Agent Skill: https://youtu.be/eC5qsSpc4h4

Repository này chứa hồ sơ thực hiện HW06 cho ba feature đã chọn:

| Pool | Feature | API family chính | Trạng thái |
| :--- | :--- | :--- | :--- |
| A | FR-02 – Login & account lockout | `POST /api/login` + supporting auth probes | 40 AI + 5 human; Newman mapped 45/45: 36 PASS, 9 FAIL; 1 genuine bug |
| B | FR-10 – Order state machine | `PUT /api/admin/orders/:id/status`, `PUT /api/orders/:id/cancel` | 47 AI + 5 human; Newman mapped 52/52: 0 PASS, 48 FAIL, 4 BLOCKED; 1 confirmed bug |
| C | FR-15 – Product CRUD | `GET/POST/PUT/DELETE /api/products[/:id]` | 50 AI + 5 human; Newman mapped 55/55: 7 PASS, 48 FAIL; 2 confirmed bugs |

Lựa chọn này hợp lệ vì lấy đúng một feature từ mỗi Pool A, B, C. Trước khi bắt đầu, phải xác nhận bộ ba không trùng với thành viên khác trong nhóm.

## Test summary

Chỉ điền số liệu từ kết quả thực tế; không suy đoán hoặc sao chép số liệu mẫu.

| Chỉ số | FR-02 | FR-10 | FR-15 | Tổng |
| :--- | ---: | ---: | ---: | ---: |
| AI-generated test cases | `40` | `47` | `50` | `137` |
| Human-added test cases | `5` | `5` | `5` | `15` |
| Planned test cases (generated + human-added) | `45` | `52` | `55` | `152` |
| Final executable after human audit | `45` | `52` | `55` | `152` |
| Executed | `45` | `48` | `55` | `148` |
| Passed | `36` | `0` | `7` | `43` |
| Failed | `9` | `48` | `48` | `105` |
| Blocked | `0` | `4` | `0` | `4` |
| Genuine bugs | `1` | `1` | `2` | `4` |

## Self-assessment

| No. | Criteria | Grade | Self-Assessed Grade | Evidence |
| :--- | :--- | ---: | ---: | :--- |
| 1 | API 1 – FR-02 full pipeline | 30 | `30` | [Main report](report/MAIN_REPORT.md#5-fr-02--login--account-lockout) |
| 2 | API 2 – FR-10 full pipeline | 30 | `30` | [Main report](report/MAIN_REPORT.md#6-fr-10--order-state-machine) |
| 3 | API 3 – FR-15 full pipeline | 30 | `30` | [Main report](report/MAIN_REPORT.md#7-fr-15--product-crud) |
| 4 | Agent Skill – AI-driven test generator | 10 | `10` | [Skill design](report/AGENT_SKILL_DESIGN.md) |
| **Total** | | **100** | **`100`** | |

## Document map

- [Kiến thức nền](docs/FOUNDATION.md)
- [Kế hoạch và hướng dẫn từng task](docs/TASK_GUIDE.md)
- [Checklist bằng chứng và đóng gói](docs/SUBMISSION_CHECKLIST.md)
- [Main report](report/MAIN_REPORT.md)
- [Test summary](report/TEST_SUMMARY.md)
- [Bug report](report/BUG_REPORT.md)
- GitHub issues: [BUG-001](https://github.com/nbmp2005/SoftwareTesting-HW06-23127104/issues/1), [BUG-002](https://github.com/nbmp2005/SoftwareTesting-HW06-23127104/issues/2), [BUG-003](https://github.com/nbmp2005/SoftwareTesting-HW06-23127104/issues/3), [BUG-004](https://github.com/nbmp2005/SoftwareTesting-HW06-23127104/issues/4), [BUG-005](https://github.com/nbmp2005/SoftwareTesting-HW06-23127104/issues/5), [BUG-006](https://github.com/nbmp2005/SoftwareTesting-HW06-23127104/issues/6), [BUG-007](https://github.com/nbmp2005/SoftwareTesting-HW06-23127104/issues/7)
- [CI/CD report](report/CICD_REPORT.md)
- [Agent Skill design](report/AGENT_SKILL_DESIGN.md)
- [AI Critique](report/AI_CRITIQUE.md)
- [AI Audit Report](report/AI_AUDIT_REPORT.md)
- [Git commit log](report/GIT_COMMIT_LOG.md)
- [Raw Git commit log](git_commit_log.txt)

## Agent Skill workflow

Các skill trong `.agents/skills/` được tổ chức theo pipeline và phải cập nhật artifact trong repository, không chỉ trả nội dung để copy:

1. `eshop-api-test-generator` tạo test design có traceability cho một feature.
2. `postman-script-writer` triển khai assertion khi test case đã có oracle được review.
3. `newman-evidence-reconciler` nhập kết quả chạy thật và phân loại failure.
4. `bug-report-writer` chỉ ghi genuine bug sau triage và reproduction.
5. `hw06-deliverable-sync` đồng bộ source artifact sang main report, test summary, README và checklist.
6. `ai-audit-logger` ghi interaction hiện tại bằng prompt nguyên văn và timestamp thật.




