---
name: eshop-api-test-generator
description: Trích xuất contract, lập coverage model và sinh ≥35 candidate API test cases cho một feature EShop HW06; ghi artifact và đồng bộ report nhưng không tự audit thay sinh viên hoặc bịa kết quả chạy.
---

# EShop API Test Generator (Mở rộng & Chuẩn hoá)

Skill này chịu trách nhiệm sinh kịch bản kiểm thử (test design) có tính truy vết (traceability) cao cho chính xác một feature (FR-02, FR-10, hoặc FR-15) dựa trên requirements và API specification của EShop HW06. Mục tiêu bài tập là ít nhất 35 AI-generated candidate cases cho mỗi API. Nếu không thể đạt 35 mà không padding, phải bàn giao trạng thái `PARTIAL` và coverage gap; không được mô tả deliverable là hoàn tất.

## Routing references
- Luôn đọc [references/output-schema.md](references/output-schema.md) trước khi tạo/sửa cases.
- Đọc [references/eshop-rules.md](references/eshop-rules.md) khi scope là FR-02/FR-10/FR-15; đối chiếu lại với spec thật, không coi reference là nguồn cao hơn spec.
- Đọc [references/quality-gates.md](references/quality-gates.md) trước khi handoff.

## 1. Trigger Conditions / Context
- Kích hoạt khi người dùng yêu cầu "sinh test case", "viết test design", "generate test cases" cho một trong các feature FR-02, FR-10, FR-15.
- Cần chạy khi hệ thống chưa có đủ số lượng test case yêu cầu, hoặc cần rà soát độ bao phủ của một API mới.

### Operating modes

- **Generate:** tạo candidate cases mới từ contract/coverage model.
- **Coverage review:** không sinh hàng loạt; kiểm tra traceability, duplicate và gaps của cases hiện có.
- **Revise:** sửa candidate AI cases theo feedback nhưng giữ raw history/correction mapping.
- **Human-audit support:** phân tích và đề xuất nhãn; không ghi quyết định cuối hoặc `Source=HUMAN` khi sinh viên chưa xác nhận.

## 2. Pre-requisites & Input Validation
- **Đầu vào bắt buộc**:
  - Tên Feature rõ ràng.
  - File Requirements và API Specification tương ứng (nguồn chân lý).
- **Validation**:
  - Luôn phải đọc file tham chiếu (ví dụ: `references/output-schema.md`, `references/eshop-rules.md`, `references/quality-gates.md`) TRƯỚC KHI sinh hoặc sửa test cases.
  - Tìm requirement/API spec trong workspace và nguồn người dùng đã cung cấp trước khi kết luận thiếu. Nếu vẫn thiếu phần contract cốt lõi, báo `BLOCKED: Missing Spec`; không suy đoán field/business rule.
  - Ghi phiên bản/link/commit của spec nếu có. Nếu không biết version, đánh dấu pending thay vì tự gắn commit.

## 3. Strict Constraints & Anti-patterns (CÁC HÀNH VI BỊ CẤM)
- **Cấm độn số lượng (Padding)**: Không được sinh ra các test case trùng lặp về mặt ngữ nghĩa (semantic duplicate) chỉ để cho đủ chỉ tiêu 35 test cases. Nếu đã bao phủ toàn bộ mà mới chỉ có 25 cases, hãy báo cáo rõ thay vì đẻ thêm rác.
- **Cấm tự duyệt thay người dùng (No Auto-Audit)**: Không bao giờ tự ý gán nhãn `VALID/INVALID/INCOMPLETE` hoặc đánh dấu test case là "human-added" (do người thêm) nếu đó là do AI sinh ra. Chỉ ghi nhãn sau khi người dùng explicit xác nhận.
- **Cấm sinh Evidence/Bug ảo**: Không được đính kèm các execution result `PASS/FAIL`, hay tạo link Bug giả, screenshot giả, hoặc commit SHA giả cho các test case vừa được thiết kế. Test case mới luôn có `Execution = NOT RUN`.
- **Cấm lấy Bug SUT làm Oracle**: Hành vi thực tế của server (SUT) không được dùng làm Expected Result (Oracle) nếu nó đi ngược lại Requirement. Requirement luôn là chân lý.

## 4. Detailed Step-by-Step Workflow
1. **Contract Inventory**: Trích xuất tất cả endpoints, actors, auth methods, headers, schemas (input/output), business rules, pre/post-conditions, và các điểm chưa rõ ràng (ambiguities).
2. **Xây dựng Coverage Models**:
   - Dùng *Equivalence Partitioning (EP)* & *Boundary Value Analysis (BVA)* cho tất cả các field đầu vào.
   - Dùng *Decision Table* cho các nghiệp vụ có điều kiện rẽ nhánh.
   - Dùng *State Matrix* cho các quy trình trạng thái (ví dụ FR-10 Order State).
3. **Security/Schema Mapping**: Đánh giá tính áp dụng của SEC-01 tới SEC-07; map rule áp dụng, giải thích rule không áp dụng, và phân định cái test được qua API với cái cần code/UI evidence. Cover success/error schema và forbidden sensitive fields.
4. **Candidate Generation**: Sinh setup, literal/named fixture data, request, expected status/body/schema/post-state và cleanup cụ thể. ID phải tuân thủ chuẩn, `Source=AI`, audit fields để trống và execution=`NOT RUN`.
5. **Traceability Review**: Review nội bộ đảm bảo mỗi test case map đúng về Requirement ID và Rule ID tương ứng.
6. **Ghi Output (Write Artifacts)**: Cập nhật trực tiếp vào đúng file test design (ví dụ `test-cases/FR-02_LOGIN.md`). Tuyệt đối KHÔNG ghi đè các case đã được review hoặc evidence của sinh viên.
7. **Validation & Sync**: Chạy quality gates. Đếm số test cases tạo ra từ dữ liệu thật, không đếm ảo. Gọi `$hw06-deliverable-sync` để cập nhật bảng `TEST_SUMMARY.md` và `MAIN_REPORT.md` (chỉ update Design Metrics, giữ nguyên Execution Metrics).

## 5. Error Handling & Edge Cases
- **Mâu thuẫn Spec**: Ghi ambiguity/working assumption riêng. Candidate phụ thuộc ambiguity phải được đánh dấu chưa executable và không tính vào `Final executable` cho tới khi sinh viên/spec owner chốt oracle.
- **Không tìm thấy File Test Design**: Nếu file đích (như `FR-02_LOGIN.md`) chưa tồn tại, tạo mới bằng template chuẩn từ `output-schema.md`.
- **Case hiện có đã được audit/chạy**: Không rewrite ID hoặc raw wording làm mất lịch sử. Thêm correction/final mapping hoặc chỉ patch field được người dùng yêu cầu.

## 6. Output Format & Synchronization
- Repo hiện dùng Markdown tables; giữ format này trừ khi người dùng yêu cầu export khác. Mỗi record phải tuân thủ toàn bộ field trong `output-schema.md`, gồm `Source`, audit lifecycle và execution evidence.
- Coverage matrix là artifact riêng với mapping modeled item → TC IDs; không suy coverage từ tổng số case.

## 7. Handoff & Audit Requirements
- Cung cấp báo cáo Handoff: Tên feature, số lượng test case vừa sinh, khoảng trống (coverage gaps) chưa thể cover, các giả định (assumptions) tạm thời, và các điểm mâu thuẫn chờ sinh viên review.
- Gọi `$ai-audit-logger` để lưu log của tác vụ sinh test design này.
- Exit status phải là `COMPLETE`, `PARTIAL` hoặc `BLOCKED`. `COMPLETE` chỉ khi target ≥35 đạt bằng cases có ý nghĩa, IDs/fields/traceability hợp lệ, raw AI cases chưa bị tự audit và report consumers đã sync.
