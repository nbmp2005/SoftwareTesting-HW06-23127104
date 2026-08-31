# Bug Report

## Summary

| Bug ID | Title | Requirement | Severity | Status | Found by | GitHub Issue |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `BUG-001` | Lộ lọt thông tin nhạy cảm (password, login_attempts) qua API Login | `FR-02`, `SEC-01` | `Critical` | `Open` | `AI-suggested` | `[URL]` |

| `BUG-002` | Lỗi Logic Trạng Thái Đơn Hàng (Cho phép chuyển trạng thái vô lý) | `FR-10` | `High` | `Open` | `AI-suggested` | `[URL]` |
| `BUG-003` | Lỗi Phân Quyền (Privilege Escalation) - User thường được quyền đổi trạng thái | `FR-10` | `Critical` | `Open` | `AI-suggested` | `[URL]` |
| `BUG-004` | Lỗi Race Condition - Thiếu cơ chế khóa (Lock) khi cập nhật đồng thời | `FR-10` | `High` | `Open` | `AI-suggested` | `[URL]` |

## Bug template

### BUG-001 – Lộ lọt thông tin nhạy cảm (password, login_attempts) qua API Login

- **Requirement violated:** `FR-02`, `SEC-01` (Không được trả về hoặc tiết lộ thông tin nhạy cảm như password hash, token nội bộ trong các phản hồi thông thường).
- **Severity / priority:** `Critical`. Kẻ tấn công có thể dễ dàng lấy được chuỗi Hash mật khẩu và các thông số khóa tài khoản, dẫn đến nguy cơ bảo mật hệ thống nghiêm trọng.
- **Environment:** Node.js Backend EShop, Newman v5+, `localhost:3000`
- **Preconditions:** Có một tài khoản hợp lệ trong hệ thống.
- **Related test case:** `FR02-AI-001` đến `FR02-AI-005`
- **AI involvement:** AI found. AI sinh ra các Test Case kiểm tra Schema và Security, phát hiện rò rỉ dữ liệu ngoài mong muốn.

#### Steps to reproduce

1. Khởi động EShop API Backend.
2. Gửi request `POST /api/login` với thông tin đăng nhập hợp lệ.
3. Kiểm tra JSON response trả về, đặc biệt trong object `user`.

#### Expected result

Response trả về Status `200 OK`, có `token` và thông tin `user` cơ bản. TUYỆT ĐỐI KHÔNG chứa trường `password`, `login_attempts`, `locked_until`, hoặc `reset_token`.

#### Actual result

Response có chứa tất cả các trường nhạy cảm nêu trên. 
*(Trích log Newman: `sensitive fields found: $.user.password, $.user.login_attempts, $.user.locked_until, $.user.reset_token: expected [ '$.user.password', ... ] to be empty`)*.

#### Reproducibility and impact

- Reproduction rate: `100%` (45/45 lần chạy).
- Impact: Rất nghiêm trọng (Data privacy/Security breach).
- Workaround: Cần sửa DTO/Mapper của Backend để bỏ các trường này trước khi trả về.

#### Evidence

- Screenshot: `(Tùy chọn)`
- Newman/Postman evidence: `newman-report-FR02.json`
- GitHub Issue: `[public URL]`

---


### BUG-002 – Lỗi Logic Trạng Thái Đơn Hàng (Cho phép chuyển trạng thái vô lý)

- **Requirement violated:** `FR-10` (Order State Machine quy định rõ các trạng thái hợp lệ. Ví dụ: Đơn đã `canceled` không thể chuyển về `pending` hay `confirmed`).
- **Severity / priority:** `High`. Làm sai lệch quy trình kinh doanh nghiệp vụ, có thể gây thất thoát hàng hóa.
- **Environment:** Node.js Backend EShop, Newman v5+, `localhost:3000`
- **Preconditions:** Có một đơn hàng ở trạng thái cuối (VD: `canceled` hoặc `delivered`).
- **Related test case:** `FR10-AI-001` đến `FR10-AI-030`, `FR10-H-003`.
- **AI involvement:** AI found. Kịch bản Data-driven đã vét cạn tất cả 25 cặp trạng thái có thể, phát hiện lỗ hổng kiểm soát trạng thái.

#### Steps to reproduce

1. Khởi động EShop API Backend.
2. Gửi request `PUT /api/admin/orders/{id}/status` chuyển đơn hàng từ `canceled` sang `pending`.
3. Kiểm tra JSON response và Status Code.

#### Expected result

Response trả về Status `400 Bad Request` vì vi phạm State Machine Rules.

#### Actual result

Response trả về Status `200 OK`, đơn hàng thực sự bị chuyển ngược trạng thái.

#### Reproducibility and impact

- Reproduction rate: `100%` (Tái hiện được trên toàn bộ kịch bản lỗi).
- Impact: Nghiêm trọng (Business Logic Breach).
- Workaround: Backend cần bổ sung hàm kiểm tra State hợp lệ (vd: dùng State Machine library hoặc if-else map) trước khi cho phép update DB.

#### Evidence

- Screenshot: `(Tùy chọn)`
- Newman/Postman evidence: `newman-report-FR10.zip`
- GitHub Issue: `[public URL]`

---

### BUG-003 – Lỗi Phân Quyền (Privilege Escalation) - User thường đổi được trạng thái

- **Requirement violated:** `FR-10` (Chỉ có quyền Admin mới được gọi API đổi trạng thái từ pending sang confirmed, shipping, delivered).
- **Severity / priority:** `Critical`. Lỗ hổng bảo mật chết người (IDOR / Broken Access Control).
- **Environment:** Node.js Backend EShop, Newman v5+, `localhost:3000`
- **Preconditions:** Có một đơn hàng ở trạng thái `pending`. User đăng nhập hợp lệ với role thường.
- **Related test case:** `FR10-AI-031`, `FR10-AI-032`, `FR10-AI-035`.
- **AI involvement:** AI found. Nhờ tạo token User động trong Setup, AI phát hiện User thường cũng chọc được vào API admin.

#### Steps to reproduce

1. Khởi động EShop API Backend.
2. Gửi request `PUT /api/admin/orders/{id}/status` bằng token của User thường (không phải Admin).

#### Expected result

Response trả về Status `403 Forbidden`.

#### Actual result

Response trả về Status `200 OK`, trạng thái đơn hàng bị thay đổi bởi người dùng không có thẩm quyền.

#### Reproducibility and impact

- Reproduction rate: `100%`.
- Impact: Đặc biệt Nghiêm trọng (Critical Security Breach). Khách hàng có thể tự đổi đơn hàng của mình thành `delivered` để quỵt tiền.
- Workaround: Backend cần check `req.user.role === 'admin'` trong endpoint `/api/admin/orders/:id/status`.

#### Evidence

- Screenshot: `(Tùy chọn)`
- Newman/Postman evidence: `newman-report-FR10.zip`
- GitHub Issue: `[public URL]`

---

### BUG-004 – Lỗi Race Condition - Thiếu cơ chế khóa (Lock) khi cập nhật đồng thời

- **Requirement violated:** `FR-10` (Concurrent updates). Khi có 2 request đồng thời cố gắng cập nhật trạng thái của cùng 1 đơn hàng, chỉ 1 request được thành công (200), request còn lại phải bị từ chối (409 Conflict hoặc 400).
- **Severity / priority:** `High`.
- **Environment:** Node.js Backend EShop, Newman v5+, `localhost:3000`
- **Preconditions:** Có một đơn hàng ở trạng thái `pending`.
- **Related test case:** `FR10-H-004`.
- **AI involvement:** AI found. Kiểm tra bằng cách bắn song song (Promise.all).

#### Steps to reproduce

1. Bắn 2 request `PUT` trạng thái đơn hàng cùng lúc (ví dụ: request 1 chuyển sang `canceled`, request 2 chuyển sang `confirmed`).

#### Expected result

Hệ thống trả về 1 request `200 OK` và 1 request `409 Conflict`. Trạng thái cuối cùng của DB phải nhất quán với request `200 OK`.

#### Actual result

Hệ thống trả về cả 2 request `200 OK`. Trạng thái cuối cùng của DB là trạng thái của request chạy xong sau (Ghi đè - Lost Update).

#### Reproducibility and impact

- Reproduction rate: Cao (thường xuyên trả về 200+200 trong môi trường test).
- Impact: Mất tính toàn vẹn dữ liệu (Data Integrity).
- Workaround: Sử dụng Optimistic Locking (cột version) hoặc Transaction Lock trong SQLite/Backend.

#### Evidence

- Screenshot: `(Tùy chọn)`
- Newman/Postman evidence: `newman-report-FR10.zip`
- GitHub Issue: `[public URL]`

---
