# AI Audit Report

I use AI tools for the following tasks.

- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-29T18:50:34.8122652+07:00
- Prompt: 
```
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW06\SoftwareTesting-HW06-23127104\\.agents\skills\ai-audit-logger\SKILL.md)&#x20;

Dựa vào yêu cầu đề trong docs/hw6.md. Hãy hướng dẫn tôi toàn bộ bài tập này:

1. Giảng cho tôi chi tiết về kiến thức foundation về bài này
2. Liệt kê chi tiết và hướng dẫn tôi toàn bộ detail các task tôi cần làm
3. Tôi muốn build agent skill từ đầu đến cuối, hãy hướng dẫn tôi nhuwgx phương án để build agent skill cho các task trong bài tập này
4. Chuẩn bị toàn bộ các file md theo đúng format yêu cầu này
5. Tôi chọn fr2, fr10, fr15; đánh giá xem tôi chọn vậy hợp lí chưa
```
- AI Output: 
```
Đã phân tích đề HW06 và đặc tả EShop; đánh giá FR-02/FR-10/FR-15 là bộ ba hợp lệ, cân bằng giữa authentication, state-transition và admin CRUD. Đã tạo tài liệu kiến thức nền, hướng dẫn từng phase, checklist nộp bài, template main report/test summary/bug/CI-CD/AI critique/Git log, ba test-design template, cùng reusable Agent Skill có references và quality gates. Skill được kiểm tra bằng quick_validate.py và không tạo giả execution evidence hay sơ đồ self-drawn.
```

## Interaction 002

- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-30T20:48:13.6714377+07:00
- Prompt:
```
[$ai-audit-logger](C:\Users\cpshc\Y3\SoftwareTesting\SoftwareTesting-HW06\SoftwareTesting-HW06-23127104\\.agents\skills\ai-audit-logger\SKILL.md) Dựa vào đề bài yêu cầu và những task tôi cần làm, hãy viết lại bộ skill  chặt chẽ và chính xác hơn, đồng thời yêu cầu agent cập nhật toàn bộ những file liên quan (ví dụ như main report phần nào) để sau khi hoàn thành agent tự cập nhật các file. Thêm skill nếu cần thiết và tiện cho tôi
```
- AI Output:
```
Đã siết lại bốn skill hiện có theo source-of-truth, human-review và evidence gates; thêm hw06-deliverable-sync để đồng bộ report consumer và newman-evidence-reconciler để nhập kết quả chạy thật. Đã cập nhật README, task guide, submission checklist, main report và Agent Skill design để mô tả pipeline close-out; cả sáu skill đều pass quick_validate.py trong Python UTF-8 mode. Không thay execution metrics hoặc tick evidence checklist vì repository chưa có kết quả chạy thật tương ứng.
```

## Interaction 003

- Name of the AI tool: OpenAI Codex
- Date/time: 2026-08-30T21:24:31.0487982+07:00
- Prompt:
```
sao skill thấy ngắn quá, những bài tập trước skill nào của t cũng cả hơn trăm dòng, ít vậy có đủ chặt chẽ không, hãy rà soát và chỉnh sửa giúp tôi
```
- AI Output:
```
Đã rà soát cả sáu skill theo yêu cầu HW06 và nguyên tắc progressive disclosure. Đã sửa các mâu thuẫn về prompt nguyên văn/secret/truncation, metadata Newman, bug lifecycle, TC mapping và counting; thêm năm reference protocol/decision files; chuẩn hóa ba template test case với Source và Execution/evidence; cập nhật README, task guide, main report và Agent Skill design. Cả sáu package hiện có ít nhất 100 dòng Markdown, pass quick_validate.py; sáu openai.yaml parse thành công, mọi local skill link hợp lệ và các dòng mẫu bảng TC nhất quán. Không thay execution metrics vì chưa có Newman evidence thật.
```

<!-- Append each later interaction using the exact four-field format above. Keep the user's prompt verbatim and use the real interaction timestamp. -->
