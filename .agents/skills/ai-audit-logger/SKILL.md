---
name: ai-audit-logger
description: Ghi hoặc đối soát log tương tác AI cho HW06 bằng prompt nguyên văn, timestamp thật và output có căn cứ; đồng bộ phần khai báo AI liên quan. Dùng khi kết thúc một tác vụ AI hoặc khi người dùng yêu cầu sửa AI Audit Report.
---

# AI Audit Logger (Mở rộng & Chuẩn hoá)

Skill này chịu trách nhiệm ghi lại minh bạch lịch sử tương tác giữa sinh viên và AI (Audit Logs) vào báo cáo `report/AI_AUDIT_REPORT.md` nhằm mục đích truy xuất, truy nguyên và chứng minh tính hợp lệ (academic integrity) cho HW06.

## Routing reference

- Luôn đọc [references/audit-entry-protocol.md](references/audit-entry-protocol.md) trước khi append hoặc sửa một audit entry. Reference này định nghĩa nguồn dữ liệu, interaction boundary, xử lý secret và quy tắc chống trùng.

## 1. Trigger Conditions / Context
- Tự động gọi (kích hoạt ngầm) ở cuối một task phức tạp của AI (như gen test, patch collection, triaging bug).
- Hoặc khi người dùng trực tiếp yêu cầu "Lưu log lại", "Ghi log đoạn chat vừa rồi vào AI Audit".

## 2. Pre-requisites & Input Validation
- **Đầu vào bắt buộc**:
  - `Prompt nguyên văn`: Từ câu hỏi/yêu cầu của người dùng.
  - `Tên AI Tool`: (ví dụ: ChatGPT, Claude, Gemini, hoặc tên của Agent hiện tại).
  - `Timestamp`: Thời gian thật thuộc interaction; ưu tiên timestamp được chụp lúc bắt đầu hoặc metadata transcript.
  - `AI Output`: Bản tóm tắt các việc AI đã làm.
- **Validation**:
  - Nếu transcript hiện tại bị mất hoặc không thể truy xuất được prompt gốc, phải báo lỗi và yêu cầu người dùng cung cấp lại bằng tay. KHÔNG tự chế ra một câu prompt giả mạo.

## 3. Strict Constraints & Anti-patterns (CÁC HÀNH VI BỊ CẤM)
- **Cấm Encode/Làm sai lệch Prompt**: Giữ nguyên mọi dấu câu, lỗi chính tả, thẻ HTML/Markdown, đường dẫn trong Prompt người dùng. CẤM tóm tắt hoặc dịch lại prompt. Ngoại lệ duy nhất là secret phải được thay đúng vị trí bằng marker công khai theo protocol; không được redaction âm thầm.
- **Cấm Bịa Timestamp**: Bắt buộc dùng định dạng ISO 8601 kèm timezone (vd: `2024-10-31T15:30:00+07:00`). Nếu không có timezone/giờ hệ thống, đánh dấu `[TIMESTAMP UNAVAILABLE]` và nhờ user xác nhận, tuyệt đối CẤM lấy giờ hiện tại làm giờ của một interaction đã diễn ra từ hôm qua.
- **Cấm Đoán Model**: Nếu không chắc AI tool nào đã chạy (trong trường hợp log hồi cứu), ghi `Unknown - User Input Required`. Cấm điền bừa tên một tool bất kỳ.
- **Cấm Ghi đè Lịch sử**: Append (nối thêm) log mới vào cuối danh sách. CẤM sửa đổi, xóa, hoặc làm sai lệch các log đã ghi trước đó (trừ khi có lệnh trực tiếp và rõ ràng từ người dùng).
- **Cấm Ghi Log Rác (Internal Tools)**: Không ghi từng lệnh tool call nội bộ (vd `view_file`, `grep`) thành các audit log riêng. Chỉ ghi 1 log tổng cho toàn bộ prompt của người dùng.
- **Cấm Lộ Secret**: Không ghi credential vào repo. Nếu prompt chứa secret, áp dụng quy trình redaction có audit note trong reference và cảnh báo người dùng rotate credential; không được tuyên bố prompt vẫn byte-for-byte nguyên văn.

## 4. Detailed Step-by-Step Workflow
1. **Chụp mốc thời gian**: Khi skill được kích hoạt cho interaction hiện tại, ghi nhận timestamp ISO 8601 có timezone trước các thao tác close-out. Với log hồi cứu, chỉ dùng transcript metadata hoặc timestamp do người dùng xác nhận.
2. **Thu thập Dữ liệu**: Đọc transcript/query state để lấy nguyên văn prompt, tool identity và phạm vi interaction theo protocol.
3. **Kiểm tra Cấu trúc File**: Đọc file `report/AI_AUDIT_REPORT.md` (hoặc tạo theo template nếu chưa có).
4. **Phát hiện Trùng lặp (De-duplication)**: Quét các log hiện tại. Nếu cặp `Date/time` + `Prompt` đã tồn tại thì bỏ qua, không ghi đè.
5. **Định dạng Entry**: Ghi đúng 4 field bắt buộc theo chuẩn của bài tập:

   ````markdown
   - Name of the AI tool: <actual tool name>
   - Date/time: <real ISO-8601 timestamp with timezone>
   - Prompt:
   ```
   (Nguyên văn user prompt)
   ```
   - AI Output:
   ```
   (Tóm tắt trung thực những thao tác AI đã thay đổi ở file nào)
   ```
   ````
6. **Cập nhật Main Report**: Nếu đây là một loại task AI hoàn toàn mới chưa từng được khai báo, cập nhật mô tả loại task đó vào phần **AI declaration** của `report/MAIN_REPORT.md`.
7. **Cross-check**: Đảm bảo entry mới có đủ 4 trường, output chỉ nói việc đã hoàn thành, và Markdown không bị phá vỡ.

## 5. Error Handling & Edge Cases
- **Prompt quá dài**: Không cắt prompt vì lý do thẩm mỹ hoặc số dòng. Chia thành nhiều fence liên tiếp nếu cần, nhưng giữ đủ mọi ký tự không phải secret. Nếu hệ thống thực sự không còn toàn bộ prompt, ghi blocker thay vì gắn nhãn “truncated” cho một bản không thể kiểm chứng.

## 6. Output Format & Synchronization
- Thông báo nhẹ nhàng: Đã lưu Audit Log thành công với Timestamp nào.
- KHÔNG thay đổi các chỉ số thực thi test (`Execution Metrics`) trong các file báo cáo khác. Việc ghi log chỉ là hành chính, không chứng minh test đã passed/failed.

## 7. Handoff & Audit Requirements
- Nếu thiếu dữ liệu (đặc biệt là Timestamp), báo cáo blocker để người dùng cung cấp thay vì tự đóng task.
- Thông báo rõ đường dẫn file `AI_AUDIT_REPORT.md` để user có thể click vào kiểm tra.
- Exit criteria: entry xuất hiện đúng một lần, có đủ bốn field bắt buộc, timestamp có provenance, secret không bị commit và AI declaration chỉ đổi khi có task category mới.
