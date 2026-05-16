"""
Fix skills 30 và 31:
- Thêm output_template section (HTML đầy đủ + Telegram bullet)
- Fix priority: stage1=1, stage2=2, stage3=3
- Mở rộng context_intake
- Xóa ref Skill 18 trong checklist
- Chuẩn hóa encoding skill 31
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()
sb = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_KEY'))

updates = []

# ══════════════════════════════════════════════════════════════
# SKILL 30 — RETENTION STRATEGY
# ══════════════════════════════════════════════════════════════

updates.append({
    'skill_id': '30-retention-strategy',
    'section_id': 'context_intake',
    'section_type': 'context_intake',
    'priority': 1,
    'modes': ['all'],
    'industries': ['all'],
    'tags': ['session_context', 'retention', 'onboarding'],
    'content': """> Với spa/clinic: 60–70% doanh thu đến từ khách quay lại. Retention không phải "chăm sóc" — đây là hệ thống doanh thu có thể dự báo được.

Khi chạy skill này, Master Agent cần:
- Kiểm tra `session_context.industry` + `session_context.business_stage` trước
- Nếu đã có → bỏ qua phần data_collection, chạy thẳng framework theo giai đoạn
- Nếu chưa có → hỏi 2 câu ở data_collection trước
- Output theo template `output_template` ở cuối file
- Telegram: chỉ bullet points tóm tắt → hỏi HTML/Excel"""
})

updates.append({
    'skill_id': '30-retention-strategy',
    'section_id': 'retention_stage1',
    'section_type': 'template',
    'priority': 1,
    'modes': ['all'],
    'industries': ['all'],
    'tags': ['retention', 'stage1', 'new_business', 'framework'],
    'content': """## Framework Retention theo Giai Đoạn Kinh Doanh

### Giai đoạn 1 — Mới mở (0–6 tháng)

**Ưu tiên:** Tạo thói quen quay lại ngay từ lần đầu. Chưa cần hệ thống phức tạp.

| Hành động | Cách làm | Kênh |
|-----------|---------|------|
| Follow-up 24–48h sau lần đầu | Hỏi thăm kết quả, cảm nhận | Zalo cá nhân, Messenger |
| Offer lần 2 ngay tại điểm bán | "Đặt lịch hôm nay được giảm X%" | Offline + Zalo |
| Thu SDT / Zalo 100% khách | Bắt buộc — đây là tài sản số | Form điện tử, sổ tay |
| Gửi tips/giá trị sau dịch vụ | Skincare routine sau trị liệu, bài tập về nhà | Zalo OA, Messenger |

**Mục tiêu giai đoạn:** 30% khách quay lại trong 60 ngày."""
})

updates.append({
    'skill_id': '30-retention-strategy',
    'section_id': 'retention_stage2_segmentation',
    'section_type': 'template',
    'priority': 2,
    'modes': ['all'],
    'industries': ['all'],
    'tags': ['retention', 'stage2', 'segmentation', 'funnel'],
    'content': """### Giai đoạn 2 — Tăng trưởng (6–24 tháng)

**Ưu tiên:** Phân tầng khách, tạo chu kỳ liên hệ, bắt đầu loyalty đơn giản.

#### Phân tầng 4 nhóm khách

| Nhóm | Định nghĩa | % Khách TB | Content phù hợp | Kênh | Ưu đãi | Hành động ưu tiên |
|------|-----------|-----------|----------------|------|--------|-------------------|
| **Mới** | Mua lần đầu, chưa quay lại | 40–50% | TOFU: giáo dục, social proof, kết quả thực tế | TikTok, Facebook, Zalo cá nhân | Trial, lần 2 giảm nhẹ | Onboarding tốt, follow-up nhanh trong 48h |
| **Đang active** | Mua 2+ lần trong 90 ngày | 20–30% | MOFU: giá trị thêm, dịch vụ mới, kết quả | Zalo OA, Email, Messenger | Loyalty tier, upsell nhẹ | Nurture, chăm sóc đều đặn, không để churn |
| **Có nguy cơ** | Quá 60 ngày không quay lại | 15–20% | Nhắc nhở, ưu đãi có thời hạn, case study | Zalo OA, Email, SMS | Ưu đãi nhẹ kèm hạn dùng | Nhắn tin cá nhân — hỏi lý do, gửi offer |
| **Đã bỏ** | Quá 90 ngày không tương tác | 10–20% | Win-back: hỏi lý do, offer đặc biệt | Email, Zalo, SMS | Comeback offer mạnh hơn | Chuyển sang Skill 31 — win-back campaign |

#### Chu kỳ liên hệ gợi ý theo ngành

| Ngành | Chu kỳ tự nhiên | Liên hệ lần 1 | Liên hệ lần 2 | Liên hệ lần 3 |
|-------|---------------|--------------|--------------|--------------|
| Spa (skincare) | 4–6 tuần | Ngày 3 sau dịch vụ | Ngày 25 (nhắc lịch) | Ngày 35 (ưu đãi) |
| Clinic thẩm mỹ | 3–6 tháng | Ngày 7 (kiểm tra kết quả) | Tháng 2 (nhắc tái khám) | Tháng 5 (offer liệu trình mới) |
| Gym / Yoga | Hàng tuần | Ngày 3 (hỏi thăm) | Tuần 3 (check-in) | Hết tháng (gia hạn) |
| F&B | 1–2 tuần | Ngày sau ăn (cảm ơn) | Tuần 2 (offer) | Tháng 1 (loyalty) |
| Giáo dục | Theo khóa | Tuần 1 (onboarding) | Giữa khóa (engagement) | Cuối khóa (upsell khóa tiếp) |
| Ecommerce | 30–45 ngày | Ngày 3 (unboxing check) | Ngày 20 (review) | Ngày 40 (offer lần 2) |"""
})

updates.append({
    'skill_id': '30-retention-strategy',
    'section_id': 'retention_stage3_loyalty',
    'section_type': 'template',
    'priority': 3,
    'modes': ['full'],
    'industries': ['all'],
    'tags': ['retention', 'stage3', 'loyalty', 'ltv', 'advocate'],
    'content': """### Giai đoạn 3 — Ổn định (2 năm+)

**Ưu tiên:** Hệ thống loyalty bài bản, tối ưu LTV, biến khách thành advocate.

#### Mô hình Loyalty Tier gợi ý

| Tier | Điều kiện | Quyền lợi | Mục tiêu |
|------|-----------|-----------|---------|
| **Member** | Đã mua 1 lần | Tích điểm cơ bản, sinh nhật | Khuyến khích lần 2 |
| **Silver** | 3–5 lần / 6 tháng | Ưu đãi 5–10%, ưu tiên đặt lịch | Tạo thói quen |
| **Gold** | 6–10 lần / 6 tháng | Ưu đãi 10–15%, quà tặng, preview dịch vụ mới | Giữ khách trung thành |
| **VIP** | Top 10% khách | Ưu đãi 15–20%, dịch vụ exclusive, sự kiện riêng | Biến thành advocate |

#### Upsell / Cross-sell đúng thời điểm

| Thời điểm | Gợi ý | Cách nói |
|-----------|-------|---------|
| Đang dùng dịch vụ | Cross-sell dịch vụ bổ sung | "Chị đang làm da, kết hợp massage mặt sẽ giữ kết quả lâu hơn" |
| Vừa xong dịch vụ | Upsell gói dài hạn | "Nếu làm theo liệu trình 4 buổi tiết kiệm được 20%" |
| Nhắc lịch tái khám | Cross-sell sản phẩm chăm sóc tại nhà | "Để duy trì kết quả, chị có thể dùng thêm sản phẩm này" |
| Sinh nhật | Offer đặc biệt | "Quà sinh nhật của chị: ưu đãi 20% buổi tiếp theo" |

#### Khách VIP — Biến thành Advocate

| Hành động | Cách làm |
|-----------|---------|
| Ghi nhận công khai | Tag/mention khi họ cho phép, highlight story của họ |
| Mời trải nghiệm trước | Preview dịch vụ mới trước khi ra mắt |
| Chương trình referral | "Giới thiệu bạn được X% — bạn được Y%" |
| Sự kiện VIP | Buổi trị liệu miễn phí, event riêng cho nhóm VIP |
| Feedback loop | Hỏi ý kiến về dịch vụ mới — họ cảm thấy được trân trọng |"""
})

updates.append({
    'skill_id': '30-retention-strategy',
    'section_id': 'quality_checklist',
    'section_type': 'quality_checklist',
    'priority': 1,
    'modes': ['all'],
    'industries': ['all'],
    'tags': ['quality', 'checklist', 'validation'],
    'content': """## Checklist Chất Lượng

- [ ] Đã xác định ngành và giai đoạn kinh doanh
- [ ] Phân tầng đủ 4 nhóm khách (Mới / Active / Có nguy cơ / Đã bỏ) với hành động cụ thể cho từng nhóm
- [ ] Chu kỳ liên hệ phù hợp với chu kỳ tự nhiên của ngành
- [ ] Kênh retention phù hợp với đối tượng khách (không áp Zalo OA cho SaaS)
- [ ] Có ít nhất 1 trigger cụ thể cho từng nhóm khách
- [ ] Offer retention không phá vỡ margin (không giảm giá liên tục)
- [ ] KPI đã xác định và biết cách đo
- [ ] Nhóm "Đã bỏ" → chuyển sang Skill 31 Winback
- [ ] Nhóm VIP → có kế hoạch referral / advocate cụ thể
- [ ] Output đúng template: đủ 7 phần (tổng quan → phân tầng → hành động → kênh → lịch 30 ngày → KPI → quick wins)"""
})

updates.append({
    'skill_id': '30-retention-strategy',
    'section_id': 'output_template',
    'section_type': 'output_template',
    'priority': 1,
    'modes': ['all'],
    'industries': ['all'],
    'tags': ['output', 'template', 'html', 'telegram'],
    'content': """## Cấu trúc Output

### Telegram — Bullet points tóm tắt

```
🔄 Retention Strategy — [Tên doanh nghiệp]
Ngành: [X] | Giai đoạn: [X]

📊 Tình trạng:
• Repeat Rate hiện tại: ~X% (benchmark: >35%)
• Nhóm nguy cơ ước tính: X% khách hàng

👥 4 nhóm khách & hành động:
• Mới (X%): follow-up 48h + offer lần 2
• Active (X%): upsell + loyalty
• Nguy cơ (X%): nhắc + offer có hạn
• Đã bỏ (X%): → chuyển Skill 31 Winback

⚡ Quick wins tuần 1:
• [Hành động 1]
• [Hành động 2]
• [Hành động 3]

🎯 KPI mục tiêu 90 ngày:
• Repeat Rate: X% → X%
• Churn Rate: X% → X%

📎 Chọn định dạng bản đầy đủ:
```

---

### HTML / Excel — Output đầy đủ (7 phần bắt buộc)

# Chiến lược Retention — [Tên doanh nghiệp]
**Ngành:** [X] | **Giai đoạn:** [Mới mở / Tăng trưởng / Ổn định] | **Ngày tạo:** [YYYY-MM-DD]

---

## 1. Tổng quan & KPI hiện tại

| KPI | Ước tính hiện tại | Mục tiêu 90 ngày | Benchmark VN 2025 |
|-----|------------------|-----------------|-------------------|
| Repeat Purchase Rate | ?% | ?% | Beauty: >35% |
| Churn Rate (90 ngày) | ?% | ?% | Beauty: <30% |
| LTV (12 tháng) | ?x AOV | ?x AOV | Beauty: 3–5x AOV |
| Time to 2nd Purchase | ? ngày | ? ngày | Beauty: <45 ngày |
| Zalo OA Read Rate | ?% | >60% | TB: 40–60% |

---

## 2. Phân tầng 4 nhóm khách

| Nhóm | Định nghĩa | % Ước tính | Trigger | Hành động ưu tiên | Kênh | Offer |
|------|-----------|-----------|---------|-------------------|------|-------|
| **Mới** | Mua lần đầu, <60 ngày chưa quay lại | X% | 48h sau lần 1 | Follow-up hỏi thăm + offer lần 2 | Zalo cá nhân | [Offer cụ thể] |
| **Active** | Mua 2+ lần / 90 ngày | X% | Theo chu kỳ | Upsell / loyalty | Zalo OA | [Gói giá trị] |
| **Có nguy cơ** | 60–90 ngày chưa quay lại | X% | Ngày 60 | Nhắc + offer có hạn | Zalo OA + SMS | [Ưu đãi X%] |
| **Đã bỏ** | 90+ ngày không tương tác | X% | — | → Skill 31 Winback | — | — |

---

## 3. Kế hoạch hành động từng nhóm

### 🟢 Nhóm Mới — [X] khách ước tính

| Trigger | Hành động | Kênh | Timeline | Script mẫu |
|---------|-----------|------|----------|-----------|
| 24–48h sau lần đầu | Hỏi thăm kết quả | Zalo cá nhân | Ngay sau dịch vụ | "[Tên] ơi, hôm qua [dịch vụ] thế nào rồi ạ?" |
| Ngày 7 chưa đặt lại | Offer lần 2 | Zalo OA | T+7 | "[Tên] ơi, tuần này có slot trống cho chị..." |
| Ngày 30 chưa quay | Offer có thời hạn | Zalo OA | T+30 | "Chỉ còn đến [ngày], chị đặt lịch hôm nay được ưu đãi..." |

### 🔵 Nhóm Active — [X] khách ước tính

| Trigger | Hành động | Kênh | Timeline | Mục tiêu |
|---------|-----------|------|----------|---------|
| Sau mỗi lần dùng dịch vụ | Cross-sell / upsell | Trực tiếp + Zalo | Ngay tại điểm bán | Tăng AOV |
| Đạt mốc tier mới | Thông báo quyền lợi | Zalo cá nhân | Tự động | Tăng loyalty |
| Theo chu kỳ tự nhiên | Nhắc lịch | Zalo OA | Theo ngành | Giảm churn |

### 🟡 Nhóm Có nguy cơ — [X] khách ước tính

| Trigger | Hành động | Kênh | Offer | Script mẫu |
|---------|-----------|------|-------|-----------|
| Ngày 60 không quay | Nhắn tin cá nhân hỏi thăm | Zalo cá nhân | Không có offer | "Chị ơi, lâu rồi chưa gặp..." |
| Không phản hồi sau 3 ngày | Offer có thời hạn | Zalo OA | [Ưu đãi nhẹ] | "Tuần này có slot, chị muốn em giữ không?" |
| Không phản hồi tiếp | → Chuyển nhóm Đã bỏ | — | — | → Skill 31 |

---

## 4. Kênh & Tần suất

| Kênh | Nhóm phục vụ | Tần suất | Loại nội dung | Chi phí ước tính/tháng |
|------|-------------|---------|--------------|----------------------|
| Zalo cá nhân | Mới + Nguy cơ + VIP | Theo trigger | Follow-up, hỏi thăm | Miễn phí |
| Zalo OA | Active + Nguy cơ | 2–3 lần/tuần | Tips, nhắc lịch, ưu đãi | ~200K–500K |
| Email | Ecommerce / SaaS / Giáo dục | 1–2 lần/tuần | Newsletter, lifecycle | Miễn phí (Brevo) |
| Facebook Group | Gym / Giáo dục | 3–5 lần/tuần | Community, tips, Q&A | Miễn phí |

---

## 5. Lịch triển khai 30 ngày đầu

| Tuần | Hành động | Nhóm | Kênh | Người thực hiện | Kết quả kỳ vọng |
|------|-----------|------|------|----------------|----------------|
| Tuần 1 | Setup Zalo OA + chuẩn hóa danh sách | Tất cả | Offline | [Tên] | Có danh sách đầy đủ |
| Tuần 1 | Nhắn tin hỏi thăm nhóm Nguy cơ | Nguy cơ | Zalo cá nhân | [Tên] | X% phản hồi |
| Tuần 2 | Broadcast tips lần đầu | Active | Zalo OA | [Tên] | Read rate >50% |
| Tuần 3 | Follow-up nhóm Mới tuần 1 | Mới | Zalo cá nhân | [Tên] | X% đặt lịch lần 2 |
| Tuần 4 | Review số liệu + điều chỉnh | — | — | [Tên] | Dashboard KPI |

---

## 6. KPI Mục tiêu

| KPI | Hiện tại | Mục tiêu 30 ngày | Mục tiêu 90 ngày | Cách đo |
|-----|---------|-----------------|-----------------|--------|
| Repeat Purchase Rate | ?% | +5% | +15% | CRM / POS / sổ tay |
| Churn Rate | ?% | -3% | -10% | Khách không quay / tổng |
| Zalo OA Read Rate | ?% | >50% | >65% | Zalo OA dashboard |
| LTV 12 tháng | ?x AOV | +0.5x | +1x | Doanh thu / số khách active |
| Time to 2nd Purchase | ? ngày | -10 ngày | -20 ngày | Ngày TB giữa lần 1 và 2 |

---

## 7. Quick Wins — Làm ngay trong tuần 1

1. **[Hành động 1]** — không cần budget, impact ngay trong 48h
2. **[Hành động 2]** — cost thấp, setup 1 lần, chạy tự động
3. **[Hành động 3]** — tác động trực tiếp đến nhóm Nguy cơ lớn nhất"""
})

# ══════════════════════════════════════════════════════════════
# SKILL 31 — WINBACK CAMPAIGN
# ══════════════════════════════════════════════════════════════

updates.append({
    'skill_id': '31-winback-campaign',
    'section_id': 'context_intake',
    'section_type': 'context_intake',
    'priority': 1,
    'modes': ['all'],
    'industries': ['all'],
    'tags': ['session_context', 'winback', 'onboarding'],
    'content': """> Win-back rẻ hơn acquisition 5–7 lần. Nhưng làm sai (spam, offer sai, timing sai) thì mất luôn — danh sách khách cũ là tài sản không thể phục hồi nếu bị đốt.

Khi chạy skill này, Master Agent cần:
- Kiểm tra `session_context.industry` trước — nếu đã có, chỉ hỏi câu 2 trong data_collection
- Xác định nhóm khách cần win-back trước khi đề xuất offer
- Bắt buộc đề xuất quy trình test 10% trước khi chạy toàn bộ
- Output theo template `output_template` ở cuối file
- Telegram: chỉ bullet points tóm tắt → hỏi HTML/Excel"""
})

updates.append({
    'skill_id': '31-winback-campaign',
    'section_id': 'data_collection',
    'section_type': 'data_collection',
    'priority': 1,
    'modes': ['all'],
    'industries': ['all'],
    'tags': ['intake', 'adaptive', 'winback'],
    'content': """## Thu thập thông tin

Nếu `session_context.industry` đã có → chỉ hỏi câu 2.
Nếu chưa có → hỏi đủ 2 câu.

1. **Ngành và loại dịch vụ?** (Spa / Clinic / F&B / Gym / Ecommerce / Giáo dục / Khác)
2. **Đối tượng cần win-back là ai?**
   - Khách mua 1 lần, chưa quay lại (>60 ngày)
   - Khách đã mua nhiều lần, đột ngột dừng (>90 ngày)
   - Khách VIP cũ, mất liên lạc lâu (>6 tháng)"""
})

updates.append({
    'skill_id': '31-winback-campaign',
    'section_id': 'output_template',
    'section_type': 'output_template',
    'priority': 1,
    'modes': ['all'],
    'industries': ['all'],
    'tags': ['output', 'template', 'html', 'telegram'],
    'content': """## Cấu trúc Output

### Telegram — Bullet points tóm tắt

```
🔁 Winback Campaign — [Tên doanh nghiệp]
Ngành: [X] | Nhóm mục tiêu: [X] | Trigger: [X] ngày không mua

🔍 Lý do bỏ chính: [Quên mất / Chưa hài lòng / Bị đối thủ kéo]

📋 Sequence 3 bước:
• Ngày 1: Kết nối lại — không offer
• Ngày 5–7: Offer nhẹ + deadline
• Ngày 12–14: Best offer cuối

💰 Offer đề xuất:
• Tier 1: [Offer nhẹ]
• Tier 2: [Offer mạnh — dùng lần 3]

⚠️ Test 10% danh sách trước khi scale
🎯 Win-back rate kỳ vọng: >20%

📎 Chọn định dạng bản đầy đủ:
```

---

### HTML / Excel — Output đầy đủ (6 phần bắt buộc)

# Winback Campaign — [Tên doanh nghiệp]
**Ngành:** [X] | **Nhóm mục tiêu:** [X]
**Trigger:** [X] ngày không mua | **Số lượng ước tính:** [X] khách | **Ngày chạy:** [YYYY-MM-DD]

---

## 1. Phân loại lý do bỏ

| Nhóm | Dấu hiệu nhận biết | Lý do có thể | % Ước tính | Cách tiếp cận |
|------|--------------------|-------------|-----------|--------------|
| **Quên mất** | Không tương tác, không phàn nàn | Busy, không ai nhắc | X% | Nhắc nhở nhẹ nhàng, không offer ngay |
| **Chưa hài lòng** | Có phàn nàn cũ hoặc không để lại review | Trải nghiệm chưa tốt | X% | Xin lỗi + cải thiện + offer đền bù |
| **Bị đối thủ kéo** | Tương tác với đối thủ trên MXH | Deal tốt hơn | X% | Offer cạnh tranh + nhấn mạnh điểm khác biệt |
| **Nhu cầu thay đổi** | Ngừng hẳn không có lý do rõ | Hoàn cảnh thay đổi | X% | Giới thiệu dịch vụ mới phù hợp hơn |

---

## 2. Sequence 3 bước — Chi tiết

| Lần | Ngày | Mục tiêu | Tone | Offer | Kênh | Script |
|-----|------|---------|------|-------|------|--------|
| **Lần 1** | Ngày 1 | Kết nối lại — không bán | Quan tâm, cá nhân | Không có offer | Zalo cá nhân | Xem bên dưới |
| **Lần 2** | Ngày 5–7 | Tạo lý do quay lại | Ưu đãi giới hạn | [Offer Tier 1] | Zalo OA | Xem bên dưới |
| **Lần 3** | Ngày 12–14 | Best offer cuối | Trân trọng, không ép | [Offer Tier 2] | Zalo cá nhân | Xem bên dưới |

### Script Lần 1 — Kết nối lại
> *"[Tên] ơi, lâu rồi mình chưa gặp nhau. Không biết gần đây [tên khách] thế nào rồi? [Câu hỏi cụ thể theo ngành — da, kết quả tập, đơn hàng...]. Bên em vừa có thêm [điều mới], để em chia sẻ tham khảo nhé."*

### Script Lần 2 — Offer nhẹ
> *"[Tên] ơi, bên em đang có chương trình dành riêng cho khách cũ — [offer cụ thể, ví dụ: miễn phí 1 bước X / giảm 10% / free ship]. Chỉ còn đến [ngày cụ thể]. [Tên] có muốn em giữ lịch / giữ ưu đãi không?"*

### Script Lần 3 — Best offer
> *"[Tên] ơi, em biết [tên khách] bận. Đây là ưu đãi tốt nhất em có thể dành cho [tên khách] — [offer cụ thể + deadline]. Nếu không tiện lần này, em hiểu. Khi nào cần, em vẫn ở đây."*

---

## 3. Offer theo Tier — [Ngành cụ thể]

| Tier | Dùng khi | Offer | Giá trị | Tác động margin | Điều kiện |
|------|---------|-------|---------|----------------|----------|
| **Tier 1** (Lần 2) | Nhóm "Quên mất" | [Offer nhẹ theo ngành] | Thấp | ~0% | Không cần điều kiện |
| **Tier 2** (Lần 3) | Tất cả nhóm chưa phản hồi | [Offer mạnh hơn] | Trung bình | -5–15% | Deadline cụ thể |

> Không giảm giá quá 20% — tạo thói quen chờ deal, phá vỡ giá trị thương hiệu.

---

## 4. Quy trình Test (BẮT BUỘC trước khi chạy toàn bộ)

```
Bước 1 — Chọn 10% danh sách (tối thiểu 5 người, tối đa 10 người)
  → Ưu tiên khách từng có tương tác tốt, ít rủi ro nhất

Bước 2 — Gửi Tin 1 cho nhóm test
  → Theo dõi 48–72h: reply rate, tone phản hồi, có ai bực bội không

Bước 3 — Đánh giá kết quả
  → Reply rate > 30%: script tốt → chạy toàn bộ
  → Reply rate 10–30%: chỉnh lại Tin 1 → test lần 2
  → Reply rate < 10% hoặc phản hồi tiêu cực: dừng, xem lại tone + offer

Bước 4 — Scale sau khi test cho kết quả tốt
```

---

## 5. KPI Campaign

| KPI | Target | Thực tế | Đánh giá |
|-----|--------|---------|---------|
| **Win-back rate** | >20% | | Số khách quay lại / tổng danh sách |
| **Open/Read rate** (Zalo OA) | >40% | | Zalo OA dashboard |
| **Re-conversion rate** | >15% | | Số mua lại / số phản hồi |
| **Block/Unsubscribe rate** | <5% | | Số bị chặn / tổng gửi |
| **Revenue from winback** | [X VNĐ] | | Đơn hàng có tag winback |

---

## 6. Danh sách triển khai

| # | Tên khách | SĐT / Zalo | Nhóm lý do bỏ | Ngày Lần 1 | Phản hồi L1 | Ngày Lần 2 | Phản hồi L2 | Ngày Lần 3 | Kết quả |
|---|----------|-----------|--------------|-----------|------------|-----------|------------|-----------|---------|
| 1 | | | | | | | | | |
| 2 | | | | | | | | | |
| 3 | | | | | | | | | |"""
})

# Upsert all
print(f'Upsert {len(updates)} sections...')
for u in updates:
    sb.table('skill_sections').upsert(u, on_conflict='skill_id,section_id').execute()
    print(f'  OK  {u["skill_id"]:30s} / {u["section_id"]:25s} (priority={u["priority"]})')

print()
print('=== DONE ===')

# Verify
for sid in ['30-retention-strategy', '31-winback-campaign']:
    res = sb.table('skill_sections').select('section_id, priority').eq('skill_id', sid).order('priority').execute()
    print(f'\n{sid}:')
    for s in res.data:
        print(f'  [{s["priority"]}] {s["section_id"]}')
