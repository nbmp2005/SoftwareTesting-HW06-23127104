# Bug Report

## Summary

| Bug ID | Title | Requirement | Severity | Status | Found by | GitHub Issue |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `BUG-001` | Lộ lọt thông tin nhạy cảm (password, login_attempts) qua API Login | `FR-02`, `SEC-01` | `Critical` | `Open` | `AI-suggested` | `[URL]` |

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
