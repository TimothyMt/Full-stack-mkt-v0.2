---
name: 06-brief-ugc-egc
skill_id: "06-brief-ugc-egc"
agent: "content-producer"
description: Tao brief chi tiet cho UGC (khach hang), EGC (nhan vien), KOC (creator tra phi) — gom huong dan quay, do/don't, quyen su dung, quan ly batch
metadata:
  version: 3.0.0
  category: content
triggers:
  - "brief creator"
  - "brief UGC"
  - "brief EGC"
  - "huong dan quay video nhan vien"
  - "brief KOC"
  - "brief seeding"
  - "quan ly creator"
output: file .md gom brief chi tiet theo loai (UGC/EGC/KOC), tieu chi chon creator, huong dan quay, hop dong quyen, bang quan ly batch
related:
  - 04-script-video
  - 05-copy-quang-cao
  - 01-lich-noi-dung
  - 03-danh-gia-hieu-suat
context_requirements:
  required:
    - product_name
    - target_audience
  optional:
    - industry
    - budget_monthly
---

# Brief UGC / EGC / KOC

<!-- #SECTION
id: context_intake
type: context_intake
priority: 1
modes: [all]
industries: [all]
tags: [session_context, mode, onboarding]
-->

## Bước 0 — Đọc session_context

Trước khi hỏi, kiểm tra session_context:

| Field | Nếu có → | Nếu null → |
|-------|-----------|------------|
| `product_name` | Dùng luôn, không hỏi Q1 | Hỏi Q1 |
| `target_audience` | Dùng luôn, không hỏi Q1 | Hỏi Q1 |
| `industry` | Ghi nhận, dùng khi viết DO/DON'T ngành | Detect từ câu trả lời |
| `budget_monthly` | Gợi ý co cau thanh toan phù hợp | Hỏi Q4 |
| `mode` | `product` = mode A / `personal_brand` = mode B | Mặc định `product` |

<!-- #/SECTION -->

<!-- #SECTION
id: data_collection
type: data_collection
priority: 1
modes: [all]
industries: [all]
tags: [intake, adaptive]
-->

## Thu thập thông tin

**Nếu session_context đã có `product_name` + `target_audience` → chỉ hỏi Q2, Q3, Q4.**
**Nếu chưa có → hỏi đủ 4 câu.**

1. **Sản phẩm / dịch vụ gì?** Mô tả ngắn, USP, giá, đối tượng khách hàng.
   *(Bỏ qua nếu session_context đã có)*
2. **Loại creator nào?** UGC (khách hàng thật), EGC (nhân viên), KOC (creator trả phí). Nếu không chọn — mặc định UGC.
3. **Mục tiêu nội dung?** TOFU (nhận biết), MOFU (thuyết phục), BOFU (chốt đơn). Số lượng video cần.
4. **Ngân sách và thời gian?** Ngân sách/video, deadline giao video, thời gian chiến dịch.

<!-- #/SECTION -->

<!-- #SECTION
id: creator_framework
type: logic
priority: 1
modes: [all]
industries: [all]
tags: [ugc, egc, koc, framework]
-->

## Nguyên tắc cốt lõi

### Phân biệt 3 loại creator

| Tiêu chí | UGC (User) | EGC (Employee) | KOC (Key Opinion Consumer) |
|----------|-----------|----------------|--------------------------|
| Người quay | Khách hàng thật | Nhân viên công ty | Creator trả phí / đổi sản phẩm |
| Độ tin cậy | Cao nhất — khách thật | Cao — người trong cuộc | Trung bình — nhận diện là quảng cáo |
| Chi phí | Thấp (sản phẩm + voucher) | Lương nhân viên (đã có) | 500K–10M/video tùy follower |
| Kiểm soát nội dung | Thấp | Cao | Trung bình — có brief nhưng creator tự sáng tạo |
| Quyền sử dụng | Cần xin phép | Mặc định thuộc công ty | Theo hợp đồng |
| Phù hợp cho | Social proof, MOFU | Behind-the-scenes, employer branding | Reach, awareness, TOFU |

### Tiêu chí chọn creator

#### UGC — Khách hàng

| Tiêu chí | Yêu cầu |
|----------|---------|
| Đã sử dụng sản phẩm | Bắt buộc — có bằng chứng (đơn hàng, check-in, review cũ) |
| Chất lượng camera | iPhone 11+ hoặc tương đương — video không bể, không mờ |
| Phong cách nói | Tự nhiên, không đọc script cứng — có cảm xúc |
| Ngoại hình | Phù hợp đối tượng mục tiêu (cùng demographic) |
| Độ sẵn lòng | Đồng ý quay + cho phép sử dụng trên kênh thương hiệu |

#### EGC — Nhân viên

| Tiêu chí | Yêu cầu |
|----------|---------|
| Phòng ban | Ưu tiên: sale, kỹ thuật, chăm sóc khách hàng — người tiếp xúc khách trực tiếp |
| Phong cách | Tự nhiên, không quá "corporate" — như kể chuyện cho bạn nghe |
| Thiết bị | Điện thoại cá nhân (không cần máy quay chuyên nghiệp) |
| Tần suất | 2–4 video/tháng/người |
| Động lực | Thưởng theo view/engagement, ngày phép, quà tặng |

#### KOC — Creator trả phí

| Tiêu chí | Mức chấp nhận |
|----------|--------------|
| Follower | Nano: 1K–10K / Micro: 10K–50K / Mid: 50K–200K |
| Engagement rate | >3% (nano), >2% (micro), >1.5% (mid) |
| Niche | Phù hợp ngành hàng (beauty, F&B, lifestyle, tech) |
| Content style | Tự nhiên, không "ads quá rõ" — storytelling, review, daily vlog |
| Demographics kéo | 70%+ follower là đối tượng mục tiêu (độ tuổi, giới tính, địa lý) |
| Lịch sử brand deal | Kiểm tra — tránh creator đã làm với đối thủ trực tiếp trong 3 tháng |

<!-- #/SECTION -->

<!-- #SECTION
id: brief_structure
type: output_template
priority: 1
modes: [all]
industries: [all]
tags: [brief, template, core]
-->

## Cấu trúc brief chi tiết

### Phần 1 — Tổng quan

```markdown
# Brief [UGC/EGC/KOC]: [Tên sản phẩm/chiến dịch]
Ngày tạo: [YYYY-MM-DD]
Deadline giao video: [YYYY-MM-DD]
Loại creator: [UGC / EGC / KOC]
Số lượng video cần: [X video]
Nền tảng đăng: [TikTok / Reels / YouTube Shorts / Tất cả]
```

### Phần 2 — Thông tin sản phẩm

| Hạng mục | Chi tiết |
|----------|---------|
| Tên sản phẩm / dịch vụ | [Tên] |
| Mô tả 1 câu | [Mô tả ngắn] |
| USP chính (1–2 điểm) | [Điểm khác biệt] |
| Giá | [Giá bán / Giá khuyến mãi] |
| Đối tượng khách hàng | [Giới tính, độ tuổi, nỗi đau] |
| Link sản phẩm | [URL hoặc thông tin đặt hàng] |
| Hashtag bắt buộc | [#TênThươngHiệu, #TênChiếnDịch] |

### Phần 3 — DO / DON'T

| DO — Nên làm | DON'T — Không làm |
|-------------|------------------|
| Nói tự nhiên, như kể chuyện cho bạn nghe | Không đọc script cứng nhắc |
| Nhắc tên sản phẩm / dịch vụ rõ ràng | Không nhắc tên đối thủ |
| Show kết quả / trải nghiệm thật | Không cam kết kết quả "100%", "đảm bảo" |
| Quay dọc 9:16, ánh sáng tốt | Không quay ngang, không quay tối |
| Nhắc CTA cuối video | Không quên CTA |
| Dùng âm thanh rõ, không ồn | Không quay ở nơi ồn ào |
| **Gắn #quangcao hoặc #PR trong caption (bắt buộc theo NĐ 147/2024)** | **Không đăng paid content mà không khai báo → rủi ro pháp lý cho brand** |
| [Thêm theo sản phẩm cụ thể] | Không sử dụng nhạc có bản quyền |

> **Lưu ý pháp lý:** Nghị định 147/2024 yêu cầu mọi nội dung được tài trợ/trả phí phải khai báo rõ ràng bằng hashtag `#quangcao`, `#PR`, hoặc `#sponsored` trong caption. Creator vi phạm có thể bị phạt — brand thuê creator cũng có trách nhiệm liên đới.

### Phần 4 — 3 góc độ video (chọn 1 hoặc quay cả 3)

| Góc độ | Mô tả | Hook gợi ý | Phù hợp |
|--------|-------|-----------|---------|
| Góc độ 1: [VD: Review thật] | Kể lại trải nghiệm sử dụng — trước/sau | "Mình dùng cái này [X] tuần — kết quả đây" | MOFU |
| Góc độ 2: [VD: Day in my life] | Lồng ghép sản phẩm vào sinh hoạt hàng ngày | "1 ngày của mình — có thứ này không thể thiếu" | TOFU |
| Góc độ 3: [VD: So sánh] | So sánh với phương pháp cũ / sản phẩm khác (không nhắc tên đối thủ) | "Trước mình dùng cách này — giờ đổi sang cái này" | MOFU |

### Phần 5 — Cấu trúc video

| Timestamp | Nội dung | Ghi chú |
|-----------|---------|--------|
| [0–3s] | Hook — gây tò mò, giữ người xem | Không giới thiệu bản thân |
| [3–10s] | Context — vấn đề hoặc tình huống | Liên kết với nỗi đau của đối tượng |
| [10–25s] | Sản phẩm — show/demo/trải nghiệm | Nhắc tên sản phẩm, show bao bì/dịch vụ |
| [25–35s] | Kết quả — trước/sau, cảm nhận | Thành thật, không quá hoa mỹ |
| [35–45s] | CTA — khuyến nghị hành động | Cụ thể: "Nhắn tin fanpage để tư vấn" |

*(Điều chỉnh timestamp theo thời lượng: 15s, 30s, 45s, 60s — tham khảo 04-script-video)*

### Phần 6 — Hướng dẫn quay kỹ thuật

| Hạng mục | Yêu cầu |
|----------|---------|
| Tỉ lệ khung hình | 9:16 (dọc) — bắt buộc |
| Độ phân giải | Tối thiểu 1080p |
| Ánh sáng | Ánh sáng tự nhiên hoặc ring light — không ngược sáng |
| Âm thanh | Phòng yên tĩnh, nói rõ ràng. Mic cài áo nếu có |
| Độ dài | [15s / 30s / 45s / 60s] — theo brief |
| Số take | Quay tối thiểu 2 take — gửi cả 2 để chọn |
| Cảnh quay | Close-up sản phẩm + medium shot người dùng + B-roll |

### Phần 7 — Format giao nộp

| Hạng mục | Yêu cầu |
|----------|---------|
| Định dạng file | .mp4 (không nén, không filter nặng) |
| Cách gửi | Google Drive / Dropbox — KHÔNG gửi qua Messenger/Zalo (nén chất lượng) |
| Tên file | [TênCreator]_[GócĐộ]_[Take1/2]_[YYYYMMDD].mp4 |
| Deadline | [YYYY-MM-DD] trước 18:00 |
| Người nhận | [Tên + số điện thoại / email] |
| Review | Thương hiệu review trong 48h — phản hồi chỉnh sửa (nếu có) trong 24h |

<!-- #/SECTION -->

<!-- #SECTION
id: negative_example
type: negative_example
priority: 2
modes: [all]
industries: [all]
tags: [quality, anchor, example]
-->

## Ví dụ: Brief xấu vs Brief tốt

### ❌ Brief xấu — Thiếu định hướng, creator không biết làm gì

```
Brief: Quay video giới thiệu sản phẩm kem dưỡng da của chúng tôi.
Nội dung: Nói về công dụng sản phẩm, review cảm nhận sau khi dùng.
Deadline: Cuối tuần.
Liên hệ: 0912xxxxxx
```

**Vấn đề:**
- Không có cấu trúc video (creator tự nghĩ → random)
- Không có DO/DON'T → không khai báo #quangcao → rủi ro pháp lý
- Không có USP → creator không biết nhấn điểm gì
- Không có góc độ → 5 creator quay 5 kiểu khác nhau
- Không có format giao nộp → nhận file qua Zalo, bị nén
- Deadline mơ hồ "cuối tuần" → không giờ cụ thể

---

### ✅ Brief tốt — Creator đọc xong biết chính xác phải làm gì

```
# Brief UGC: Kem dưỡng da Sakura 20ml
Ngày tạo: 2026-05-15 | Deadline: 2026-05-22 trước 18:00
Loại: UGC (khách hàng thật) | Cần: 3 video | Đăng: TikTok + Reels

## Sản phẩm
- Kem dưỡng trắng da chiết xuất hoa anh đào Nhật
- USP: Thấm nhanh trong 30 giây, không nhờn, không bít lỗ chân lông
- Giá: 280K/20ml | Đối tượng: Nữ 22–35, da dầu/hỗn hợp
- Hashtag: #SakuraSkin #KemDưỡngSakura #quangcao

## Góc độ bạn chọn (quay 1 trong 3)
- Góc độ 1: Review 7 ngày dùng — kết quả da thay đổi thế nào
- Góc độ 2: Skincare routine sáng — show cách dùng tự nhiên
- Góc độ 3: "Trước dùng kem X giờ đổi sang cái này — so sánh cảm giác"

## Cấu trúc video (45 giây)
- 0–3s: Hook — không giới thiệu bản thân
- 3–10s: Kể vấn đề da (nhờn, bít lỗ chân lông)
- 10–30s: Dùng kem — show texture, thấm nhanh
- 30–40s: Kết quả sau 7 ngày
- 40–45s: CTA — "Nhắn tin fanpage Sakura Skin được tư vấn miễn phí"

## DO / DON'T
✅ Nói tự nhiên, quay 9:16, ánh sáng mặt rõ
✅ Gắn #quangcao hoặc #PR trong caption (bắt buộc)
❌ Không cam kết "trắng 100%", không nhắc tên đối thủ
❌ Không gửi file qua Zalo — upload Google Drive

## Giao nộp
File: SakuraSkin_[TênBạn]_Take1_20260522.mp4
Gửi về: drive.google.com/... trước 18:00 ngày 22/5
Liên hệ: Chị Mai 0912xxxxxx
```

**Tại sao tốt:**
- Creator biết chính xác 1 trong 3 góc độ để chọn
- Cấu trúc timestamp → không cần sáng tạo cấu trúc, chỉ cần điền nội dung
- DO/DON'T rõ ràng kể cả khai báo #quangcao
- Format giao nộp cụ thể → không mất file qua Zalo

<!-- #/SECTION -->

<!-- #SECTION
id: contract
type: reference
priority: 2
modes: [full]
industries: [all]
tags: [legal, contract, rights]
-->

## Hợp đồng quyền sử dụng nội dung

### Template ngắn (cho UGC / KOC)

```markdown
THỎA THUẬN SỬ DỤNG NỘI DUNG

Bên A (Thương hiệu): [Tên công ty]
Bên B (Creator): [Tên creator]
Ngày ký: [YYYY-MM-DD]

1. NỘI DUNG: [Số lượng] video về [sản phẩm/dịch vụ], thời lượng [Xs].
2. QUYỀN SỬ DỤNG: Bên A được quyền sử dụng nội dung trên:
   - [ ] Kênh thương hiệu (fanpage, TikTok, IG)
   - [ ] Quảng cáo trả phí (Meta Ads, TikTok Ads)
   - [ ] Website, landing page
   - [ ] Kênh offline (event, POS)
3. THỜI HẠN: [X tháng] kể từ ngày giao nội dung.
4. CHỈNH SỬA: Bên A được phép cắt, ghép, thêm text overlay. Không được thay đổi nội dung lời nói.
5. THANH TOÁN: [Số tiền] — thanh toán trong [X ngày] sau khi giao nội dung đạt yêu cầu.
6. ĐỘC QUYỀN: Creator không quay cho đối thủ trực tiếp trong [X tháng].
7. KHAI BÁO QUẢNG CÁO: Creator có nghĩa vụ gắn #quangcao và/hoặc #PR trong caption
   khi đăng nội dung theo hợp đồng này (theo Nghị định 147/2024). Không thực hiện →
   Bên A có quyền giữ lại 20% thanh toán cho đến khi creator cập nhật caption.

Chữ ký Bên A: _______________
Chữ ký Bên B: _______________
```

### Lưu ý pháp lý

- Với UGC (khách hàng): Xin phép bằng tin nhắn có screenshot — lưu lại làm bằng chứng
- Với KOC: Hợp đồng viết — cả 2 bên ký (điện tử hoặc giấy)
- Với EGC: Không cần hợp đồng riêng — nội dung tạo trong giờ làm việc thuộc công ty (ghi rõ trong hợp đồng lao động)
- Quyền hình ảnh: Creator đồng ý cho dùng hình ảnh cá nhân — ghi rõ trong hợp đồng

<!-- #/SECTION -->

<!-- #SECTION
id: payment_structure
type: reference
priority: 2
modes: [all]
industries: [all]
tags: [payment, pricing, vn-benchmark]
-->

## Cơ cấu thanh toán

### Bảng giá tham khảo (thị trường VN 2025–2026)

| Hạng creator | Follower | Giá/video (VND) | Ghi chú |
|-------------|---------|----------------|--------|
| Nano KOC | 1K–10K | 500K–2M | Thường đổi sản phẩm + tiền |
| Micro KOC | 10K–50K | 2M–5M | Có thể barter (sản phẩm) nếu giá trị tương đương |
| Mid KOC | 50K–200K | 5M–15M | Thường chỉ nhận tiền mặt |
| UGC (khách hàng) | Không yêu cầu | Sản phẩm + voucher 200K–500K | Không trả tiền — trả giá trị |
| EGC (nhân viên) | Không yêu cầu | 0 (lương đã có) + thưởng 200K–500K/video | Thưởng theo hiệu suất video |

### Mô hình thanh toán

| Mô hình | Mô tả | Phù hợp |
|---------|-------|---------|
| Per video | Trả cố định/video — đơn giản, dễ quản lý | KOC nano/micro, số lượng ít |
| Revenue share | Trả % doanh thu từ video — động lực cao | KOC có ảnh hưởng, sản phẩm có tracking |
| Product exchange | Đổi sản phẩm/dịch vụ — không trả tiền | UGC, nano KOC, sản phẩm giá trị cao |
| Retainer | Trả tháng — cam kết số lượng video/tháng | Creator dài hạn, 4+ video/tháng |

<!-- #/SECTION -->

<!-- #SECTION
id: performance_tracking
type: reference
priority: 2
modes: [all]
industries: [all]
tags: [analytics, tracking, kpi]
-->

## Theo dõi hiệu suất creator

### Bảng theo dõi từng creator

| Creator | Nền tảng | Video | View | Like | Comment | Share | Save | ER | CPV | Lead | Doanh thu |
|---------|---------|-------|------|------|---------|-------|------|----|-----|------|-----------|
| [Tên 1] | TikTok | [Link] | | | | | | | | | |
| [Tên 2] | Reels | [Link] | | | | | | | | | |
| [Tên 3] | TikTok | [Link] | | | | | | | | | |

### Chỉ số đánh giá

| Chỉ số | Kém | Trung bình | Tốt | Xuất sắc |
|--------|-----|------------|-----|----------|
| Engagement rate (ER) | <2% | 2–5% | 5–10% | >10% |
| Save rate | <0.5% | 0.5–2% | 2–5% | >5% |
| CPV (chi phí/view) | >500đ | 200–500đ | 100–200đ | <100đ |
| Video completion rate | <20% | 20–40% | 40–60% | >60% |

### Quy định re-book

- ER > 5% + Save rate > 2% → Re-book ngay cho đợt tiếp theo
- ER 2–5% + nội dung tốt → Re-book với góc độ khác
- ER < 2% → Không re-book — tìm creator mới

<!-- #/SECTION -->

<!-- #SECTION
id: batch_management
type: reference
priority: 3
modes: [full]
industries: [all]
tags: [batch, operations, scale]
-->

## Quản lý batch (10+ creator cùng lúc)

### Bảng quản lý tiến độ

| # | Creator | Loại | Trạng thái | Ngày gửi brief | Ngày giao video | Review | Duyệt | Đăng | Ghi chú |
|---|---------|------|-----------|---------------|----------------|--------|-------|------|--------|
| 1 | [Tên] | KOC | [Chưa gửi / Đã gửi / Đang quay / Đã giao / Cần chỉnh / Đã duyệt / Đã đăng] | | | | | | |
| 2 | | | | | | | | | |
| 3 | | | | | | | | | |

### Trạng thái video

```
Chưa gửi brief → Đã gửi brief → Đang quay → Đã giao video
  → Review (48h) → Cần chỉnh sửa → Chỉnh sửa xong → Đã duyệt → Đã đăng
```

### Quy trình quản lý

1. **Chuẩn bị batch:** Tạo danh sách creator + brief riêng cho từng người (cùng template, khác góc độ)
2. **Gửi brief:** Gửi brief + sản phẩm (nếu cần) cùng lúc — ghi nhận ngày gửi
3. **Follow-up:** Nhắc nhở 3 ngày trước deadline nếu chưa giao
4. **Review:** Xem video trong 48h — phản hồi chỉnh sửa cụ thể (timestamp + nội dung cần sửa)
5. **Duyệt:** Confirm final — gửi lên kênh hoặc chạy ads
6. **Theo dõi:** Cập nhật hiệu suất hàng tuần — quyết định re-book

### Mẫu tin nhắn follow-up

```
[Follow-up nhắc nhở]
"Chào [Tên], brief bên [Thương hiệu] gửi hôm [ngày] — bạn quay đến đâu rồi?
Deadline [ngày] nhé. Nếu cần hỗ trợ gì cứ nhắn tin nha!"

[Phản hồi chỉnh sửa]
"Video tốt lắm! Có 2 chỗ mình muốn chỉnh:
1. [0:05] — thêm text overlay tên sản phẩm
2. [0:25] — CTA đổi thành 'Nhắn tin fanpage để tư vấn'
Bạn chỉnh giúp trong 24h nhé — cảm ơn nhiều!"
```

<!-- #/SECTION -->

<!-- #SECTION
id: output_format
type: output_format
priority: 1
modes: [all]
industries: [all]
tags: [output, telegram, excel]
-->

## Output format

### Telegram (mode: quick) — Bullet tóm tắt ý chính

Khi user nhắn qua Telegram, trả về dạng ngắn gọn:

```
📋 Brief [UGC/EGC/KOC]: [Tên chiến dịch]

👥 Creator: [Loại] — [Số lượng] người
🎯 Mục tiêu: [TOFU/MOFU/BOFU] — [Số lượng] video
📅 Deadline: [Ngày]
💰 Ngân sách: [Tổng / Per video]

✅ DO: [3 điểm quan trọng nhất]
❌ DON'T: [2 điểm quan trọng nhất, bao gồm #quangcao]

📹 Góc độ gợi ý: [Tên góc độ 1] / [Góc độ 2] / [Góc độ 3]

📎 File brief đầy đủ: [Link Google Sheet hoặc nhắn "full" để nhận file]
```

### Full (mode: full) — Excel / Google Sheet

Khi user cần file chi tiết, output cấu trúc Excel gồm các tab:

| Tab | Nội dung |
|-----|---------|
| Brief Overview | Phần 1–2 (tổng quan + sản phẩm) |
| DO/DON'T | Phần 3 — bao gồm disclosure requirement |
| Video Angles | Phần 4–5 (góc độ + cấu trúc timestamp) |
| Tech Guide | Phần 6–7 (kỹ thuật + giao nộp) |
| Contract | Template hợp đồng + Điều 7 khai báo |
| Creator Tracker | Bảng theo dõi tiến độ + hiệu suất |
| Batch Management | Trạng thái từng creator (nếu 10+) |

<!-- #/SECTION -->

<!-- #SECTION
id: quality_checklist
type: quality_checklist
priority: 1
modes: [all]
industries: [all]
tags: [checklist, quality]
-->

## Liên kết skill liên quan

- **04-script-video** — Script chi tiết cho creator tham khảo khi quay
- **05-copy-quang-cao** — Dùng video UGC/KOC làm creative cho ads — cần copy đi kèm
- **01-lich-noi-dung** — Xếp lịch đăng video creator vào lịch nội dung tổng
- **03-danh-gia-hieu-suat** — Đánh giá hiệu suất creator để quyết định re-book

---

## Checklist chất lượng

Kiểm tra trước khi gửi brief:

- [ ] Rõ loại creator: UGC, EGC, hay KOC
- [ ] Có thông tin sản phẩm đầy đủ (tên, USP, giá, đối tượng)
- [ ] Có bảng DO / DON'T cụ thể
- [ ] DO/DON'T **có yêu cầu gắn #quangcao / #PR** (NĐ 147/2024)
- [ ] Có ít nhất 3 góc độ video để creator chọn
- [ ] Có cấu trúc video theo timestamp
- [ ] Có hướng dẫn quay kỹ thuật (khung hình, ánh sáng, âm thanh)
- [ ] Có format giao nộp rõ ràng (định dạng, cách gửi, deadline)
- [ ] Có hợp đồng / thỏa thuận quyền sử dụng nội dung
- [ ] Hợp đồng **có Điều 7 — khai báo quảng cáo**
- [ ] Có cơ cấu thanh toán rõ ràng
- [ ] Có bảng theo dõi hiệu suất cho từng creator
- [ ] Nếu batch 10+ creator — có bảng quản lý tiến độ
- [ ] Không yêu cầu creator nói điều vi phạm chính sách quảng cáo

<!-- #/SECTION -->
