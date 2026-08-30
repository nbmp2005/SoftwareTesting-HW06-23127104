---
name: hw06-deliverable-sync
description: Đối soát và đồng bộ các deliverable HW06 từ artifact có thật sang main report, test summary, README và checklist. Dùng sau thay đổi test design, Postman/Newman, bug, CI/CD, skill hoặc khi số liệu báo cáo lệch nhau.
---

# HW06 Deliverable Sync (Mở rộng & Chuẩn hoá)

Skill này hoạt động như một công cụ kiểm toán chéo (Cross-check & Synchronizer), đảm bảo tính nhất quán của toàn bộ tài liệu dự án HW06 (Main Report, Test Summary, Bug Report, README). Biến repository thành một bộ hồ sơ đồng bộ tuyệt đối dựa trên nguyên tắc "Bằng chứng thật, Số liệu thật".

## Routing references
- Đọc [references/artifact-map.md](references/artifact-map.md) để chọn đúng file thao tác theo từng loại thay đổi.
- Đọc [references/consistency-rules.md](references/consistency-rules.md) trước khi tính metrics, giải quyết conflict hoặc thay đổi checklist.

## 1. Trigger Conditions / Context
- Tự động gọi ở cuối chu trình của các skill khác (sau khi sửa test design, chạy Newman, ghi Bug).
- Hoặc người dùng gọi khi phát hiện các số liệu trong báo cáo "đá" nhau (Discrepancy) và cần đối soát lại toàn bộ repo.

## 2. Pre-requisites & Input Validation
- **Đầu vào bắt buộc**:
  - Truy cập toàn bộ thư mục `report/` và `test-cases/`.
  - Tham chiếu file `references/artifact-map.md` để biết bảng mapping (File nào lấy số liệu từ file nào).
- **Nguyên tắc "Nguồn sự thật" (Source of Truth)**:
  - Raw execution/Git artifacts > tool summaries > structured test-case records > report prose > placeholder.
  - LUÔN tính toán/đếm lại từ file gốc thay vì copy con số mù quáng từ report này sang report khác.

## 3. Strict Constraints & Anti-patterns (CÁC HÀNH VI BỊ CẤM)
- **Cấm ngụy tạo dữ liệu (Fabrication)**: Không tự chế ra timestamp cũ, SHA ảo, screenshot giả, URL bừa bãi, mã số sinh viên giả, version công cụ ảo hay kết quả điểm (grade).
- **Cấm đánh đồng Khái niệm (Concept Confusion)**:
  - Phải phân biệt rạch ròi: `Planned` (đã sinh thiết kế) ≠ `Implemented` (đã có script `.pm.test`) ≠ `Executed` (đã chạy ra log thật).
  - Phải phân biệt: `Assertion Failed` (đỏ trong Postman) ≠ `Genuine Bug` (Lỗi phần mềm đã verify).
- **Cấm tự tick Checklist ảo**: Trên file README checklist, CHỈ ĐƯỢC tick (`[x]`) nếu từng điều kiện của dòng đó có artifact thật sự kiểm chứng được.
- **Cấm thay đổi Code/Nghiệp vụ**: Skill này chỉ làm nhiệm vụ đồng bộ tài liệu, TUYỆT ĐỐI không sinh thêm Test case, không tự chạy API thay cho sinh viên, không export PDF/Zip.
- **Cấm tự ý Push Git**: Không gọi các lệnh commit/push tự động.

## 4. Detailed Step-by-Step Workflow
1. **Đọc Artifact Map**: Nhận dạng xem vừa có sự kiện gì (vd: Mới sinh test case, hay mới chạy Newman) để chọn file Consumer tương ứng cần đồng bộ.
2. **Tính toán Metrics**:
   - Đếm structured TC records theo unique ID; không đếm header/separator/table row mù quáng.
   - Nếu đầu vào là raw Newman artifact, áp dụng `$newman-evidence-reconciler` trước khi sync execution metrics.
   - Đếm genuine bug theo lifecycle/classification trong bug report, không theo số heading hoặc failed assertions.
3. **Đối chiếu (Cross-check)**: So sánh các số liệu vừa tính được với số hiện có trong `TEST_SUMMARY.md`, `MAIN_REPORT.md` và `README.md`.
4. **Patching (Đồng bộ)**:
   - Cập nhật số mới vào các file nếu có sai lệch.
   - Giữ nguyên các dòng Placeholder chưa làm (VD: "Pending evidence") nếu chưa có data thật.
   - Cập nhật trạng thái ở `README.md` và `docs/SUBMISSION_CHECKLIST.md` chỉ theo artifact map. Nếu tick hiện có mất bằng chứng, báo `Discrepancy: Missing Evidence` thay vì âm thầm sửa lịch sử người dùng.
5. **Consistency Checks (Kiểm tra An toàn)**:
   - Áp dụng đúng phương trình/counting convention trong consistency reference; không gộp `Blocked` vào `Executed` nếu report không định nghĩa vậy.
   - Quét kiểm tra xem có vô tình phơi bày Secret Tokens ra file `.md` nào không.
6. **Báo cáo Handoff**: Liệt kê chi tiết file nào vừa bị sửa, số liệu lấy từ nguồn nào, và trường dữ liệu nào vẫn đang "Pending".

## 5. Error Handling & Edge Cases
- **Trạng thái Rejected/Merged**: Chỉ loại khỏi `Final executable` khi có field/audit mapping rõ ràng. Không suy trạng thái chỉ từ strikethrough nếu repo chưa định nghĩa convention đó.
- **Xung đột File (Data Conflict)**: Nếu phát hiện số lượng Test Case trong file Design là 35, nhưng Newman Log báo chạy 40 Test Cases, lập tức cảnh báo "Orphan Executions Detected" và dừng thao tác đồng bộ Execution để người dùng tự review.

## 6. Output Format & Synchronization
- Tuân thủ định dạng bảng và cấu trúc của từng file Consumer theo Spec HW06. Không làm xô lệch cấu trúc Markdown.

## 7. Handoff & Audit Requirements
- Cung cấp một tóm tắt ngắn về sự thay đổi của các chỉ số (ví dụ: `FR-02: Planned tăng từ 20 -> 35. Executed giữ nguyên 0`).
- Nếu user chạy skill này thủ công, kết thúc bằng cách gọi `$ai-audit-logger`. (Không log nếu đây chỉ là bước ẩn của một skill khác).
- Exit criteria: sync idempotent, sources và consumer changes được liệt kê, totals nhất quán, unresolved discrepancies được giữ rõ, và không có evidence/checkbox nào được suy diễn.
