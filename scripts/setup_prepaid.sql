-- CMO AI Bot — Prepaid Token System
-- Chạy trong Supabase Dashboard > SQL Editor

-- Bảng users: lưu token balance của từng user
CREATE TABLE IF NOT EXISTS users (
    user_id        TEXT PRIMARY KEY,
    token_balance  BIGINT DEFAULT 0,
    created_at     TIMESTAMPTZ DEFAULT now(),
    updated_at     TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_users_token_balance ON users(token_balance);

-- Function deduct_tokens: trừ token atomic (tránh race condition)
CREATE OR REPLACE FUNCTION deduct_tokens(p_user_id TEXT, p_tokens BIGINT)
RETURNS void AS $$
BEGIN
    INSERT INTO users (user_id, token_balance, updated_at)
    VALUES (p_user_id, -p_tokens, now())
    ON CONFLICT (user_id) DO UPDATE
        SET token_balance = users.token_balance - p_tokens,
            updated_at    = now();
END;
$$ LANGUAGE plpgsql;

-- Function add_tokens: admin nạp token cho user
CREATE OR REPLACE FUNCTION add_tokens(p_user_id TEXT, p_tokens BIGINT)
RETURNS void AS $$
BEGIN
    INSERT INTO users (user_id, token_balance, updated_at)
    VALUES (p_user_id, p_tokens, now())
    ON CONFLICT (user_id) DO UPDATE
        SET token_balance = users.token_balance + p_tokens,
            updated_at    = now();
END;
$$ LANGUAGE plpgsql;

-- Nạp token cho user (chạy thủ công khi user thanh toán):
-- SELECT add_tokens('<telegram_user_id>', 500000);

-- Xem balance tất cả users:
-- SELECT user_id, token_balance, updated_at FROM users ORDER BY updated_at DESC;

-- Xem chi tiết usage của 1 user:
-- SELECT model, skill_id, input_tokens, output_tokens,
--        (input_tokens + output_tokens) as total, created_at
-- FROM usage_logs
-- WHERE user_id = '<telegram_user_id>'
-- ORDER BY created_at DESC LIMIT 50;
