---
name: postman-script-writer
description: Sinh hoặc chèn Postman JavaScript assertions từ test case HW06 đã có oracle, giữ traceability TC và đồng bộ trạng thái implementation. Không dùng để bịa response hay execution result.
---

# Postman Script Writer (Mở rộng & Chuẩn hoá)

Chuyển đổi các test case đã được sinh viên review thành các script kiểm tra (assertion `pm.test`) có thể chạy trực tiếp. Khi có file collection JSON phù hợp trong repo, thực hiện cập nhật thẳng vào file thay vì chỉ trả về đoạn code snippet trong chat.

## Routing reference

- Đọc [references/assertion-patterns.md](references/assertion-patterns.md) trước khi sinh assertion hoặc patch collection. Reference định nghĩa oracle mapping, data-driven TC identity và patch-safety checks.

## 1. Trigger Conditions / Context
- Kích hoạt khi người dùng yêu cầu "viết test", "thêm assertion", "generate pm.test" cho một test case cụ thể đã có Oracle rõ ràng.
- Hoặc khi người dùng muốn map các test cases từ markdown file vào một Postman Collection JSON.

## 2. Pre-requisites & Input Validation
- **Đầu vào bắt buộc**:
  - `TC ID`, phương thức request (GET/POST/...), đường dẫn (path).
  - Các oracle áp dụng cho TC: status code và, tùy contract, content type, schema, body values, headers, hậu điều kiện/no-side-effect.
  - Trạng thái Review: Test case đó phải có dấu vết đã được người dùng audit (ví dụ: đã sửa logic, hoặc người dùng explicit xác nhận).
- **Validation**:
  - Nếu thiếu oracle bắt buộc theo spec, không tự đoán. Có thể tự đọc source spec trong workspace trước; chỉ hỏi khi không thể xác định an toàn.
  - Phải xác định đúng request mục tiêu trong collection (dựa trên tên, path, method). Nếu nhiều request trùng nhau, dừng việc patch file tự động và yêu cầu confirm.

## 3. Strict Constraints & Anti-patterns (CÁC HÀNH VI BỊ CẤM)
- **Cấm giả lập (Mocking/Fabrication)**: Không được lấy một "Response mẫu" từ log chạy thực tế rồi biến nó thành "Expected Oracle" nếu nó mâu thuẫn với Specification (Spec). Phải tin Spec hơn hành vi hiện tại của SUT.
- **Cấm che giấu lỗi (Swallowing Errors)**: Tuyệt đối không dùng `try-catch` lồng nhau để bắt lỗi mà không fail test. Assert phải rõ ràng, sai là phải báo sai.
- **Cấm Assert quá chung chung**: Ví dụ `pm.response.text() !== null` là không chấp nhận được. Phải assert đúng format, đúng value.
- **Cấm rò rỉ Secret**: Không được `console.log()` hoặc nhúng trực tiếp API keys, Bearer token thật vào trong script. Phải sử dụng cú pháp biến môi trường của Postman (`pm.environment.get("TOKEN")`).
- **Cấm sửa Script không liên quan**: Khi patch file JSON, chỉ sửa phần script `test` của đúng request được yêu cầu, cấm chạm vào setup/teardown của thư mục hoặc request khác.

## 4. Detailed Step-by-Step Workflow
1. **Phân tích Input**: Đọc kỹ test case nguồn và các Spec/Rule mà nó tham chiếu.
2. **Liệt kê Oracles**: Lên danh sách tất cả các yếu tố cần tự động hóa (status, content-type, schema, field data, business value).
3. **Sinh Assertion (Scripting)**:
   - Tạo tên test: `pm.test("[TC-ID] Should ...", function() { ... })`.
   - Viết assert Status trước: `pm.response.to.have.status(...)`.
   - Trích xuất JSON body theo pattern reference. Không giả định test status thất bại sẽ chặn JavaScript/test block tiếp theo; parse failure phải tạo assertion failure rõ ràng và consumer phải guard an toàn.
   - Viết các assert cho schema và body, bám sát các điều kiện biên.
4. **Patching Collection (Nếu có quyền/Có file)**:
   - Locate đúng object request trong file `*.postman_collection.json`.
   - Cập nhật an toàn mảng `event` loại `test`.
   - Đảm bảo file JSON vẫn parse được và diff chỉ chạm target request/event dự kiến.
5. **Ghi lại Mapping**: Cập nhật mapping từ `TC ID` -> `Request Name/Script` vào tài liệu.
6. **Đồng bộ & Báo cáo**: Chạy `$hw06-deliverable-sync` để cập nhật trạng thái "Implemented" vào `MAIN_REPORT.md`.

## 5. Error Handling & Edge Cases
- **Không parse được Response Body**: Nếu API trả về `204 No Content` hoặc `HTML` thay vì JSON, phải handle ngoại lệ (vd: check Content-Length hoặc header trước) để không gây lỗi `JSON.parse` làm sập toàn bộ test script.
- **Dữ liệu mảng (Array data)**: Nếu assert trên list/array, cần handle trường hợp mảng rỗng hoặc thứ tự mảng không ổn định bằng cách tìm theo filter thay vì hardcode index `[0]`.
- **Data-driven request**: Giữ TC ID trong iteration data và đưa TC ID vào tên assertion để Newman có thể map từng scenario.
- **Post-state cần request thứ hai**: Tạo verification flow có mapping rõ; không coi response của mutate request là đủ chứng minh persistence nếu requirement đòi kiểm tra trạng thái lưu.

## 6. Output Format & Synchronization
- Trả về mã nguồn snippet `javascript` trong block code để người dùng dễ review.
- Thông báo rõ: File `collection.json` đã được patch thành công ở những dòng nào, hoặc lý do không thể patch (do request name bị trùng/không tìm thấy).

## 7. Handoff & Audit Requirements
- Yêu cầu sinh viên import file Collection vào Postman, chạy thử (Send) để verify syntax, và kiểm tra xem test result hiển thị đúng tên TC-ID chưa.
- Ghi log lại tác vụ bằng `$ai-audit-logger` với prompt gốc.
- Exit criteria: oracle-to-assertion mapping đầy đủ, TC identity ổn định, JSON parse được, unrelated collection content không đổi, không có secret, và chưa tuyên bố PASS khi chưa chạy thật.
