"""
CMO AI - Telegram Bot v3
3-layer architecture:
  Layer 1: Haiku Classify  -> {skill_id, agent, mode}
  Layer 2: Master Agent    -> orchestrate (hoi hoac execute)
  Layer 3: Critic Review   -> QA truoc khi gui (chi khi final output)

Flow:
  User message
    -> Haiku classify intent
    -> Load agent persona + skill sections
    -> Master Agent respond
    -> is_final_output()?
        YES -> Critic review -> Sonnet summarize -> HTML/Excel buttons
        NO  -> Send normally (intake question)
    -> Extract context -> Save session
"""

import os
import re
import json
import asyncio
import logging
from io import BytesIO
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
import anthropic
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
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

# ── Clients ────────────────────────────────────────────────────────────────────
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)
claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ── Maps ───────────────────────────────────────────────────────────────────────
SKILL_AGENT_MAP = {
    "00-ke-hoach-mkt":      "mkt-strategist",
    "01-lich-noi-dung":     "content-producer",
    "02-brief-chien-dich":  "mkt-strategist",
    "03-danh-gia-hieu-suat":"performance-analyst",
    "04-script-video":      "content-producer",
    "05-copy-quang-cao":    "content-producer",
    "06-brief-ugc-egc":     "content-producer",
    "30-retention-strategy":"mkt-strategist",
    "31-winback-campaign":  "mkt-strategist",
}

# Absolute path từ vị trí file script (fix #1)
BASE_DIR = Path(__file__).parent.parent

AGENT_FILES = {
    "mkt-strategist":      BASE_DIR / "agents/mkt-strategist.md",
    "content-producer":    BASE_DIR / "agents/content-producer.md",
    "performance-analyst": BASE_DIR / "agents/performance-analyst.md",
    "channel-operator":    BASE_DIR / "agents/channel-operator.md",
}

# Skill chain: skill X can output tu skill nao truoc do lam context
SKILL_CHAIN_INPUTS = {
    "01-lich-noi-dung":      ["00-ke-hoach-mkt", "02-brief-chien-dich"],
    "02-brief-chien-dich":   ["00-ke-hoach-mkt"],
    "03-danh-gia-hieu-suat": ["00-ke-hoach-mkt", "02-brief-chien-dich"],
    "04-script-video":       ["02-brief-chien-dich", "00-ke-hoach-mkt"],
    "05-copy-quang-cao":     ["02-brief-chien-dich", "00-ke-hoach-mkt"],
    "06-brief-ugc-egc":      ["02-brief-chien-dich", "00-ke-hoach-mkt"],
    "31-winback-campaign":   ["30-retention-strategy", "00-ke-hoach-mkt"],
}

# ── In-memory ─────────────────────────────────────────────────────────────────
chat_history: dict = {}     # {user_id: {skill_id: [messages]}}
pending_response: dict = {} # {user_id: full_content}
_persona_cache: dict = {}   # {agent_name: persona_text}      — cache #2
_sections_cache: dict = {}  # {(skill_id,mode,industry): []}  — cache #2


# ── Session helpers ────────────────────────────────────────────────────────────

def default_context() -> dict:
    return {
        "industry": None, "business_name": None, "business_stage": None,
        "team_size": None, "active_channels": None, "budget_monthly": None,
        "kpi_targets": None, "mode": "quick", "output_format": None,
        "skill_outputs": {},
        "daily_count": 0,
        "last_reset_date": "",
    }


def load_session(user_id: str) -> dict:
    try:
        res = supabase.table("sessions") \
            .select("session_context, last_skill, message_count") \
            .eq("user_id", user_id).execute()
        if res.data:
            row = res.data[0]
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
    except Exception as e:
        logger.warning(f"[{user_id}] Save session error: {e}")


# ── Pending output helpers (bảng riêng — không truncate) ──────────────────────

def save_pending_output(user_id: str, content: str, skill_id: str) -> None:
    """Luu full output vao bang pending_outputs (khong gioi han do dai)."""
    pending_response[user_id] = content
    try:
        supabase.table("pending_outputs").upsert({
            "user_id": user_id,
            "content": content,
            "skill_id": skill_id,
            "created_at": datetime.now().isoformat(),
        }, on_conflict="user_id").execute()
    except Exception as e:
        logger.warning(f"[{user_id}] Save pending error: {e}")


def load_pending_output(user_id: str) -> str:
    """Load pending output tu RAM truoc, fallback Supabase."""
    if user_id in pending_response:
        return pending_response[user_id]
    try:
        res = supabase.table("pending_outputs") \
            .select("content").eq("user_id", user_id).execute()
        if res.data:
            return res.data[0].get("content", "")
    except Exception as e:
        logger.warning(f"[{user_id}] Load pending error: {e}")
    return ""


def clear_pending_output(user_id: str) -> None:
    """Xoa pending output sau khi user da nhan file."""
    pending_response.pop(user_id, None)
    try:
        supabase.table("pending_outputs").delete().eq("user_id", user_id).execute()
    except Exception as e:
        logger.warning(f"[{user_id}] Clear pending error: {e}")


def reset_session(user_id: str) -> None:
    try:
        supabase.table("sessions").delete().eq("user_id", user_id).execute()
    except Exception as e:
        logger.warning(f"[{user_id}] Delete error: {e}")
    chat_history.pop(user_id, None)
    pending_response.pop(user_id, None)


# ── Load agent persona ─────────────────────────────────────────────────────────

def load_agent_persona(agent_name: str) -> str:
    """Doc file .md cua agent — cache in-memory, chi doc disk 1 lan."""
    if agent_name in _persona_cache:
        return _persona_cache[agent_name]
    file_path = AGENT_FILES.get(agent_name, AGENT_FILES["mkt-strategist"])
    try:
        content = Path(file_path).read_text(encoding="utf-8")
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2].strip()
        _persona_cache[agent_name] = content
        return content
    except Exception as e:
        logger.warning(f"Load agent persona error ({agent_name}): {e}")
        return "Ban la CMO AI — tro ly marketing chuyen nghiep."


# ── Supabase fetch sections ────────────────────────────────────────────────────

def fetch_sections(skill_id: str, mode: str = "quick", industry: str = "general") -> list[dict]:
    """Fetch sections tu Supabase — cache in-memory theo (skill_id, mode, industry)."""
    cache_key = (skill_id, mode, industry)
    if cache_key in _sections_cache:
        return _sections_cache[cache_key]
    res = supabase.table("skill_sections") \
        .select("section_id, section_type, priority, modes, industries, content") \
        .eq("skill_id", skill_id).order("priority").execute()
    filtered = []
    for sec in res.data:
        p, modes, inds = sec["priority"], sec["modes"], sec["industries"]
        if p <= 2:
            filtered.append(sec)
        elif ("all" in modes or mode in modes) and ("all" in inds or industry in inds):
            filtered.append(sec)
    _sections_cache[cache_key] = filtered
    return filtered


# ── Skill chain context ───────────────────────────────────────────────────────

def build_chain_context(skill_id: str, session_context: dict) -> str:
    """
    Lay output cua cac skill truoc lien quan de inject vao Master Agent.
    Vi du: skill 05 se nhan output cua 02 va 00 neu da co.
    """
    skill_outputs = session_context.get("skill_outputs") or {}
    if not skill_outputs:
        return ""

    relevant = SKILL_CHAIN_INPUTS.get(skill_id, [])
    if not relevant:
        return ""

    parts = []
    for prev_skill in relevant:
        out = skill_outputs.get(prev_skill, "")
        if out:
            parts.append(f"### [{prev_skill}]\n{out[:1500]}")

    if not parts:
        return ""

    return "\n\n".join(parts)


# ── Layer 1: Haiku Classify ────────────────────────────────────────────────────

def is_skill_switch(message: str) -> bool:
    """
    Detect neu user muon chuyen sang skill moi (fix #2, fix #8).
    Chi dung keyword dac trung cua skill request — tranh false positive voi
    cau tra loi intake ("toi can ngan sach 20 trieu", "giup toi hieu hon"...).
    """
    SKILL_KEYWORDS = [
        # Ke hoach / chien luoc
        "ke hoach marketing", "ke hoach mkt", "chien luoc marketing",
        "lap ke hoach", "xay dung chien luoc",
        # Lich noi dung
        "lich noi dung", "content calendar", "lich dang bai", "content plan",
        # Brief chien dich
        "brief chien dich", "brief campaign", "chien dich quang cao",
        # Danh gia hieu suat
        "danh gia hieu suat", "audit quang cao", "audit marketing",
        "phan tich kpi", "phan tich roas",
        # Script / video
        "script video", "kich ban video", "viet script", "script tiktok",
        # Copy quang cao
        "copy quang cao", "viet copy", "viet ads", "ad copy",
        "facebook ads", "tiktok ads", "quang cao facebook",
        # UGC / KOC
        "brief ugc", "brief koc", "brief influencer", "ugc creator",
        # Retention / Winback
        "giu chan khach", "retention", "khach quay lai", "giam churn",
        "winback", "lay lai khach", "khach cu da bo", "tai kich hoat",
        # Explicit skill switch signals
        "chuyen sang", "skill moi", "lam moi",
    ]
    msg = message.lower()
    return any(k in msg for k in SKILL_KEYWORDS) and len(message) > 20


def haiku_classify(message: str, current_skill: str = None) -> dict:
    """
    Dung Haiku phan loai intent.
    Returns: {skill_id, agent, mode}
    """
    # Giu skill hien tai neu message la cau tra loi ngan (khong co keyword moi)
    if current_skill and not is_skill_switch(message):
        return {
            "skill_id": current_skill,
            "agent": SKILL_AGENT_MAP.get(current_skill, "mkt-strategist"),
            "mode": "quick"
        }

    try:
        res = claude.messages.create(
            model="claude-haiku-4-5",
            max_tokens=150,
            messages=[{
                "role": "user",
                "content": f"""Classify marketing request. Return JSON only, no explanation.

Message: "{message}"

Skills available:
- 00-ke-hoach-mkt: ke hoach marketing, chien luoc, GTM
- 01-lich-noi-dung: lich noi dung, content calendar, bai dang
- 02-brief-chien-dich: brief chien dich quang cao, campaign
- 03-danh-gia-hieu-suat: danh gia hieu suat, audit, ROAS, ROI, CPM
- 04-script-video: script video, TikTok, Reels, kich ban
- 05-copy-quang-cao: copy quang cao, ad copy, Facebook/TikTok ads
- 06-brief-ugc-egc: brief UGC, KOC, influencer, creator
- 30-retention-strategy: giu khach, retention, khach quay lai, churn, loyalty
- 31-winback-campaign: winback, lay lai khach cu, khach da bo, tai kich hoat

Agents:
- mkt-strategist: skills 00, 02, 30, 31
- content-producer: skills 01, 04, 05, 06
- performance-analyst: skill 03

Return:
{{"skill_id": "00-ke-hoach-mkt", "agent": "mkt-strategist", "mode": "quick"}}"""
            }]
        )
        raw = res.content[0].text.strip()
        if "```" in raw:
            raw = raw.split("```")[1].replace("json", "").strip()
        result = json.loads(raw)
        logger.info(f"Haiku classify: {result}")
        return result
    except Exception as e:
        logger.warning(f"Haiku classify error: {e}")
        return {"skill_id": "00-ke-hoach-mkt", "agent": "mkt-strategist", "mode": "quick"}


# ── Layer 2: Master Agent ──────────────────────────────────────────────────────

def master_agent_respond(
    agent_name: str,
    skill_id: str,
    session_context: dict,
    history: list,
    sections: list[dict],
    chain_context: str = ""
) -> str:
    """
    Master Agent = Agent Persona + Session Context + Skill Sections + Chain Context.
    Quyet dinh: hoi them hay generate output.
    """
    # Load agent persona
    persona = load_agent_persona(agent_name)

    # Build skill content
    skill_content = "\n\n---\n\n".join(
        f"<!-- SECTION: {s['section_id']} -->\n{s['content']}\n<!-- /SECTION -->"
        for s in sections
    )

    # Build null fields list (fix #7: exclude internal fields)
    INTERNAL_FIELDS = {"output_format", "_pending_response", "skill_outputs"}
    null_fields = [k for k, v in session_context.items()
                   if v is None and k not in INTERNAL_FIELDS]

    # Build chain context section (skill chaining)
    chain_section = ""
    if chain_context:
        chain_section = f"""
---

[OUTPUT TU SKILL TRUOC — Dung lam context, KHONG lap lai nguyen van]
{chain_context}
"""

    system = f"""{persona}

---

[SESSION CONTEXT - Da biet]
industry: {session_context.get('industry', 'null')}
business_name: {session_context.get('business_name', 'null')}
business_stage: {session_context.get('business_stage', 'null')}
team_size: {session_context.get('team_size', 'null')}
active_channels: {session_context.get('active_channels', 'null')}
budget_monthly: {session_context.get('budget_monthly', 'null')}
kpi_targets: {session_context.get('kpi_targets', 'null')}
mode: {session_context.get('mode', 'quick')}

Thong tin con thieu: {null_fields if null_fields else 'Du - co the generate output'}
{chain_section}
---

[SKILL BEING EXECUTED: {skill_id}]
{skill_content}

---

QUAN TRONG:
- Neu con thieu thong tin quan trong -> hoi toi da 2 cau (ngan gon)
- Neu da du thong tin -> generate output day du theo skill template
- KHONG hoi lai thong tin da co trong SESSION CONTEXT
- Neu co OUTPUT TU SKILL TRUOC -> ke thua, khong hoi lai nhung gi da co"""

    return claude.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        system=system,
        messages=history
    )


# ── Layer 3: Critic Review ─────────────────────────────────────────────────────

def critic_review(content: str, skill_id: str, user_id: str = None, industry: str = None) -> str:
    """
    Sonnet Critic review output.
    - APPROVED -> tra ve content goc (co the chinh sua nho)
    - NEEDS_FIX -> log vao Supabase + fix 1 vong
    Toi da 1 vong fix.
    """
    critic_system = """Ban la Quality Reviewer cho he thong CMO AI.

Nhiem vu: Review marketing output va dam bao chat luong.
KHONG rewrite toan bo. Chi flag phan sai va sua chinh xac.

Tieu chi review:
1. Co du cac section theo skill template khong?
2. So lieu co cu the (KPI, budget, timeline) khong?
3. Co insight thuc te, khong chung chung khong?
4. Ngon ngu chuyen nghiep, phu hop thuong hieu khong?

Output format:
- Neu dat yeu cau: tra ve APPROVED::[noi dung da chinh sua nho neu can]
- Neu can sua: tra ve NEEDS_FIX::[mo ta van de]::[phan can sua]"""

    try:
        res = claude.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            system=critic_system,
            messages=[{
                "role": "user",
                "content": f"Review output nay cho skill {skill_id}:\n\n{content}"
            }]
        )
        log_usage(user_id or "unknown", "claude-sonnet-4-5 (critic)", skill_id, res)
        review = res.content[0].text

        if review.startswith("APPROVED::"):
            logger.info(f"Critic: APPROVED -> returning original content")
            return content

        elif review.startswith("NEEDS_FIX::"):
            logger.info(f"Critic: NEEDS_FIX -> logging + fix round")
            fix_instruction = review[len("NEEDS_FIX::"):]

            try:
                supabase.table("skill_feedback").insert({
                    "skill_id": skill_id,
                    "issue": fix_instruction[:500],
                    "industry": industry or "unknown",
                    "user_id": user_id or "unknown",
                    "created_at": datetime.now().isoformat()
                }).execute()
                logger.info(f"Skill feedback logged: {skill_id} | {industry}")
            except Exception as log_err:
                logger.warning(f"Skill feedback log error: {log_err}")

            fix_res = claude.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": f"Day la output marketing:\n\n{content}"},
                    {"role": "assistant", "content": "Da nhan output."},
                    {"role": "user", "content": f"Sua theo huong dan sau, giu nguyen cac phan da tot:\n{fix_instruction}"}
                ]
            )
            log_usage(user_id or "unknown", "claude-sonnet-4-5 (critic-fix)", skill_id, fix_res)
            fixed = fix_res.content[0].text
            logger.info(f"Critic: Fixed output ({len(fixed)} chars)")
            return fixed

        else:
            return content

    except Exception as e:
        logger.warning(f"Critic review error: {e}")
        return content


# ── Usage logging ─────────────────────────────────────────────────────────────

def log_usage(user_id: str, model: str, skill_id: str, response) -> None:
    """Ghi token usage vao Supabase usage_logs sau moi API call."""
    try:
        usage = response.usage
        supabase.table("usage_logs").insert({
            "user_id": user_id,
            "model": model,
            "skill_id": skill_id,
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "created_at": datetime.now().isoformat(),
        }).execute()
    except Exception as e:
        logger.warning(f"[{user_id}] Usage log error: {e}")


# ── Detect final output ────────────────────────────────────────────────────────

def is_final_output(reply: str) -> bool:
    """Final output = co cau truc ro rang + dai + KHONG ket thuc bang cau hoi."""
    header_count = len(re.findall(r'^#{1,3}\s', reply, re.MULTILINE))
    has_table = reply.count('|') > 6
    is_long = len(reply) > 1000
    is_very_long = len(reply) > 2000

    # Neu ket thuc bang cau hoi → la intake, khong phai output
    last_100 = reply[-100:] if len(reply) > 100 else reply
    ends_with_question = last_100.count('?') >= 1
    if ends_with_question:
        return False

    return (
        ((header_count >= 2 or has_table) and is_long)
        or (is_very_long and header_count >= 1)
    )


# ── Sonnet Summarize → Bullets ─────────────────────────────────────────────────

def summarize_to_bullets(full_content: str, skill_id: str) -> str:
    """Dung Haiku tom tat thanh 5-8 bullet points."""
    try:
        res = claude.messages.create(
            model="claude-haiku-4-5",
            max_tokens=800,
            messages=[{
                "role": "user",
                "content": f"""Tom tat noi dung marketing nay thanh 5-8 bullet points ngan gon, actionable.
Moi bullet = 1 dong, bat dau bang •
Format chuan:
• [Hanh dong / Insight chinh]

Cuoi: "📎 Chon dinh dang ban day du:"

Noi dung:
{full_content[:3000]}"""
            }]
        )
        log_usage("system", "claude-haiku-4-5 (summarize)", skill_id, res)
        return res.content[0].text
    except Exception as e:
        logger.warning(f"Summarize error: {e}")
        lines = [l for l in full_content.split('\n') if l.strip().startswith(('•', '-', '*', '#'))]
        return '\n'.join(lines[:7]) + "\n\n📎 Chon dinh dang ban day du:"


# ── Context extraction ─────────────────────────────────────────────────────────

def extract_context_update(user_msg: str, assistant_reply: str, ctx: dict) -> dict:
    try:
        res = claude.messages.create(
            model="claude-haiku-4-5",
            max_tokens=200,
            messages=[{
                "role": "user",
                "content": f"""Extract thong tin doanh nghiep tu cuoc hoi thoai. Chi lay thong tin user da noi ro rang.

User: {user_msg}
Assistant: {assistant_reply[:300]}

Tra ve JSON thuan tuy (khong markdown, khong giai thich). Cac truong:
- industry: "spa" | "clinic" | "fnb" | "fashion" | "edu" | null
- business_name: ten that cua doanh nghiep hoac null
- business_stage: "startup" | "growth" | "scale" | null
- team_size: so luong nhan vien (chuoi so) hoac null
- active_channels: cac kenh dang dung (chuoi) hoac null
- budget_monthly: ngan sach thang (chuoi so + don vi) hoac null
- kpi_targets: cac chi so KPI muc tieu hoac null

Neu khong co thong tin ro rang cho truong nao, de null. KHONG doan mo."""
            }]
        )
        raw = res.content[0].text.strip()
        if "```" in raw:
            raw = raw.split("```")[1].replace("json", "").strip()
        extracted = json.loads(raw)
        updated = ctx.copy()
        for k, v in extracted.items():
            if v and v != "null" and k in updated and not updated.get(k):
                updated[k] = v
        return updated
    except Exception as e:
        logger.warning(f"Context extract error: {e}")
        return ctx


# ── File generators ────────────────────────────────────────────────────────────

def generate_html(skill_id: str, content: str, business_name: str = "") -> BytesIO:
    date_str = datetime.now().strftime("%d/%m/%Y")
    title = f"CMO AI — {business_name or skill_id} — {date_str}"
    html_body = md_lib.markdown(content, extensions=["tables", "fenced_code", "nl2br"])
    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  body{{font-family:'Segoe UI',Arial,sans-serif;max-width:900px;margin:40px auto;padding:0 24px;color:#222;line-height:1.7}}
  .header{{background:linear-gradient(135deg,#1a1a2e,#16213e);color:white;padding:32px;border-radius:12px;margin-bottom:32px}}
  .header h1{{margin:0;font-size:22px}} .header p{{margin:8px 0 0;opacity:.7;font-size:13px}}
  h1{{color:#1a1a2e;border-bottom:3px solid #e94560;padding-bottom:8px}}
  h2{{color:#16213e;border-left:4px solid #e94560;padding-left:12px}}
  h3{{color:#0f3460}}
  table{{border-collapse:collapse;width:100%;margin:16px 0;box-shadow:0 1px 4px rgba(0,0,0,.1)}}
  th{{background:#1a1a2e;color:white;padding:10px 14px;text-align:left;font-size:13px}}
  td{{padding:9px 14px;border-bottom:1px solid #eee;font-size:13px}}
  tr:nth-child(even){{background:#f8f9fa}}
  blockquote{{border-left:4px solid #e94560;margin:16px 0;padding:12px 20px;background:#fff5f5;color:#555}}
  code{{background:#f4f4f4;padding:2px 6px;border-radius:4px;font-size:13px}}
  hr{{border:none;border-top:2px dashed #ddd;margin:24px 0}}
  .footer{{margin-top:48px;padding-top:16px;border-top:1px solid #eee;font-size:12px;color:#999;text-align:center}}
  @media print{{.header{{-webkit-print-color-adjust:exact}} th{{-webkit-print-color-adjust:exact}}}}
</style>
</head>
<body>
<div class="header"><h1>📊 {title}</h1><p>Generated by CMO AI — Over Powers Agency Framework</p></div>
{html_body}
<div class="footer">CMO AI • {date_str} • Claude Sonnet</div>
</body></html>"""
    buf = BytesIO()
    buf.write(html.encode("utf-8"))
    buf.seek(0)
    return buf


def generate_excel(skill_id: str, content: str, business_name: str = "") -> BytesIO:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = (business_name or skill_id)[:28]
    date_str = datetime.now().strftime("%d/%m/%Y")

    def hstyle(cell, level=1):
        colors = {1: "1a1a2e", 2: "16213e", 3: "0f3460"}
        cell.font = Font(bold=True, size=14-level, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=colors.get(level, "1a1a2e"))
        cell.alignment = Alignment(wrap_text=True, vertical="center")

    def tstyle(cell):
        cell.font = Font(bold=True, size=10, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="e94560")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    def nstyle(cell, even=False):
        cell.font = Font(size=10)
        if even: cell.fill = PatternFill("solid", fgColor="F8F9FA")
        cell.alignment = Alignment(wrap_text=True, vertical="top")

    # Title
    ws.merge_cells("A1:F1")
    tc = ws["A1"]
    tc.value = f"CMO AI — {business_name or skill_id} — {date_str}"
    tc.font = Font(bold=True, size=15, color="FFFFFF")
    tc.fill = PatternFill("solid", fgColor="1a1a2e")
    tc.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 38
    row = 3
    in_table, trow = False, 0

    for line in content.split('\n'):
        if line.startswith("# ") and not line.startswith("## "):
            ws.merge_cells(f"A{row}:F{row}")
            hstyle(ws.cell(row=row, column=1, value=line[2:].strip()), 1)
            ws.row_dimensions[row].height = 26; row += 1
        elif line.startswith("## ") and not line.startswith("### "):
            ws.merge_cells(f"A{row}:F{row}")
            hstyle(ws.cell(row=row, column=1, value=line[3:].strip()), 2)
            ws.row_dimensions[row].height = 22; row += 1
        elif line.startswith("### "):
            ws.merge_cells(f"A{row}:F{row}")
            hstyle(ws.cell(row=row, column=1, value=line[4:].strip()), 3)
            ws.row_dimensions[row].height = 20; row += 1
        elif "|" in line and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|") if c.strip()]
            if not cells: continue
            if all(set(c) <= set("-: ") for c in cells): continue
            if not in_table:
                in_table, trow = True, 0
                for col, h in enumerate(cells, 1):
                    tstyle(ws.cell(row=row, column=col, value=h))
                ws.row_dimensions[row].height = 20; row += 1
            else:
                trow += 1
                for col, v in enumerate(cells, 1):
                    v = re.sub(r'\*\*(.+?)\*\*', r'\1', v)
                    nstyle(ws.cell(row=row, column=col, value=v), trow % 2 == 0)
                ws.row_dimensions[row].height = 18; row += 1
        elif line.strip() in ("---", "***"):
            in_table = False; row += 1
        elif line.strip():
            in_table = False
            clean = re.sub(r'\*\*(.+?)\*\*', r'\1', re.sub(r'\*(.+?)\*', r'\1', line))
            if clean.startswith(("- ", "* ")): clean = "• " + clean[2:]
            ws.merge_cells(f"A{row}:F{row}")
            nstyle(ws.cell(row=row, column=1, value=clean))
            ws.row_dimensions[row].height = 16; row += 1
        else:
            row += 1

    for i, w in enumerate([60, 25, 25, 25, 25, 25], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A3"

    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


# ── Telegram handlers ──────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    reset_session(user_id)
    await update.message.reply_text(
        "Xin chao! Toi la CMO AI — tro ly marketing chuyen nghiep.\n\n"
        "He thong gom 3 tang:\n"
        "1. Phan loai yeu cau (Haiku)\n"
        "2. Master Agent hoi & xu ly (Sonnet)\n"
        "3. Critic review chat luong (Sonnet)\n\n"
        "Output: Bullet points + file HTML hoac Excel\n\n"
        "Thu nhan:\n"
        "• Lap ke hoach marketing cho spa\n"
        "• Viet script TikTok ban ao dai\n"
        "• Viet copy Facebook Ads cho clinic\n"
        "• Audit hieu suat quang cao\n\n"
        "/reset - bat dau lai"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    reset_session(user_id)
    await update.message.reply_text("Session da reset.")


async def handle_format_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User bam HTML hoac Excel button."""
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    fmt = query.data

    full_content = await asyncio.to_thread(load_pending_output, user_id)
    if not full_content:
        await query.message.reply_text("Het session. Vui long nhan lai yeu cau.")
        return

    session = await asyncio.to_thread(load_session, user_id)
    business_name = session["session_context"].get("business_name") or ""
    skill_id = session.get("skill_id") or "report"
    date_str = datetime.now().strftime("%Y%m%d")

    await query.message.reply_text(f"Dang tao file {fmt.upper()}...")

    try:
        if fmt == "html":
            buf = generate_html(skill_id, full_content, business_name)
            fname = f"cmo-ai-{skill_id}-{date_str}.html"
        else:
            buf = generate_excel(skill_id, full_content, business_name)
            fname = f"cmo-ai-{skill_id}-{date_str}.xlsx"

        await query.message.reply_document(document=buf, filename=fname,
            caption=f"Ban day du — {skill_id} | {date_str}")
        logger.info(f"[{user_id}] Sent {fmt}: {fname}")

        await asyncio.to_thread(clear_pending_output, user_id)

    except Exception as e:
        logger.error(f"[{user_id}] File gen error: {e}", exc_info=True)
        await query.message.reply_text(f"Loi tao file: {str(e)[:100]}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    user_message = update.message.text

    session = await asyncio.to_thread(load_session, user_id)
    if user_id not in chat_history:
        chat_history[user_id] = {}

    await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")

    # ── Rate limit: 50 messages/ngay ──────────────────────────────────────────
    today = datetime.now().strftime("%Y-%m-%d")
    ctx = session["session_context"]
    if ctx.get("last_reset_date") != today:
        ctx["daily_count"] = 0
        ctx["last_reset_date"] = today
    ctx["daily_count"] = ctx.get("daily_count", 0) + 1
    if ctx["daily_count"] > 50:
        await update.message.reply_text("Bạn đã dùng hết 50 tin nhắn hôm nay. Quay lại vào ngày mai.")
        return

    # ── Layer 1: Haiku Classify ────────────────────────────────────────────────
    old_skill = session.get("skill_id")
    classify = haiku_classify(user_message, old_skill)
    skill_id   = classify.get("skill_id", "00-ke-hoach-mkt")
    agent_name = classify.get("agent", "mkt-strategist")
    mode       = classify.get("mode", "quick")

    if old_skill and old_skill != skill_id:
        logger.info(f"[{user_id}] Skill switched: {old_skill} -> {skill_id}")

    session["skill_id"] = skill_id
    ctx["mode"] = mode
    session["message_count"] = session.get("message_count", 0) + 1

    logger.info(f"[{user_id}] Classify: skill={skill_id} agent={agent_name} mode={mode}")

    if skill_id not in chat_history[user_id]:
        chat_history[user_id][skill_id] = []
    chat_history[user_id][skill_id].append({"role": "user", "content": user_message})

    try:
        # ── Layer 2: Master Agent ──────────────────────────────────────────────
        industry = ctx.get("industry") or "general"
        sections = fetch_sections(skill_id, mode, industry)
        logger.info(f"[{user_id}] Fetched {len(sections)} sections")

        chain_context = build_chain_context(skill_id, ctx)
        if chain_context:
            logger.info(f"[{user_id}] Chain context injected for {skill_id}")

        master_res = master_agent_respond(
            agent_name=agent_name,
            skill_id=skill_id,
            session_context=ctx,
            history=chat_history[user_id].get(skill_id, []),
            sections=sections,
            chain_context=chain_context
        )
        full_content = master_res.content[0].text
        log_usage(user_id, "claude-sonnet-4-5", skill_id, master_res)

        chat_history[user_id][skill_id].append({"role": "assistant", "content": full_content})
        logger.info(f"[{user_id}] Master Agent: {len(full_content)} chars")

        final_output = is_final_output(full_content)
        reviewed_content = None

        if final_output:
            logger.info(f"[{user_id}] Final output -> Critic -> Summarize")

            # ── Layer 3: Critic Review ─────────────────────────────────────────
            await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
            reviewed_content = critic_review(
                full_content, skill_id,
                user_id=user_id,
                industry=ctx.get("industry")
            )

            save_pending_output(user_id, reviewed_content, skill_id)

            if "skill_outputs" not in ctx:
                ctx["skill_outputs"] = {}
            ctx["skill_outputs"][skill_id] = reviewed_content[:2000]
            logger.info(f"[{user_id}] Saved output for skill chain: {skill_id}")

            # Haiku Summarize → bullets
            await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
            bullets = summarize_to_bullets(reviewed_content, skill_id)

            if len(bullets) > 4000:
                for chunk in [bullets[i:i+4000] for i in range(0, len(bullets), 4000)]:
                    await update.message.reply_text(chunk)
            else:
                await update.message.reply_text(bullets)

            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("📄 HTML (in duoc, dep)", callback_data="html"),
                InlineKeyboardButton("📊 Excel (chinh sua duoc)", callback_data="excel"),
            ]])
            await update.message.reply_text("Chon dinh dang ban day du:", reply_markup=keyboard)

        else:
            logger.info(f"[{user_id}] Intake question -> send normally")
            if len(full_content) > 4000:
                for chunk in [full_content[i:i+4000] for i in range(0, len(full_content), 4000)]:
                    await update.message.reply_text(chunk)
            else:
                await update.message.reply_text(full_content)

        # ── Extract context (chi khi con null fields va message du dai) ────────
        INTERNAL_FIELDS = {"output_format", "_pending_response", "skill_outputs",
                           "daily_count", "last_reset_date"}
        null_fields = [k for k, v in ctx.items() if v is None and k not in INTERNAL_FIELDS]
        if len(user_message) > 20 and null_fields:
            session["session_context"] = extract_context_update(
                user_message, full_content[:400], ctx
            )

        await asyncio.to_thread(save_session, user_id, session)

    except Exception as e:
        logger.error(f"[{user_id}] Error: {e}", exc_info=True)
        await update.message.reply_text(f"Co loi: {str(e)[:100]}\n\nThu lai hoac /reset.")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if not TELEGRAM_TOKEN:
        print("Thieu TELEGRAM_BOT_TOKEN")
        return

    print("CMO AI Bot v3 — 3-layer architecture")
    print("  Haiku Classify -> Master Agent (Sonnet) -> Critic (Sonnet)")
    print("  /start /reset")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CallbackQueryHandler(handle_format_choice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        app.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        print("Bot stopped.")


if __name__ == "__main__":
    main()
