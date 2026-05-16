-- CMO AI Bot — Tạo các bảng mới
-- Chạy trong Supabase Dashboard > SQL Editor

-- Bảng 1: pending_outputs (thay thế _pending_response trong session_context)
-- Không truncate, lưu full output để export HTML/Excel đầy đủ
CREATE TABLE IF NOT EXISTS pending_outputs (
    user_id     TEXT PRIMARY KEY,
    content     TEXT NOT NULL,
    skill_id    TEXT,
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- Tự động xoá record cũ hơn 24h (tránh rác tích tụ)
CREATE INDEX IF NOT EXISTS idx_pending_outputs_created
    ON pending_outputs(created_at);

-- Bảng 2: usage_logs (theo dõi token per user để tính phí)
CREATE TABLE IF NOT EXISTS usage_logs (
    id             BIGSERIAL PRIMARY KEY,
    user_id        TEXT NOT NULL,
    model          TEXT NOT NULL,
    skill_id       TEXT,
    input_tokens   INT DEFAULT 0,
    output_tokens  INT DEFAULT 0,
    created_at     TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_usage_logs_user_id
    ON usage_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_usage_logs_created
    ON usage_logs(created_at);

-- Query tính phí theo user (chạy cuối tháng):
-- SELECT user_id,
--        SUM(input_tokens + output_tokens) as total_tokens,
--        ROUND(SUM(input_tokens * 0.000003 + output_tokens * 0.000015), 4) as usd_cost
-- FROM usage_logs
-- WHERE created_at >= date_trunc('month', now())
-- GROUP BY user_id
-- ORDER BY usd_cost DESC;
