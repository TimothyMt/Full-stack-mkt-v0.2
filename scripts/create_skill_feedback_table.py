"""
Tao bang skill_feedback trong Supabase.
Chay 1 lan: python scripts/create_skill_feedback_table.py
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

# Test insert de kiem tra table da ton tai chua
try:
    res = supabase.table("skill_feedback").select("id").limit(1).execute()
    print("Table skill_feedback da ton tai. OK.")
except Exception as e:
    print(f"Table chua ton tai hoac loi: {e}")
    print("\nVui long chay SQL nay trong Supabase Dashboard > SQL Editor:\n")
    print("""
CREATE TABLE skill_feedback (
    id          bigserial PRIMARY KEY,
    skill_id    text NOT NULL,
    issue       text,
    industry    text,
    user_id     text,
    created_at  timestamptz DEFAULT now()
);

CREATE INDEX idx_skill_feedback_skill_id ON skill_feedback(skill_id);
CREATE INDEX idx_skill_feedback_created_at ON skill_feedback(created_at);
""")
