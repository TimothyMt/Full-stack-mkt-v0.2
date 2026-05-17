# HANDOFF — CMO AI Bot v3
> Đọc file này trước khi làm việc với project. Chứa toàn bộ context cần thiết.

---

## 1. LINKS & CREDENTIALS

### GitHub
```
Repo:   https://github.com/TimothyMt/Full-stack-mkt-v0.2
Branch: main
Commit: 18c6a99 (latest)
```

### Anthropic API
```
Key:    ANTHROPIC_API_KEY=sk-ant-...   (điền trong Railway / .env)
Models đang dùng:
  - claude-haiku-4-5   → Layer 1 classify, summarize, chain summary, context extract
  - claude-sonnet-4-5  → Layer 2 Master Agent, Layer 3 Critic, self-improve
```

### Supabase
```
URL:     SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
Key:     SUPABASE_SERVICE_KEY=eyJ...   (Service Role key, không phải anon key)
Dashboard: https://supabase.com/dashboard
```

### Telegram Bot
```
Token:  TELEGRAM_BOT_TOKEN=...   (lấy từ @BotFather)
```

### Railway (Deploy)
```
Platform: railway.app
Procfile: worker: python scripts/telegram_bot.py
Env vars cần set trên Railway:
  - SUPABASE_URL
  - SUPABASE_SERVICE_KEY
  - TELEGRAM_BOT_TOKEN
  - ANTHROPIC_API_KEY
  - ADMIN_USER_IDS=7011450357
```

---

## 2. KIẾN TRÚC HỆ THỐNG

```
User message (Telegram)
    │
    ▼
[Layer 1] Haiku Classify
    → {skill_id, agent, mode}
    │
    ▼
[Layer 2] Master Agent (Sonnet)
    → Load agent persona + skill sections từ Supabase
    → Inject session_context + chain_context (output skills trước)
    → Quyết định: hỏi thêm hay generate output
    │
    ├── is_final_output()? NO  → gửi câu hỏi intake thẳng cho user
    │
    └── YES
        │
        ├── skill trong PASS2_SKILLS? → self_improve() (Sonnet tự phản biện)
        │
        ▼
    [Layer 3] Critic Review (Sonnet)
        → APPROVED: mark completed, log APPROVED signal
        → NEEDS_FIX: fix nội bộ, increment retry counter
        → retry >= 3: Haiku diagnose → gợi ý user → DỪNG
        │
        ▼
    summarize_to_bullets() [Haiku]
        → gửi bullet points cho user
        → nút HTML / Excel
        │
    User tải file → log EXPORTED signal
```

---

## 3. SUPABASE SCHEMA — Tất cả bảng đã tạo ✅

### `sessions`
```
user_id         TEXT PRIMARY KEY
session_context JSONB   -- {industry, business_name, business_stage, team_size,
                        --  active_channels, budget_monthly, kpi_targets, mode,
                        --  output_format, skill_outputs:{}, completed_skills:[]}
last_skill      TEXT    -- skill_id đang active
message_count   INT
```

### `skill_sections`
```
skill_id        TEXT
section_id      TEXT
section_type    TEXT
priority        INT     -- <=2: luôn load; >2: filter theo mode/industry
modes           TEXT[]  -- ['quick','detail','all']
industries      TEXT[]  -- ['spa','clinic','fnb','all',...]
content         TEXT
```
Skills đang có data: 00, 01, 02, 03, 04, 05, 06, 08, 09, 30, 31

### `pending_outputs`
```
user_id     TEXT PRIMARY KEY
content     TEXT            -- full output không truncate
skill_id    TEXT
created_at  TIMESTAMPTZ
```

### `usage_logs`
```
id            BIGSERIAL PRIMARY KEY
user_id       TEXT
model         TEXT    -- 'claude-sonnet-4-5', 'claude-haiku-4-5 (summarize)', ...
skill_id      TEXT
input_tokens  INT
output_tokens INT
created_at    TIMESTAMPTZ
```
Query chi phí tháng:
```sql
SELECT user_id,
       SUM(input_tokens + output_tokens) AS total_tokens,
       ROUND(SUM(input_tokens * 0.000003 + output_tokens * 0.000015), 4) AS usd_cost
FROM usage_logs
WHERE created_at >= date_trunc('month', now())
GROUP BY user_id ORDER BY usd_cost DESC;
```

### `skill_feedback`
```
id          BIGSERIAL PRIMARY KEY
skill_id    TEXT
issue       TEXT    -- mô tả vấn đề (NULL nếu APPROVED/EXPORTED)
industry    TEXT
user_id     TEXT
outcome     TEXT    -- 'APPROVED' | 'EXPORTED' | 'NEEDS_FIX'
created_at  TIMESTAMPTZ
```
Query chất lượng skill:
```sql
SELECT skill_id, industry,
       COUNT(*) FILTER (WHERE outcome = 'APPROVED')  AS approved,
       COUNT(*) FILTER (WHERE outcome = 'EXPORTED')  AS exported,
       COUNT(*) FILTER (WHERE outcome = 'NEEDS_FIX') AS needs_fix
FROM skill_feedback
WHERE created_at >= now() - interval '30 days'
GROUP BY skill_id, industry ORDER BY needs_fix DESC;
```

### `users`
```
user_id        TEXT PRIMARY KEY
token_balance  BIGINT DEFAULT 0
created_at     TIMESTAMPTZ
updated_at     TIMESTAMPTZ
```

### Supabase RPCs đã tạo
```sql
-- Nạp token cho user (dùng bởi /addtoken command)
SELECT add_tokens('telegram_user_id', 500000);

-- Trừ token sau mỗi API call (atomic)
SELECT deduct_tokens('telegram_user_id', 1500);
```

---

## 4. BOT COMMANDS

| Command | Ai dùng | Chức năng |
|---------|---------|-----------|
| `/start` | User | Reset session + giới thiệu |
| `/reset` | User | Xóa session, bắt đầu lại |
| `/balance` | User | Xem token còn lại |
| `/balance all` | Admin | Xem tất cả users |
| `/addtoken <user_id> <tokens>` | Admin | Nạp token thủ công |

Admin được cấu hình qua env: `ADMIN_USER_IDS=7011450357`

Workflow nạp token thủ công:
```
User báo hết token → gửi Telegram ID của họ cho admin
Admin: /addtoken <user_telegram_id> <số_token>
Bot: cộng token atomic qua RPC + tự notify user
```

---

## 5. CODE MAP — scripts/telegram_bot.py (1,286 dòng)

| Vùng | Nội dung |
|------|---------|
| 1–46 | Docstring + imports |
| 47–84 | Config: ADMIN_USER_IDS, Supabase/Claude/Telegram clients |
| 85–134 | SKILL_AGENT_MAP, AGENT_FILES, SKILL_CHAIN_INPUTS, in-memory dicts |
| 135–153 | `trim_chat_history()` — giới hạn 24K chars context |
| 154–244 | Session helpers: load/save/reset, `default_context()` |
| 245–290 | `pending_outputs` helpers |
| 291–330 | Prepaid: `get_token_balance`, `deduct_tokens`, `preflight_check` |
| 331–397 | `load_agent_persona()` + `fetch_sections()` — cả 2 có in-memory cache |
| 398–425 | `build_chain_context()` — inject output skill trước |
| 426–510 | `is_skill_switch()` + `haiku_classify()` — Layer 1 |
| 511–600 | `master_agent_respond()` — Layer 2 |
| 601–700 | `critic_review()` — Layer 3, return `(content, was_approved)` |
| 701–742 | `log_usage()` + `is_final_output()` |
| 743–863 | `summarize_to_bullets`, `self_improve`, `summarize_skill_output`, `extract_context_update` |
| 864–990 | `generate_html()`, `generate_excel()` |
| 991–1250 | Telegram handlers: `start`, `reset`, `cmd_addtoken`, `cmd_balance`, `handle_format_choice`, `handle_message` |
| 1260–1286 | `main()` — `app.run_polling()` |

---

## 6. SKILL MAP

### Agents active trong bot

| Agent | Skills active | Agent file |
|-------|--------------|------------|
| `mkt-strategist` | 00, 02, 30, 31 ✅ \| 08, 09 ⚠️ chưa sync | `agents/mkt-strategist.md` |
| `content-producer` | 01, 04, 05, 06 | `agents/content-producer.md` |
| `performance-analyst` | 03 | `agents/performance-analyst.md` |
| `channel-operator` | — chưa có skill nào | `agents/channel-operator.md` |
| `personal-brand-builder` | — file có nhưng chưa khai báo trong `AGENT_FILES` | `agents/personal-brand-builder.md` |

### Skill Chain

```
08-nghien-cuu-doi-thu ──┐
                        ├──▶ 00-ke-hoach-mkt ──▶ 01-lich-noi-dung
09-insight-khach-hang ──┘         │
                                  └──▶ 02-brief-chien-dich ──▶ 04, 05, 06
                                            │
                                            └──▶ 03-danh-gia-hieu-suat

30-retention-strategy ──▶ 31-winback-campaign
```

### PASS2_SKILLS (Sonnet self-improve trước Critic)
```python
PASS2_SKILLS = {"00-ke-hoach-mkt", "02-brief-chien-dich"}
```

---

## 7. BUGS ĐÃ BIẾT — CHƯA FIX

### BUG 1 — `reset_session` không xóa được `_critic_retry`
**File:** `telegram_bot.py` line ~243

```python
# HIỆN TẠI (sai — key format không khớp, không xóa được gì)
_critic_retry.pop((user_id,), None)

# FIX ĐÚNG
keys_to_remove = [k for k in _critic_retry if k[0] == user_id]
for k in keys_to_remove:
    del _critic_retry[k]
```
**Hệ quả:** User `/reset` nhưng retry counter không reset → safety valve kích hoạt sai.

### BUG 2 — Skills 08, 09 chưa đồng bộ đủ 3 chỗ
Cần thêm đồng thời vào 3 nơi trong `telegram_bot.py`:

```python
# 1. SKILL_AGENT_MAP (line ~104) — thêm 2 dòng
"08-nghien-cuu-doi-thu": "mkt-strategist",
"09-insight-khach-hang": "mkt-strategist",

# 2. haiku_classify() prompt (line ~428) — thêm vào "Skills available:"
"- 08-nghien-cuu-doi-thu: nghien cuu doi thu, competitor analysis, benchmark"
"- 09-insight-khach-hang: insight khach hang, customer research, hanh vi nguoi dung"
# Và sửa Agents: mkt-strategist: skills 00, 02, 08, 09, 30, 31

# 3. SKILL_CHAIN_INPUTS (line ~119) — thêm/sửa 2 dòng
"00-ke-hoach-mkt":     ["08-nghien-cuu-doi-thu", "09-insight-khach-hang"],
"02-brief-chien-dich": ["00-ke-hoach-mkt", "08-nghien-cuu-doi-thu", "09-insight-khach-hang"],
```

---

## 8. TODO / BACKLOG

| Priority | Task |
|----------|------|
| 🔴 | Fix Bug 1: `reset_session` `_critic_retry` wrong key |
| 🔴 | Fix Bug 2: sync skills 08+09 vào 3 chỗ |
| 🟡 | Thêm `personal-brand-builder` vào `AGENT_FILES` dict khi cần dùng PB skills |
| 🟡 | Wrap blocking calls `asyncio.to_thread` — khi >3 concurrent users |
| 🟡 | `_sections_cache` không có TTL → stale nếu update Supabase content |
| 🔵 | Admin audit log: `/addtoken` chưa ghi vào DB (ai nạp, bao nhiêu, lúc nào) |
| 🔵 | Weekly skill feedback review từ bảng `skill_feedback` |
| 🔵 | Tích hợp Tara Agent auto-post LinkedIn/Facebook (repo: `thaolst/tara-agent`) |
| 🔵 | Tái tích hợp MoMo/ZaloPay khi sẵn sàng (code cũ ở commit `baf7432`) |

---

## 9. SQL SCRIPTS STATUS

| File | Đã chạy? | Mục đích |
|------|---------|---------|
| `scripts/setup_db_tables.sql` | ✅ | Tạo `pending_outputs`, `usage_logs` |
| `scripts/setup_prepaid.sql` | ✅ | Tạo `users` table, RPC `add_tokens`, `deduct_tokens` |
| `scripts/add_outcome_column.sql` | ✅ | Thêm cột `outcome` vào `skill_feedback` |
| `scripts/setup_payments.sql` | ⬜ chưa cần | Tạo `payment_orders` (để dành khi tái tích hợp payment) |

---

## 10. PROJECT STRUCTURE

```
Full-stack-mkt-v0.2/
├── scripts/
│   ├── telegram_bot.py          ← File chính (1,286 dòng)
│   ├── fix_skills_30_31.py      ← Script upsert skills vào Supabase
│   ├── setup_db_tables.sql      ← ✅ đã chạy
│   ├── setup_prepaid.sql        ← ✅ đã chạy
│   ├── add_outcome_column.sql   ← ✅ đã chạy
│   └── setup_payments.sql       ← ⬜ để dành
├── agents/
│   ├── mkt-strategist.md
│   ├── content-producer.md
│   ├── performance-analyst.md
│   ├── channel-operator.md
│   └── personal-brand-builder.md
├── Procfile                     ← worker: python scripts/telegram_bot.py
├── requirements.txt             ← 7 deps (supabase, anthropic, python-telegram-bot, openpyxl, markdown, dotenv, PyYAML)
├── .env.example                 ← 5 env vars cần thiết
└── HANDOFF.md                   ← file này
```

---

## 11. GIT HISTORY

```
18c6a99  refactor: remove MoMo/ZaloPay — admin adds tokens manually  ← LATEST
baf7432  feat: MoMo + ZaloPay payment (code vẫn còn trong git history nếu cần)
64a558e  feat: admin /addtoken + /balance
7671f59  feat: Sprint 2 — retry introspection, state machine, Pass@2, prepaid tokens
51bfedb  feat: Sprint 1 — context trim, smart summary, log signals
48337f8  perf: CTO optimizations #1-8
c7b4479  feat: context isolation per skill + feedback log
26a8354  feat: skills 30-retention + 31-winback
```
