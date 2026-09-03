# FR-15 – Product CRUD Test Design

## 1. Source, contract and lifecycle

| Item | Value |
| :--- | :--- |
| Sources | `docs/hw6.md` §6; `docs/api_specification.md` §3.1–§3.3; repository FR-15 rule set |
| API source SHA-256 | `488CBCB790099BA9CBB34C7C80BA04C6AEC9E9EBB598F031FFA575737547B139` |
| Endpoints | `GET /api/products`; `GET /api/products/:id`; admin-only `POST /api/products`, `PUT /api/products/:id`, `DELETE /api/products/:id` |
| Fields/rules | `name` required/≤255; numeric `price>0`; existing required `category_id`; optional `description`, `imageUrl`; updates must not affect other products |
| Generated set | 50 unique AI candidates (`FR15-AI-001`–`FR15-AI-050`) |
| Lifecycle | Raw AI output awaiting student audit; audit fields blank; all cases `NOT RUN` |

All requests include `X-Student-Id: 23127104`. Mutations also use JSON content type and a named runtime bearer token; no real credential is stored.

## 2. Ambiguities and working assumptions

| ID | Ambiguity | Working assumption | Decision required |
| :--- | :--- | :--- | :--- |
| `ASM-FR15-01` | Local API spec gives an example body but omits the FR-15 constraints. | Apply repository rules: name required/≤255, numeric price >0, category required/existing. | Confirm against tested SUT commit. |
| `ASM-FR15-02` | Success status/schema omitted. | GET/PUT/DELETE → `200`; POST → `201`; product JSON has numeric `id/price/category_id`, string `name`, optional string/null description/image. | Confirm exact status/schema. |
| `ASM-FR15-03` | Validation/not-found contract omitted. | Invalid body/path → `400`; absent product/category → `404`; JSON error; no mutation. | Confirm framework contract. |
| `ASM-FR15-04` | Auth error contract omitted. | Missing/invalid token → `401`; valid non-admin → `403`; generic JSON error; no mutation. | Confirm middleware behavior. |
| `ASM-FR15-05` | PUT partial/full semantics omitted. | PUT is partial; omitted fields retain existing values. | Confirm update semantics. |
| `ASM-FR15-06` | Optional-field nullability/type/URL rules omitted. | Omitted/null allowed; present description/image must be strings; URL syntax is not validated. | Confirm optional-field rules. |
| `ASM-FR15-07` | Read auth and list/search envelope omitted. | Reads are public; list/search returns an array or documented product-array envelope. | Confirm access/envelope. |
| `ASM-FR15-08` | Unknown properties and concurrency policy omitted. | Reject privileged/unknown fields with `400`; concurrent partial updates serialize, both return `200`, and the final product contains both non-conflicting changes without a lost update. | Confirm allow-list/locking. |

Candidates depending on these assumptions are not final executable until human audit confirms or corrects their oracle.

## 3. Coverage model and fixtures

| Field/area | Partitions and boundaries | TC IDs |
| :--- | :--- | :--- |
| CRUD/read/search | valid create/minimal; list/detail/search; partial/full update; delete/absent/replay | `001`–`016` |
| `name` | missing/null/empty/whitespace; 1/254/255/256 chars; Unicode | `017`–`025` |
| `price` | missing/null/negative/zero; `0.01`; decimal; numeric string | `026`–`032` |
| `category_id` | missing/null; existing 10/11; absent 999999999; string type | `001`, `002`, `011`, `033`–`036` |
| Optional fields | omitted/string/null/empty; object wrong type | `001`, `002`, `012`, `037`, `038` |
| Auth/role | missing, invalid, non-admin across create/update/delete | `039`–`045` |
| Security/isolation | SQLi path/body; stored XSS API probe; mass assignment; concurrent update | `046`–`050` |

- `ADM-A` and `USR-A` are fixture actors. `CAT-A=10`, `CAT-B=11` exist. `P-A` is the target; `P-B` is an unrelated sentinel.
- `N1="A"`, `N254="A"*254`, `N255="A"*255`, `N256="A"*256` are deterministic named strings.
- Restore snapshots before each case. Track/delete created IDs; restore updated/deleted fixtures and compare `P-B`.

## 4. AI-generated candidate cases

| TC ID | Source | Req | Technique | Priority | Preconditions | Request/data | Expected status/body/post-state | Cleanup | Audit label | Audit reason | Correction/final ID | Execution/evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FR15-AI-001` | `AI` | FR-15; FR-12; API §3.3 | CRUD, happy path | P0 | `ADM-A`; `CAT-A` exists | POST products with `{"name":"HW06-P-001","price":100000,"description":"Mô tả","imageUrl":"https://example.test/p.png","category_id":10}` | `201` per ASM-02; exact values/schema/new id; one row created; `P-B` unchanged | Delete returned ID |  |  |  | `FAIL` |
| `FR15-AI-002` | `AI` | FR-15; API §3.3 | CRUD, minimal | P1 | `ADM-A`; `CAT-A` | POST `{"name":"M","price":0.01,"category_id":10}` | `201`; optional fields absent/null; exact persistence | Delete returned ID |  |  |  | `FAIL` |
| `FR15-AI-003` | `AI` | FR-15; API §3.1 | CRUD, schema | P0 | `P-A/P-B` exist | GET product list without bearer | `200` per ASM-07; array/envelope; item types valid; no credential fields; no mutation | None |  |  |  | `PASS` |
| `FR15-AI-004` | `AI` | FR-15; API §3.2 | CRUD, schema | P0 | `P-A` exists | GET product `P-A` | `200`; exact id/name/price/category, valid schema, no sensitive fields | None |  |  |  | `FAIL` |
| `FR15-AI-005` | `AI` | FR-15; API §3.1 | EP, search | P1 | Unique `HW06-Needle-005` exists | GET `?search=HW06-Needle-005` | `200`; includes fixture; every result matches name-search semantics; no mutation | Delete fixture |  |  |  | `FAIL` |
| `FR15-AI-006` | `AI` | FR-15; API §3.1 | EP, search | P2 | No matching name | GET `?search=HW06-NO-MATCH-006` | `200`; empty product collection; no mutation | None |  |  |  | `PASS` |
| `FR15-AI-007` | `AI` | FR-15; API §3.2 | EP, ID | P1 | ID absent | GET product `999999999` | `404` per ASM-03; generic JSON error; unchanged repository | None |  |  |  | `FAIL` |
| `FR15-AI-008` | `AI` | FR-15; API §3.2 | EP, ID | P1 | Snapshots recorded | GET product `abc` | `400`; no internal detail or mutation | None |  |  |  | `FAIL` |
| `FR15-AI-009` | `AI` | FR-15; API §3.3 | CRUD, partial, isolation | P0 | `P-A/P-B` snapshotted | PUT `P-A` `{"name":"HW06-Renamed-009"}` | `200` per ASM-05; only name changes; omitted fields and `P-B` unchanged | Restore `P-A` |  |  |  | `FAIL` |
| `FR15-AI-010` | `AI` | FR-15; API §3.3 | CRUD, partial, isolation | P0 | Same | PUT `P-A` `{"price":125000.5}` | `200`; exact numeric price only; sentinel unchanged | Restore `P-A` |  |  |  | `FAIL` |
| `FR15-AI-011` | `AI` | FR-15; API §3.3 | CRUD, dependency | P0 | `CAT-B=11` exists | PUT `P-A` `{"category_id":11}` | `200`; category changes only; sentinel unchanged | Restore `P-A` |  |  |  | `FAIL` |
| `FR15-AI-012` | `AI` | FR-15; API §3.3 | CRUD, optional fields | P1 | `P-A/P-B` | PUT `P-A` `{"description":null,"imageUrl":""}` | `200` per ASM-06; exact null/empty values persist; required fields and sentinel unchanged | Restore `P-A` |  |  |  | `FAIL` |
| `FR15-AI-013` | `AI` | FR-15; API §3.3 | CRUD, full update | P0 | `CAT-B` exists | PUT all fields: `HW06-Full-013`, price 99000, `D13`, HTTPS image, category 11 | `200`; all values persisted; one target only; sentinel unchanged | Restore `P-A` |  |  |  | `FAIL` |
| `FR15-AI-014` | `AI` | FR-15; API §3.2/3.3 | CRUD, lifecycle | P0 | Disposable `P-D` | DELETE `P-D`, then GET it | DELETE `200`; subsequent GET `404`; only target removed | Recreate fixture |  |  |  | `FAIL` |
| `FR15-AI-015` | `AI` | FR-15; API §3.3 | CRUD, absent delete | P1 | ID absent | DELETE `999999999` | `404`; product count/sentinel unchanged | None |  |  |  | `FAIL` |
| `FR15-AI-016` | `AI` | FR-15; API §3.3 | CRUD, replay delete | P1 | Disposable `P-D` | DELETE same ID twice | First `200`, second `404`; one deletion only; sentinel unchanged | Recreate fixture |  |  |  | `FAIL` |
| `FR15-AI-017` | `AI` | FR-15; API §3.3 | EP, required name | P0 | Baseline count | POST without name; price 100, category 10 | `400`; no creation | None |  |  |  | `FAIL` |
| `FR15-AI-018` | `AI` | FR-15; API §3.3 | EP, null name | P0 | Same | POST `name:null` | `400`; no creation | None |  |  |  | `FAIL` |
| `FR15-AI-019` | `AI` | FR-15; API §3.3 | EP, empty name | P0 | Same | POST `name:""` | `400`; no creation | None |  |  |  | `FAIL` |
| `FR15-AI-020` | `AI` | FR-15; API §3.3 | EP, whitespace | P1 | Same | POST `name:"   "` | `400`; whitespace not persisted; no creation | None |  |  |  | `FAIL` |
| `FR15-AI-021` | `AI` | FR-15; API §3.3 | BVA, min name | P2 | `ADM-A`; `CAT-A` | POST `name:N1` | `201`; one-character name exact | Delete created |  |  |  | `FAIL` |
| `FR15-AI-022` | `AI` | FR-15; API §3.3 | BVA, 254 | P2 | Same | POST `name:N254` | `201`; stored length 254 contract units | Delete created |  |  |  | `FAIL` |
| `FR15-AI-023` | `AI` | FR-15; API §3.3 | BVA, max | P0 | Same | POST `name:N255` | `201`; stored length 255 | Delete created |  |  |  | `FAIL` |
| `FR15-AI-024` | `AI` | FR-15; API §3.3 | BVA, max+1 | P0 | Baseline count | POST `name:N256` | `400`; no truncation or creation | None |  |  |  | `FAIL` |
| `FR15-AI-025` | `AI` | FR-15; API §3.3 | EP, Unicode | P1 | `ADM-A`; `CAT-A` | POST name `Cà phê ☕ 商品` | `201`; Unicode round-trips and JSON remains valid | Delete created |  |  |  | `FAIL` |
| `FR15-AI-026` | `AI` | FR-15; API §3.3 | EP, required price | P0 | Baseline count | POST without price | `400`; no creation | None |  |  |  | `FAIL` |
| `FR15-AI-027` | `AI` | FR-15; API §3.3 | EP, null price | P0 | Same | POST `price:null` | `400`; no creation | None |  |  |  | `FAIL` |
| `FR15-AI-028` | `AI` | FR-15; API §3.3 | EP, negative price | P0 | Same | POST `price:-1` | `400`; no negative persistence | None |  |  |  | `FAIL` |
| `FR15-AI-029` | `AI` | FR-15; API §3.3 | BVA, zero | P0 | Same | POST `price:0` | `400`; no creation | None |  |  |  | `FAIL` |
| `FR15-AI-030` | `AI` | FR-15; API §3.3 | BVA, positive | P0 | `ADM-A`; `CAT-A` | POST `price:0.01` | `201`; positive numeric price equals 0.01 | Delete created |  |  |  | `FAIL` |
| `FR15-AI-031` | `AI` | FR-15; API §3.3 | EP, decimal | P1 | Same | POST `price:99.99` | `201`; decimal remains numeric/exact per precision contract | Delete created |  |  |  | `FAIL` |
| `FR15-AI-032` | `AI` | FR-15; API §3.3 | EP, wrong type | P0 | Baseline count | POST `price:"100"` | `400`; no coercion or creation | None |  |  |  | `FAIL` |
| `FR15-AI-033` | `AI` | FR-15; API §3.3 | EP, required category | P0 | Baseline count | POST omitting category | `400`; no creation | None |  |  |  | `FAIL` |
| `FR15-AI-034` | `AI` | FR-15; API §3.3 | EP, null category | P0 | Same | POST `category_id:null` | `400`; no creation | None |  |  |  | `FAIL` |
| `FR15-AI-035` | `AI` | FR-15; API §3.3 | EP, referential integrity | P0 | Category absent | POST `category_id:999999999` | `404`; no orphan product | None |  |  |  | `FAIL` |
| `FR15-AI-036` | `AI` | FR-15; API §3.3 | EP, wrong type | P1 | `CAT-A=10` | POST `category_id:"10"` | `400`; no coercion or creation | None |  |  |  | `FAIL` |
| `FR15-AI-037` | `AI` | FR-15; API §3.3 | EP, optional wrong type | P1 | `P-A/P-B` | PUT description object `{"text":"bad"}` | `400` per ASM-06; target/sentinel unchanged | None |  |  |  | `FAIL` |
| `FR15-AI-038` | `AI` | FR-15; API §3.3 | EP, optional wrong type | P1 | Same | PUT imageUrl object `{"href":"https://example.test"}` | `400`; target/sentinel unchanged | None |  |  |  | `FAIL` |
| `FR15-AI-039` | `AI` | FR-15; FR-12; SEC-02 | Security, auth | P0 | No token | POST valid body without Authorization | `401` per ASM-04; no creation/data leak | None |  |  |  | `FAIL` |
| `FR15-AI-040` | `AI` | FR-15; FR-12; SEC-03 | Security, role | P0 | `USR-A` non-admin | POST valid body with user token | `403`; no creation | None |  |  |  | `FAIL` |
| `FR15-AI-041` | `AI` | FR-15; FR-12; SEC-02 | Security, auth | P0 | `P-A/P-B`; no token | PUT `P-A` `{"price":1}` | `401`; both unchanged | None |  |  |  | `FAIL` |
| `FR15-AI-042` | `AI` | FR-15; FR-12; SEC-03 | Security, role | P0 | `USR-A`; `P-A/P-B` | PUT `P-A` `{"price":1}` | `403`; both unchanged | None |  |  |  | `FAIL` |
| `FR15-AI-043` | `AI` | FR-15; FR-12; SEC-02 | Security, auth | P0 | Disposable product; no token | DELETE target | `401`; product remains retrievable; sentinel unchanged | Remove fixture |  |  |  | `FAIL` |
| `FR15-AI-044` | `AI` | FR-15; FR-12; SEC-03 | Security, role | P0 | `USR-A`; disposable product | DELETE with user token | `403`; target remains; no side effect | Remove fixture |  |  |  | `FAIL` |
| `FR15-AI-045` | `AI` | FR-15; FR-12; SEC-02 | Security, invalid auth | P0 | `P-A/P-B` | PUT with `Bearer invalid.fixture.token` | `401`; target/sentinel unchanged | None |  |  |  | `FAIL` |
| `FR15-AI-046` | `AI` | FR-15; SEC-05; API §3.2 | Security, injection | P0 | Snapshots/count | GET product path `1%20OR%201=1` | `400`; no SQL/internal detail, multi-row disclosure or mutation; behavioral only | None |  |  |  | `FAIL` |
| `FR15-AI-047` | `AI` | FR-15; SEC-05; API §3.3 | Security, injection | P0 | `ADM-A`; baseline | POST name `x'); DROP TABLE products;--` with valid other fields | `201` under string-domain rule; exact literal stored; never SQL execution/internal error; other products remain readable | Delete created row |  |  |  | `FAIL` |
| `FR15-AI-048` | `AI` | FR-15; SEC-04; API §3.1/3.3 | Security, stored XSS | P0 | `ADM-A`; `CAT-A` | POST name `<img src=x onerror=alert(1)>`, then GET it | API returns inert JSON string without server execution/error; UI-safe rendering needs separate evidence | Delete created |  |  |  | `FAIL` |
| `FR15-AI-049` | `AI` | FR-15; FR-12; API §3.3 | Security, mass assignment | P0 | `ADM-A`; baseline | POST valid fields plus `id:777`, `role:"admin"`, `isAdmin:true`, forged `created_at` | `400` per ASM-08; no chosen ID/privilege/internal metadata or creation | Inspect/remove only if violation observed |  |  |  | `FAIL` |
| `FR15-AI-050` | `AI` | FR-15; ASM-FR15-05/08 | Concurrency, isolation | P0 | Dedicated `P-A`; `P-B`; synchronized admins | Concurrent PUTs: `{"name":"Race-A"}` and `{"price":222}` | Both `200`; final `P-A` has name `Race-A` and price `222` with other fields retained; no lost update; `P-B` unchanged | Barrier and snapshot restore |  |  |  | `PASS` |

## 5. Human-added cases

Five student-authored HUMAN cases have been supplied with explicit "Why AI missed" analysis, covering cross-feature interactions, alternate injection vectors, missing boundary evaluations, and JSON parsing artifacts.

| TC ID | Source | Req | Technique | Priority | Preconditions | Request/data | Expected status/body/post-state | Cleanup | Why AI missed | Execution/evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `FR15-H-001` | `HUMAN` | FR-15; FR-14 (cross-feature); Referential integrity | State, Orphan reference | P0 | `ADM-A`; tạo `P-TEMP` với `category_id=CAT-TEMP` (danh mục mới tạo riêng cho case này) | Xóa `CAT-TEMP` qua `DELETE /api/categories/:id` (FR-14), sau đó `GET /api/products/P-TEMP` và `GET /api/products` | Phải xác định rõ 1 trong 2 hành vi và assert tường minh: (a) xóa category bị chặn vì còn product tham chiếu (409/400, category không bị xóa) — đây là hành vi an toàn; hoặc (b) category bị xóa, product `P-TEMP` vẫn tồn tại nhưng `category_id` trỏ tới bản ghi không còn tồn tại (orphan) — phải kiểm tra response của `GET /api/products/P-TEMP` không bị lỗi 5xx và không crash danh sách sản phẩm chung. Test case không được bỏ trống kết quả này | Dọn `P-TEMP`; khôi phục danh mục nếu bị chặn xóa | Đây là quan hệ giữa FR-15 và FR-14, nhưng cả 2 file test-design được sinh độc lập, mỗi file chỉ nhìn đúng endpoint của feature mình. AI khi sinh case 035/036 chỉ hỏi "category có tồn tại lúc tạo product không", không có ngữ cảnh (và cũng không được prompt) để hỏi ngược "category có thể biến mất sau khi product đã tạo không" — đây là lỗi do phạm vi prompt bị chia nhỏ theo từng FR, khiến AI mất khả năng suy luận quan hệ chéo (relational reasoning) giữa 2 bảng dữ liệu | `PASS` |
| `FR15-H-002` | `HUMAN` | FR-15; FR-10/FR-11 (cross-feature); Data integrity | State, Historical consistency | P0 | `USR-A` đã checkout thành công 1 đơn hàng `O-HIST` có chứa `P-DEL` (sản phẩm được snapshot lúc đặt hàng) | `ADM-A` xóa `P-DEL` qua `DELETE /api/products/:id`, sau đó `USR-A` gọi `GET /api/orders/O-HIST` (xem lại đơn hàng cũ) | Đơn hàng `O-HIST` vẫn phải hiển thị được thông tin sản phẩm đã đặt (tên, giá tại thời điểm mua) dù `P-DEL` đã bị xóa khỏi bảng sản phẩm — không được trả 404/lỗi 5xx cho toàn bộ đơn hàng chỉ vì 1 sản phẩm con đã bị xóa; đồng thời `GET /api/products/P-DEL` phải trả 404 bình thường | Không thể khôi phục `P-DEL` sau xóa; ghi nhận là dữ liệu one-way | Đây là kịch bản đòi hỏi phối hợp 2 luồng nghiệp vụ hoàn toàn khác nhau (Admin xóa sản phẩm — Pool C, và User xem lịch sử đơn hàng — Pool B) mà không FR nào riêng lẻ tự "thấy" được. Với AI, mỗi lần sinh case nó chỉ được cấp đúng 1 API spec cục bộ (§3.3 cho FR-15) — nó không được yêu cầu truy vấn xem sản phẩm này có đang được tham chiếu ở đâu khác trong hệ thống hay không. Đây vừa là giới hạn model (không tự "nhớ" toàn bộ ERD hệ thống khi chỉ được cấp 1 đoạn spec) vừa là hệ quả của độ phức tạp API: quan hệ order-snapshot-product là quan hệ ẩn, không được mô tả tường minh trong api_specification.md | `PASS` |
| `FR15-H-003` | `HUMAN` | FR-15; SEC-05; API §3.1 (khác bề mặt với 046) | Security, Injection (query param) | P0 | Baseline sản phẩm đã seed sẵn (≥3 sản phẩm với tên khác nhau) | `GET /api/products?search=%25' OR '1'='1` và `GET /api/products?search=_` (wildcard LIKE injection qua query string, khác hẳn injection qua path ID) | Server không được trả toàn bộ danh sách sản phẩm (dấu hiệu injection thành công làm điều kiện WHERE name LIKE '%...%' bị vô hiệu hóa thành luôn đúng) và không lộ lỗi SQL/stack trace; kết quả trả về đúng ngữ nghĩa "không tìm thấy" hoặc tập con hợp lệ | Không cần | Case FR15-AI-046 đã đóng dấu "SEC-05 covered" trong bảng coverage (mục 6) sau khi test đúng 1 điểm injection duy nhất (path ID). Đây là lỗi kinh điển: AI coi injection đã được phủ đủ chỉ vì đã có 1 case gắn nhãn Security, injection, mà không nhận ra cùng 1 endpoint `GET /api/products` có tới 2 tham số nhận input khác nhau (`:id` dùng so sánh chính xác, `?search=` dùng pattern-matching LIKE) — về lý thuyết đây là 2 câu SQL khác nhau, cần 2 bộ payload khác nhau. Đây là giới hạn của model khi tổng quát hóa "đã test 1 field = đã test đủ security cho cả endpoint", không phải lỗi API phức tạp hay lỗi prompt | `PASS` |
| `FR15-H-004` | `HUMAN` | FR-15; ASM-FR15-05 (làm rõ boundary) | EP, No-op ambiguity | P1 | `P-A` snapshot đầy đủ | `PUT /api/products/P-A` với body rỗng `{}` | Phải xác định và assert rõ ràng 1 trong 2: (a) coi là "không có gì để cập nhật" → 200, sản phẩm giữ nguyên toàn bộ giá trị cũ (no-op hợp lệ theo ASM-05 "PUT là partial"); hoặc (b) coi là request thiếu dữ liệu bắt buộc → 400. Hiện bảng AI có case 009–013 test partial update với ít nhất 1 field, nhưng chưa từng test 0 field — đây là ranh giới chưa được xác định giữa "partial update hợp lệ" và "request rỗng vô nghĩa" | Không cần (nếu no-op) | ASM-FR15-05 (PUT là partial, field bị bỏ giữ nguyên) là 1 giả định được AI tự đặt ra, nhưng AI không tự kiểm tra giới hạn của chính giả định mình vừa đặt — nó sinh case cho "partial update với 1–vài field" nhưng bỏ sót trường hợp biên cực đoan nhất của chính khái niệm "partial" là "partial = 0 field". Đây là lỗi logic khi tự-audit case theo 1 assumption vừa mới generate, cho thấy giới hạn của model trong việc suy luận đầy đủ các boundary của chính giả định nó đưa ra | `PASS` |
| `FR15-H-005` | `HUMAN` | FR-15; API §3.3 (numeric robustness) | Robustness, JSON number edge case | P1 | `ADM-A`; `CAT-A` | POST với `price: 1e309` (vượt giới hạn double, JSON parser có thể trả Infinity), và POST riêng với `price: -0` | Với `1e309`: server phải từ chối an toàn (400) hoặc lưu giá trị hữu hạn hợp lệ, tuyệt đối không được để lọt giá trị Infinity/null vào DB rồi làm hỏng các phép tính khác (ví dụ tổng tiền checkout sau này nếu sản phẩm này được thêm vào giỏ). Với `-0`: phải làm rõ có bị coi là price <= 0 (vi phạm rule price > 0, phải 400) hay được chấp nhận nhầm vì so sánh số học JS coi `-0 == 0` nhưng `-0 > 0` là false — cả 2 trường hợp cần assert tường minh, không được bỏ ngỏ | Xóa sản phẩm nếu lỡ tạo | Case 026–032 của AI phủ rất tốt các boundary "nghiệp vụ" (0, -1, 0.01, 99.99, kiểu chuỗi "100"), đúng theo tư duy EP/BVA kinh điển dạy trong ISTQB. Nhưng AI không tự nghĩ tới giới hạn kỹ thuật của kiểu dữ liệu JSON/double (số quá lớn thành Infinity, số âm-không -0) — đây là lớp lỗi đòi hỏi hiểu biết về cách JSON parser và IEEE-754 xử lý số, một chi tiết implementation nằm ngoài những gì spec mô tả ("price là số dương"), nên đây là giới hạn kiến thức miền (domain knowledge) của model khi chỉ đọc spec ở mức nghiệp vụ chứ không xét tầng biểu diễn dữ liệu bên dưới | `FAIL` |

## 6. Coverage closure

| Modeled item | TC IDs | Status/gap |
| :--- | :--- | :--- |
| CRUD lifecycle/read/search | `001`–`016` | Covered; status/schema assumptions pending |
| All request fields and boundaries | `017`–`038` plus `001`, `002`, `009`–`013` | Covered; precision, URL and PUT semantics pending |
| Authentication/authorization | `039`–`045` | Covered across create/update/delete |
| SEC-04/05 and mass assignment | `046`–`049` | API behavioral coverage; UI/code evidence still needed |
| Isolation/concurrency | `009`–`013`, `037`, `038`, `041`–`045`, `050` | Sentinel assertions covered; race harness pending |
| Success/error schemas and credential exclusion | All cases | Covered under ASM-02–04 |
| SEC-01, SEC-06, SEC-07 | None | Not applicable: no password storage, upload or rate-limit rule in this feature |
| `X-Student-Id` | All cases | Designed; real console/request evidence pending |
| Orphan reference (FR-14 cross-feature) | FR15-H-001 | Category-delete impact on existing products |
| Historical data integrity (FR-10/FR-11) | FR15-H-002 | Order snapshot persistence after product deletion |
| SQL injection via `?search=` LIKE | FR15-H-003 | Distinct from path-ID injection (AI-046) |
| PUT empty-body no-op boundary | FR15-H-004 | ASM-FR15-05 extreme boundary |
| JSON/IEEE-754 numeric edge cases | FR15-H-005 | Infinity (`1e309`) and negative-zero (`-0`) |

## 7. Quality-gate result

- 50 unique AI IDs plus 5 HUMAN extensions; audit triplets remain blank; latest Tier-A execution maps 55/55 IDs with 7 PASS and 48 FAIL.
- CRUD, every request field, BVA/EP, auth/role, schemas, isolation and applicable security are traceable without semantic padding.
- Execution evidence comes from `newman-report-FR15.json` (SHA-256 `AE21D309C08924BD1B75DA54141F8BBD15539E5B3077270FC2E27A305AE806E0`); 2 genuine bugs are confirmed (`BUG-006`, `BUG-007`). `BUG-005` is rejected because the cited `201`/full-object response contract is absent from the specification.
- Gaps: `ASM-FR15-01`–`08`, human audit, deterministic fixture reset/concurrency limitations, and retest after fixes.

**Generation status: COMPLETE; execution reconciliation: COMPLETE for the current artifact.** Folder `FR-15 Product CRUD`, request `FR-15 Mutation Router (Data-Driven)` and sanitized `FR15_data.csv` (55 rows, 55 unique IDs) are present. Runtime JWTs remain in raw Newman evidence and must be rotated/sanitized before publication; deterministic fixture reset and the `FR15-H-005` secondary-status parser also remain limitations.
