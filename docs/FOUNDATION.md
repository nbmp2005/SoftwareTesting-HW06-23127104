# Kiến thức nền cho HW06 – API Testing

## 1. Tư duy cốt lõi

API test kiểm tra hợp đồng giữa client và server, không chỉ kiểm tra “status code có phải 200”. Mỗi test cần bốn phần: precondition, request, oracle kỳ vọng và postcondition. Oracle phải đến từ requirement/API specification, không đến từ hành vi hiện tại của code. Nếu đặc tả nói khóa 30 giây nhưng server khóa 180 giây, kỳ vọng vẫn là 30 giây và hành vi 180 giây là failure.

Ba lớp cần phân biệt:

- **Specification:** hệ thống phải làm gì (`README.md`, `api_specification.md`, FR, SEC).
- **Implementation:** hệ thống thực tế làm gì.
- **Test oracle:** tiêu chí quyết định pass/fail, được suy ra từ specification.

Một test tốt có thể lặp lại, độc lập, quan sát được kết quả và nêu rõ dữ liệu trước/sau. Với API có trạng thái, phải chuẩn bị fixture và cleanup; nếu không, kết quả lần chạy sau có thể khác lần đầu.

## 2. HTTP và hợp đồng API

Mỗi request gồm method, URL/path, headers, query/path parameters và body. Mỗi response gồm status, headers, body và thời gian phản hồi.

- `GET` đọc dữ liệu và về nguyên tắc không gây thay đổi state.
- `POST` thường tạo resource hoặc thực hiện command.
- `PUT` cập nhật resource/transition state; cần kiểm tra idempotency theo contract.
- `DELETE` xóa resource; cần kiểm tra quyền, resource không tồn tại và tác động liên đới.
- Nhóm status thường gặp: `2xx` thành công, `4xx` lỗi phía request/quyền, `5xx` lỗi server. Không tự áp đặt một mã cụ thể nếu spec không quy định; ghi assumption và xác minh với giảng viên/implementation contract.

**Contract/schema validation** kiểm tra chính xác kiểu, field bắt buộc, field không được phép lộ, nullability và cấu trúc lồng nhau. Ví dụ login thành công phải có token và user, nhưng response không được lộ `password`, `reset_token` hoặc dữ liệu nhạy cảm. Schema test cần tách khỏi business assertion để biết failure thuộc loại nào.

## 3. Kỹ thuật thiết kế test

### 3.1 Equivalence Partitioning

Chia miền dữ liệu thành các lớp mà hệ thống được kỳ vọng xử lý giống nhau; chọn đại diện cho từng lớp.

Ví dụ `price > 0` của FR-15:

- Valid: số nguyên dương, số dương hợp lệ theo kiểu dữ liệu được chấp nhận.
- Invalid: `0`, số âm, chuỗi không phải số, `null`, thiếu field, Boolean, số quá lớn.
- Cần làm rõ: số thập phân có hợp lệ không vì spec chỉ nói “số dương”. Ghi assumption thay vì tự bịa.

### 3.2 Boundary Value Analysis

Lỗi thường nằm sát biên. Với tên sản phẩm tối đa 255 ký tự, kiểm tra ít nhất 254, 255, 256; thêm rỗng/whitespace nếu trường bắt buộc. Với khóa tài khoản sau 3 lần sai, kiểm tra lần 1, 2, 3; trước và sau mốc 30 giây.

### 3.3 Decision Table

Dùng khi kết quả phụ thuộc nhiều điều kiện. Login có các điều kiện: email tồn tại, password đúng, tài khoản đang khóa. Mỗi rule của bảng quyết định phải dẫn đến action rõ ràng: trả token, tăng counter, khóa tài khoản hoặc từ chối.

### 3.4 State Transition Testing

FR-10 là state machine:

```text
pending -> confirmed -> shipping -> delivered
   |           |
   +---------> canceled
```

`delivered` và `canceled` là final states. User chỉ được cancel khi `pending` hoặc `confirmed`; admin cập nhật theo các transition được phép. Phải kiểm tra:

- Mỗi transition hợp lệ.
- Mỗi transition không hợp lệ, bao gồm skip, backward, self-transition và từ final state.
- Vai trò thực hiện transition.
- State không đổi sau request bị từ chối.
- Hai request đồng thời hoặc lặp lại nếu có nguy cơ race/idempotency.

### 3.5 CRUD coverage

FR-15 không chỉ là bốn happy paths. Kiểm tra create/read/update/delete, validation từng field, referential integrity của `category_id`, quyền admin, không tồn tại, update isolation, deletion effect và schema. Với update isolation, snapshot sản phẩm mục tiêu và một sản phẩm đối chứng trước request; sau update, chỉ target được đổi.

## 4. Security testing trong phạm vi bài

Phân biệt:

- **Authentication:** token có hợp lệ và đại diện đúng user không (SEC-02).
- **Authorization:** user đã xác thực có đúng role/quyền trên resource không (SEC-03, IDOR).
- **Input handling:** parameterized query chống SQL injection (SEC-05); encode output chống stored/reflected XSS (SEC-04).
- **Sensitive data:** mật khẩu không plaintext (SEC-01), response không lộ secret.
- **Token handling:** thiếu token, token sai chữ ký, hết hạn, malformed, scheme sai, token user dùng cho admin endpoint.

SQL injection test không chỉ mong “không đăng nhập được”; còn phải khẳng định server không `5xx`, không lộ SQL error và dữ liệu không bị thay đổi. IDOR test dùng hai user A/B: A không được xem/sửa/hủy resource của B. Role escalation test dùng token user thường trên endpoint admin.

Không thực hiện destructive security testing ngoài local SUT hoặc phạm vi được cho phép.

## 5. Áp dụng vào ba feature đã chọn

### FR-02

Đây là lựa chọn tốt cho partition, boundary, decision table, authentication và time-dependent behavior. Điểm khó là reset state của `login_attempts`/`locked_until` và chờ 30 giây. Nên tạo user riêng cho từng scenario hoặc có script reset database/fixture. Các oracle chính: mỗi lần sai tăng đúng 1, khóa từ lần thứ 3, khóa đúng 30 giây, lỗi không làm lộ email tồn tại, login đúng reset counter, token hợp lệ và response không lộ password.

### FR-10

Đây là lựa chọn tốt nhất để chứng minh state-transition testing. Scope nên gồm cả admin update status và user cancel vì requirement mô tả cả actor lẫn transition. Dùng data-driven testing cho ma trận `current_state × requested_state × actor`. Sau mỗi request phải đọc lại order để xác nhận postcondition.

### FR-15

Đây là lựa chọn rộng và có thể tạo nhiều test chất lượng, nhưng cần định nghĩa là **Product CRUD API family**. Scope gồm danh sách/chi tiết nếu dùng để xác minh, cùng POST/PUT/DELETE. Oracle đến từ FR-12 + FR-15 + SEC-02/03/04/05. Đặc biệt kiểm tra user thường không được mutate product, input name/price/category và update isolation.

## 6. Postman/Newman foundation

Tổ chức đề xuất:

```text
Collection
├── 00 Setup/Auth
├── FR-02 Login
├── FR-10 Order state machine
├── FR-15 Product CRUD
└── 99 Cleanup
```

Variable scopes: global (tránh dùng), collection (giá trị dùng chung), environment (`baseUrl`, `studentId`), data variable (mỗi dòng test), local variable. Không commit token/password thật. Pre-request script ở collection level gắn `X-Student-Id`; test script kiểm tra status/schema/business rule và lưu dynamic IDs.

Ví dụ pre-request script cần chính bạn chạy và chụp console thật:

```javascript
pm.request.headers.upsert({
  key: "X-Student-Id",
  value: pm.environment.get("studentId")
});
console.log("X-Student-Id attached:", pm.environment.get("studentId"));
```

Newman chạy cùng collection, environment và data file, xuất CLI + HTML/JUnit. Exit code khác 0 phải làm pipeline fail. Dữ liệu chạy phải deterministic: seed/reset database trước test và cleanup sau test.

## 7. AI-assisted testing đúng tinh thần đề

Không dùng một prompt “generate everything”. Pipeline hợp lý:

1. Trích xuất contract và assumption.
2. Lập parameter inventory và partitions.
3. Lập state/decision model.
4. Lập security mapping SEC-01–SEC-07.
5. Lập schema assertions.
6. Sinh test cases có traceability.
7. Con người audit từng case.
8. Con người bổ sung ít nhất 5 case/API mà AI bỏ sót.

Label audit:

- `VALID`: đúng requirement, executable, oracle rõ và không trùng vô ích.
- `INVALID`: mâu thuẫn spec, endpoint/data/oracle sai hoặc ngoài scope.
- `INCOMPLETE`: ý tưởng đúng nhưng thiếu precondition, data, expected result hoặc cleanup.

Không sửa đè raw AI output. Giữ `AI_TC_ID`, thêm `Audit status`, `Reason`, rồi tạo/cập nhật final test case có trace về nguồn.

## 8. CI/CD và bằng chứng

Pipeline tối thiểu: checkout → setup Node/Newman → start/reset SUT → health wait → run Newman → upload report. Hai run phải đến từ hai commit thật: một all-pass và một intentional failing test. Commit failing chỉ thay expectation/test fixture có chủ đích, ghi rõ đây là demonstration; sau đó khôi phục ở commit kế tiếp.

Screenshot không thay thế link và raw artifact. Mỗi evidence nên có: ID, timestamp, commit SHA, URL/path, mô tả nó chứng minh điều gì. Tuyệt đối không tạo giả Newman output, console header, screenshot, GitHub Issue hoặc sơ đồ Agent Skill.
