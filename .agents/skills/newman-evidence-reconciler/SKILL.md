---
name: newman-evidence-reconciler
description: Parse and reconcile real Newman/Postman run evidence for HW06, update execution metrics and classify failures without fabricating bugs. Use after local or CI collection runs.
---

# Newman Evidence Reconciler (Mở rộng & Chuẩn hoá)

Skill này đảm nhiệm việc phân tích (parse), đối soát (reconcile) các bằng chứng chạy thật (execution evidence) từ Newman (CLI/JSON/HTML/JUnit) hoặc file export từ Postman, nối kết quả về các Test Case IDs (TC IDs) tương ứng, sau đó đồng bộ report.

## Routing reference

- Luôn đọc [references/result-mapping.md](references/result-mapping.md) trước khi map TC, tính metrics hoặc ghi kết quả. Reference định nghĩa evidence tiers, identity precedence và thuật toán PASS/FAIL/BLOCKED/SKIPPED/UNVERIFIED.

## 1. Trigger Conditions / Context
- Chỉ kích hoạt khi có sẵn file kết quả/log thật từ Newman (ví dụ: `newman-run-report.json`, HTML report, JUnit XML) hoặc khi người dùng cung cấp text log/screenshot hợp lệ của một phiên chạy Postman/Newman.
- Tuyệt đối **không kích hoạt** khi chưa có bằng chứng thực thi chạy qua API, hoặc khi người dùng chỉ cung cấp phỏng đoán kết quả.

## 2. Pre-requisites & Input Validation
- **Đầu vào tối thiểu**: Một artifact thật có thể quy về một run cụ thể. JSON/JUnit là ưu tiên; full CLI/HTML có thể tạo kết quả một phần theo evidence tier.
- **Metadata mong muốn**: collection/environment/data paths, command, SUT commit, base host, start/end timestamp. Không phải format Newman nào cũng chứa đủ; chỉ trích trường có thật và để phần còn lại pending.
- **Mapping**: TC ID rõ ràng là điều kiện để ghi TC-level result. Artifact vẫn có thể được parse ở mức run nếu mapping chưa đủ, nhưng không được đoán mapping.
- **Validation**: 
  - Nếu thiếu timestamp thật, phải đánh dấu `[TIMESTAMP UNAVAILABLE — USER CONFIRMATION REQUIRED]`.
  - Screenshot/log một phần chỉ hỗ trợ observation tương ứng, không được dùng suy ra full-suite totals.

## 3. Strict Constraints & Anti-patterns (CÁC HÀNH VI BỊ CẤM)
- **Cấm bịa đặt số liệu**: Tuyệt đối không tự sửa số liệu test pass/fail cho khớp với chỉ tiêu (metrics) mong đợi. Số báo cáo phải là số thật đếm được từ file log.
- **Cấm tạo bug mù quáng**: Không phải mọi test fail (rớt assertion) đều là "product bug". Không chuyển thẳng sang `$bug-report-writer` nếu chưa xác minh qua human review hoặc thiếu evidence tái hiện.
- **Cấm nhầm lẫn khái niệm**: Không đồng nhất "số lượng Assertions" với "số lượng Test Cases". Một test case có thể chứa nhiều assertions. Chỉ đếm 1 TC là PASS khi toàn bộ assertions của nó PASS.
- **Cấm lộ lọt Secret**: Không bao giờ trích xuất hoặc ghi ra các secret (API keys, passwords, tokens) nằm trong environment/current values ra các artifact output.
- **Cấm giả mạo Header**: Một run parse thành công không tự chứng minh header `X-Student-Id` đã được gửi đúng. Chỉ tick yêu cầu có liên quan khi console/request evidence thể hiện rõ header đó.

## 4. Detailed Step-by-Step Workflow
1. **Kiểm tra tính hợp lệ**: Đọc file artifact. Xác minh nó tồn tại, parse được (đúng định dạng JSON/XML) và thuộc về đúng run/collection/feature của HW06.
2. **Trích xuất Metadata**: Lấy các thông tin SUT commit, environment, host, timestamp. Các trường không có dữ liệu thật thì ghi "pending", KHÔNG tự điền bằng giờ hiện tại của hệ thống.
3. **Phân tích số liệu Test Cases**:
   - Duyệt qua từng iteration/request.
   - Map chúng tới các `TC ID` theo quy ước (convention).
   - Tổng hợp số lượng test (Passed, Failed, Skipped).
4. **Phân loại kết quả (Mapping Result)**:
   - Map mỗi case theo thuật toán reference sang `PASS`, `FAIL`, `BLOCKED`, `SKIPPED` hoặc `UNVERIFIED`.
   - Nếu phát hiện Duplicate IDs hoặc Missing IDs (trong report có mà log không có hoặc ngược lại), phải highlight và báo cáo "Mismatch discrepancy".
5. **Đánh giá Thất bại (Failure Triage)**:
   - Phân loại sơ bộ các case `FAIL`: Có thể là `Test bug` (do script sai), `Environment` (môi trường chết), `Spec ambiguity` (tài liệu mô tả không rõ), hoặc `Product bug` (lỗi thật của API).
6. **Cập nhật Artifacts**: Chỉ cập nhật `Execution result/evidence` cho TC map chắc chắn; giữ raw run artifact bất biến và không ghi đè human notes.
7. **Đồng bộ báo cáo**: Thực hiện gọi `$hw06-deliverable-sync` để cập nhật các bảng tổng kết (`report/TEST_SUMMARY.md`, `report/MAIN_REPORT.md`, `README.md` và checklist).
8. **Ghi Log AI**: Gọi `$ai-audit-logger` duy nhất một lần vào cuối phiên làm việc để ghi log cho interaction hiện tại.

## 5. Error Handling & Edge Cases
- **Mất Mapping (Orphan Requests)**: Nếu có request fail/pass nhưng không map được với bất kỳ TC ID nào đã khai báo, đưa chúng vào danh sách "Unmapped Executions" và yêu cầu người dùng map lại.
- **Thiếu Data**: Nếu run bị crash giữa chừng hoặc thiếu data, chỉ parse phần data hợp lệ và đánh dấu rõ trạng thái "Incomplete run".
- **Lỗi Parse File**: Nếu file JSON bị malformed, xuất câu báo lỗi yêu cầu người dùng chạy lại `newman` và cung cấp file chuẩn.
- **Nhiều run/retry**: Không trộn kết quả khác commit/environment. Chỉ chọn authoritative rerun khi artifact hoặc người dùng xác định rõ.

## 6. Output Format & Synchronization
- Xuất báo cáo tóm tắt (Summary table) dạng Markdown với các cột: `TC ID`, `Status`, `Assertions Passed/Failed`, `Failure Reason (Sơ bộ)`.
- Đánh dấu sao (`*`) hoặc bôi đậm những TC bị mâu thuẫn giữa thiết kế và thực thi.

## 7. Handoff & Audit Requirements
- Kết thúc task, cung cấp một đoạn văn tóm tắt nêu rõ: Tên artifact/run đã đọc, độ phủ (mapping coverage), số lượng cases, discrepancy tìm thấy, failure classifications dự kiến, các files đã sửa.
- Nhắc người dùng tự kiểm tra lại những "mismatch discrepancy" và cung cấp các evidence còn thiếu trước khi chốt sổ.
- Exit criteria: evidence tier được nêu, mapping coverage được tính, totals chỉ gồm TC ID hợp lệ, `UNVERIFIED` không bị tính pass, report consumers đã sync và raw artifacts không đổi.
