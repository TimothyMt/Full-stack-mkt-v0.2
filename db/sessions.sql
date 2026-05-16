-- ============================================================
-- CMO AI — Sessions Table
-- Paste vào Supabase SQL Editor và chạy
-- Lưu session context per user_id cho Telegram bot / n8n workflow
-- ============================================================

CREATE TABLE IF NOT EXISTS sessions (
  user_id       TEXT         PRIMARY KEY,          -- Telegram user ID (string)
  session_context JSONB      DEFAULT '{}',         -- {skill_id, mode, industry, business_name, ...}
  message_count INTEGER      DEFAULT 0,            -- số tin nhắn trong session
  last_skill    TEXT,                              -- skill dùng lần cuối
  updated_at    TIMESTAMPTZ  DEFAULT NOW(),
  created_at    TIMESTAMPTZ  DEFAULT NOW()
);

-- Index để query nhanh
CREATE INDEX IF NOT EXISTS idx_sessions_updated_at ON sessions(updated_at);

-- Trigger tự update updated_at
CREATE TRIGGER trg_sessions_updated_at
  BEFORE UPDATE ON sessions
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- RLS: chỉ service_role có quyền (bot dùng service_role key)
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role full access" ON sessions
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);
