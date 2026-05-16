---
skill_id: "01-lich-noi-dung"
name: "Lich Noi Dung"
description: Lich noi dung thang — len lich dang bai da kenh voi ti le pheu, content pillar, repurposing matrix, va scoring tieu chi.
agent: "content-producer"
metadata:
  version: 2.2.0
  category: content
triggers:
  - "lich noi dung"
  - "len lich dang bai"
  - "ke hoach noi dung thang"
  - "content calendar"
  - "lich dang"
output: File .md gom lich noi dung hang tuan co day du cot — ngay, kenh, dinh dang, tang pheu, pillar, CTA, nguoi thuc hien, trang thai
related:
  - 00-ke-hoach-mkt
  - 04-script-video
  - 05-copy-quang-cao
  - 06-brief-ugc-egc
  - 09-insight-khach-hang
  - 15-social-listening
  - references/hook-formulas-vn
context_requirements:
  required: []
  optional:
    - industry        # co → dung vi du Content Matrix dung nganh, skip hoi nganh
    - active_channels # co → skip cau hoi kenh
    - source_type_mix # co → dung luon, khong hoi lai
    - team_size       # co → tu dong ap template phu hop (1 nguoi / 2-3 / 4+)
---

# Lich Noi Dung

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

- `industry` co → dung vi du Content Matrix dung nganh, skip cau hoi nganh
- `active_channels` co → skip Buoc 2 cau 1 (kenh dang co)
- `source_type_mix` co → dung luon, khong quyet dinh lai
- `team_size` co → tu dong chon template (1 nguoi / 2–3 / 4+), skip Buoc 3

<!-- #/SECTION -->

---

<!-- #SECTION
id: data_collection
type: data_collection
priority: 1
modes: [all]
industries: [all]
tags: [questions, channels, objectives, team_size, resources]
-->

### Buoc 2 — Hoi nhung gi chua co trong session_context (toi da 3 cau)

1. **Kenh dang co?** (neu chua co trong session_context) — TikTok / FB / IG / Zalo / Email / Blog, so follower hien tai
2. **Muc tieu thang nay?** — Tang follower / tang mess / tang don / ra mat san pham / chien dich dac biet?
3. **Nguon luc content?** — May nguoi lam content? Co quay video duoc khong? Co UGC/testimonial san khong?

### Buoc 3 — Xac dinh nguon luc thuc te

> Skip neu `team_size` va `team_roles` da co trong session_context.

Hoi 1 cau:
> "Team content cua ban co bao nhieu nguoi, va vai tro cua tung nguoi la gi?"
> Vi du: "2 nguoi — 1 quay/dung video, 1 viet bai + chay ads"

**Logic tinh tu dong sau khi co so nguoi:**

| Bien | Cong thuc | Vi du (3 nguoi) |
|------|-----------|----------------|
| So kenh uu tien | `min(so_nguoi + 1, 5)` | 4 kenh |
| So bai / tuan | `so_nguoi × 3` den `so_nguoi × 4` | 9–12 bai |
| Nguoi thuc hien | Dien ten that vao cot "Nguoi TH" | Anh A, Chi B, Em C |

> Khong ap dung tier co dinh. Moi team co cau hinh khac nhau — dieu chinh theo vai tro thuc te.

<!-- #/SECTION -->

---

<!-- #SECTION
id: logic_funnel_principles
type: logic
priority: 2
modes: [all]
industries: [all]
tags: [funnel, content_pillar, source_type_mix, distribution]
-->

## Nguyen tac xay lich noi dung

### 1. Quy tac phan bo pheu (Funnel Distribution)

| Tang pheu | Ti le | Muc dich | Loai noi dung |
|-----------|-------|----------|--------------|
| TOFU (Nhan biet) | 40% | Thu hut nguoi moi | Trend, tips, POV, behind scenes, cham noi dau |
| MOFU (Can nhac) | 35% | Xay trust, thuyet phuc | Case study, review, so sanh, quy trinh, FAQ |
| BOFU (Chuyen doi) | 15% | Chot don | Offer, deal, countdown, retarget, livestream |
| Retention | 10% | Giu khach cu | VIP content, referral, community, re-engage |

> Tham khao chi tiet goc do noi dung tai `references/content-angles.md`.

### 2. Content Pillar Balance

Moi thuong hieu can 3–5 pillar. Kiem tra balance moi tuan.

| Pillar | Ti le khuyen nghi | Kiem tra tuan nay |
|--------|-------------------|-------------------|
| Giao duc (Education) | 30–35% | [so bai] / [tong bai] = [%] |
| Cam hung (Inspiration) | 20–25% | [so bai] / [tong bai] = [%] |
| Giai tri (Entertainment) | 20–25% | [so bai] / [tong bai] = [%] |
| Ban hang (Selling) | 10–15% | [so bai] / [tong bai] = [%] |
| Cong dong (Community) | 5–10% | [so bai] / [tong bai] = [%] |

**Quy tac:** Neu 1 pillar lech qua 10% so voi khuyen nghi → dieu chinh tuan sau.

### 3. Source Type Mix

> Ti le duoi day doc tu `session_context.source_type_mix` (da xac dinh o Skill 00).
> Neu chua co → dung bang mac dinh, KHONG tu quyet dinh lai.

| Loai noi dung | Mac dinh (chua co Skill 00) | Mo ta |
|---------------|-----------------------------|-------|
| FGC (Founder Generated) | 20% | Thuong lai tu Skill 00 theo founder availability |
| Brand Content | 40% | Noi dung thuong hieu chinh thuc |
| UGC (User Generated) | 25% | Khach hang tu tao — social proof |
| EGC (Employee Generated) | 15% | Nhan vien chia se — authentic |

<!-- #/SECTION -->

---

<!-- #SECTION
id: reference_content_matrix
type: reference
priority: 2
modes: [all]
industries: [all]
tags: [content_matrix, ideas, formats, justin_welsh]
-->

## Content Matrix — Y tuong noi dung tu dong

> Ap dung tu `social-media-skills/content-matrix` (Justin Welsh method) — adapt cho VN.

Ghep **content pillar** cua brand voi **8 dinh dang** de tao 24–40 y tuong cung luc.

### 8 dinh dang content

| # | Dinh dang | Mo ta | Vi du |
|---|-----------|-------|-------|
| 1 | **Huong dan** | Day 1 ky nang cu the, buoc-buoc | "3 buoc setup Pixel Meta dung chuan" |
| 2 | **Truyen cam hung** | Cau chuyen thanh cong, vuot kho | "Tu 0 follower den 50K trong 6 thang — chuyen that" |
| 3 | **Phan tich** | Giai thich tai sao, co che hoat dong | "Tai sao ads ban dat ma khong co don? Root cause analysis" |
| 4 | **Nguoc doi** | Thach thuc niem tin pho bien | "Chay ads nhieu hon KHONG phai la cach tang don" |
| 5 | **Quan sat** | Xu huong an, dieu it ai de y | "Dieu dang xay ra tren TikTok Shop ma it ai biet" |
| 6 | **So sanh X vs Y** | 2 cong cu/cach tiep can/chien luoc | "Meta Ads vs TikTok Ads: nganh nao chon gi?" |
| 7 | **Hien tai vs Tuong lai** | Du bao, xu huong sap den | "Marketing 2025 vs 2026: 5 thay doi lon" |
| 8 | **Danh sach** | Tips, sai lam, bai hoc, cong cu | "7 sai lam chay ads pho bien nhat cua SME Viet" |

### Vi du theo nganh (doc tu session_context.industry)

| Nganh | Vi du Huong dan | Vi du Nguoc doi | Vi du Danh sach |
|-------|----------------|----------------|----------------|
| `spa` | "Quy trinh cham soc da mun 4 buoc tai nha" | "Dung kem duong NHIEU hon khong phai tot cho da" | "5 loi khach hay mac khi tri mun" |
| `clinic` | "Truoc va sau Botox: nhung dieu can biet" | "Tham my khong xam lan KHONG an toan hon ban nghi" | "7 cau hoi nen hoi bac si truoc khi lam dep" |
| `fnb` | "Bi quyet lam banh khong bi xep" | "Mon ngon khong phai luc nao cung can nhieu nguyen lieu dat" | "5 quan ca phe co goc check-in dep o Ha Noi" |
| `fitness` | "Bai tap 20 phut cho nguoi ban" | "Tap nhieu chua chac da giam can" | "6 sai lam khi tap gym lan dau" |
| `education` | "Cach hoc tieng Anh 30 phut/ngay con nho duoc" | "Hoc nhieu khoa khong bang hoc dung 1 khoa" | "4 app hoc tieng Anh mien phi tot nhat 2025" |
| `ecommerce` | "Cach dong hang dep de khach review" | "Free ship khong phai luc nao cung lam tang don" | "3 ly do khach them hang vao gio roi bo" |
| `saas` | "Setup automation email trong 10 phut" | "Phan mem dat tien chua chac tot hon phan mem re" | "5 tinh nang it ai biet cua [ten tool]" |

### Template content matrix

```
| Pillar \ Dinh dang | Huong dan | Truyen cam hung | Phan tich | Nguoc doi | Quan sat | X vs Y | Hien tai vs TL | Danh sach |
|---------------------|----------|-----------------|-----------|-----------|---------|--------|----------------|-----------|
| [Pillar 1] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] |
| [Pillar 2] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] |
| [Pillar 3] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] | [Y tuong] |
```

> **Tip:** Chay content matrix 1 lan/thang → co san 24+ y tuong.

<!-- #/SECTION -->

---

<!-- #SECTION
id: reference_scoring
type: reference
priority: 2
modes: [all]
industries: [all]
tags: [scoring, quality, hook, cta, visual]
-->

## AI Content Scoring

Cham diem moi content truoc khi dang (thang diem 10):

| Tieu chi | Trong so | Diem (1–10) | Diem x Trong so |
|----------|----------|-------------|-----------------|
| **Hook** (3s dau co giu chan khong?) | 25% | [diem] | |
| **Relevance** (dung insight khach hang?) | 20% | [diem] | |
| **Value** (khach nhan duoc gi?) | 20% | [diem] | |
| **CTA** (ro rang, de hanh dong?) | 15% | [diem] | |
| **Visual** (chat luong hinh/video?) | 10% | [diem] | |
| **Brand consistency** (dung tone, mau sac?) | 10% | [diem] | |
| **Tong** | **100%** | | **[tong]/10** |

**Nguong dang:**
- 8–10: Dang ngay, co the boost paid
- 6–7.9: Dang duoc, can chinh sua nhe
- 4–5.9: Can viet lai hook hoac CTA
- <4: Khong dang, lam lai

<!-- #/SECTION -->

---

<!-- #SECTION
id: reference_posting_time
type: reference
priority: 2
modes: [all]
industries: [all]
tags: [posting_time, golden_hours, vietnam, seasonal]
-->

## Thoi gian dang toi uu — Vietnam

### Gio vang theo kenh (UTC+7)

| Kenh | Thu 2–6 | Thu 7 | Chu Nhat | Ghi chu |
|------|---------|-------|----------|---------|
| **TikTok** | 6:30–8:00, 11:30–13:00, 19:00–21:30 | 9:00–11:00, 19:00–22:00 | 10:00–12:00, 19:00–22:00 | Peak: 20:00–21:00 |
| **Facebook** | 7:00–8:30, 11:00–13:00, 19:00–21:00 | 8:00–10:00, 19:00–21:00 | 9:00–11:00, 19:00–21:00 | Peak: 12:00, 20:00 |
| **Instagram** | 7:00–9:00, 12:00–14:00, 18:00–20:00 | 9:00–11:00, 18:00–20:00 | 10:00–12:00 | Peak: 12:00–13:00 |
| **Zalo OA** | 8:00–9:00, 17:00–18:30 | 9:00–10:00 | Khong gui | Gioi han 2–3 broadcast/tuan |
| **Email** | 8:00–9:30, 14:00–15:00 | Khong gui | Khong gui | Thu 3 + Thu 5 tot nhat |
| **YouTube** | 17:00–20:00 | 14:00–17:00 | 14:00–17:00 | Video dai — cuoi tuan tot hon |

### Mua cao diem Vietnam

| Thoi diem | Ghi chu | Dieu chinh |
|-----------|---------|------------|
| Tet Nguyen Dan (T1–T2) | CPM tang 30–50%, engagement tang | Tang content tru Tet, len lich truoc 2 tuan |
| 8/3 + 20/10 | Nganh Beauty, F&B tang manh | Chay chien dich truoc 1 tuan |
| Black Friday (T11) | E-commerce, courses | CPM tang 20–30% |
| Back to school (T8–T9) | Education, edtech | Content giao duc tang |
| He (T6–T8) | F&B, du lich, giai tri | Tang content giai tri, lifestyle |

<!-- #/SECTION -->

---

<!-- #SECTION
id: template_schedule
type: template
priority: 2
modes: [all]
industries: [all]
tags: [schedule, weekly, calendar, balance_check]
-->

## Template lich noi dung tuan

> Template duoi day la 1 khung duy nhat — so hang, so kenh, va cot "Nguoi TH" tu dong dieu chinh theo so nguoi va vai tro user da cung cap o Buoc 3.

### Tuan [so] — [ngay bat dau] den [ngay ket thuc]

| Ngay | Thu | Kenh | Gio dang | Dinh dang | Tang pheu | Pillar | Chu de | Hook / Headline | CTA | Source type | Nguoi TH | Trang thai |
|------|-----|------|----------|-----------|-----------|--------|--------|-----------------|-----|-------------|----------|------------|
| [ngay] | T2 | [kenh] | [gio] | [dinh dang] | TOFU | Giao duc | [chu de] | [hook 3s] | [CTA] | [loai] | [ten] | Draft |
| [ngay] | T2 | [kenh] | [gio] | [dinh dang] | MOFU | Cam hung | [chu de] | [headline] | [CTA] | [loai] | [ten] | |
| [ngay] | T3 | [kenh] | [gio] | [dinh dang] | TOFU | Giai tri | [chu de] | [hook] | [CTA] | [loai] | [ten] | |
| [ngay] | T4 | [kenh] | [gio] | [dinh dang] | MOFU | Giao duc | [chu de] | [hook] | [CTA] | [loai] | [ten] | |
| [ngay] | T5 | [kenh] | [gio] | [dinh dang] | BOFU | Ban hang | [chu de] | [headline] | [CTA] | [loai] | [ten] | |
| [ngay] | T6 | [kenh] | [gio] | [dinh dang] | TOFU | Giai tri | [chu de] | [hook] | [CTA] | [loai] | [ten] | |
| [ngay] | T7 | [kenh] | [gio] | [dinh dang] | MOFU | Cam hung | [chu de] | [hook] | [CTA] | [loai] | [ten] | |
| [ngay] | CN | Zalo OA | 09:00 | Broadcast | Retention | Cong dong | [chu de] | [tieu de] | [CTA] | Brand | [ten] | |

> Them hoac bot hang tuy theo `so_nguoi × 3–4 bai/tuan`. Dien ten that vao "Nguoi TH" — khong de "[ten]" chung.

### Kiem tra balance tuan

| Hang muc | Ke hoach | Thuc te | Dung ti le? |
|----------|----------|---------|-------------|
| **Pheu:** TOFU | 40% | [so] | Co / Khong |
| **Pheu:** MOFU | 35% | [so] | |
| **Pheu:** BOFU | 15% | [so] | |
| **Pheu:** Retention | 10% | [so] | |
| **Pillar:** Giao duc | 30–35% | [so] | |
| **Pillar:** Cam hung | 20–25% | [so] | |
| **Pillar:** Giai tri | 20–25% | [so] | |
| **Pillar:** Ban hang | 10–15% | [so] | |
| **Pillar:** Cong dong | 5–10% | [so] | |

<!-- #/SECTION -->

---

<!-- #SECTION
id: template_repurposing
type: template
priority: 3
modes: [full]
industries: [all]
tags: [repurposing, 1to7, multi_format, distribution]
-->

## Content Repurposing Matrix

Quy tac 1:7 — moi noi dung goc tao ra it nhat 7 phien ban:

| STT | Noi dung goc | Phien ban | Kenh muc tieu | Thoi luong / Do dai | Thoi gian san xuat |
|-----|-------------|-----------|---------------|---------------------|--------------------|
| 1 | Video dai 3–5 phut | Nguyen ban | YouTube | 3–5 phut | 2–4h |
| 2 | | Clip ngan #1 (hook) | TikTok | 15–30s | 15 phut |
| 3 | | Clip ngan #2 (tip chinh) | Reels | 15–30s | 15 phut |
| 4 | | Clip ngan #3 (ket qua) | TikTok | 15–30s | 15 phut |
| 5 | | Carousel 5–7 slide | Facebook, Instagram | 5–7 anh | 30 phut |
| 6 | | Bai blog SEO | Website | 800–1500 tu | 1–2h |
| 7 | | Email newsletter | Email list | 300–500 tu | 30 phut |
| 8 | | 3 quote card | Story, Threads | 1 anh/card | 15 phut |
| 9 | | Audio snippet | Zalo OA voice note | 1–2 phut | 10 phut |

### Quy trinh repurpose

```
Ngay 1: Quay/viet noi dung goc
Ngay 1: Cat clip ngan (3 clip, 45 phut)
Ngay 2: Lam carousel + quote card (45 phut)
Ngay 2: Viet blog tu noi dung goc (1–2h)
Ngay 3: Gui email newsletter (30 phut)
Ngay 3–7: Dang rai cac phien ban theo lich
```

<!-- #/SECTION -->

---

<!-- #SECTION
id: reference_frequency
type: reference
priority: 3
modes: [full]
industries: [all]
tags: [frequency, posting_rate, channel_limits]
-->

## Tan suat dang khuyen nghi theo kenh

| Kenh | Toi thieu | Khuyen nghi | Toi uu | Ghi chu |
|------|-----------|-------------|--------|---------|
| TikTok | 3 video/tuan | 5–7 video/tuan | 1–2 video/ngay | Nhieu hon = nhieu data test |
| Facebook | 3 post/tuan | 4–5 post/tuan | 1 post/ngay | Mix video + carousel + text |
| Instagram | 3 post/tuan | 4–5 post/tuan | 1 post/ngay | Reels uu tien |
| Zalo OA | 1 broadcast/tuan | 2–3 broadcast/tuan | 3 broadcast/tuan | Qua 3 → unfollow tang |
| Email | 1 email/tuan | 2 email/tuan | 2 email/tuan | Qua nhieu → spam |
| YouTube | 1 video/tuan | 1–2 video/tuan | 2 video/tuan | Chat luong > so luong |
| Blog/SEO | 1 bai/tuan | 2–4 bai/tuan | 1 bai/ngay | SEO can thoi gian |

<!-- #/SECTION -->

---

<!-- #SECTION
id: skill_chaining
type: logic
priority: 2
modes: [all]
industries: [all]
tags: [chaining, cross_reference, related_skills]
-->

## Cross-reference

| Khi can | Goi skill |
|---------|-----------|
| Script cho video TikTok trong lich | `04-script-video` |
| Copy cho bai dang Facebook | `05-copy-quang-cao` |
| Brief cho UGC/EGC trong lich | `06-brief-ugc-egc` |
| Insight de chon chu de | `09-insight-khach-hang` |
| Ke hoach tong the (lich nam trong do) | `00-ke-hoach-mkt` |

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

Truoc khi giao lich noi dung, kiem tra:

- [ ] So bai/tuan = so nguoi × 3–4 (tinh tu Buoc 3)
- [ ] So kenh = min(so nguoi + 1, 5) — khong ep them kenh khi khong co nguoi lam
- [ ] Cot "Nguoi TH" dien ten that — khong de trong hoac "[ten]" chung
- [ ] Ti le pheu cong dung: TOFU 40% + MOFU 35% + BOFU 15% + Retention 10%
- [ ] Content pillar balance — khong lech qua 10%
- [ ] Source type mix doc tu session_context / Skill 00 — khong tu quyet dinh lai
- [ ] Vi du Content Matrix dung nganh cua khach — khong dung vi du marketing chung
- [ ] Moi bai co hook/headline cu the — khong de trong
- [ ] Moi bai co CTA ro rang
- [ ] Gio dang theo gio vang Vietnam (UTC+7)
- [ ] Khong dang 2 bai cung kenh cung gio
- [ ] Content repurposing — moi noi dung goc co it nhat 3 phien ban
- [ ] Zalo OA khong qua 3 broadcast/tuan
- [ ] Email khong qua 2 email/tuan (tru chuoi welcome)
- [ ] AI Content Score >= 6 cho moi bai

<!-- #/SECTION -->
