---
name: 02-brief-chien-dich
description: Brief chien dich marketing — 9 phan day du tu Context den Risk, bao gom creative direction, RACI, budget allocation theo phase, va auto-trigger cac skill lien quan.
skill_id: "02-brief-chien-dich"
agent: "mkt-strategist"
metadata:
  version: 2.1.0
  category: strategy
triggers:
  - "brief chien dich"
  - "brief sang tao"
  - "brief Tet"
  - "brief ra mat san pham"
  - "viet brief"
  - "creative brief"
output: File .md brief chien dich 10 phan — Context, Objectives, Target, Core Message, Offer, Creative Direction, Channel System, Timeline, Deliverables, Risks
related:
  - 00-ke-hoach-mkt
  - 01-lich-noi-dung
  - 04-script-video
  - 05-copy-quang-cao
  - 06-brief-ugc-egc
  - 09-insight-khach-hang
context_requirements:
  required: []
  optional:
    - industry          # co → skip hoi lai thuong hieu/nganh o Section 1
    - active_channels   # co → dung luon cho Channel System (Section 6)
    - customer_profile  # co → Section 3 chi hoi neu segment khac
    - team_size         # co → skip Buoc 4 hoi so nguoi
    - team_roles        # co → build RACI truc tiep voi ten thuc te
---

# Brief Chien Dich

<!-- #SECTION
id: context_intake
type: context_intake
priority: 1
modes: [all]
industries: [all]
tags: [onboarding, session_context, mode_select]
-->

## Thu thap thong tin

### Buoc 0 — Nhan tu session_context

> Master Agent da inject session_context truoc khi skill nay chay. Dung truc tiep — KHONG hoi lai neu da co.

- `industry` + `business.*` co → skip hoi lai thong tin thuong hieu, nganh
- `active_channels` co → dung luon cho Channel System (Section 6)
- `customer_profile` co → Section 3 chi hoi them neu campaign nay co segment khac
- `team_size` + `team_roles` co → build RACI truc tiep, skip Buoc 4

<!-- #/SECTION -->

<!-- #SECTION
id: logic_campaign_type
type: logic
priority: 1
modes: [all]
industries: [all]
tags: [campaign_type, phase_model, budget_allocation]
-->

### Buoc 2 — Xac dinh loai chien dich → chon phase model

| Loai chien dich | Phase model | Ghi chu |
|----------------|------------|---------|
| Flash sale (1–3 ngay) | 2 phases: Bung manh 70% + Duy tri 30% | Khong can Teasing |
| Ra mat san pham moi | 4 phases: Teasing 20% + Soft 20% + Launch 40% + Sustain 20% | Teasing dai hon |
| Seasonal (Tet, 8/3, 20/10) | 4 phases: Teasing 15% + Soft 20% + Launch 40% + Sustain 25% | Giu nguyen mac dinh |
| Retarget campaign | 1 phase: 100% conversion | Chi warm audience |
| Brand awareness | 3 phases: Awareness 50% + Engagement 30% + Conversion 20% | Khong focus chot don |

<!-- #/SECTION -->

<!-- #SECTION
id: data_collection
type: data_collection
priority: 1
modes: [all]
industries: [all]
tags: [campaign_info, team, assets]
-->

### Buoc 3 — Hoi nhung gi chua co trong memory (toi da 3 cau)

1. **Chien dich gi + thoi gian?** Ten chien dich, ngay bat dau, thoi luong bao nhieu tuan
2. **Ngan sach tong?** Bao nhieu, phan bo the nao (ads / content / khac)?
3. **Da co gi san?** Asset hien co: UGC, testimonial, landing page, creative cu?

### Buoc 4 — Xac dinh team → build RACI thuc te

Hoi user 2 cau:
1. **Team hien tai co bao nhieu nguoi lam marketing?** (tinh ca chu/founder neu truc tiep tham gia)
2. **Cac vai tro / phong ban hien co la gi?** (VD: "chi co minh chu + 1 ban content" / "co team 4 nguoi: marketing manager, designer, content, ads" / "thue agency ngoai")

→ Dua tren cau tra loi, tu dong tao RACI voi dung ten vai tro thuc te cua khach — khong dung ten chung chung.

<!-- #/SECTION -->

<!-- #SECTION
id: template_context
type: template
priority: 2
modes: [all]
industries: [all]
tags: [context, campaign_overview, market_situation]
-->

## Phan 1 — Context (Boi canh)

### 1.1 Tong quan

| Hang muc | Noi dung |
|----------|----------|
| Ten chien dich | [ten chien dich] |
| Loai | Launch / Seasonal / Awareness / Sales / Re-launch |
| Thuong hieu | [ten thuong hieu] |
| San pham / Dich vu | [mo ta ngan] |
| Ly do chay chien dich | [tai sao chay luc nay? trigger la gi?] |

### 1.2 Tinh hinh thi truong

| Yeu to | Mo ta |
|--------|-------|
| Xu huong nganh | [xu huong hien tai] |
| Hanh vi khach hang mua nay | [thay doi gi?] |
| Doi thu dang lam gi | [hoat dong noi bat cua doi thu] |
| Co hoi khai thac | [khe thi truong] |

### 1.3 Bai hoc tu chien dich truoc

| Chien dich truoc | Ket qua | Bai hoc |
|------------------|---------|---------|
| [ten chien dich] | [KPI dat / khong dat] | [dieu gi hieu qua / khong hieu qua] |

<!-- #/SECTION -->

<!-- #SECTION
id: template_objectives
type: template
priority: 2
modes: [all]
industries: [all]
tags: [objectives, kpi, smart_goals]
-->

## Phan 2 — Objectives (Muc tieu)

### 2.1 Muc tieu SMART

| Loai | Muc tieu | Do bang gi | Deadline |
|------|----------|-----------|----------|
| Business | [VD: Doanh thu 500 trieu trong 4 tuan] | Doanh so, GMV | [ngay] |
| Marketing | [VD: 5,000 tin nhan, CPMess <30K] | So mess, CPMess, ROAS | [ngay] |
| Brand | [VD: Reach 2 trieu, tang 3K follower] | Reach, follower, mention | [ngay] |

### 2.2 KPI chi tiet

| KPI | Muc tieu | Benchmark nganh | Gap |
|-----|----------|-----------------|-----|
| CPMess | [so] | [benchmark tu references/benchmarks-vietnam.md] | |
| ROAS | [so]x | >3x | |
| CPL | [so] | [benchmark] | |
| Reach | [so] | | |
| Engagement rate | [so]% | | |
| So don hang | [so] | | |

<!-- #/SECTION -->

<!-- #SECTION
id: template_message
type: template
priority: 2
modes: [all]
industries: [all]
tags: [core_message, tagline, tone_of_voice]
-->

## Phan 4 — Core Message (Thong diep cot loi)

### 4.1 Message Framework

| Tang | Thong diep | Dung cho |
|------|-----------|----------|
| Tagline | [5–8 tu, de nho] | Moi noi — nhat quan xuyen suot |
| Key message | [1–2 cau, giai thich gia tri] | Website, landing page, ads chinh |
| Supporting message #1 | [bang chung/tinh nang ho tro] | Content giao duc |
| Supporting message #2 | [bang chung/tinh nang ho tro] | Content thuyet phuc |
| Supporting message #3 | [bang chung/tinh nang ho tro] | Content chot don |

### 4.2 Tone of Voice

| Thuoc tinh | La | Khong phai |
|-----------|-----|-----------|
| Giong dieu | [VD: than thien, chuyen gia] | [VD: kho khan, xa cach] |
| Ngon ngu | [VD: don gian, doi thuong] | [VD: hoc thuat, chuyen nganh] |
| Cam xuc | [VD: tu tin, an tam] | [VD: lo lang, ap luc] |

<!-- #/SECTION -->

<!-- #SECTION
id: template_timeline_phases
type: template
priority: 2
modes: [all]
industries: [all]
tags: [timeline, phases, budget_allocation, milestone]
-->

## Phan 7 — Timeline & Phases

### 7.1 Phan bo ngan sach theo phase

> Phase model duoc chon tu buoc Thu thap thong tin dua tren loai chien dich. Dien vao bang phu hop.

**Flash sale (1–3 ngay):**

| Phase | Thoi gian | % Ngan sach | Muc dich | Kenh chinh |
|-------|----------|-------------|----------|------------|
| Bung manh | Ngay 1–2 | 70% | Chot don nhanh, tao urgency | Paid ads toan luc, Zalo blast |
| Duy tri | Ngay 3 | 30% | Vot lai, retarget | Retarget, Messenger |

**Ra mat san pham moi:**

| Phase | Thoi gian | % Ngan sach | Muc dich | Kenh chinh |
|-------|----------|-------------|----------|------------|
| Teasing | Tuan 1–2 | 20% | Xay curiosity, thu email/follow | Organic, email teaser, UGC |
| Soft launch | Tuan 3 | 20% | Test creative, thu data | Paid ads ngan sach nho |
| Full launch | Tuan 4–6 | 40% | Scale, chot don | Paid ads toan luc, retarget |
| Sustain | Tuan 7+ | 20% | Re-engage, cross-sell | Retarget, Zalo, email |

**Seasonal / Chien dich dinh ky (Tet, 8/3, 20/10):**

| Phase | Thoi gian | % Ngan sach | Muc dich | Kenh chinh |
|-------|----------|-------------|----------|------------|
| Teasing | Tuan 1 | 15% | Tao to mo, build anticipation | Organic TikTok/FB, email teaser |
| Soft launch | Tuan 2 | 20% | Test creative, thu data | Paid ads ngan sach nho, UGC |
| Full launch | Tuan 3–4 | 40% | Scale winning creative, chot don | Paid ads toan luc, retarget |
| Sustain | Tuan 5+ | 25% | Re-engage, retarget | Retarget, email, Zalo nurture |

### 7.2 Chi tiet timeline

| Ngay | Hang muc | Chi tiet | Nguoi chiu TN | Trang thai |
|------|----------|----------|--------------|------------|
| [D-14] | Creative production | San xuat video + anh | [ten] | |
| [D-7] | UGC brief gui | Brief cho UGC creators | [ten] | |
| [D-5] | Landing page live | Setup + test toan bo | [ten] | |
| [D-3] | Teasing bat dau | Organic post + story | [ten] | |
| [D-Day] | Launch chinh thuc | Ads live, blast email, broadcast | [ten] | |
| [D+3] | Review data dau | Check CPMess, CTR, creative nao tot | [ten] | |
| [D+7] | Toi uu vong 1 | Cut creative kem, scale creative tot | [ten] | |
| [D+14] | Review giua chien dich | So sanh vs KPI, dieu chinh | [ten] | |
| [D+21] | Retarget phase | Focus retarget warm audience | [ten] | |
| [D+28] | Ket thuc + bao cao | Tong ket, bai hoc, de xuat tiep theo | [ten] | |

<!-- #/SECTION -->

<!-- #SECTION
id: template_target
type: template
priority: 3
modes: [full]
industries: [all]
tags: [target_audience, persona, insight_validation]
-->

## Phan 3 — Target Audience (Doi tuong muc tieu)

> Doc tu `customer_memory.customer_profile` truoc. Chi hien thi bang duoi neu chua co trong memory hoac campaign nay co segment khac voi binh thuong.

**Hoi them 1 cau neu memory da co:** "Chien dich nay co nham vao nhom khach hang khac binh thuong khong?"
- Neu khong → dung nguyen tu memory, khong hoi them
- Neu co → hoi mo ta segment moi, chi cap nhat phan khac biet

### 3.1 Chan dung khach hang

| Thuoc tinh | Primary | Secondary |
|-----------|---------|-----------|
| Do tuoi | [doc tu memory hoac hoi] | [khoang tuoi] |
| Gioi tinh | [doc tu memory hoac hoi] | |
| Khu vuc | [doc tu memory hoac hoi] | |
| Thu nhap | [doc tu memory hoac hoi] | |
| Nghe nghiep | [doc tu memory hoac hoi] | |
| Noi dau chinh | [doc tu memory hoac hoi] | |
| Mong muon | [doc tu memory hoac hoi] | |
| Rao can | [doc tu memory hoac hoi] | |
| Kenh ho dung | [doc tu memory hoac hoi] | |
| Ai anh huong ho | [doc tu memory hoac hoi] | |

### 3.2 Insight khach hang

> Doc tu `customer_memory.customer_profile.main_pain_points` truoc. Goi `09-insight-khach-hang` neu can khai thac sau hon.

**Insight chinh:** [doc tu memory hoac phat bieu moi neu campaign co segment khac]

### 3.3 Insight Validation Checklist

Kiem tra xem insight co that su la insight hay chi la observation:

| Tieu chi | Dat | Khong dat |
|----------|-----|-----------|
| **Specific** — Cu the cho nhom khach nay, khong chung chung? | [ ] | [ ] |
| **Hidden** — Khach hang khong tu noi ra, phai khai thac? | [ ] | [ ] |
| **Actionable** — Co the bien thanh thong diep/creative? | [ ] | [ ] |
| **Emotional** — Cham vao cam xuc, khong chi ly tri? | [ ] | [ ] |
| **True** — Dua tren du lieu/quan sat thuc, khong phai gia dinh? | [ ] | [ ] |

**Quy tac:** Phai dat it nhat 4/5 tieu chi. Neu khong → do la observation, chua phai insight. Tim lai.

**Phan biet:**
- Observation: "Phu nu 25–35 quan tam cham soc da" → ai cung biet, khong co gi moi
- Insight: "Ho mua serum khong phai vi da dep hon — ma vi cam giac dang tu thuong minh sau 1 ngay met moi" → cham cam xuc, co the lam creative

<!-- #/SECTION -->

<!-- #SECTION
id: template_offer
type: template
priority: 2
modes: [all]
industries: [all]
tags: [offer, pricing, mechanic, urgency]
-->

## Phan 4B — Tao Offer Chien Dich (Gia · Goi · Mechanic)

> **Tai sao phai co:** Creative dep nhung offer mu → khach xem xong khong biet phai lam gi, gia the nao, con bao nhieu. Offer ro rang = tang conversion 30–50% so voi chay ads khong offer.

### 4B.1 Cau truc offer

| Hang muc | Chi tiet |
|----------|---------|
| San pham / Dich vu chinh | [ten + mo ta ngan] |
| Gia goc (gia niem yet) | [so tien] |
| Gia uu dai chien dich | [so tien] |
| % Giam / Gia tri qua tang | [VD: giam 30% / tang kem tri gia 200K] |
| Thoi han offer | [ngay bat dau — ngay ket thuc, hoac "chi con X suat"] |
| Dieu kien ap dung | [VD: ap dung khi dat lich qua fanpage / ap dung cho khach moi] |
| CTA chinh | [VD: "Nhan tin fanpage de dat lich" / "Mua ngay — giao trong 24h"] |

### 4B.2 Dang goi (chon 1 hoac ket hop)

| Dang goi | Mo ta | Phu hop |
|----------|-------|---------|
| Single product | 1 san pham / dich vu — gia ro, de hieu | Launch don, kiem nhanh |
| Bundle | Nhom 2–3 san pham kem — gia bundle tot hon mua le | Upsell, tang AOV |
| Tiered offer | 3 cap do: Co ban / Nang cao / Pro — khach tu chon | Segment theo ngan sach |
| Gift with purchase | Mua chinh duoc tang kem qua tang co gia tri ro | F&B, beauty, spa |
| Trial / Intro offer | Gia uu dai cho lan dau su dung | Dich vu, subscription |
| Membership / Package | Mua goi nhieu buoi — gia tot hon don le | Spa, fitness, clinic |

**Goi da chon:** [mo ta cu the goi + gia tung cap do neu co]

### 4B.3 Mechanic uu dai (cach khuyen khich hanh dong)

| Mechanic | Mo ta | Urgency | Phu hop |
|----------|-------|---------|---------|
| Flash sale | Giam manh trong 24–72h — dem nguoc thoi gian | ⭐⭐⭐ | Hang tieu dung nhanh, ecom |
| Early bird | Dat truoc duoc gia tot hon — het han tang gia | ⭐⭐ | Ra mat san pham, khoa hoc |
| Gioi han so luong | "Chi con X suat" — khan cap that | ⭐⭐⭐ | Dich vu, workshop |
| Buy X get Y | Mua 2 tang 1 / mua 500K tang san pham XYZ | ⭐ | FMCG, spa combo |
| Referral offer | Gioi thieu ban duoc them X% / giam Y% | ⭐ | Dich vu re-visit, subscription |
| Voucher tang kem | Tang voucher cho lan su dung tiep theo | ⭐ | Spa, clinic, F&B |
| Combo khuyen mai | Gop dich vu A + B gia tot hon mua rieng | ⭐ | Spa, clinic, fitness |

**Mechanic da chon:** [ten mechanic + mo ta cu the]

### 4B.4 Urgency & Scarcity (bat buoc co it nhat 1)

| Loai | Noi dung cu the |
|------|----------------|
| Time limit | [VD: "Uu dai het han 23:59 ngay 30/5"] |
| Quantity limit | [VD: "Chi con 20 suat gia soc — da ban 180/200"] |
| Exclusive | [VD: "Chi ap dung cho khach dat lich qua Fanpage — khong ap dung tai quay"] |
| Social proof | [VD: "500+ khach da su dung trong thang nay"] |

### 4B.5 Vi du — Offer mu vs Offer ro

**Offer mu (khong lam):**
> "Giam gia dich vu triet long gia re. Lien he de biet them chi tiet."

Tai sao toi: Khong co gia → khach khong biet co phu hop ngan sach khong. Khong co thoi han → khong urgent. Khong co CTA ro → khach phai tu hoi.

---

**Offer ro (lam theo):**
> "Goi triet long chan tron: 3 buoi chi 990K (goc 1.5 trieu — giam 34%). Tang kem 1 buoi cham soc da mat tri gia 300K.
> Chi con 15 suat — het han 31/5. Nhan tin Fanpage dat lich trong hom nay nhan them voucher 100K buoi tiep theo."

Tai sao tot: Gia ro → khach quyet dinh duoc ngay. Urgency 2 tang (thoi gian + so luong). Gift ro gia tri. CTA cu the. Voucher khuyen khich re-visit.

<!-- #/SECTION -->

<!-- #SECTION
id: template_creative
type: template
priority: 3
modes: [full]
industries: [all]
tags: [creative_direction, visual, format_by_channel]
-->

## Phan 5 — Creative Direction (Dinh huong sang tao)

### 5.1 Creative Territory

| Hang muc | Chi tiet |
|----------|----------|
| Visual mood | [VD: am ap, tu nhien, dang tin — khong bong bay, fake] |
| Color palette | [mau chinh + mau phu] |
| Typography | [font heading + body] |
| Photography style | [VD: lifestyle that, khong stock photo] |
| Video style | [VD: talking head + b-roll, UGC style, cinematic] |
| Do's | [lam gi — VD: dung anh khach that, quay vertical] |
| Don'ts | [khong lam gi — VD: khong dung nhac buon, khong font nhieu mau] |

### 5.2 Key Visual

| Yeu to | Mo ta |
|--------|-------|
| Hero image/video | [mo ta visual chinh] |
| Thumbnail style | [mo ta] |
| Text overlay | [co/khong, style] |
| Logo placement | [vi tri, kich thuoc] |

### 5.3 Creative brief theo kenh

| Kenh | Dinh dang | Kich thuoc | Thoi luong | So luong creative |
|------|-----------|-----------|------------|-------------------|
| TikTok | Video dung | 9:16 (1080x1920) | 15–60s | [so] |
| Facebook (feed) | Video + anh | 1:1, 4:5 | 15–30s | [so] |
| Instagram (Reels) | Video dung | 9:16 | 15–30s | [so] |
| Instagram (feed) | Carousel | 1:1 (1080x1080) | 5–7 slide | [so] |
| Zalo OA | Banner + text | 600x315 | -- | [so] |
| Email | Banner + body | 600px width | -- | [so] |
| Landing page | Hero + sections | Responsive | -- | 1 |

<!-- #/SECTION -->

<!-- #SECTION
id: template_channels
type: template
priority: 3
modes: [full]
industries: [all]
tags: [channel_system, paid_media, channel_roles]
-->

## Phan 6 — Channel System (He thong kenh)

### 6.1 Kenh su dung

> Tham khao `references/channel-system.md`

| Kenh | Vai tro | Ngay bat dau | Ngan sach | KPI |
|------|---------|-------------|-----------|-----|
| TikTok (organic) | Reach + awareness | [ngay] | [production cost] | View, follower |
| TikTok (ads) | Mess + conversion | [ngay] | [so tien] | CPMess, ROAS |
| Facebook (ads) | Retarget + conversion | [ngay] | [so tien] | CPMess, ROAS |
| UGC Network | Social proof | [ngay] | [thu lao] | View, trust |
| Zalo OA | Nurture | [ngay] | -- | Read rate |
| Email | Nurture + offer | [ngay] | -- | Open rate |
| Landing page | Conversion | [ngay] | [thiet ke] | Conv rate |

### 6.2 Paid Media Plan

| Kenh | Muc tieu | Audience | Ngan sach/ngay | Creative | Thoi gian |
|------|----------|----------|---------------|----------|-----------|
| Meta — Awareness | Reach | Broad, LAL 1–3% | [so tien] | Video 15s hook | [tuan] |
| Meta — Conversion | Mess/Lead | Retarget + Interest | [so tien] | Video + carousel | [tuan] |
| TikTok — Reach | View + Mess | Broad | [so tien] | UGC style video | [tuan] |

<!-- #/SECTION -->

<!-- #SECTION
id: template_deliverables
type: template
priority: 3
modes: [full]
industries: [all]
tags: [deliverables, raci, team_roles]
-->

## Phan 8 — Deliverables & RACI

### 8.1 Danh sach san pham ban giao

| STT | Deliverable | So luong | Deadline | Nguoi lam | Nguoi duyet |
|-----|------------|----------|----------|-----------|-------------|
| 1 | Video TikTok (30s) | [so] | [ngay] | [ten] | [ten] |
| 2 | Video Facebook (15s) | [so] | [ngay] | [ten] | [ten] |
| 3 | Carousel (5–7 slide) | [so] | [ngay] | [ten] | [ten] |
| 4 | Copy quang cao (3 phien ban) | [so] | [ngay] | [ten] | [ten] |
| 5 | Landing page | 1 | [ngay] | [ten] | [ten] |
| 6 | Email template (welcome + offer) | 2 | [ngay] | [ten] | [ten] |
| 7 | UGC brief | [so] | [ngay] | [ten] | [ten] |
| 8 | Script video | [so] | [ngay] | [ten] | [ten] |
| 9 | Zalo broadcast noi dung | [so] | [ngay] | [ten] | [ten] |
| 10 | Bao cao ket thuc chien dich | 1 | [ngay] | [ten] | [ten] |

### 8.2 RACI Matrix

> RACI duoi day duoc tao tu dong dua tren so luong va vai tro thuc te user cung cap o Buoc 4.
> Cot = cac vai tro thuc te cua team (dung ten ho cung cap, khong dung ten mac dinh).
> Hang = cac deliverable o Section 8.1.

| Deliverable | [Vai tro 1] | [Vai tro 2] | [Vai tro 3] | ... |
|------------|------------|------------|------------|-----|
| [Deliverable 1] | R/A/C/I | | | |
| [Deliverable 2] | | | | |
| ... | | | | |

**Vi du — "chi co minh + 1 ban content":**

| Deliverable | Chu (Linh) | Nhan vien content (Hoa) |
|------------|-----------|------------------------|
| Brief chien dich | **A+R** | I |
| San xuat creative | A | **R** |
| Chay ads | **R** | I |
| Toi uu + bao cao | **R** | C |

**Vi du — "4 nguoi: marketing manager, designer, content, ads":**

| Deliverable | MKT Manager | Designer | Content | Ads |
|------------|------------|---------|---------|-----|
| Brief chien dich | **A+R** | I | I | I |
| Creative | A | **R** | **R** | C |
| Copy | A | I | **R** | C |
| Setup ads | A | I | I | **R** |
| Toi uu | A | I | C | **R** |
| Bao cao | **R** | I | C | C |

**RACI la gi?** Ma tran phan cong trach nhiem — giup moi nguoi biet ro vai tro cua minh, tranh chong cheo hoac bo sot:
- **R — Responsible** (Nguoi thuc hien): Nguoi truc tiep lam ra san pham do
- **A — Accountable** (Nguoi chiu trach nhiem): Nguoi duyet cuoi, chiu trach nhiem neu sai
- **C — Consulted** (Nguoi duoc hoi): Duoc hoi y kien truoc khi lam — co the phan bien
- **I — Informed** (Nguoi duoc bao): Chi can biet ket qua, khong can tham gia

> Moi deliverable phai co dung 1 chu **A** — neu co 2 nguoi cung chiu trach nhiem = khong ai chiu trach nhiem.

<!-- #/SECTION -->

<!-- #SECTION
id: template_risks
type: template
priority: 3
modes: [full]
industries: [all]
tags: [risks, mitigation, fallback_plan]
-->

## Phan 9 — Risks & Mitigation

### 9.1 Bang rui ro chien dich

| Rui ro | Xac suat | Anh huong | Severity | Ke hoach giam thieu | Trigger canh bao |
|--------|----------|-----------|----------|---------------------|------------------|
| CPMess tang >50% vs target | Cao | Cao | **CRITICAL** | Chuan bi 5 creative du phong, giam spend + chuyen organic | CPMess > target + 30% sau 3 ngay |
| Creative khong hieu qua | Cao | Cao | **CRITICAL** | A/B test tu ngay 1, 3–5 creative moi/tuan | CTR < 1% sau 2 ngay |
| Landing page conv rate thap | Trung binh | Cao | **HIGH** | Test A/B headline + CTA, heatmap | Conv rate < 10% sau 1 tuan |
| UGC giao tre | Trung binh | Trung binh | **MEDIUM** | Brief som, co noi dung backup | Chua nhan UGC D-3 |
| Doi thu chay deal cung luc | Thap | Cao | **HIGH** | Tang USP messaging, khong canh tranh gia | Phat hien doi thu ads cung thoi diem |
| Phan hoi tieu cuc | Thap | Rat cao | **CRITICAL** | Crisis protocol: phan hoi <2h, transparent, co template | Comment/review tieu cuc vuot 5 trong 1 ngay |
| Audience fatigue | Trung binh | Trung binh | **MEDIUM** | Rotate creative moi 5–7 ngay, expand audience | Frequency > 3, CTR giam 30% |
| Budget vuot ke hoach | Thap | Trung binh | **MEDIUM** | Cap daily budget, review chi phi hang ngay | Spend > 110% ke hoach |

### 9.2 Ke hoach B (Fallback)

| Tinh huong | Hanh dong |
|-----------|-----------|
| Ngan sach bi cat 50% | Chuyen 100% sang organic + UGC, chi chay retarget |
| Kenh chinh bi gian doan (bi ban ads, ...) | Chuyen ngan sach sang kenh phu trong 24h |
| Khong dat KPI giua chien dich | Hop khan, re-brief creative, thu hep audience |

<!-- #/SECTION -->

<!-- #SECTION
id: skill_chaining
type: skill_chaining
priority: 2
modes: [all]
industries: [all]
tags: [auto_trigger, next_skills]
-->

## Auto-trigger cac skill lien quan

Khi brief hoan thanh, tu dong de xuat chay:

```
02-brief-chien-dich (HOAN THANH)
  |
  |-- [Tiep theo 1] 05-copy-quang-cao  → Viet copy ads dua tren core message
  |-- [Tiep theo 2] 04-script-video    → Viet script dua tren creative direction
  |-- [Tiep theo 3] 01-lich-noi-dung   → Len lich dang bai dua tren timeline + kenh
  |-- [Tiep theo 4] 06-brief-ugc-egc   → Brief cho UGC creators dua tren deliverables
```

<!-- #/SECTION -->

<!-- #SECTION
id: quality_checklist
type: quality_checklist
priority: 1
modes: [all]
industries: [all]
tags: [checklist, quality_gate, final_review]
-->

## Checklist chat luong

Truoc khi giao brief, kiem tra:

- [ ] Du 10 phan (Context, Objectives, Target, Core Message, **Offer**, Creative Direction, Channel, Timeline, Deliverables, Risks)
- [ ] Muc tieu SMART — cu the, do duoc, co deadline
- [ ] Insight da qua 5 tieu chi validation — khong phai observation
- [ ] Core message co 3 tang: tagline + key message + supporting
- [ ] Offer co gia ro, thoi han ro, CTA cu the — khong de "lien he de biet them"
- [ ] Co it nhat 1 urgency/scarcity element trong offer
- [ ] Creative direction co Do's va Don'ts ro rang
- [ ] Tong % ngan sach cac phase = 100%
- [ ] % phan bo phu hop loai chien dich (Flash sale: tap trung Bung manh / Product launch: Teasing dai / Seasonal: 4 phase can bang)
- [ ] Timeline co milestone review cu the (D+3, D+7, D+14)
- [ ] RACI ro rang — moi deliverable co R va A
- [ ] Rui ro co it nhat 5 muc, moi muc co severity + trigger canh bao
- [ ] Co ke hoach B (fallback) cho it nhat 3 tinh huong
- [ ] Benchmark su dung so lieu Vietnam 2025–2026
- [ ] Tone of voice nhat quan voi thuong hieu
- [ ] Tat ca deadline kha thi — khong bi chen nhau

<!-- #/SECTION -->
