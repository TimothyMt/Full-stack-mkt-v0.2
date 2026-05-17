-- Sprint 1 migration: thêm cột outcome vào skill_feedback
-- Chạy trong Supabase Dashboard > SQL Editor

ALTER TABLE skill_feedback
    ADD COLUMN IF NOT EXISTS outcome TEXT DEFAULT 'NEEDS_FIX';

CREATE INDEX IF NOT EXISTS idx_skill_feedback_outcome
    ON skill_feedback(outcome);

-- Query tháng để xem skill nào cần cải thiện:
-- SELECT skill_id, industry,
--        COUNT(*) FILTER (WHERE outcome = 'APPROVED')  AS approved,
--        COUNT(*) FILTER (WHERE outcome = 'EXPORTED')  AS exported,
--        COUNT(*) FILTER (WHERE outcome = 'NEEDS_FIX') AS needs_fix,
--        ROUND(
--            COUNT(*) FILTER (WHERE outcome = 'EXPORTED')::numeric /
--            NULLIF(COUNT(*) FILTER (WHERE outcome = 'APPROVED'), 0) * 100, 1
--        ) AS export_rate_pct
-- FROM skill_feedback
-- WHERE created_at >= now() - interval '30 days'
-- GROUP BY skill_id, industry
-- ORDER BY export_rate_pct ASC;
