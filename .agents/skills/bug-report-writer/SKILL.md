---
name: bug-report-writer
description: Triage và ghi bug HW06 từ bằng chứng Postman/Newman có thật, đồng thời đồng bộ bug metrics và tham chiếu báo cáo. Không dùng để biến mọi failed assertion thành product bug.
---

# Bug Report Writer (Mở rộng & Chuẩn hoá)

Tạo hoặc cập nhật bug log vào `report/BUG_REPORT.md` dựa trên các vi phạm (violations) so với Requirement/Oracle, kèm theo bằng chứng tái hiện (reproduction evidence) rõ ràng. Skill này có nhiệm vụ phân loại (Triage) kỹ lưỡng trước khi kết luận đó là một Bug thực sự của hệ thống (Product Bug).

## Routing reference

- Đọc [references/triage-matrix.md](references/triage-matrix.md) trước khi xác nhận classification, lifecycle, evidence completeness hoặc severity.

## 1. Trigger Conditions / Context
- Được gọi sau quá trình chạy test (execution) khi phát hiện có test case `FAIL`.
- Hoặc khi người dùng yêu cầu phân tích một lỗi cụ thể và tạo Bug Report.

## 2. Pre-requisites & Input Validation
- **Đầu vào bắt buộc tối thiểu**:
  - `Test Case ID` và feature tương ứng (FR-02, FR-10, FR-15).
  - `Requirement/API rule` bị vi phạm (kèm nguồn trích dẫn).
  - Request/setup có thể tái hiện được lỗi (Steps to reproduce).
  - `Actual Result` lấy từ lần chạy thật (Status/Body/Post-state) và evidence tái hiện đủ để kiểm tra nhận định.
  - `Expected Result` dựa trên Spec (KHÔNG dựa trên hành vi của Server hiện tại).
- **Validation**:
  - Requirement oracle, request/setup và actual result là điều kiện để triage. GitHub Issue + screenshot là điều kiện hoàn tất hồ sơ nộp bài, không phải điều kiện logic duy nhất để nhận diện product bug.
  - Thiếu oracle/setup/actual evidence: đưa vào **Triage Pending**. Bug đã tái hiện nhưng thiếu issue/screenshot: ghi `Confirmed — submission evidence pending`, được tính là genuine bug nhưng không tick checklist evidence.

## 3. Strict Constraints & Anti-patterns (CÁC HÀNH VI BỊ CẤM)
- **Cấm đánh tráo khái niệm Bug**: Mọi Failed Assertion không đồng nghĩa với Product Bug. Phải loại trừ các nguyên nhân: Script test bị sai (Test Bug), môi trường sập (Environment Issue), data setup bị bẩn, hoặc mô tả Spec chưa rõ ràng (Spec ambiguity).
- **Cấm bịa đặt Tỷ lệ tái hiện (Repro Rate)**: Không mặc định gán `10/10` hoặc `100%` nếu chưa có bằng chứng chạy nhiều lần. Hãy ghi đúng số lần test thử (vd: `1/1`).
- **Cấm tự ý tạo GitHub Issue/Upload ảnh**: Không gọi script tạo Issue trên Git hoặc gọi lệnh upload ảnh nếu người dùng chưa ra lệnh explicit.
- **Cấm ngụy tạo Evidence URL**: Không ghi link giả trỏ tới `image.png` nếu file ảnh đó chưa được người dùng cung cấp hoặc chụp thật.
- **Cấm tự ý thay đổi Logic Sinh Viên**: Chỉ gợi ý Severity (Nghiêm trọng) / Priority (Ưu tiên) kèm lý do. Nếu sinh viên đã điền trước, bắt buộc tôn trọng quyết định của sinh viên.

## 4. Detailed Step-by-Step Workflow
1. **Kiểm tra Nguồn**: Đọc Rule gốc trong Spec, Test Case và log Evidence (SUT commit/env nếu có).
2. **Sàng lọc (Triage)**:
   - Loại trừ lỗi Script (cú pháp, biến null).
   - Loại trừ lỗi Network (timeout, 502 Bad Gateway do sập server).
   - Chỉ xác nhận là `Product Bug` khi: `Actual != Expected` VÀ `Expected đúng theo Spec`.
3. **Định danh Bug**: Gán BUG ID tiếp theo theo format đang dùng trong report (hiện là `BUG-001`, `BUG-002`). Đảm bảo tính duy nhất, không cấp ID cho mục Triage Pending.
4. **Ghi Bug Report**:
   - Cập nhật cả `Summary row` (bảng tóm tắt) và `Detail section` (phần chi tiết) trong `report/BUG_REPORT.md`.
   - Một Bug hợp lệ phải có đủ: Title, Rule nguồn, Rationale cho Severity, Environment, Preconditions, TC liên kết, Request/Steps, Expected vs Actual, và trạng thái Evidence.
5. **Đồng bộ báo cáo**: Sau khi ghi xong, CHỈ cập nhật con số `Genuine Bug Count` trong `TEST_SUMMARY.md` và `MAIN_REPORT.md` bằng cách gọi `$hw06-deliverable-sync`.
6. **Log AI**: Gọi `$ai-audit-logger` để lưu lịch sử làm việc.

## 5. Error Handling & Edge Cases
- **Báo cáo Lỗi trùng (Duplicate Bug)**: Nếu 2 Test Cases khác nhau cùng phát hiện ra 1 nguyên nhân lỗi (ví dụ cùng sập ở 1 field chung), chỉ ghi 1 Bug duy nhất nhưng map cả 2 `TC ID` vào Bug đó.
- **Thiếu Spec / Ambiguity**: Nếu không chắc hành vi của Server là Bug hay Tính năng (do tài liệu không nói tới), KHÔNG ghi thành Bug. Tạo riêng một mục `[Q&A - Mâu thuẫn Spec]` để người dùng review.
- **Bug đã sửa hoặc không còn tái hiện**: Không xóa lịch sử. Cập nhật status, tested build và evidence retest; giữ liên kết tới lần phát hiện ban đầu.

## 6. Output Format & Synchronization
- Xuất file `report/BUG_REPORT.md` theo đúng cấu trúc Markdown chuẩn của môn học.
- TUYỆT ĐỐI không thay đổi số lượng `Executed` hay `Failed` trong Execution Metrics chỉ vì thêm 1 Bug (số đó phải được tính từ log Newman).

## 7. Handoff & Audit Requirements
- Đưa ra bản tóm tắt các Bug vừa chẩn đoán. Ghi rõ Bug nào là thật, lỗi nào là do Test/Môi trường.
- Báo cáo rõ Evidence nào (hình ảnh, log) đang bị khuyết để người dùng bổ sung trước khi nộp bài.
- Exit criteria: classification có căn cứ, summary/detail nhất quán, duplicate được hợp nhất theo root cause, genuine-bug metrics được sync, và checklist chỉ tick khi đủ Issue + screenshot.
