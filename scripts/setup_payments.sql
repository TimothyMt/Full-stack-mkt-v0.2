-- CMO AI Bot — Payment Orders Table
-- Chạy trong Supabase Dashboard > SQL Editor

CREATE TABLE IF NOT EXISTS payment_orders (
    order_id    TEXT PRIMARY KEY,
    user_id     TEXT NOT NULL,
    amount      INT  NOT NULL,          -- số tiền VND
    tokens      INT  NOT NULL,          -- số token sẽ cộng khi thanh toán xong
    provider    TEXT NOT NULL,          -- 'momo' | 'zalopay'
    status      TEXT DEFAULT 'pending', -- 'pending' | 'completed' | 'failed'
    created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_payment_orders_user_id ON payment_orders(user_id);
CREATE INDEX IF NOT EXISTS idx_payment_orders_status  ON payment_orders(status);

-- Tự xoá đơn pending quá 1 giờ (chạy thủ công hoặc scheduled):
-- DELETE FROM payment_orders
-- WHERE status = 'pending' AND created_at < now() - interval '1 hour';
