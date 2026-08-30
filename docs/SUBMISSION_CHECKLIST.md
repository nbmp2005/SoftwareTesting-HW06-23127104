# Submission & Evidence Checklist

## Bằng chứng bắt buộc do sinh viên tự tạo

- [ ] Screenshot Postman Console thể hiện `X-Student-Id: [STUDENT_ID]` từ lần chạy thật.
- [ ] Newman CLI/HTML report thật, hostname khớp deployment.
- [ ] Sơ đồ AI test-generator do chính sinh viên tự vẽ.
- [ ] Screenshot từng genuine bug trên GitHub Issues.
- [ ] Link repository công khai, issue, workflow run và video (nếu có) truy cập được.

## Per API

| Hạng mục | FR-02 | FR-10 | FR-15 |
| :--- | :---: | :---: | :---: |
| ≥35 AI-generated cases | [ ] | [ ] | [ ] |
| 100% labeled VALID/INVALID/INCOMPLETE | [ ] | [ ] | [ ] |
| Corrections cho invalid/incomplete | [ ] | [ ] | [ ] |
| ≥5 human-added cases + miss analysis | [ ] | [ ] | [ ] |
| Postman implementation | [ ] | [ ] | [ ] |
| Newman execution evidence | [ ] | [ ] | [ ] |
| Bugs triaged/reported | [ ] | [ ] | [ ] |

## Technical/package

- [ ] `README.md` có self-assessment và summary.
- [ ] Main report có Markdown và PDF.
- [ ] AI Audit Report có declaration, Markdown và PDF.
- [ ] AI Critique dài 200–300 English words (hoặc ngôn ngữ theo yêu cầu lớp).
- [ ] Excel test cases + test summary khớp Markdown/Newman.
- [ ] Postman collection JSON + sanitized environment/data files.
- [ ] Newman HTML report.
- [ ] Danh sách Postman features đã dùng và evidence.
- [ ] CI/CD config + report + passing/failing run screenshots/links.
- [ ] Agent skill source + pseudocode + self-drawn diagram PNG.
- [ ] Bug report + issue screenshots/links.
- [ ] Git commit log xuất từ Git.
- [ ] Không commit secret/token/current environment values.
- [ ] Không còn placeholder dạng `[TODO]`, `[URL]`, `[0]` ở deliverable cuối.
- [ ] Zip tên `[STUDENT_ID]_HW06_AI_API_[000-100].zip`.

## Consistency checks

- [ ] Tổng generated + added = final (sau khi giải thích rejected/merged cases).
- [ ] Executed = passed + failed + skipped (nếu có).
- [ ] Mọi failed test đã được phân loại: product bug/test bug/environment issue.
- [ ] Mọi bug có requirement trace và reproducible evidence.
- [ ] Commit SHA trong report trùng workflow run.
- [ ] Timestamp trong AI audit là timestamp thật của từng interaction.
- [ ] Mỗi interaction AI có thay đổi artifact đã được ghi đúng một audit entry, prompt nguyên văn.
- [ ] Số liệu trong README, main report và test summary được tính từ cùng source artifact, không copy từ placeholder.
- [ ] Không đánh dấu implemented/executed/passed hoặc genuine bug chỉ từ nội dung AI sinh.
