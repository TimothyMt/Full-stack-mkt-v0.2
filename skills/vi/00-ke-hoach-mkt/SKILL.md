---
skill_id: "00-ke-hoach-mkt"
name: "Ke Hoach Fullstack Marketing"
description: Ke hoach Fullstack Marketing — master skill tong hop chien luoc, noi dung, trien khai, hieu suat, va timeline. Goi cac skill con de hoan thien output.
agent: "mkt-strategist"
metadata:
  version: 2.1.0
  category: strategy
triggers:
  - "lap ke hoach marketing"
  - "fullstack marketing plan"
  - "chien luoc marketing"
  - "ke hoach trien khai"
  - "ke hoach content"
  - "performance plan"
  - "phan bo ngan sach"
  - "ke hoach kenh"
  - "GTM"
  - "launch san pham"
  - "ke hoach campaign"
output: File .md hoan chinh gom 7 phan — Strategy, SAVE Framework, Content Plan, Channel & Budget, Performance KPI, Risk Matrix, Timeline
related:
  - 08-nghien-cuu-doi-thu
  - 09-insight-khach-hang
  - 10-tinh-kpi-nguoc
  - 01-lich-noi-dung
  - 02-brief-chien-dich
  - 03-danh-gia-hieu-suat
context_requirements:
  required: []
  optional:
    - industry        # co → skip Buoc 2 detect nganh
    - business_stage  # co → skip hoi giai doan kinh doanh
    - objectives      # co → skip hoi muc tieu
    - budget          # co → skip hoi ngan sach
---

# Ke Hoach Fullstack Marketing

> Master skill — goi 08-nghien-cuu-doi-thu, 09-insight-khach-hang, 10-tinh-kpi-nguoc truoc khi xuat output.

---

<!-- #SECTION
id: context_intake
type: context_intake
priority: 1
modes: [all]
industries: [all]
tags: [session_context, industry, onboarding]
-->

## Thu thap thong tin

### Buoc 0 — Nhan tu session_context

> Master Agent da inject session_context truoc khi skill nay chay. Dung truc tiep — KHONG hoi lai neu da co.

- `industry` co → skip Buoc 2, load variant nganh tuong ung ngay
- `industry` chua co → hoi detect nganh o Buoc 2, Master Agent cap nhat session_context

<!-- #/SECTION -->

---

<!-- #SECTION
id: industry_detect
type: logic
priority: 1
modes: [all]
industries: [all]
tags: [industry, routing, nganh, detect]
-->

### Buoc 2 — Detect nganh (neu chua co trong session_context)

| Nganh nguoi dung noi | Industry code | Variant ap dung |
|----------------------|--------------|----------------|
| Spa, beauty salon, nail, tham my khong xam lan | `spa` | Kenh: TikTok+FB+Zalo / KPI: Mess→Lead→Booking |
| Phong kham, nha khoa, tham my co xam lan | `clinic` | Kenh: FB+Google+Zalo / KPI: Lead→Tu van→Deposit |
| Nha hang, quan cafe, F&B | `fnb` | Kenh: TikTok+FB+GrabFood / KPI: Order+FootTraffic |
| Gym, yoga, fitness studio | `fitness` | Kenh: FB+Zalo+Community / KPI: Trial→Member→Renew |
| Khoa hoc, trung tam day them | `education` | Kenh: FB+Google+Zalo / KPI: Lead→Trial→Enroll |
| Ecommerce, ban hang online | `ecommerce` | Kenh: TikTok+FB+Shopee / KPI: ROAS+CAC+LTV |
| SaaS, phan mem, app | `saas` | Kenh: Google+LinkedIn+Email / KPI: Trial→Paid→MRR |
| Bat dong san | `realestate` | Kenh: Google+FB+Batdongsan / KPI: Lead→Site visit→Deposit |
| Nganh khac | `general` | Dung template chung, hoi them |

Neu nganh chua co variant → dung `general` + ghi chu de bo sung sau.

<!-- #/SECTION -->

---

<!-- #SECTION
id: data_collection
type: data_collection
priority: 1
modes: [all]
industries: [all]
tags: [questions, objectives, budget, fgc, founder]
-->

### Buoc 3 — Hoi toi da 3 cau con lai

> Skip tung cau neu da co trong session_context.

1. **Muc tieu cu the?** Doanh thu muc tieu/thang, so don/thang, hay KPI khac?
   → Skip neu `objectives` co trong session_context
2. **Ngan sach marketing?** Tong ngan sach/thang (ads + content + nhan su)?
   → Skip neu `budget` co trong session_context
3. **Chu founder/chinh chu co san sang xuat hien tren content khong?** (Co / Khong / Thinh thoang)
   → Co → FGC 25–30% trong Source Type Mix
   → Khong → Tang Brand Content + UGC bu vao, FGC = 0%
   → Thinh thoang → FGC 10–15%

<!-- #/SECTION -->

---

<!-- #SECTION
id: template_strategy
type: template
priority: 2
modes: [all]
industries: [all]
tags: [strategy, swot, competitive_moat, customer_insight, phan1]
-->

## Phan 1 — Chien luoc tong the

### 1.1 Tom tat tinh hinh

| Hang muc | Noi dung |
|----------|----------|
| San pham / Dich vu | [ten + USP] |
| Thi truong | [dia ly + quy mo] |
| Giai doan | Launch / Growth / Mature |
| Thoi gian ke hoach | [so thang] |
| Ngan sach tong | [so tien] |

### 1.2 Phan tich SWOT

| | Tich cuc | Tieu cuc |
|---|---------|---------|
| **Noi bo** | Strengths: [liet ke] | Weaknesses: [liet ke] |
| **Ben ngoai** | Opportunities: [liet ke] | Threats: [liet ke] |

### 1.3 Competitive Moat Analysis

> Goi skill `08-nghien-cuu-doi-thu` de co du lieu day du.

| Doi thu | Kenh manh | Diem yeu khai thac | Moat cua ho | Moat cua minh |
|---------|-----------|--------------------|--------------| --------------|
| [Doi thu 1] | | | | |
| [Doi thu 2] | | | | |
| [Doi thu 3] | | | | |

**Loai moat can xay:**
- Brand trust (nhan dien + do tin cay)
- Content depth (noi dung chuyen sau doi thu khong lam)
- Community lock-in (cong dong khach hang trung thanh)
- Data advantage (hieu khach hon doi thu)
- Distribution (nhieu kenh phan phoi hon)

### 1.4 Customer Insight

> Goi skill `09-insight-khach-hang` de xac dinh insight chinh.

| Yeu to | Mo ta |
|--------|-------|
| Noi dau lon nhat | [mieu ta cu the] |
| Mong muon tham kin | [dieu ho thuc su muon nhung chua noi ra] |
| Rao can mua hang | [ly do ho chua mua] |
| Trigger mua hang | [tinh huong khien ho san sang chi tien] |
| Kenh ho tin tuong | [nguoi/kenh nao anh huong quyet dinh] |

<!-- #/SECTION -->

---

<!-- #SECTION
id: template_save
type: template
priority: 2
modes: [all]
industries: [all]
tags: [save, solution, access, value, education, framework, phan2]
-->

## Phan 2 — SAVE Framework

> Thay the 4P truyen thong. Phu hop hon cho dich vu va san pham so.

### 2.1 Solution (Giai phap — thay vi Product)

| Cau hoi | Tra loi |
|---------|---------|
| Khach hang dang gap van de gi? | [noi dau cu the] |
| San pham giai quyet nhu the nao? | [co che giai quyet] |
| Ket qua ho nhan duoc la gi? | [outcome cu the, do duoc] |
| Trong bao lau ho thay ket qua? | [timeline ky vong] |

### 2.2 Access (Tiep can — thay vi Place)

| Kenh | Vai tro | Uu tien |
|------|---------|---------|
| [Kenh 1] | TOFU — thu hut | Cao / Trung binh / Thap |
| [Kenh 2] | MOFU — nurture | |
| [Kenh 3] | BOFU — chuyen doi | |
| [Kenh 4] | Retention — giu chan | |

> Tham khao `references/channel-system.md` de chon kenh phu hop.

### 2.3 Value (Gia tri — thay vi Price)

| Hang muc | Chi tiet |
|----------|----------|
| Gia san pham / dich vu | [muc gia] |
| Gia tri khach nhan duoc | [dinh luong: tiet kiem X, tang Y] |
| Ti le gia tri / gia | [bao nhieu lan] |
| So sanh voi doi thu | [re hon / dat hon — ly do] |
| Pricing psychology | [anchor, bundle, tier, free trial] |

### 2.4 Education (Giao duc — thay vi Promotion)

| Giai doan | Noi dung giao duc | Muc dich |
|-----------|-------------------|----------|
| Chua biet van de | Content noi dau, awareness | De ho nhan ra van de |
| Biet van de, chua biet giai phap | How-to, so sanh phuong phap | De ho hieu cac lua chon |
| Biet giai phap, chua chon | Case study, testimonial, demo | De ho tin tuong minh |
| Da chon, chua hanh dong | Offer, khan cap, social proof | De ho hanh dong ngay |

<!-- #/SECTION -->

---

<!-- #SECTION
id: template_content_plan
type: template
priority: 3
modes: [full]
industries: [all]
tags: [content, pillar, funnel, source_type_mix, repurposing, phan3]
-->

## Phan 3 — Ke hoach noi dung

### 3.1 Content Pillar

| Pillar | Ti le | Muc dich | Vi du |
|--------|-------|----------|-------|
| Giao duc (Education) | 35% | Xay trust, SEO | How-to, tips, giai thich |
| Cam hung (Inspiration) | 25% | Engagement, viral | Case study, truoc/sau, story |
| Giai tri (Entertainment) | 20% | Reach, follower | Trend, POV, behind scenes |
| Ban hang (Selling) | 15% | Chuyen doi | Offer, deal, CTA truc tiep |
| Cong dong (Community) | 5% | Retention | Q&A, poll, user spotlight |

### 3.2 Funnel Distribution

| Tang pheu | Ti le noi dung | Goc do chinh | KPI |
|-----------|---------------|--------------|-----|
| TOFU (Nhan biet) | 40% | Cham noi dau, giai tri, giao duc | View, reach, follower |
| MOFU (Can nhac) | 35% | Bang chung, chuyen gia, quy trinh | Engagement, save, click |
| BOFU (Chuyen doi) | 15% | Offer, khan cap, retarget | Mess, lead, don hang |
| Retention | 10% | Gia tri VIP, referral | Re-purchase, LTV |

> Tham khao `references/content-angles.md` de chon goc do cu the.

### 3.3 Nguyen tac san xuat noi dung

- Moi noi dung goc duoc tai su dung toi thieu 3 dinh dang — chi tiet tai `01-lich-noi-dung`
- Uu tien video ngan lam goc (TikTok/Reels) — tai su dung duoc nhieu nhat, chi phi thap nhat

### 3.4 Source Type Mix

> Ti le duoi day duoc dieu chinh tu dong dua tren tra loi cau hoi FGC o buoc Thu thap thong tin.

| Loai | Founder xuat hien | Founder khong xuat hien | Founder thinh thoang |
|------|------------------|------------------------|---------------------|
| FGC (Founder Generated Content) | 25–30% | 0% | 10–15% |
| Brand Content | 25–30% | 45–50% | 30–35% |
| UGC (User Generated Content) | 25% | 35% | 30% |
| EGC (Employee Generated Content) | 15–20% | 15–20% | 15–20% |

<!-- #/SECTION -->

---

<!-- #SECTION
id: template_channel_budget
type: template
priority: 3
modes: [full]
industries: [all]
tags: [channel, budget, allocation, paid_ads, phan4]
-->

## Phan 4 — He thong kenh & Ngan sach

### 4.1 Kenh trien khai

> Tham khao `references/channel-system.md` cho chi tiet tung tang.

| Kenh | Tang pheu | Ngan sach/thang | KPI chinh |
|------|----------|-----------------|-----------|
| TikTok (organic + ads) | TOFU + BOFU | [so tien] | View, mess, CPMess |
| Facebook (organic + ads) | MOFU + BOFU | [so tien] | Reach, mess, CPMess |
| Zalo OA | MOFU + Retention | [so tien] | Read rate, click rate |
| Email (Brevo) | MOFU + Retention | [so tien] | Open rate, click rate |
| Website / SEO | MOFU | [so tien] | Traffic, time on site |
| UGC Network | TOFU | [so tien] | View, reach |
| [Kenh khac] | | | |

### 4.2 Phan bo ngan sach theo giai doan

| Hang muc | Launch (thang 1–3) | Growth (thang 4–6) | Mature (thang 7+) |
|----------|-------------------|--------------------|--------------------|
| Paid ads | 45–55% | 35–45% | 25–35% |
| Content production | 20–25% | 20–25% | 15–20% |
| UGC / KOL | 15–20% | 15–20% | 10–15% |
| Tool & platform | 5–10% | 5–10% | 5–10% |
| Community & retention | 5% | 10–15% | 20–25% |
| Du phong (contingency) | 5% | 5% | 5% |
| **Tong** | **100%** | **100%** | **100%** |

### 4.3 Bang phan bo ngan sach cu the

| Hang muc | Ngan sach/thang | % Tong | Ghi chu |
|----------|-----------------|--------|---------|
| Meta Ads | [so tien] | [%] | |
| TikTok Ads | [so tien] | [%] | |
| Content (nhan su + tool) | [so tien] | [%] | |
| UGC thu lao | [so tien] | [%] | |
| Tool (Canva, Brevo, ...) | [so tien] | [%] | |
| Du phong | [so tien] | 5% | |
| **Tong** | **[so tien]** | **100%** | |

<!-- #/SECTION -->

---

<!-- #SECTION
id: template_kpi
type: template
priority: 2
modes: [all]
industries: [all]
tags: [kpi, performance, reverse_kpi, scenarios, roas, cac, ltv, phan5]
-->

## Phan 5 — KPI & Performance

### 5.1 Tinh KPI nguoc

> Goi skill `10-tinh-kpi-nguoc` de tinh chinh xac.

```
Doanh thu muc tieu: [so tien]
  / AOV: [so tien]
  = So don can: [so]
  / Booking->Customer [25–40%]: [so]
  = So booking can: [so]
  / Lead->Booking [50–60%]: [so]
  = So lead can: [so]
  / Mess->Lead [50–60%]: [so]
  = So tin nhan can: [so]
  x CPMess [25–35K]: [so tien]
  = Ngan sach ads can: [so tien]
```

### 5.2 Bang KPI 3 kich ban

| Chi so | Xau (Pessimistic) | Co so (Base) | Tot (Optimistic) |
|--------|-------------------|-------------|------------------|
| CPMess | +30% vs benchmark | Benchmark nganh | -20% vs benchmark |
| Mess->Lead | -15% vs TB | TB nganh (55%) | +15% vs TB |
| Lead->Booking | -10% vs TB | TB nganh (55%) | +10% vs TB |
| Booking->Customer | -10% vs TB | TB nganh (35%) | +10% vs TB |
| **So don/thang** | [so] | [so] | [so] |
| **Doanh thu/thang** | [so tien] | [so tien] | [so tien] |
| **ROAS** | [so]x | [so]x | [so]x |
| **Ngan sach can** | [so tien] | [so tien] | [so tien] |

> Benchmark Vietnam 2025–2026: xem `references/benchmarks-vietnam.md`

### 5.3 KPI theo kenh

| Kenh | KPI chinh | Muc tieu thang 1 | Muc tieu thang 3 | Muc tieu thang 6 |
|------|-----------|-------------------|-------------------|-------------------|
| TikTok organic | View/video, follower | | | |
| TikTok ads | CPMess, ROAS | | | |
| FB ads | CPMess, CPL, ROAS | | | |
| Zalo OA | Read rate, click rate | | | |
| Email | Open rate, click rate | | | |
| SEO | Organic traffic, ranking | | | |

### 5.4 Business KPI

| Chi so | Cong thuc | Muc tieu |
|--------|----------|----------|
| ROAS | Doanh thu / Chi phi ads | >3x |
| CAC | Tong chi MKT / So khach moi | <30% AOV |
| LTV | AOV x So lan mua TB x Thoi gian | >3x CAC |
| Payback period | CAC / (AOV x Margin) | <90 ngay |
| LTV:CAC | LTV / CAC | >3:1 |

<!-- #/SECTION -->

---

<!-- #SECTION
id: template_risk
type: template
priority: 3
modes: [full]
industries: [all]
tags: [risk, matrix, mitigation, crisis, phan6]
-->

## Phan 6 — Risk Matrix

### 6.1 Bang rui ro

| Rui ro | Xac suat | Muc do anh huong | Muc do nghiem trong | Ke hoach xu ly |
|--------|----------|------------------|---------------------|----------------|
| CPMess tang dot bien (mua le) | Cao | Cao | **CRITICAL** | Giam ngan sach ads 30%, chuyen sang organic + UGC |
| Creative fatigue (duoi 2 tuan) | Cao | Trung binh | **HIGH** | Chuan bi 3–5 creative moi/tuan, A/B test lien tuc |
| Doi thu giam gia manh | Trung binh | Cao | **HIGH** | Tap trung gia tri + trust, khong canh tranh gia |
| Thay doi algorithm (TikTok/FB) | Trung binh | Cao | **HIGH** | Da dang kenh, khong phu thuoc 1 platform |
| Nhan su nghi viec (content creator) | Thap | Cao | **MEDIUM** | SOP hoa quy trinh, backup nhan su |
| Phan hoi tieu cuc viral | Thap | Rat cao | **CRITICAL** | Crisis protocol: phan hoi trong 2h, transparent |
| Ngan sach bi cat giam | Trung binh | Trung binh | **MEDIUM** | Ke hoach B voi 50% ngan sach — uu tien organic |
| Thieu data khach hang | Thap | Trung binh | **LOW** | Thu thap data tu ngay 1, form + pixel + CRM |

### 6.2 Muc do nghiem trong

| Muc | Dinh nghia | Hanh dong |
|-----|-----------|-----------|
| **CRITICAL** | Anh huong truc tiep doanh thu, mat khach | Xu ly trong 24h, escalate stakeholder |
| **HIGH** | Giam hieu suat dang ke, mat co hoi | Xu ly trong 48h, dieu chinh ke hoach |
| **MEDIUM** | Anh huong nhe, co the bu dap | Xu ly trong 1 tuan, theo doi |
| **LOW** | Anh huong khong dang ke | Ghi nhan, xu ly khi co thoi gian |

<!-- #/SECTION -->

---

<!-- #SECTION
id: template_timeline
type: template
priority: 3
modes: [full]
industries: [all]
tags: [timeline, phases, milestones, results_based, phan7]
-->

## Phan 7 — Timeline trien khai

> Timeline duoi day theo **ket qua dat duoc**, khong theo lich. Moi giai doan chi chuyen sang giai doan tiep khi dieu kien dau vao duoc thoa man — co the mat 2 tuan hoac 3 thang tuy thuc te.

### 7.1 Cac giai doan theo ket qua

| Giai doan | Dieu kien buoc vao | Viec can lam | Dieu kien chuyen sang giai doan tiep |
|-----------|-------------------|-------------|--------------------------------------|
| **1 — Khoi dong** | Chua co data, chua co winning creative | Setup kenh, san xuat 3–5 creative test, chay ads ngan sach thap | Co du lieu 2 tuan, CPMess < benchmark nganh |
| **2 — Tim winning** | Da co data dau, biet kenh nao co tiem nang | A/B test creative, thu nghiem audience, do CPMess/CPL | ROAS > 2x lien tuc trong 2 tuan |
| **3 — Scale** | ROAS on dinh > 2x, biet ro winning creative + audience | Tang ngan sach toi da 20%/tuan, nhan rong kenh tot, cat kenh kem | Doanh thu dat 70%+ muc tieu, he thong on dinh |
| **4 — Duy tri** | Doanh thu dat muc tieu, he thong chay on | Giam paid dan, tang organic + retention, bat dau referral | Organic chiem 30%+ traffic, CAC giam lien tuc |

### 7.2 Viec can lam theo giai doan

| Hang muc | Giai doan 1 | Giai doan 2 | Giai doan 3 | Giai doan 4 |
|----------|-------------|-------------|-------------|-------------|
| Ngan sach ads | 30–40% tong ngan sach | 50–60% | 60–70% | Giam dan 30–40% |
| So creative chay | 3–5 (test) | 1–2 winning + 2–3 test moi | Scale winning, 1–2 test/tuan | Duy tri winning, test it hon |
| Kenh tap trung | 1 kenh chinh | 1–2 kenh | 2–3 kenh | Kenh da chung minh |
| Retention | Chua can | Bat dau thu thap contact | Setup Zalo OA + email | He thong day du |
| Nguoi chiu trach nhiem | [ten] | [ten] | [ten] | [ten] |

### 7.3 Dau hieu canh bao — Dung lai va xem xet lai

| Dau hieu | Y nghia | Hanh dong |
|---------|---------|----------|
| CPMess tang > 30% sau 1 tuan scale | Creative fatigue hoac audience bao hoa | Tao creative moi, mo rong audience |
| ROAS giam > 30% khi tang ngan sach | Scale qua nhanh | Giam ngan sach 20%, on dinh lai |
| Ty le Mess→Lead giam > 20% | Van de tu van hoac chat luong lead | Kiem tra lai script tu van, retarget audience |
| Khong chuyen sang giai doan 2 sau 4 tuan | Creative chua du tot hoac sai audience | Stop, review lai insight khach hang (Skill 09) |

<!-- #/SECTION -->

---

<!-- #SECTION
id: skill_chaining
type: logic
priority: 2
modes: [all]
industries: [all]
tags: [chaining, workflow, sequence, sub_skills]
-->

## Skill Chaining — Chuoi ky nang

Skill nay la master — goi cac skill con theo thu tu:

```
00-ke-hoach-mkt (MASTER)
  |
  |-- [1] 08-nghien-cuu-doi-thu  → Phan tich doi thu, tim khe
  |-- [2] 09-insight-khach-hang  → Insight khach hang, noi dau
  |-- [3] 10-tinh-kpi-nguoc      → Tinh ngan sach va KPI tu doanh thu muc tieu
  |
  |-- [4] Xuat ke hoach (file nay)
  |
  |-- [5] 01-lich-noi-dung       → Lich noi dung thang chi tiet
  |-- [6] 02-brief-chien-dich    → Brief chien dich dau tien
```

Khi user yeu cau ke hoach marketing:
1. Kiem tra session_context — neu da co industry, skip cau hoi nganh
2. Neu chua co industry → detect tu input, luu vao memory
3. Hoi 3 cau con lai (muc tieu, ngan sach, FGC)
4. Chay skill 08, 09, 10 (co the song song)
5. Tong hop thanh ke hoach day du 7 phan — dung variant theo nganh
6. Giao output full cho Master Agent → Master Agent format theo kenh (Telegram/Excel)
7. De xuat chay tiep 01, 02 neu user can

<!-- #/SECTION -->

---

<!-- #SECTION
id: quality_checklist
type: quality_checklist
priority: 1
modes: [all]
industries: [all]
tags: [quality, checklist, validation, pre_delivery]
-->

## Checklist chat luong

Truoc khi giao ke hoach, kiem tra:

- [ ] Co du 7 phan (Strategy, SAVE, Content, Channel, Performance, Risk, Timeline)
- [ ] SWOT dua tren du lieu thuc, khong doan
- [ ] Competitive moat xac dinh ro — khong chung chung
- [ ] SAVE Framework day du 4 yeu to
- [ ] Content pillar co ti le cu the, cong = 100%
- [ ] Funnel distribution dung ti le (TOFU 40%, MOFU 35%, BOFU 15%, Retention 10%)
- [ ] Ngan sach phan bo theo giai doan (Launch/Growth/Mature)
- [ ] Bang KPI 3 kich ban (Pessimistic/Base/Optimistic) da tinh
- [ ] Risk matrix co it nhat 5 rui ro voi muc do + ke hoach xu ly
- [ ] Timeline co milestone cu the theo thang
- [ ] Benchmark su dung so lieu Vietnam 2025–2026
- [ ] Cross-reference den cac skill lien quan
- [ ] Tat ca so lieu co the do duoc — khong co cum tu "tang manh", "nhieu hon"
- [ ] Tong ngan sach cong chinh xac 100%

<!-- #/SECTION -->
