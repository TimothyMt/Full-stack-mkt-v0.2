# HANDOFF — CMO AI Product v0.2

> Đọc file này trước khi làm bất cứ gì. Đây là nguồn sự thật duy nhất về trạng thái project.

---

## 1. MỤC TIÊU SẢN PHẨM

**Xây dựng một AI Marketing Assistant cho SME Việt Nam** — chạy qua Telegram, được vận hành bởi n8n + Claude API + Supabase.

**Khách hàng mục tiêu:** Chủ spa, phòng khám, F&B, gym, education center — những người không có team marketing chuyên nghiệp nhưng cần làm marketing bài bản.

**Giá trị cốt lõi:** User nhắn Telegram → nhận kế hoạch marketing, content, brief chiến dịch, phân tích hiệu suất — chất lượng ngang senior marketer, trong vài phút.

**Không phải chatbot thông thường.** Là hệ thống có:
- Skills chuyên biệt theo từng task marketing
- Memory per user (lưu ngành, mục tiêu, ngân sách — không hỏi lại)
- Critic pattern (AI tự review trước khi gửi user)
- Output chuẩn: bullet point trên Telegram + file Excel/HTML đầy đủ

---

## 2. KIẾN TRÚC HỆ THỐNG

### Luồng chính (đã xác lập — KHÔNG thay đổi)

```
Telegram User gửi tin nhắn
    ↓
[1] Haiku Classify
    — xác nhận user_id
    — parse order của user (họ muốn làm gì?)
    ↓
[2] Master Agent (Sonnet)
    — load session_context từ Supabase (by user_id)
    — quyết định: skill_id, mode (product/personal_brand), industry
    ↓
[3] Supabase fetch skill_sections
    — filter theo skill_id + priority + mode
    — priority 1: luôn load | priority 2: standard | priority 3: chỉ khi mode=full
    ↓
[4] Sonnet execute skill
    — chạy skill với session_context + sections
    — output FULL structured markdown (không hỏi user quick/full)
    ↓
[5] Sonnet Critic review
    — kiểm tra CRITICAL + HIGH + MEDIUM issues
    — nếu NEEDS_FIX → sub-agent sửa đúng section bị flag → re-review (tối đa 2 vòng)
    ↓
[6] Master Agent format output
    — Telegram: bullet point summary ≤800 chars
    — Excel/HTML: file đầy đủ đính kèm
    — lưu session_context vào Supabase (user_id, last_skill, mode, industry)
    ↓
Telegram User nhận cả 2: tóm tắt + file
```

### Nguyên tắc thiết kế không thay đổi

| Nguyên tắc | Chi tiết |
|-----------|---------|
| **Skills output FULL** | Skills không hỏi quick/full — luôn output full structured markdown. Master Agent quyết định format. |
| **Master Agent bắt buộc** | Mọi path đều đi qua Master Agent (Critic role). Không bao giờ bypass. |
| **Session per user_id** | Memory lưu theo user_id trong Supabase sessions table. Không hỏi lại ngành/mục tiêu đã biết. |
| **Sonnet Critic, không phải Haiku** | Critic dùng Sonnet để review đủ chất lượng. |
| **Skills không đọc DB** | Skills nhận session_context từ Master Agent. Không tự query Supabase. |
| **mode = product/personal_brand** | `mode` field trong session chỉ có 2 giá trị này. Không dùng quick/full trong skills. |

---

## 3. SUPABASE — CẤU TRÚC DỮ LIỆU

### Tables đã có

```
table: skills
  skill_id (PK), name, description, agent, version, category,
  context_requirements (jsonb), triggers (jsonb)

table: skill_sections
  skill_id (FK), section_id, section_type, content,
  priority, modes TEXT[], industries TEXT[], tags TEXT[]
  — GIN indexes on modes, industries arrays

table: sessions          ← dùng cho n8n
  user_id (PK text), session_context (jsonb),
  last_skill text, updated_at timestamptz
  — RLS enabled, service_role only
```

### Files schema

- `db/schema.sql` — tạo bảng skills + skill_sections
- `db/sessions.sql` — tạo bảng sessions (chạy trong Supabase SQL Editor trước khi dùng n8n)

### Skills đã ingested (v0.2 — chỉ core 7 skills)

| Skill | Agent | Sections | Trạng thái |
|-------|-------|---------|-----------|
| 00-ke-hoach-mkt | mkt-strategist | 12 | ✅ ingested |
| 01-lich-noi-dung | content-producer | 11 | ✅ ingested |
| 02-brief-chien-dich | mkt-strategist | 15 | ✅ ingested |
| 03-danh-gia-hieu-suat | performance-analyst | 14 | ✅ ingested |
| 04-script-video | content-producer | 11 | ✅ ingested |
| 05-copy-quang-cao | content-producer | 9 | ✅ ingested |
| 06-brief-ugc-egc | content-producer | 11 | ✅ ingested |
| **Tổng** | | **83 sections** | |

### Ingest lại khi sửa skill

```bash
# Từ root project (Windows PowerShell):
Set-Location "C:\Users\dtnhien\Full-stack-mkt-v0.1"
python -X utf8 scripts/ingest_skill.py --all

# Hoặc 1 skill cụ thể:
python -X utf8 scripts/ingest_skill.py skills/vi/00-ke-hoach-mkt/SKILL.md
```

---

## 4. N8N — TRẠNG THÁI

### File đã tạo

| File | Mục đích |
|------|---------|
| `n8n/workflow-mkt-bot.json` | Workflow JSON — import trực tiếp vào n8n Cloud |
| `n8n/SETUP.md` | Hướng dẫn setup step-by-step |

### Workflow gồm các nodes

```
Telegram Trigger → Extract Message → Get Session (Supabase)
→ Build Haiku Input → Haiku Classify → Parse Classification
→ IF Needs Clarification
  → [Yes] Send Clarification
  → [No] Fetch Sections (Supabase) → Build System Prompt
       → Sonnet Execute → Sonnet Critic → Format Response
       → Save Session (Supabase) → Send Response (Telegram)
```

### Còn cần làm trước khi dùng được

1. **Chạy `db/sessions.sql`** trong Supabase SQL Editor → tạo bảng sessions
2. **Import workflow** vào n8n Cloud (n8n.io)
3. **Thay `[PROJECT_REF]`** trong workflow JSON → Supabase project ref thực tế
4. **Gán credentials** trong n8n: Anthropic API key + Supabase + Telegram Bot Token
5. **Fix Format Response node** — hiện chưa lưu `mode` + `industry` vào session. Code cần thêm:

```javascript
// Trong Format Response node (JavaScript):
const updatedSession = {
  ...context.session_context,
  last_skill: context.skill_id,
  mode: classify.mode || context.session_context.mode,
  industry: classify.industry || context.session_context.industry,
  last_interaction: new Date().toISOString()
};
```

---

## 5. ARCHITECTURE DECISIONS ĐÃ CHỐT

Tất cả decisions dưới đây đã được implement và ingested vào Supabase:

| Decision | Nội dung | Đã làm |
|---------|---------|--------|
| **C1** | Skills không hỏi quick/full — xóa "Buoc 1 — Xac dinh mode output" khỏi skills 00, 01, 02, 03, 06 | ✅ |
| **C2** | Skill 04 `personal_brand_mode` đổi `modes: [all]` → `modes: [full]` | ✅ |
| **C3** | n8n Format Response node phải lưu mode + industry vào session | ⏳ Cần fix |
| **H1** | Skill 02 YAML output: "9 phan" → "10 phan" (thêm phần Offer) | ✅ |
| **H2** | Skill 02 checklist: xóa hardcode "Teasing 15% + Bung nhe 20%..." → generic total=100% | ✅ |
| **H3** | Skills 00, 01: `type: output_schema` → `type: quality_checklist` trong section cuối | ✅ |
| **H4** | Sync benchmark Booking→Customer về 25-40% (skills 00 và 03 đều dùng cùng số) | ✅ |
| **M1** | Skill 06: di chuyển H1 title lên trước `<!-- #SECTION -->` đầu tiên | ✅ |

---

## 6. CẤU TRÚC #SECTION MARKERS

Mỗi SKILL.md được chia thành sections, lưu vào Supabase, chỉ load sections cần thiết → tiết kiệm ~44% token.

```markdown
<!-- #SECTION
id: context_intake
type: context_intake     ← context_intake | data_collection | logic | template |
                            output_template | negative_example | reference |
                            skill_chaining | quality_checklist
priority: 1              ← 1=luôn load | 2=standard | 3=chỉ khi mode=full
modes: [all]             ← [all] hoặc [full] hoặc [product] hoặc [personal_brand]
industries: [all]        ← [all] hoặc list ngành cụ thể
tags: [session_context]
-->

... nội dung section ...

<!-- #/SECTION -->
```

---

## 7. FILES QUAN TRỌNG

| File | Mục đích |
|------|---------|
| `HANDOFF.md` | File này — đọc đầu tiên |
| `CLAUDE.md` | Identity + workflow toàn hệ thống cho Claude Code local |
| `skills/vi/00-06/SKILL.md` | 7 core skills — đã hoàn chỉnh + ingested |
| `db/schema.sql` | Supabase schema: skills + skill_sections |
| `db/sessions.sql` | Supabase schema: sessions table cho n8n |
| `n8n/workflow-mkt-bot.json` | n8n workflow — import vào n8n Cloud |
| `n8n/SETUP.md` | Hướng dẫn setup n8n Cloud step-by-step |
| `scripts/ingest_skill.py` | Parse SKILL.md → upsert Supabase |
| `scripts/telegram_bot.py` | Telegram bot Python (prototype local, dùng để test) |
| `agents/` | 5 agent definitions (mkt-strategist, content-producer, ...) |
| `sub-agents/master-agent-critic.md` | Critic pattern — section markers, checklist 3 tầng |
| `sub-agents/master-agent-contract.md` | session_context schema + inject format |

---

## 8. PENDING TASKS — LÀM TIẾP Ở SESSION SAU

### Ưu tiên cao (cần để test được end-to-end)

- [ ] **Fix n8n Format Response node** — thêm `mode` + `industry` vào updatedSession (C3)
- [ ] **Chạy `db/sessions.sql`** trong Supabase SQL Editor
- [ ] **Import + configure n8n workflow** theo `n8n/SETUP.md`
- [ ] **Tạo `sub-agents/master-agent-output-format.md`** — quy tắc format: Telegram bullet ≤800 chars + Excel/HTML structure

### Ưu tiên trung bình

- [ ] **Test end-to-end trên n8n** — gửi Telegram, check flow qua từng node
- [ ] **Verify references tồn tại** — `references/copy-frameworks-vn.md` + `references/hook-formulas-vn.md` được reference trong skill 05

### Phase tiếp theo (sau khi v0.2 chạy được)

- [ ] Thêm skills 07–10 vào scope (thêm skill_id vào YAML + #SECTION markers + ingest)
- [ ] Upgrade `telegram_bot.py` Haiku → Sonnet (hiện output lỏng)
- [ ] Thêm Master Agent output formatter vào n8n workflow (hiện chỉ có raw text)
- [ ] Test với khách hàng thực tế (spa/clinic) — thu feedback

---

## 9. CÁCH TIẾP TỤC

**Paste đoạn này vào đầu session mới:**

> "Đọc HANDOFF.md tại root của repo Full-stack-mkt-v0.2. Tôi đang xây dựng CMO AI — Telegram Bot + n8n + Claude API + Supabase. 7 core skills (00–06) đã hoàn chỉnh và ingested. n8n workflow đã tạo nhưng chưa configure. Việc tiếp theo: fix C3 (Format Response node), setup n8n Cloud, test end-to-end."

---

## 10. REPO

| Repo | Link | Nội dung |
|------|------|---------|
| v0.1 (cũ) | https://github.com/TimothyMt/Full-stack-mkt-v0.1 | Toàn bộ 32 skills — lưu trữ |
| **v0.2 (đang dùng)** | **https://github.com/TimothyMt/Full-stack-mkt-v0.2** | **Core 7 skills + n8n + db** |
