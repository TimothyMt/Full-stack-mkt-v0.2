"""
CMO AI — Telegram Bot
Multi-turn conversation + Supabase session persistence

Flow:
  User message
    -> Load session tu Supabase (neu co)
    -> Fetch skill sections tu Supabase
    -> Build prompt (session_context + sections + history)
    -> Claude generate reply
    -> Save session vao Supabase
    -> Telegram reply
"""

import os
import asyncio
import logging
from dotenv import load_dotenv
from supabase import create_client, Client
import anthropic
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, MessageHandler,
    CommandHandler, filters, ContextTypes
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

# -- In-memory history (conversation turns, not persisted) --
# Supabase luu session_context, RAM luu history turns
chat_history: dict = {}


# -- Supabase session helpers --

def load_session(user_id: str) -> dict:
    """Load session_context tu Supabase. Neu chua co thi tao moi."""
    try:
        res = supabase.table("sessions") \
            .select("session_context, last_skill, message_count") \
            .eq("user_id", user_id) \
            .execute()

        if res.data:
            row = res.data[0]
            logger.info(f"[{user_id}] Session loaded from Supabase (skill: {row.get('last_skill')})")
            return {
                "session_context": row.get("session_context") or default_context(),
                "skill_id": row.get("last_skill"),
                "message_count": row.get("message_count") or 0,
            }
    except Exception as e:
        logger.warning(f"[{user_id}] Load session error: {e}")

    logger.info(f"[{user_id}] New session created")
    return {
        "session_context": default_context(),
        "skill_id": None,
        "message_count": 0,
    }


def save_session(user_id: str, session: dict) -> None:
    """Upsert session vao Supabase sau moi message."""
    try:
        supabase.table("sessions").upsert({
            "user_id": user_id,
            "session_context": session["session_context"],
            "last_skill": session.get("skill_id"),
            "message_count": session.get("message_count", 0),
        }, on_conflict="user_id").execute()
        logger.info(f"[{user_id}] Session saved to Supabase")
    except Exception as e:
        logger.warning(f"[{user_id}] Save session error: {e}")


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
    }


def reset_session(user_id: str) -> None:
    """Xoa session trong Supabase va RAM."""
    try:
        supabase.table("sessions").delete().eq("user_id", user_id).execute()
        logger.info(f"[{user_id}] Session deleted from Supabase")
    except Exception as e:
        logger.warning(f"[{user_id}] Delete session error: {e}")
    chat_history.pop(user_id, None)


# -- Skill detection --

def detect_skill(message: str) -> str:
    msg = message.lower()
    if any(k in msg for k in ["ke hoach", "marketing plan", "chien luoc", "gtm", "launch", "lap ke"]):
        return "00-ke-hoach-mkt"
    if any(k in msg for k in ["lich noi dung", "content calendar", "lich dang", "bai viet thang"]):
        return "01-lich-noi-dung"
    if any(k in msg for k in ["brief chien dich", "campaign brief", "chien dich"]):
        return "02-brief-chien-dich"
    if any(k in msg for k in ["danh gia", "hieu suat", "performance", "audit", "roi", "roas"]):
        return "03-danh-gia-hieu-suat"
    if any(k in msg for k in ["script", "video", "tiktok", "reels", "clip"]):
        return "04-script-video"
    if any(k in msg for k in ["copy", "quang cao", "ad copy", "facebook ads", "chay ads"]):
        return "05-copy-quang-cao"
    if any(k in msg for k in ["ugc", "egc", "koc", "creator", "influencer"]):
        return "06-brief-ugc-egc"
    return "00-ke-hoach-mkt"


# -- Fetch skill sections --

def fetch_sections(skill_id: str, mode: str = "quick", industry: str = "general") -> list[dict]:
    res = supabase.table("skill_sections") \
        .select("section_id, section_type, priority, modes, industries, content") \
        .eq("skill_id", skill_id) \
        .order("priority") \
        .execute()

    filtered = []
    for sec in res.data:
        p = sec["priority"]
        modes = sec["modes"]
        industries = sec["industries"]
        if p <= 2:
            filtered.append(sec)
        elif ("all" in modes or mode in modes) and \
             ("all" in industries or industry in industries):
            filtered.append(sec)
    return filtered


# -- Extract context from conversation --

def extract_context_update(user_message: str, assistant_reply: str, current_context: dict) -> dict:
    """
    Dung Haiku de extract thong tin tu conversation va update session_context.
    Chi update field nao co gia tri moi, giu nguyen field da co.
    """
    try:
        extract_prompt = f"""Extract thong tin tu doan hoi thoai sau va tra ve JSON.
Chi lay thong tin USER da noi ro rang. Neu khong ro, de null.

Conversation:
User: {user_message}
Assistant: {assistant_reply}

Current context (chi update neu co thong tin moi):
{current_context}

Tra ve JSON voi cac field sau (chi field co thong tin moi, bo qua field khac):
{{
  "industry": "spa | clinic | fnb | fashion | edu | null",
  "business_name": "ten thuong hieu hoac null",
  "business_stage": "startup | growth | scale | null",
  "team_size": "so nguoi hoac null",
  "active_channels": "facebook,tiktok,... hoac null",
  "budget_monthly": "so tien VND hoac null",
  "kpi_targets": "mo ta KPI hoac null"
}}

Chi tra ve JSON thuan tuy, khong giai thich."""

        res = claude.messages.create(
            model="claude-haiku-4-5",
            max_tokens=300,
            messages=[{"role": "user", "content": extract_prompt}]
        )

        import json
        raw = res.content[0].text.strip()
        # Clean JSON neu co markdown
        if "```" in raw:
            raw = raw.split("```")[1].replace("json", "").strip()

        extracted = json.loads(raw)

        # Merge: chi update field null hoac co gia tri moi
        updated = current_context.copy()
        for key, value in extracted.items():
            if value and value != "null" and key in updated:
                updated[key] = value

        logger.info(f"Context extracted: {extracted}")
        return updated

    except Exception as e:
        logger.warning(f"Context extraction failed: {e}")
        return current_context


# -- Build system prompt --

def build_system_prompt(session_context: dict, sections: list[dict]) -> str:
    null_fields = [k for k, v in session_context.items() if v is None]
    ctx = session_context
    prefix = f"""[SESSION CONTEXT]
industry: {ctx.get('industry', 'null -- chua biet, can hoi')}
business_name: {ctx.get('business_name', 'null')}
business_stage: {ctx.get('business_stage', 'null')}
team_size: {ctx.get('team_size', 'null')}
active_channels: {ctx.get('active_channels', 'null')}
budget: {ctx.get('budget_monthly', 'null')}
kpi_targets: {ctx.get('kpi_targets', 'null')}
mode: {ctx.get('mode', 'quick')}
---
Cac field null (can hoi user): {null_fields if null_fields else 'khong co -- du thong tin'}

[SKILL INSTRUCTION]
"""
    skill_content = "\n\n---\n\n".join(
        f"<!-- SECTION: {s['section_id']} -->\n{s['content']}\n<!-- /SECTION: {s['section_id']} -->"
        for s in sections
    )
    return prefix + skill_content


# -- Telegram Handlers --

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    reset_session(user_id)

    await update.message.reply_text(
        "Xin chao! Toi la CMO AI -- tro ly marketing chuyen nghiep.\n\n"
        "Ban muon lam gi hom nay?\n\n"
        "Thu nhan:\n"
        "- Lap ke hoach marketing cho spa cua toi\n"
        "- Viet script TikTok ban ao dai\n"
        "- Audit hieu suat quang cao thang nay\n"
        "- Viet copy Facebook Ads cho clinic\n\n"
        "Go /reset de bat dau lai session."
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    reset_session(user_id)
    await update.message.reply_text("Session da reset. Nhan lai de bat dau moi.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    user_message = update.message.text

    # Load session tu Supabase
    session = load_session(user_id)

    # Init history neu chua co
    if user_id not in chat_history:
        chat_history[user_id] = []

    # Detect skill neu chua co
    if not session["skill_id"]:
        session["skill_id"] = detect_skill(user_message)
        logger.info(f"[{user_id}] Skill detected: {session['skill_id']}")

    # Tang message count
    session["message_count"] = session.get("message_count", 0) + 1

    # Them message vao history
    chat_history[user_id].append({"role": "user", "content": user_message})

    # Typing indicator
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")

    try:
        skill_id = session["skill_id"]
        ctx = session["session_context"]

        # Fetch sections tu Supabase
        industry = ctx.get("industry") or "general"
        mode = ctx.get("mode") or "quick"
        sections = fetch_sections(skill_id, mode, industry)
        logger.info(f"[{user_id}] Fetched {len(sections)} sections for skill '{skill_id}'")

        # Build system prompt
        system_prompt = build_system_prompt(ctx, sections)

        # Goi Claude
        response = claude.messages.create(
            model="claude-haiku-4-5",
            max_tokens=2048,
            system=system_prompt,
            messages=chat_history[user_id]
        )

        reply = response.content[0].text

        # Luu reply vao history
        chat_history[user_id].append({"role": "assistant", "content": reply})

        # Extract va update session_context tu conversation
        session["session_context"] = extract_context_update(
            user_message, reply, session["session_context"]
        )

        logger.info(f"[{user_id}] Reply: {len(reply)} chars | Turns: {len(chat_history[user_id])} | Skill: {skill_id}")
        logger.info(f"[{user_id}] Context: {session['session_context']}")

        # Save session vao Supabase
        save_session(user_id, session)

        # Gui reply (chia nho neu > 4000 chars)
        if len(reply) > 4000:
            chunks = [reply[i:i+4000] for i in range(0, len(reply), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"[{user_id}] Error: {e}", exc_info=True)
        await update.message.reply_text(
            f"Co loi xay ra: {str(e)[:100]}\n\nThu lai hoac /reset de bat dau lai."
        )


# -- Main --

def main():
    if not TELEGRAM_TOKEN:
        print("Thieu TELEGRAM_BOT_TOKEN trong .env")
        return

    print("CMO AI Bot dang chay...")
    print("  /start -- bat dau session moi")
    print("  /reset -- reset conversation")
    print("  Ctrl+C de dung\n")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        app.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        print("Bot da dung.")


if __name__ == "__main__":
    main()
