---
name: 04-script-video
description: Viet script video ngan cho TikTok, Reels, YouTube Shorts — 2 ban A/B, hook, CTA, huong dan quay, caption, hashtag, viral score. Ho tro ca mode viet san va mode tu viet co huong dan.
skill_id: "04-script-video"
agent: "content-producer"
metadata:
  version: 3.0.0
  category: content
triggers:
  - "viet script"
  - "script TikTok"
  - "kich ban video"
  - "hook TikTok"
  - "script UGC"
  - "script Reels"
  - "kich ban quay"
  - "viet script personal brand"
  - "script ca nhan TikTok"
  - "story video"
  - "viet video LinkedIn ca nhan"
output: Script A/B hoan chinh (loi thoai that, khong placeholder) hoac huong dan tu viet tung buoc — kem timestamp, huong dan quay, caption, hashtag, viral score, QA score
context_requirements:
  required: []
  optional:
    - industry
    - target_audience
    - business_name
    - mode          # "product" | "personal_brand"
---

# Script Video

<!-- #SECTION
id: context_intake
type: context_intake
priority: 1
modes: [all]
industries: [all]
tags: [session_context, mode, product, personal_brand]
-->

## Buoc 0 — Xac dinh Mode

Doc tu `session_context.mode`:

| session_context.mode | Mode ap dung |
|---------------------|-------------|
| `product` | **Mode A** — ban san pham / conversion |
| `personal_brand` | **Mode B** — xay authority / trust |
| Ca hai | Hoi 1 cau: "Ban dang viet video ban san pham hay xay personal brand?" |
| Khong co | Mac dinh **Mode A** |

### Khac biet cot loi — Mode A vs Mode B

| Yeu to | Mode A (San pham) | Mode B (Personal Brand) |
|--------|-------------------|------------------------|
| Muc tieu | Sell / Convert | Build trust + Authority |
| Hook | Pain point san pham | Trai nghiem ca nhan / Industry insight |
| CTA | "Inbox/Comment" mua hang | Soft CTA: "Ban nghi sao?", "Follow them" |
| Story | Customer story | Founder/Coach story (chinh ban) |
| Trust signal | Review, USP | Track record ca nhan, contrarian view |
| Tone | Selling-focused | Conversational, vulnerable, authoritative |

<!-- #/SECTION -->

<!-- #SECTION
id: data_collection
type: data_collection
priority: 1
modes: [all]
industries: [all]
tags: [intake, adaptive, coaching_question, platform, funnel]
-->

## Thu thap thong tin

### Buoc 1 — Lay tu session_context

Neu da co → **khong hoi lai:**
- `industry`, `target_audience` → bo Q1 + Q3
- `mode` → da xu ly o Buoc 0

### Buoc 2 — Hoi nhung gi con thieu (toi da 4 cau)

1. **San pham / dich vu gi?** USP chinh, gia (neu co) — *skip neu session_context da co*
2. **Nen tang + thoi luong mong muon?** TikTok / Reels / YouTube Shorts (15 / 30 / 45 / 60s). Khong chon → mac dinh TikTok 30s.
3. **Doi tuong muc tieu?** Gioi tinh, do tuoi, noi dau chinh — *skip neu session_context da co*
4. **Goc do noi dung?** TOFU / MOFU / BOFU. Khong chon → mac dinh TOFU.

### Buoc 3 — Cau hoi coaching (bat buoc, hoi sau khi du thong tin)

> *"Ban muon minh ho tro viet script san de dung ngay, hay muon tu viet voi su huong dan tung buoc? Nhieu ban chon cach 2 vi script tu viet thuong hieu qua hon — ban hieu khach cua ban hon minh, nen hook va loi thoai se tu nhien va dung tone hon. Nhung neu ban dang ban hoac can dung ngay, minh viet san cung duoc."*

| Chon | Hanh dong |
|------|-----------|
| **Viet san** | Claude viet full 2 ban A/B — loi thoai that, khong placeholder |
| **Tu viet co huong dan** | Claude dan tung buoc: chon hook → viet van de → viet giai phap → review tung phan |

<!-- #/SECTION -->

<!-- #SECTION
id: hook_framework
type: logic
priority: 1
modes: [all]
industries: [all]
tags: [hook, 6_formulas, negative_examples, rules]
-->

## Nguyen tac Hook

### 6 cong thuc hook (3 giay dau)

Moi hook gom **2 dong**: Dong 1 (mo) toi da 50 ky tu, Dong 2 (twist) toi da 50 ky tu.

| # | Kieu hook | Cong thuc | Vi du VN |
|---|-----------|-----------|----------|
| 1 | **Con so dan dau** | Mo bang so lieu cu the, bat ngo | "97% chu spa dang lam sai buoc nay" / "Va no ton 200 trieu/nam" |
| 2 | **Nguoc doi** | Noi dieu pho bien roi lat nguoc | "Chay ads nhieu hon khong giup ban" / "Toi giam budget 50% va tang don 3x" |
| 3 | **Bien doi ca nhan** | Truoc vs Sau voi con so cu the | "6 thang truoc toi khong co khach" / "Bay gio 40 booking/tuan — day la cach" |
| 4 | **Muon uy tin** | Nhac ten thuong hieu, nguoi noi tieng, cong cu | "ChatGPT vua thay doi cach toi lam MKT" / "Va 90% marketer chua biet" |
| 5 | **Thu nhan** | Chia se sai lam, mat mat | "Toi da mat 500 trieu chay ads sai" / "Day la bai hoc dat gia nhat" |
| 6 | **Du bao tuong lai** | Dieu sap thay doi ma it nguoi biet | "TikTok Shop sap thay doi hoan toan" / "Ai khong chuan bi se mat thi phan" |

**Quy tac chon hook theo tang pheu:**
- TOFU: Uu tien hook 1, 2, 6
- MOFU: Uu tien hook 3, 4
- BOFU: Uu tien hook 5, 3

**Quy tac viet hook:**
- **Khong bao gio mo bang "Toi"** — dung "Ban", "Day", con so, hoac ten nguoi/brand
- Dong 1 tao curiosity gap → Dong 2 tang stakes hoac lat nguoc
- Dem ky tu: 50 char/dong la toi da — tren mobile nhieu hon se cat

### Hook xau vs Hook tot (Negative Examples)

| Hook xau | Tai sao sai | Hook tot thay the |
|----------|------------|-------------------|
| "Xin chao moi nguoi, hom nay minh se chia se ve skincare..." | Mo bang "Xin chao", khong co tension, khong ly do o lai | "Da ban len mun sau 30 tuoi? Day la ly do — va cach fix trong 2 tuan" |
| "San pham cua chung toi rat tot, duoc nhieu nguoi tin dung" | Khong co hook, tu khen, chung chung | "97% khach cua spa minh noi ho so kem duong do 1 buoc sai nay" |
| "Hom nay minh muon gioi thieu mot san pham moi" | Chay va, khong gay to mo, khong van de | "Dung them kem duong den khi xem clip nay" |
| "Co biet khong, skincare rat quan trong..." | Cau hoi nhat, khong specific, khong gap | "Ban dang pha hong da bang 1 buoc sai ma 80% phu nu mac phai" |

<!-- #/SECTION -->

<!-- #SECTION
id: hook_by_industry
type: reference
priority: 2
modes: [all]
industries: [all]
tags: [hook, industry, spa, clinic, fnb, fitness, education, ecommerce]
-->

### Hook theo nganh (tu session_context.industry)

| Nganh | Hook manh nhat | Vi du |
|-------|---------------|-------|
| `spa` | Ket qua truoc/sau + noi dau cu the | "Da sau 2 tuan — khach cua minh noi gi sau lieu trinh nay" |
| `clinic` | Con so + bac si xac nhan | "Bac si da canh bao toi ve dieu nay — 70% khach lam sai" |
| `fnb` | Nguoc doi + mon an | "Pho ngon nhat Ha Noi khong phai o quan noi tieng nhat" |
| `fitness` | Bien doi ca nhan + con so | "Giam 8kg trong 60 ngay — khong nhin gio vao bung toi" |
| `education` | Thu nhan + bai hoc | "Toi da hoc sai 2 nam — day la dieu khong ai noi voi ban truoc" |
| `ecommerce` | Con so + so sanh | "San pham nay ban 500 don/ngay — day la ly do" |

<!-- #/SECTION -->

<!-- #SECTION
id: script_structure
type: template
priority: 1
modes: [all]
industries: [all]
tags: [tofu, mofu, bofu, timestamp, structure]
-->

## Cau truc Script theo Tang Pheu

### TOFU — Thu hut nguoi moi (mac dinh)

| Timestamp (30s) | Phan | Noi dung | Ti le |
|-----------------|------|----------|-------|
| [0–3s] | **Hook** | Gay to mo, giu nguoi o lai. Khong gioi thieu ban than. | 10% |
| [3–10s] | **Van de / Cau chuyen** | Dien ta noi dau — nguoi xem thay minh trong do | 25% |
| [10–20s] | **Giai phap / Gia tri** | San pham/dich vu nhu cach giai quyet van de | 30% |
| [20–27s] | **Bang chung** | Ket qua, review, so lieu, truoc/sau | 25% |
| [27–30s] | **CTA** | Hanh dong cu the: "Nhan tin ngay", "Link bio", "Comment de nhan" | 10% |

### MOFU — Thuyet phuc nguoi dang can nhac

| Timestamp (30s) | Phan | Noi dung |
|-----------------|------|----------|
| [0–3s] | **Hook** | Ket qua cu the hoac so lieu tin cay |
| [3–8s] | **Credibility** | Ai noi, bao nhieu nguoi da lam, ket qua do duoc |
| [8–22s] | **So sanh / Ly do chon** | Tai sao chon ban thay vi doi thu — cu the, khong chung chung |
| [22–27s] | **Social proof** | Review that, ten khach cu the (neu duoc phep) |
| [27–30s] | **CTA** | "Dat lich ngay", "Inbox de hoi gia", "Comment [tu khoa]" |

### BOFU — Chot don

| Timestamp (30s) | Phan | Noi dung |
|-----------------|------|----------|
| [0–3s] | **Hook** | Offer hoac urgency ngay tu dau |
| [3–10s] | **Offer cu the** | Gia, giam bao nhieu, con bao nhieu slot/san pham |
| [10–22s] | **Remove objections** | Giai quyet lo ngai cuoi cung: bao hanh, hoan tien, ket qua |
| [22–27s] | **Social proof nhanh** | "300 khach da lam tuan nay" / truoc-sau |
| [27–30s] | **CTA khan cap** | "Chi con X slot", "Uu dai het [ngay]", "Inbox NGAY" |

### Dieu chinh theo thoi luong

| Thoi luong | Hook | Van de/Credibility | Giai phap/Offer | Bang chung | CTA |
|------------|------|-------------------|----------------|------------|-----|
| 15s | 0–2s | 2–5s | 5–10s | 10–13s | 13–15s |
| 30s | 0–3s | 3–10s | 10–20s | 20–27s | 27–30s |
| 45s | 0–3s | 3–12s | 12–28s | 28–40s | 40–45s |
| 60s | 0–3s | 3–15s | 15–35s | 35–53s | 53–60s |

<!-- #/SECTION -->

<!-- #SECTION
id: writing_rules
type: logic
priority: 2
modes: [all]
industries: [all]
tags: [writing_rules, reverse_engineer, viral_pattern]
-->

## Quy tac Viet Script

1. **1 y chinh duy nhat** — khong noi 2 dieu trong 1 video
2. **Ngon ngu noi** — viet nhu dang noi chuyen, khong viet van
3. **Cau ngan** — toi da 15 tu/cau. Cau dai = nguoi xem luot
4. **Transition ro rang** — ghi chi dan chuyen canh trong script
5. **Text overlay bat buoc** — ghi ro noi dung text hien tren man hinh
6. **Khong dung nhac co ban quyen** — chi dung nhac trending hoac royalty-free
7. **Toi da 2 diem chinh** — 3 diem = qua nhieu, nguoi xem khong nho
8. **Khong ket luan ho** — de so lieu/su that tu noi len

### Reverse-engineer video viral

Khi user cung cap link video tham khao:

1. **Phan tich cau truc**: Hook may giay? So diem chinh? CTA kieu gi?
2. **Rut ky thuat**: Goc quay, nhip cat, text overlay style, am nhac
3. **Adapt cho brand**: Giu cau truc + ky thuat, thay bang san pham/dich vu cua user
4. **Khong copy loi thoai** — chi hoc pattern, viet lai bang giong van brand

<!-- #/SECTION -->

<!-- #SECTION
id: personal_brand_mode
type: reference
priority: 3
modes: [full]
industries: [all]
tags: [personal_brand, mode_b, authority, soft_cta, qa_score]
-->

## Personal Brand Mode (Mode B)

### 4 hook personal brand

| # | Loai hook | Cong thuc | Vi du VN |
|---|-----------|-----------|---------|
| 1 | **Personal confession** | Mo dau bang loi sai / that bai cua chinh ban | "Toi da mat 200 trieu vi sai 1 quyet dinh tuan truoc. Day la bai hoc." |
| 2 | **Contrarian take** | Phan bac dieu da so tin | "Moi nguoi noi nen scale nhanh. Toi da nay scale cham — va day la ly do." |
| 3 | **Behind the scene** | Cho thay phan it nguoi thay | "Toi 5h sang khi build startup nay. Day la what no one tells you." |
| 4 | **Industry truth** | Kien thuc nganh khong ai noi | "Sau 10 nam lam tu van, day la 3 dieu agency khong bao gio noi voi ban." |

### Cau truc script Personal Brand 30s

| Timestamp | Noi dung | Muc tieu |
|-----------|----------|---------|
| [0–3s] | Hook personal brand (1 trong 4 loai tren) | Stop scroll bang ca nhan |
| [3–10s] | Setup: ai noi, hoan canh | Establish credibility |
| [10–22s] | Insight chinh / story turning point | Deliver value |
| [22–28s] | Lesson hoc duoc / framework | Pay off the hook |
| [28–30s] | Soft CTA: "Ban tung gap chua?", "Follow them" | Build community — KHONG sell |

### QA Score Personal Brand (10 tieu chi × 10 diem)

1. Authenticity (co bua dat khong?)
2. Personal vulnerability (co share that bai/loi sai?)
3. Industry insight (co kien thuc moi nguoi can?)
4. Hook personal angle (1 trong 4 loai tren)
5. Story arc clear (setup → turning point → lesson)
6. Brand voice consistency
7. Soft CTA (KHONG hard sell)
8. Disclosure neu dung AI avatar
9. Niche relevance
10. Repurpose-able (co the cat ra short clip?)

Score: 90+ Xuat sac / 70–89 Tot / 50–69 Can fix / <50 Lam lai

### Khi nao KHONG dung Personal Brand Mode

- Chi co product context → dung Mode A
- Video ads chay tien → dung skill 05
- Tutorial thuan tuy → Mode A van phu hop

<!-- #/SECTION -->

<!-- #SECTION
id: output_template
type: output_template
priority: 1
modes: [all]
industries: [all]
tags: [output, ab_test, script_format, comparison]
-->

## Output — Cau truc ket qua

### Thong tin chung

```
San pham / Dich vu: [ten]
Nen tang: [TikTok / Reels / YouTube Shorts]
Thoi luong: [Xs]
Tang pheu: [TOFU / MOFU / BOFU]
Doi tuong: [mo ta ngan]
Mode: [A — San pham / B — Personal Brand]
```

### Ban A — [Ten hook / Goc do]

| Timestamp | Loi thoai | Hinh anh / Hanh dong | Text overlay | Am thanh |
|-----------|-----------|---------------------|-------------|----------|
| [0–3s] | "[Hook — viet nguyen van, loi thoai that]" | [Mo ta canh quay: goc may, chu the, hanh dong] | [Text hien tren man hinh] | [Nhac nen / sound trending] |
| [3–10s] | "[Van de — viet nguyen van]" | [Chuyen canh cu the] | [Text overlay] | |
| [10–20s] | "[Giai phap — viet nguyen van]" | [Hanh dong: demo, B-roll, close-up] | [Text overlay] | |
| [20–27s] | "[Bang chung — viet nguyen van]" | [Truoc/sau, review, so lieu] | [Text ket qua] | |
| [27–30s] | "[CTA — viet nguyen van]" | [Tro tay, chi link] | "[CTA text lon]" | |

### Ban B — [Ten hook / Goc do khac]

*(Cung cau truc, khac hook va goc do)*

### So sanh 2 ban

| Yeu to | Ban A | Ban B |
|--------|-------|-------|
| Kieu hook | | |
| Cam xuc chinh | | |
| CTA | | |
| Do kho quay | De / Trung binh / Kho | De / Trung binh / Kho |
| Phu hop test | Cold audience | Warm audience |
| **Khuyen dung** | | |

<!-- #/SECTION -->

<!-- #SECTION
id: production_guide
type: reference
priority: 2
modes: [all]
industries: [all]
tags: [shooting, equipment, caption, hashtag, platform]
-->

## Huong dan Quay

### Thiet bi

| Hang muc | Khuyen dung | Thay the |
|----------|------------|---------|
| May quay | iPhone 13+ / Samsung S22+ | Dien thoai co 4K |
| Chan may | Tripod co kep dien thoai | Ke sach, tu do |
| Anh sang | Ring light 26cm hoac den softbox | Quay canh cua so buoi sang |
| Am thanh | Mic cai ao Boya BY-M1 | Mic tren dien thoai (phong yen tinh) |
| Edit | CapCut (free) | VN Editor, InShot |

### Phong cach quay theo loai noi dung

| Phong cach | Mo ta | Phu hop |
|------------|-------|---------|
| Talking head | Noi thang vao camera, close-up mat | Hook cau hoi, giao duc, review |
| POV | Camera = mat nguoi xem | Tinh huong, trai nghiem |
| B-roll + voiceover | Quay san pham/khong gian, ghep giong sau | Demo san pham, behind-the-scenes |
| Truoc/sau | Chia doi man hinh | Bang chung, ket qua |
| Green screen | Nen anh/video, nguoi noi phia truoc | Phan tich, binh luan, so sanh |

### Checklist truoc khi quay

- [ ] Tat thong bao dien thoai
- [ ] Lau camera
- [ ] Kiem tra anh sang — khong nguoc sang
- [ ] Test am thanh 5 giay roi nghe lai
- [ ] Ti le khung hinh 9:16 (doc)
- [ ] Dat may ngang tam mat hoac hoi cao hon
- [ ] Doc script 2 lan truoc khi quay

## Caption va Hashtag

### Caption

```
[Dong 1 — hook lai noi dung video, toi da 125 ky tu]
[Dong 2 — bo sung gia tri hoac context]
[Dong 3 — CTA: "Save lai de lam theo" / "Tag ban can biet"]
.
.
[Hashtag block]
```

### Hashtag theo nen tang

| Nen tang | So luong | Chien luoc |
|----------|---------|-----------|
| **TikTok** | 5–8 | 1–2 trending + 2–3 niche + 1 brand + 1–2 long-tail |
| **Reels** | 3–5 | Focus keyword nganh — it hon TikTok, chat luong hon so luong |
| **YouTube Shorts** | 2–3 | Hashtag it anh huong — uu tien title + description co keyword |

<!-- #/SECTION -->

<!-- #SECTION
id: scoring
type: reference
priority: 2
modes: [all]
industries: [all]
tags: [viral_score, qa_score, quality_gate]
-->

## Viral Score

| Yeu to | Tieu chi | Diem |
|--------|----------|------|
| Hook strength | 3s dau co gay to mo, co ly do o lai? | /5 |
| Save potential | Nguoi xem co muon luu lai? (tips, huong dan) | /5 |
| Share trigger | Co ly do chia se? (hai, dong cam, huu ich) | /5 |
| Completion pull | Co suspense/payoff keo xem het? | /5 |
| Comment bait | Co gi de binh luan? (cau hoi, tranh luan, tag ban) | /5 |

| Tong | Danh gia | Hanh dong |
|------|---------|----------|
| 20–25 | Tiem nang viral cao | Chay ngay, do budget ads |
| 15–19 | Kha | A/B test, theo doi 24h dau |
| 10–14 | Trung binh | Chinh lai hook hoac CTA |
| <10 | Yeu | Viet lai |

## QA Score — Mode A (San pham)

10 tieu chi × 10 diem. **Chi giao khi dat >= 85/100.**

| # | Tieu chi | 10 diem | 0 diem |
|---|----------|---------|--------|
| 1 | Hook trong 3s | Co hook ro, khong gioi thieu ban than | Mo bang "Xin chao, hom nay minh se..." |
| 2 | Hook <= 50 ky tu | Dong 1 ngan, dam, du nghia | Dong 1 dai, cat giua y |
| 3 | 1 y chinh duy nhat | Toan bo script phuc vu 1 message | Nhieu y lan man |
| 4 | Toi da 2 diem chinh | 2 diem ro rang, de nho | 3+ diem qua nhieu |
| 5 | Ngon ngu noi | Doc len tu nhien nhu dang noi chuyen | Viet van, cung nhac |
| 6 | Cau <= 15 tu | Moi cau ngan gon | Co cau dai >15 tu |
| 7 | CTA cu the | "Nhan tin ngay", "Comment [TU KHOA]" | "Tim hieu them", "Lien he" |
| 8 | Thoi luong phu hop | Doc het trong thoi luong da chon | Qua dai hoac qua ngan |
| 9 | Khong mo bang "Toi" | Mo bang "Ban", "Day", con so, brand | Dong dau la "Toi..." |
| 10 | Co huong dan quay | Goc quay, hanh dong, text overlay ro | Chi co loi thoai, khong co visual |

| Tong | Danh gia | Hanh dong |
|------|---------|----------|
| 95–100 | Xuat sac | Giao ngay |
| 85–94 | Tot | Giao duoc, ghi chu cai thien |
| 70–84 | Trung binh | Chinh lai truoc khi giao |
| <70 | Yeu | Viet lai |

<!-- #/SECTION -->

<!-- #SECTION
id: quality_checklist
type: quality_checklist
priority: 1
modes: [all]
industries: [all]
tags: [checklist, quality, cross_reference]
-->

## Cross-reference

| Khi can | Goi skill |
|---------|-----------|
| Copy ads de boost video hieu suat tot | `05-copy-quang-cao` |
| Brief cho creator quay theo script nay | `06-brief-ugc-egc` |
| Xep lich dang video | `01-lich-noi-dung` |
| Lay noi dau khach hang de viet hook chinh xac | `09-insight-khach-hang` |

## Checklist Chat Luong

- [ ] Da hoi khach: viet san hay tu viet co huong dan
- [ ] Co 2 ban A/B voi hook va goc do khac nhau
- [ ] Hook nam trong 3 giay dau, khong gioi thieu ban than, khong mo bang "Toi"
- [ ] Script phu hop tang pheu (TOFU / MOFU / BOFU) — dung cau truc tuong ung
- [ ] Moi cau toi da 15 tu, ngon ngu noi
- [ ] Co chi dan hinh anh + text overlay cho tung timestamp
- [ ] CTA cu the, hanh dong duoc
- [ ] Thoi luong phu hop nen tang da chon
- [ ] Co huong dan quay ky thuat
- [ ] Caption + hashtag dung theo nen tang (TikTok / Reels / Shorts)
- [ ] Viral Score va QA Score da cham
- [ ] Khong co nhac co ban quyen trong script
- [ ] Neu Mode B: Soft CTA, khong hard sell, co disclosure neu dung AI avatar

<!-- #/SECTION -->
