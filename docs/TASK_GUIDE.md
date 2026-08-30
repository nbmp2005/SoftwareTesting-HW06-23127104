# Hướng dẫn thực hiện toàn bộ HW06

## 1. Quyết định scope

### Đánh giá FR-02 / FR-10 / FR-15

| Tiêu chí | FR-02 | FR-10 | FR-15 |
| :--- | :--- | :--- | :--- |
| Pool | A | B | C |
| Kỹ thuật nổi bật | Partition, boundary, decision table | State transition, actor/authorization | CRUD, validation, authorization |
| Security | Enumeration, token/data exposure | IDOR, role enforcement | SEC-02/03/04/05 |
| Khả năng đạt ≥35 cases | Cao | Cao | Rất cao |
| Rủi ro thực thi | Time/reset lock state | Fixture state phức tạp | Cleanup và category dependency |

**Kết luận:** hợp lý, cân bằng và có khả năng thể hiện đủ kỹ thuật. Xác nhận bằng văn bản rằng bộ ba không trùng trong nhóm. Trong scope, mô tả FR-10 và FR-15 là API family/feature với nhiều endpoint liên quan.

## 2. Cấu trúc công việc 10 giờ tham khảo

| Khối | Thời lượng | Outcome |
| :--- | ---: | :--- |
| Setup, đọc spec, chọn API | 0.75h | Scope + traceability ban đầu |
| AI generation cho 3 API | 2.0h | ≥35 raw cases/API |
| Human audit + correction | 2.0h | Mọi raw case có label/reason |
| Human extension | 0.75h | ≥5 case mới/API + miss analysis |
| Postman implementation/execution | 2.0h | Collection + real evidence/report |
| CI/CD hai runs | 1.0h | Pass/fail runs + links/screenshots |
| Agent Skill + self-drawn diagram/video | 0.75h | Skill/design/demo evidence |
| Report, audit, critique, package | 0.75h | Submission complete |

## 3. Phase 0 – Setup và baseline

1. Fork/clone SUT vào public repository của bạn theo quy định môn học.
2. Chạy backend local theo `setup_guide.md`; xác nhận `http://localhost:3000`.
3. Ghi commit SHA của SUT được test.
4. Tạo environment Postman: `baseUrl`, `studentId`, `adminEmail`, `userEmail`; secret để local/current value và không commit.
5. Gắn collection-level pre-request script cho `X-Student-Id`.
6. Tạo fixtures riêng: users cho lockout, orders ở từng state, category/product dùng cho CRUD.
7. Chụp screenshot console header thật sau khi chạy request.

Exit criteria: SUT chạy được, baseline smoke test pass, dữ liệu có cách reset, không commit secret.

## 4. Phase 1 – AI generation từng bước

Thực hiện riêng cho từng feature và lưu nguyên prompt/output vào AI Audit Report.

### Prompt sequence

1. **Contract extraction:** yêu cầu AI chỉ trích xuất endpoints, inputs, preconditions, outputs, business rules, FR/SEC trace và ambiguities.
2. **Parameter model:** yêu cầu partitions + boundaries cho mọi path/query/header/body field.
3. **Behavior model:** FR-02 dùng decision table; FR-10 dùng transition matrix; FR-15 dùng CRUD lifecycle/dependency model.
4. **Security model:** map SEC-01–SEC-07 và chỉ chọn requirement áp dụng; thêm authentication, authorization/IDOR, injection, output exposure.
5. **Schema model:** success/error schemas, required/forbidden fields và types.
6. **Case generation:** sinh ≥35 cases/API theo schema bảng trong `test-cases/*.md`, mỗi case có requirement trace và nguồn technique.
7. **Coverage review:** yêu cầu AI chỉ ra uncovered rule/partition/transition, không tự tuyên bố coverage 100% nếu không có trace.

Không gửi password/token thật cho AI. Mỗi prompt phải đủ context nhưng chỉ tập trung một bước.

## 5. Phase 2 – Human audit

Với từng AI case:

1. Đối chiếu endpoint và oracle với requirement/API spec.
2. Kiểm tra precondition có thể tạo được.
3. Kiểm tra test data cụ thể, không dùng từ mơ hồ như “invalid data”.
4. Kiểm tra expected status/body/state và forbidden effects.
5. Kiểm tra duplicate hoặc combination không mang thêm giá trị.
6. Gắn `VALID`, `INVALID` hoặc `INCOMPLETE` và lý do cụ thể.
7. Với case sai/thiếu, giữ lịch sử rồi ghi correction/final ID.

Exit criteria: 100% AI cases có label + reason; final cases đều executable và traceable.

## 6. Phase 3 – Human extension

Thêm tối thiểu 5 case do chính bạn thiết kế cho mỗi API. Gợi ý hướng tìm, không dùng như kết quả đã kiểm chứng:

- FR-02: chính xác lần sai thứ 3; thời điểm 29/30/31 giây; login đúng sau một/two failures reset counter; response không lộ password; account enumeration consistency.
- FR-10: user cancel `shipping`; transition từ cả hai final states; replay transition; state unchanged after rejection; concurrent admin transitions.
- FR-15: user token gọi mutate endpoint; 255/256 Unicode characters; invalid/nonexistent `category_id`; update one product does not alter another; stored XSS payload displayed safely.

Với mỗi case, viết `Why AI missed`: thiếu context/prompt, combinatorial limitation, time/state complexity, implicit oracle hoặc model assumed common behavior instead of this spec.

## 7. Phase 4 – Implement và execute

1. Map mỗi final TC thành Postman request/data row; giữ TC ID trong request name hoặc data.
2. Assertion tối thiểu: status, content type, schema, business body và postcondition.
3. Dùng setup request/script để lấy token/IDs; cleanup resource do test tạo.
4. Chạy folder riêng khi debug, sau đó full collection từ clean seed.
5. Chạy Newman CLI và HTML reporter; lưu command, timestamp, hostname, summary và artifact.
6. Đối chiếu số case trong Excel/Markdown/Postman/Newman; giải thích nếu một test case có nhiều assertions.

Không đánh dấu bug chỉ vì test fail. Reproduce độc lập, đối chiếu spec, loại lỗi test/environment trước.

## 8. Phase 5 – Bug reporting

Cho mỗi genuine bug:

1. Tạo issue theo template trong `report/BUG_REPORT.md`.
2. Ghi requirement violated, environment, precondition, exact steps/request, actual/expected, severity/priority.
3. Đính screenshot thật và Newman/Postman evidence nếu có.
4. Tạo GitHub Issue công khai, chép URL về report.
5. Ghi AI phát hiện hay con người phát hiện; nếu AI bỏ sót, giải thích.

## 9. Phase 6 – CI/CD

Workflow cần chạy deterministic. Hai minh chứng:

- **Passing run:** toàn bộ final suite pass trên một commit xác định.
- **Failing run:** một test được cố ý làm fail để chứng minh quality gate; ghi rõ thay đổi và link commit/run.

Upload Newman HTML/JUnit dù test fail bằng điều kiện `always()`. Không dùng screenshot giả hoặc URL placeholder trong bản nộp cuối.

## 10. Phase 7 – Agent Skill từ đầu đến cuối

### Ba phương án

1. **Prompt-only skill:** `SKILL.md` chứa workflow và output schema. Nhanh, dễ demo, phù hợp 10 giờ; độ deterministic vừa phải.
2. **Skill + references (được chọn trong repo):** entrypoint ngắn, tách EShop rules, output schema và prompt/audit workflow. Cân bằng giữa tái sử dụng và traceability.
3. **Skill + deterministic scripts:** thêm parser OpenAPI/Markdown và exporter CSV/Postman. Mạnh nhất nhưng tốn thời gian; chỉ nên làm khi parser có test và spec ổn định.

Repo dùng phương án 2 cho generator và bổ sung các skill close-out để toàn bộ deliverable luôn nhất quán. Quy trình build:

Không đánh giá skill bằng số dòng của riêng `SKILL.md`. Với repo này, `SKILL.md` giữ trigger, workflow, invariants và routing; các decision table/format/edge-case dễ sai nằm trong `references/`. Khi review phải tính và kiểm tra toàn bộ package, đồng thời xác nhận mọi reference link được route từ entrypoint.

1. Xác định trigger và boundary: generate **test design**, không tự bịa execution evidence.
2. Định nghĩa input bắt buộc: spec, feature, student-selected scope; optional: minimum case count, output path.
3. Trích xuất contract và ghi ambiguities.
4. Tạo coverage models trước khi sinh cases.
5. Sinh raw cases với source=`AI`, audit fields để trống cho human.
6. Chạy quality gates: unique ID, trace, concrete data/oracle, coverage matrix, ≥35 target.
7. Validate skill bằng `quick_validate.py`.
8. Demo trên một API; quay video thao tác và output thực tế.
9. Tự vẽ sơ đồ dựa trên các khối thiết kế trong report. Không dùng hình do AI sinh.

### Skill pipeline và auto-update

| Giai đoạn | Skill chính | Artifact nguồn | File được tự đồng bộ |
| :--- | :--- | :--- | :--- |
| Generate/design | `eshop-api-test-generator` | `test-cases/*.md` | feature section trong main report, design metrics trong test summary/README |
| Implement Postman | `postman-script-writer` | collection/environment/data files | main report phần implementation/Postman features |
| Execute | `newman-evidence-reconciler` | Newman JSON/JUnit/HTML/CLI thật | test summary, main report, README, checklist |
| Triage bug | `bug-report-writer` | requirement + reproduction evidence | bug report và genuine-bug metrics |
| Reconcile | `hw06-deliverable-sync` | tất cả artifact liên quan | mọi consumer bị ảnh hưởng |
| Audit AI | `ai-audit-logger` | transcript hiện tại + timestamp thật | AI audit và AI declaration |

Close-out của một task có thay đổi file phải chạy theo thứ tự: cập nhật artifact nguồn → validate → `hw06-deliverable-sync` → `ai-audit-logger`. Chỉ log một entry cho interaction; không log riêng từng tool call nội bộ.

## 11. Phase 8 – Commit discipline

Tạo commit nhỏ theo từng bước; ví dụ:

```text
docs(scope): select FR-02 FR-10 FR-15
test(fr02): add AI-generated login cases
test(fr02): audit and correct login cases
test(fr02): add human security cases
test(fr02): implement and execute Postman tests
```

Lặp pattern cho FR-10/FR-15, rồi commit CI, skill và report. Xuất log thật ở cuối; không tự gõ SHA.

## 12. Definition of Done

- Đúng 3 feature thuộc A/B/C, không trùng nhóm.
- Mỗi API ≥35 AI-generated cases, 100% audited, ≥5 human-added cases.
- Full execution có `X-Student-Id` và Newman HTML thật.
- Genuine bugs có Markdown + GitHub Issue + screenshot.
- Có Postman feature list, CI/CD report và hai run thật.
- Agent generator có skill, pseudocode, video optional, diagram do bạn tự vẽ.
- AI Critique 200–300 words và Audit Report đầy đủ.
- README summary/self-grade nhất quán; zip đúng tên; không còn placeholder bắt buộc.
- Sau mỗi task AI có thay đổi vật chất, artifact nguồn và các report consumer đã được đồng bộ; các field thiếu evidence vẫn được đánh dấu pending.
