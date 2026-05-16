# Setup n8n Cloud — MKT AI Bot

## Tổng quan flow

```
Telegram Message
      ↓
 [Haiku] Phân loại skill + context
      ↓
 [IF] Cần hỏi thêm?
  YES → Gửi câu hỏi → End
  NO  ↓
 [Supabase] Fetch skill sections
      ↓
 [Sonnet] Thực thi skill
      ↓
 [Haiku] Critic review
      ↓
 [Supabase] Lưu session
      ↓
 Gửi response Telegram
```

---

## Bước 1 — Chuẩn bị

### 1.1 Tạo Telegram Bot
1. Mở Telegram → tìm `@BotFather`
2. Gõ `/newbot` → đặt tên → đặt username (phải kết thúc bằng `bot`)
3. Copy **Bot Token** (dạng `7123456789:AAF...`)

### 1.2 Lấy Supabase credentials
- Vào Supabase project → **Settings → API**
- Copy:
  - **Project URL**: `https://xxxx.supabase.co`
  - **service_role key** (secret — dùng trong n8n, không public)

### 1.3 Tạo bảng sessions trong Supabase
- Vào Supabase → **SQL Editor**
- Paste nội dung file `db/sessions.sql` → Run

### 1.4 Lấy Anthropic API key
- Vào console.anthropic.com → API Keys → tạo key mới
- Copy key (dạng `sk-ant-api03-...`)

---

## Bước 2 — Tạo credentials trong n8n Cloud

Vào **n8n Cloud → Settings → Credentials → New**:

### Credential 1: Anthropic API
- Type: **HTTP Header Auth**
- Name: `Anthropic API`
- Name field: `x-api-key`
- Value field: `sk-ant-api03-...` (paste API key)

### Credential 2: Supabase
- Type: **HTTP Header Auth**
- Name: `Supabase Service Key`
- Name field: `Authorization`
- Value field: `Bearer eyJ...` (paste service_role key)

### Credential 3: Telegram
- Type: **Telegram**
- Name: `Telegram Bot`
- Bot Token: `7123456789:AAF...`

---

## Bước 3 — Import workflow

1. Vào **n8n Cloud → Workflows → Import from file**
2. Upload file `n8n/workflow-mkt-bot.json`
3. Mở workflow → gán credentials:
   - Tất cả node **HTTP Request → Anthropic**: chọn `Anthropic API`
   - Tất cả node **HTTP Request → Supabase**: chọn `Supabase Service Key`
   - Node **Telegram Trigger** và **Telegram Send**: chọn `Telegram Bot`

---

## Bước 4 — Cấu hình biến môi trường

Trong workflow, tìm node **"Config"** (node đầu tiên sau trigger), cập nhật:

```javascript
const SUPABASE_URL = "https://xxxx.supabase.co";  // ← Paste URL của bạn
const SUPABASE_ANON_KEY = "eyJ...";                // ← Dùng service_role key
```

---

## Bước 5 — Activate và test

1. Click **Activate** (toggle góc trên phải)
2. Mở Telegram → tìm bot của bạn → gõ `/start`
3. Gõ thử: `"Tôi cần viết kế hoạch marketing cho spa"`

### Test cases cơ bản:
| Input | Expected skill | Expected output |
|-------|---------------|-----------------|
| "làm kế hoạch marketing" | 00-ke-hoach-mkt | Hỏi 3 câu intake |
| "viết copy quảng cáo Facebook" | 05-copy-quang-cao | Hỏi sản phẩm + nền tảng |
| "nghiên cứu đối thủ" | 08-nghien-cuu-doi-thu | Hỏi 3 câu |
| "khách không quay lại" | 30-retention-strategy | Hỏi ngành + giai đoạn |

---

## Bước 6 — Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân | Cách fix |
|-----|-------------|---------|
| Bot không reply | Webhook chưa set | n8n tự set webhook khi Activate |
| "Invalid API key" | Anthropic key sai | Kiểm tra credential |
| "Row not found" | Chưa tạo sessions table | Chạy lại `db/sessions.sql` |
| Response bị cắt | Telegram limit 4096 chars | Đã xử lý trong Code node |
| Haiku không nhận diện skill | Input quá ngắn | Bot sẽ hỏi clarifying question |

---

## Cấu trúc Supabase URL

Thay `[PROJECT_REF]` bằng ref project của bạn (tìm trong Supabase URL):

```
GET sessions:
https://[PROJECT_REF].supabase.co/rest/v1/sessions?user_id=eq.{user_id}&select=*

UPSERT session:
https://[PROJECT_REF].supabase.co/rest/v1/sessions
Method: POST
Header: Prefer: resolution=merge-duplicates

GET skill sections:
https://[PROJECT_REF].supabase.co/rest/v1/skill_sections?skill_id=eq.{skill_id}&priority=lte.2&select=*
```

---

## Upgrade path

Sau khi test ổn:
1. **Thêm /full command**: Khi user gõ `/full [yêu cầu]` → set output_format = "full" → Sonnet trả về Excel-ready
2. **Thêm memory**: Tích lũy `session_context` qua nhiều lượt → skills nhận context không phải hỏi lại
3. **Thêm image input**: Nhận screenshot ads → đưa vào 03-danh-gia-hieu-suat
4. **Rate limiting**: Giới hạn 50 requests/user/ngày trong Code node
