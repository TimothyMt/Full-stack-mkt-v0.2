"""
CMO AI - Telegram Bot v2
Flow:
  User request
    -> Load session tu Supabase
    -> Fetch skill sections
    -> Sonnet execute skill (full content)
    -> Sonnet summarize -> bullet points -> Telegram
    -> Hoi format: HTML hay Excel?
    -> Generate file -> Send file qua Telegram
    -> Save session -> Extract context
"""

import os
import re
import json
import asyncio
import logging
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
import anthropic
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import markdown as md_lib
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, MessageHandler,
    CommandHandler, CallbackQueryHandler,
    filters, ContextTypes
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# -- Clients --
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)
claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# -- In-memory: history + pending response --
chat_history: dict = {}       # {user_id: [messages]}
pending_response: dict = {}   # {user_id: full_content_string}


# ── Session helpers ────────────────────────────────────────────────────────────

def default_context() -> dict:
    return {
        "industry": None,
        "business_name": None,
        "business_stage": None,
        "team_size": None,
        "active_channels": None,
        "budget_monthly": None,
        "kpi_targets": None,
        "mode": "quick",
        "output_format": None,   # "html" | "excel"
    }


def load_session(user_id: str) -> dict:
    try:
        res = supabase.table("sessions") \
            .select("session_context, last_skill, message_count") \
            .eq("user_id", user_id).execute()
        if res.data:
            row = res.data[0]
            logger.info(f"[{user_id}] Session loaded (skill: {row.get('last_skill')})")
            return {
                "session_context": row.get("session_context") or default_context(),
                "skill_id": row.get("last_skill"),
                "message_count": row.get("message_count") or 0,
            }
    except Exception as e:
        logger.warning(f"[{user_id}] Load session error: {e}")
    return {"session_context": default_context(), "skill_id": None, "message_count": 0}


def save_session(user_id: str, session: dict) -> None:
    try:
        supabase.table("sessions").upsert({
            "user_id": user_id,
            "session_context": session["session_context"],
            "last_skill": session.get("skill_id"),
            "message_count": session.get("message_count", 0),
        }, on_conflict="user_id").execute()
        logger.info(f"[{user_id}] Session saved")
    except Exception as e:
        logger.warning(f"[{user_id}] Save session error: {e}")


def reset_session(user_id: str) -> None:
    try:
        supabase.table("sessions").delete().eq("user_id", user_id).execute()
    except Exception as e:
        logger.warning(f"[{user_id}] Delete session error: {e}")
    chat_history.pop(user_id, None)
    pending_response.pop(user_id, None)


# ── Skill detection ────────────────────────────────────────────────────────────

def detect_skill(message: str) -> str:
    msg = message.lower()
    if any(k in msg for k in ["ke hoach", "marketing plan", "chien luoc", "gtm", "lap ke", "fullstack"]):
        return "00-ke-hoach-mkt"
    if any(k in msg for k in ["lich noi dung", "content calendar", "lich dang", "bai viet thang"]):
        return "01-lich-noi-dung"
    if any(k in msg for k in ["brief chien dich", "campaign brief", "chien dich quang cao"]):
        return "02-brief-chien-dich"
    if any(k in msg for k in ["danh gia", "hieu suat", "performance", "audit", "roas", "roi", "cpm"]):
        return "03-danh-gia-hieu-suat"
    if any(k in msg for k in ["script", "video", "tiktok", "reels", "clip", "kich ban"]):
        return "04-script-video"
    if any(k in msg for k in ["copy", "quang cao", "ad copy", "facebook ads", "chay ads", "viet ads"]):
        return "05-copy-quang-cao"
    if any(k in msg for k in ["ugc", "egc", "koc", "creator", "influencer", "review"]):
        return "06-brief-ugc-egc"
    return "00-ke-hoach-mkt"


# ── Supabase fetch ─────────────────────────────────────────────────────────────

def fetch_sections(skill_id: str, mode: str = "quick", industry: str = "general") -> list[dict]:
    res = supabase.table("skill_sections") \
        .select("section_id, section_type, priority, modes, industries, content") \
        .eq("skill_id", skill_id).order("priority").execute()
    filtered = []
    for sec in res.data:
        p, modes, industries = sec["priority"], sec["modes"], sec["industries"]
        if p <= 2:
            filtered.append(sec)
        elif ("all" in modes or mode in modes) and ("all" in industries or industry in industries):
            filtered.append(sec)
    return filtered


# ── Prompts ────────────────────────────────────────────────────────────────────

def build_system_prompt(session_context: dict, sections: list[dict]) -> str:
    null_fields = [k for k, v in session_context.items() if v is None and k != "output_format"]
    ctx = session_context
    prefix = f"""[SESSION CONTEXT]
industry: {ctx.get('industry', 'null - chua biet, can hoi')}
business_name: {ctx.get('business_name', 'null')}
business_stage: {ctx.get('business_stage', 'null')}
team_size: {ctx.get('team_size', 'null')}
active_channels: {ctx.get('active_channels', 'null')}
budget: {ctx.get('budget_monthly', 'null')}
kpi_targets: {ctx.get('kpi_targets', 'null')}
mode: {ctx.get('mode', 'quick')}
---
Cac field null (can hoi user): {null_fields if null_fields else 'du thong tin'}

[SKILL INSTRUCTION]
"""
    skill_content = "\n\n---\n\n".join(
        f"<!-- SECTION: {s['section_id']} -->\n{s['content']}\n<!-- /SECTION -->"
        for s in sections
    )
    return prefix + skill_content


# ── Sonnet Summarize → Bullet Points ──────────────────────────────────────────

def summarize_to_bullets(full_content: str, skill_id: str) -> str:
    """Dung Sonnet tom tat thanh bullet points ngan gon."""
    try:
        res = claude.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"""Tom tat noi dung marketing sau thanh 5-8 bullet points ngan gon, actionable.
Format:
• [Diem chinh 1]
• [Diem chinh 2]
...

Cuoi cung them 1 dong: "📎 Ban muon xem ban day du dang nao?"

Noi dung can tom tat:
{full_content[:3000]}"""
            }]
        )
        return res.content[0].text
    except Exception as e:
        logger.warning(f"Summarize error: {e}")
        # Fallback: lay 5 dong dau co bullet
        lines = [l for l in full_content.split('\n') if l.strip().startswith(('•', '-', '*', '#'))]
        bullets = '\n'.join(lines[:7]) if lines else full_content[:500]
        return f"{bullets}\n\n📎 Ban muon xem ban day du dang nao?"


# ── Context Extraction ─────────────────────────────────────────────────────────

def extract_context_update(user_message: str, assistant_reply: str, current_context: dict) -> dict:
    """Dung Sonnet extract thong tin tu conversation va update session_context."""
    try:
        res = claude.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"""Extract thong tin tu conversation nay. Chi lay thong tin user da noi ro. Neu khong ro thi de null.

User: {user_message}
Assistant: {assistant_reply[:500]}

Tra ve JSON thuan tuy (khong markdown):
{{
  "industry": "spa|clinic|fnb|fashion|edu|null",
  "business_name": "ten hoac null",
  "business_stage": "startup|growth|scale|null",
  "team_size": "so nguoi hoac null",
  "active_channels": "facebook,tiktok,... hoac null",
  "budget_monthly": "so tien hoac null",
  "kpi_targets": "mo ta hoac null"
}}"""
            }]
        )
        raw = res.content[0].text.strip()
        if "```" in raw:
            raw = raw.split("```")[1].replace("json", "").strip()
        extracted = json.loads(raw)
        updated = current_context.copy()
        for key, value in extracted.items():
            if value and value != "null" and key in updated and not updated.get(key):
                updated[key] = value
        logger.info(f"Context updated: {extracted}")
        return updated
    except Exception as e:
        logger.warning(f"Context extraction failed: {e}")
        return current_context


# ── File Generators ────────────────────────────────────────────────────────────

def generate_html(skill_id: str, content: str, business_name: str = "") -> BytesIO:
    """Convert full markdown content thanh HTML dep, co the in."""
    date_str = datetime.now().strftime("%d/%m/%Y")
    title = f"CMO AI Report — {business_name or skill_id} — {date_str}"

    # Convert markdown sang HTML
    html_body = md_lib.markdown(
        content,
        extensions=["tables", "fenced_code", "nl2br"]
    )

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    max-width: 900px;
    margin: 40px auto;
    padding: 0 24px;
    color: #222;
    line-height: 1.7;
  }}
  .header {{
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    color: white;
    padding: 32px;
    border-radius: 12px;
    margin-bottom: 32px;
  }}
  .header h1 {{ margin: 0; font-size: 24px; }}
  .header p {{ margin: 8px 0 0; opacity: 0.7; font-size: 14px; }}
  h1 {{ color: #1a1a2e; border-bottom: 3px solid #e94560; padding-bottom: 8px; }}
  h2 {{ color: #16213e; border-left: 4px solid #e94560; padding-left: 12px; }}
  h3 {{ color: #0f3460; }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  }}
  th {{
    background: #1a1a2e;
    color: white;
    padding: 10px 14px;
    text-align: left;
    font-size: 13px;
  }}
  td {{ padding: 9px 14px; border-bottom: 1px solid #eee; font-size: 13px; }}
  tr:nth-child(even) {{ background: #f8f9fa; }}
  blockquote {{
    border-left: 4px solid #e94560;
    margin: 16px 0;
    padding: 12px 20px;
    background: #fff5f5;
    color: #555;
  }}
  code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-size: 13px; }}
  hr {{ border: none; border-top: 2px dashed #ddd; margin: 24px 0; }}
  ul li, ol li {{ margin: 6px 0; }}
  .footer {{
    margin-top: 48px;
    padding-top: 16px;
    border-top: 1px solid #eee;
    font-size: 12px;
    color: #999;
    text-align: center;
  }}
  @media print {{
    .header {{ -webkit-print-color-adjust: exact; }}
    th {{ -webkit-print-color-adjust: exact; }}
  }}
</style>
</head>
<body>
  <div class="header">
    <h1>📊 {title}</h1>
    <p>Generated by CMO AI — Over Powers Agency Framework</p>
  </div>

  {html_body}

  <div class="footer">
    CMO AI • Generated {date_str} • Powered by Claude Sonnet
  </div>
</body>
</html>"""

    buf = BytesIO()
    buf.write(html.encode("utf-8"))
    buf.seek(0)
    return buf


def generate_excel(skill_id: str, content: str, business_name: str = "") -> BytesIO:
    """Convert full content thanh Excel co dinh dang dep."""
    wb = openpyxl.Workbook()
    ws = wb.active
    date_str = datetime.now().strftime("%d/%m/%Y")
    sheet_name = (business_name or skill_id)[:28]
    ws.title = sheet_name

    # Style helpers
    def header_style(cell, level=1):
        if level == 1:
            cell.font = Font(bold=True, size=14, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="1a1a2e")
        elif level == 2:
            cell.font = Font(bold=True, size=12, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="16213e")
        elif level == 3:
            cell.font = Font(bold=True, size=11, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="0f3460")
        cell.alignment = Alignment(wrap_text=True, vertical="center")

    def table_header_style(cell):
        cell.font = Font(bold=True, size=10, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="e94560")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    def normal_style(cell, is_even=False):
        cell.font = Font(size=10)
        if is_even:
            cell.fill = PatternFill("solid", fgColor="F8F9FA")
        cell.alignment = Alignment(wrap_text=True, vertical="top")

    # Title row
    ws.merge_cells("A1:F1")
    title_cell = ws["A1"]
    title_cell.value = f"CMO AI Report — {business_name or skill_id} — {date_str}"
    title_cell.font = Font(bold=True, size=16, color="FFFFFF")
    title_cell.fill = PatternFill("solid", fgColor="1a1a2e")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 40

    row = 3
    in_table = False
    table_headers = []
    table_row_count = 0

    lines = content.split('\n')

    for line in lines:
        # H1
        if line.startswith("# ") and not line.startswith("## "):
            ws.merge_cells(f"A{row}:F{row}")
            cell = ws.cell(row=row, column=1, value=line[2:].strip())
            header_style(cell, 1)
            ws.row_dimensions[row].height = 28
            row += 1

        # H2
        elif line.startswith("## ") and not line.startswith("### "):
            ws.merge_cells(f"A{row}:F{row}")
            cell = ws.cell(row=row, column=1, value=line[3:].strip())
            header_style(cell, 2)
            ws.row_dimensions[row].height = 24
            row += 1

        # H3
        elif line.startswith("### "):
            ws.merge_cells(f"A{row}:F{row}")
            cell = ws.cell(row=row, column=1, value=line[4:].strip())
            header_style(cell, 3)
            ws.row_dimensions[row].height = 22
            row += 1

        # Table row
        elif "|" in line and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            cells = [c for c in cells if c]

            if not cells:
                continue

            # Separator row
            if all(set(c) <= set("-: ") for c in cells):
                continue

            if not in_table:
                # First row = headers
                in_table = True
                table_headers = cells
                table_row_count = 0
                for col, header in enumerate(cells, 1):
                    cell = ws.cell(row=row, column=col, value=header)
                    table_header_style(cell)
                ws.row_dimensions[row].height = 20
                row += 1
            else:
                # Data rows
                table_row_count += 1
                for col, value in enumerate(cells, 1):
                    # Remove markdown bold
                    value = re.sub(r'\*\*(.+?)\*\*', r'\1', value)
                    cell = ws.cell(row=row, column=col, value=value)
                    normal_style(cell, is_even=(table_row_count % 2 == 0))
                ws.row_dimensions[row].height = 18
                row += 1

        # Horizontal rule
        elif line.strip() in ("---", "***", "___"):
            in_table = False
            table_headers = []
            row += 1

        # Bullet / normal line
        elif line.strip():
            in_table = False
            clean = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
            clean = re.sub(r'\*(.+?)\*', r'\1', clean)
            if clean.startswith(("- ", "* ", "• ")):
                clean = "• " + clean[2:]
            ws.merge_cells(f"A{row}:F{row}")
            cell = ws.cell(row=row, column=1, value=clean)
            normal_style(cell)
            ws.row_dimensions[row].height = 16
            row += 1

        else:
            # Empty line
            row += 1

    # Column widths
    col_widths = [60, 25, 25, 25, 25, 25]
    for i, width in enumerate(col_widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = width

    # Freeze top rows
    ws.freeze_panes = "A3"

    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


# ── Telegram Handlers ──────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    reset_session(user_id)
    await update.message.reply_text(
        "Xin chao! Toi la CMO AI — tro ly marketing chuyen nghiep.\n\n"
        "Toi se tra loi bang:\n"
        "1. Tom tat bullet points (nhanh, de doc)\n"
        "2. Ban day du dang HTML hoac Excel (in duoc, chỉnh sua duoc)\n\n"
        "Thu nhan:\n"
        "• Lap ke hoach marketing cho spa\n"
        "• Viet script TikTok ban ao dai\n"
        "• Viet copy Facebook Ads cho clinic\n"
        "• Audit hieu suat quang cao thang nay\n\n"
        "/reset - bat dau lai session"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    reset_session(user_id)
    await update.message.reply_text("Session da reset. Nhan lai de bat dau moi.")


async def handle_format_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xu ly khi user bam HTML hoac Excel button."""
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    fmt = query.data  # "html" hoac "excel"

    full_content = pending_response.get(user_id)
    if not full_content:
        await query.message.reply_text("Het session. Vui long nhan lai yeu cau.")
        return

    session = load_session(user_id)
    session["session_context"]["output_format"] = fmt
    save_session(user_id, session)

    business_name = session["session_context"].get("business_name") or ""
    skill_id = session.get("skill_id") or "report"
    date_str = datetime.now().strftime("%Y%m%d")

    await query.message.reply_text(f"Dang tao file {fmt.upper()}...")

    try:
        if fmt == "html":
            file_buf = generate_html(skill_id, full_content, business_name)
            filename = f"cmo-ai-{skill_id}-{date_str}.html"
            await query.message.reply_document(
                document=file_buf,
                filename=filename,
                caption=f"Ban day du dang HTML — {skill_id}"
            )
        else:
            file_buf = generate_excel(skill_id, full_content, business_name)
            filename = f"cmo-ai-{skill_id}-{date_str}.xlsx"
            await query.message.reply_document(
                document=file_buf,
                filename=filename,
                caption=f"Ban day du dang Excel — {skill_id}"
            )
        logger.info(f"[{user_id}] File {fmt} sent: {filename}")
    except Exception as e:
        logger.error(f"[{user_id}] Generate file error: {e}", exc_info=True)
        await query.message.reply_text(f"Loi tao file: {str(e)[:100]}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    user_message = update.message.text

    session = load_session(user_id)

    if user_id not in chat_history:
        chat_history[user_id] = []

    # Detect skill
    if not session["skill_id"]:
        session["skill_id"] = detect_skill(user_message)
        logger.info(f"[{user_id}] Skill: {session['skill_id']}")

    session["message_count"] = session.get("message_count", 0) + 1
    chat_history[user_id].append({"role": "user", "content": user_message})

    await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")

    try:
        skill_id = session["skill_id"]
        ctx = session["session_context"]
        industry = ctx.get("industry") or "general"
        mode = ctx.get("mode") or "quick"

        # 1. Fetch skill sections
        sections = fetch_sections(skill_id, mode, industry)
        logger.info(f"[{user_id}] Fetched {len(sections)} sections for '{skill_id}'")

        # 2. Sonnet execute skill → full content
        system_prompt = build_system_prompt(ctx, sections)
        response = claude.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            system=system_prompt,
            messages=chat_history[user_id]
        )
        full_content = response.content[0].text

        # Luu vao history va pending
        chat_history[user_id].append({"role": "assistant", "content": full_content})
        pending_response[user_id] = full_content

        logger.info(f"[{user_id}] Full content: {len(full_content)} chars")

        # 3. Sonnet summarize → bullet points
        await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        bullets = summarize_to_bullets(full_content, skill_id)

        # 4. Gui bullet points
        if len(bullets) > 4000:
            chunks = [bullets[i:i+4000] for i in range(0, len(bullets), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(bullets)

        # 5. Hoi format voi inline buttons
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📄 HTML (in duoc, dep)", callback_data="html"),
                InlineKeyboardButton("📊 Excel (chinh sua duoc)", callback_data="excel"),
            ]
        ])
        await update.message.reply_text(
            "Chon dinh dang ban day du:",
            reply_markup=keyboard
        )

        # 6. Extract context + save session
        session["session_context"] = extract_context_update(
            user_message, full_content[:500], session["session_context"]
        )
        save_session(user_id, session)

    except Exception as e:
        logger.error(f"[{user_id}] Error: {e}", exc_info=True)
        await update.message.reply_text(
            f"Co loi xay ra: {str(e)[:100]}\n\nThu lai hoac /reset."
        )


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if not TELEGRAM_TOKEN:
        print("Thieu TELEGRAM_BOT_TOKEN")
        return

    print("CMO AI Bot v2 dang chay...")
    print("  Flow: Sonnet execute -> Sonnet summarize -> HTML/Excel file")
    print("  /start /reset")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CallbackQueryHandler(handle_format_choice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        app.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        print("Bot da dung.")


if __name__ == "__main__":
    main()
