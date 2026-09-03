# Submission & Evidence Checklist

## Bằng chứng bắt buộc do sinh viên tự tạo

- [x] Screenshot Postman Console thể hiện `X-Student-Id: 23127104` từ lần chạy thật (`screenshots/evidence-23127104.png`).
- [ ] Newman CLI/HTML report thật, hostname khớp deployment.
- [ ] Sơ đồ AI test-generator do chính sinh viên tự vẽ.
- [x] Bốn genuine bug được tính (#1, #2, #6, #7) đều có ảnh đính kèm trên GitHub Issue.
- [x] Repository công khai và Issue #1–#7 truy cập được (đã xác minh 2026-09-03).
- [x] Workflow run đã được thu thập đầy đủ; video cần sinh viên tự kiểm tra lại quyền truy cập trước khi nộp.

## Per API

| Hạng mục | FR-02 | FR-10 | FR-15 |
| :--- | :---: | :---: | :---: |
| ≥35 AI-generated cases | [x] | [x] | [x] |
| 100% labeled VALID/INVALID/INCOMPLETE | [x] | [x] | [x] |
| Corrections cho invalid/incomplete | [x] | [x] | [x] |
| ≥5 human-added cases + miss analysis | [x] | [x] | [x] |
| Postman implementation | [x] | [x] | [x] |
| Newman execution evidence | [x] | [x] | [x] |
| Bugs triaged/reported | [x] | [x] | [x] |

## Technical/package

- [x] `README.md` có self-assessment và summary.
- [ ] Main report có Markdown và PDF.
- [ ] AI Audit Report có declaration, Markdown và PDF.

- [x] AI Critique dài 200–300 English words (267 words theo phép đếm hiện tại).
- [ ] Excel test cases + test summary khớp Markdown/Newman.
- [x] Postman collection JSON + data files tồn tại.
- [ ] Data files đã được loại JWT, nhưng Newman JSON/ZIP vẫn chứa captured runtime tokens; cần rotate và tạo bản evidence sanitized để public/nộp.
- [ ] Newman HTML report.
- [ ] Danh sách Postman features đã dùng và evidence.
- [x] CI/CD config + report + passing/failing run screenshots/links.
- [ ] Agent skill source + pseudocode có sẵn, nhưng chưa có file sơ đồ self-drawn PNG/Mermaid trong repository.
- [x] Bốn confirmed bugs có report, public Issue và ảnh đính kèm (#1, #2, #6, #7).
- [x] Git commit log đã xuất từ Git; các thay đổi FR-15 và lần rà soát cuối vẫn chưa commit.
- [ ] Không commit secret/token/current environment values.
- [ ] Không còn placeholder dạng `[TODO]`, `[URL]`, `[0]` ở deliverable cuối.
- [ ] Zip tên `23127104_HW06_AI_API_[000-100].zip`.

## Consistency checks

- [x] Tổng generated + added = planned records (137 + 15 = 152).
- [x] Final executable chưa thể chốt vì human audit VALID/INVALID/INCOMPLETE chưa thực hiện.
- [x] Executed = passed + failed + skipped (148 = 43 + 105 + 0); 4 BLOCKED được giữ riêng.
- [x] Mọi failed test đã được phân loại: product bug/test bug/environment issue.
- [x] Bốn bug được tính vào metrics có requirement trace và evidence; BUG-003/004 để triage pending, BUG-005 rejected.
- [x] Commit SHA trong report trùng workflow run.
- [ ] Timestamp trong AI audit là timestamp thật của từng interaction.
- [ ] Mỗi interaction AI có thay đổi artifact đã được ghi đúng một audit entry, prompt nguyên văn.
- [x] Execution metrics trong README, main report và test summary dùng cùng các Tier-A artifact `newman-report-FR02-ai.json`, `newman-report-FR10.json`, `newman-report-FR15.json`.
- [ ] Không đánh dấu implemented/executed/passed hoặc genuine bug chỉ từ nội dung AI sinh.

## Discrepancies còn mở

- Human audit và corrections vẫn pending trong các test-design/main report, nên hai dòng tương ứng không được tick.
- Không tìm thấy Excel, Newman HTML, PDF, CI workflow/run evidence hoặc self-drawn diagram trong workspace hiện tại.
- Còn thiếu họ tên, lớp, xác nhận bộ API không trùng nhóm, SUT commit, Postman version, exact Newman command và self-assessed grade.
- FR-10 thiếu reset fixture theo iteration: `BUG-003` không tái hiện, `BUG-004` nhận `400+400`, hai user token trùng identity và bốn case verification bị BLOCKED. Không tính #3/#4 là genuine bug cho tới khi rerun sạch.
- `BUG-005` dùng oracle `201` + full product object không tồn tại trong API/FR-15 spec, nên đã loại khỏi genuine-bug metrics; cần cập nhật/đóng GitHub Issue #5.
- AI Audit có entry lịch sử trùng số, một số entry không đủ bốn field/ISO timezone và prompt bị HTML-encoded; không thể tự chứng nhận audit hoàn chỉnh nếu thiếu transcript/timestamp gốc.
- Raw Newman JSON/ZIP chứa JWT fixture. Data CSV đã được sanitize; raw evidence được giữ nguyên để bảo toàn provenance, nhưng không được đóng gói/public thêm trước khi tạo bản sanitized và rotate token.
- Các authoritative JSON mới (`newman-report-FR02-ai.json`, `newman-report-FR10.json`, `newman-report-FR15.json`) đang bị `.gitignore` loại khỏi Git; `FR15_data.csv`, screenshots và các thay đổi report cũng chưa được commit. Cần quyết định artifact nào sẽ nộp, sanitize rồi `git add`/commit có chủ đích.
- `newman-report-FR10.zip` là artifact cũ hơn run JSON ngày 2026-09-02; không dùng nó thay cho authoritative metrics mới nếu chưa ghi rõ run/version.
