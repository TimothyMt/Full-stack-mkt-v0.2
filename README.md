# CMO AI — Marketing Assistant

AI Marketing Assistant cho founder và business owner — chạy qua Telegram, vận hành bởi n8n + Claude API + Supabase.

## Mô tả

Hệ thống AI giúp founder, business owner thực hiện các task marketing chuyên nghiệp thông qua Telegram — không cần team marketing, không cần kiến thức kỹ thuật.

User nhắn Telegram → nhận kế hoạch marketing, content, brief chiến dịch, phân tích hiệu suất — chất lượng ngang senior marketer, trong vài phút.

## Kiến trúc

```
Telegram → Haiku Classify → Master Agent (Sonnet)
→ Supabase fetch skill sections
→ Sonnet execute skill → Sonnet Critic review
→ Format output (Telegram summary + Excel/HTML file)
→ Save session → Telegram reply
```

## Core Skills (v0.2)

| Skill | Mô tả |
|-------|-------|
| 00-ke-hoach-mkt | Kế hoạch Fullstack Marketing |
| 01-lich-noi-dung | Lịch nội dung tháng |
| 02-brief-chien-dich | Brief chiến dịch 10 phần |
| 03-danh-gia-hieu-suat | Đánh giá hiệu suất + diagnostic |
| 04-script-video | Script TikTok/Reels/Shorts |
| 05-copy-quang-cao | Copy quảng cáo đa nền tảng |
| 06-brief-ugc-egc | Brief UGC/EGC/KOC |

## Tech Stack

- **AI:** Claude API (Haiku classify + Sonnet execute + Sonnet critic)
- **Automation:** n8n Cloud
- **Database:** Supabase (skills, skill_sections, sessions)
- **Channel:** Telegram Bot

## Setup

Xem `HANDOFF.md` để hiểu toàn bộ trạng thái project và việc cần làm tiếp theo.

Xem `n8n/SETUP.md` để setup n8n Cloud step-by-step.

## Cấu trúc thư mục

```
skills/vi/          ← 7 core skills tiếng Việt
agents/             ← 5 agent definitions
sub-agents/         ← Master Agent patterns (critic, contract, memory)
db/                 ← Supabase schema (skills + sessions)
n8n/                ← Workflow JSON + setup guide
scripts/            ← ingest_skill.py + telegram_bot.py
references/         ← Benchmark + channel system references
workflows/vi/       ← Workflow chains
```
