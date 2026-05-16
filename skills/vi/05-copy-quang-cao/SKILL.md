---
name: 05-copy-quang-cao
description: Viet 6 bien the copy quang cao theo 3 tang pheu (TOFU/MOFU/BOFU), tuan thu chinh sach quang cao, co CTA phu hop tung nen tang. Ho tro Meta Ads, TikTok Ads, Google Ads, Zalo OA.
skill_id: "05-copy-quang-cao"
agent: "content-producer"
metadata:
  version: 3.0.0
  category: content
triggers:
  - "viet quang cao"
  - "copy quang cao"
  - "noi dung chay ads"
  - "copy Facebook Ads"
  - "copy TikTok Ads"
  - "tieu de quang cao"
  - "copy retarget"
  - "ads personal brand"
  - "copy Zalo OA"
  - "broadcast Zalo"
output: |
  Telegram: Bullet tom tat — nen tang, muc tieu, hook duoc chon, y copy noi bat, watch-out compliance
  Full (Excel): 6 bien the day du (primary text + headline + description + CTA + creative notes) + A/B guide
context_requirements:
  required: []
  optional:
    - industry
    - target_audience
    - business_name
    - mode          # "product" | "personal_brand"
    - active_channels
related:
  - 04-script-video
  - 02-brief-chien-dich
  - 09-insight-khach-hang
  - references/copy-frameworks-vn
  - references/hook-formulas-vn
---

# Copy Quang Cao

<!-- #SECTION
id: context_intake
type: context_intake
priority: 1
modes: [all]
industries: [all]
tags: [session_context, mode_detection, product, personal_brand]
-->

## Buoc 0 — Xac dinh Mode

Doc tu `session_context.mode`:

| session_context.mode | Mode ap dung |
|---------------------|-------------|
| `product` | **Mode A** — ban san pham / conversion |
| `personal_brand` | **Mode B** — boost personal brand / authority |
| Ca hai | Hoi 1 cau: "Ban dang chay ads ban san pham hay boost personal brand?" |
| Khong co | Mac dinh **Mode A** |

<!-- #/SECTION -->

<!-- #SECTION
id: data_collection
type: data_collection
priority: 1
modes: [all]
industries: [all]
tags: [intake, adaptive, platform, objective]
-->

## Thu thap thong tin

**Neu session_context da co `industry` + `target_audience`:** Chi hoi 2 cau:

2. **Nen tang quang cao?** Meta Ads / TikTok Ads / Google Ads / Zalo OA. Khong chon → mac dinh Meta Ads.
4. **Muc tieu quang cao?** Tin nhan (CPMess) / Lead form / Traffic / Chuyen doi. Khong chon → mac dinh tin nhan.

**Neu chua co context:** Hoi du 4 cau:

1. **San pham / dich vu gi?** Mo ta ngan, USP chinh, gia, uu dai dang chay.
2. **Nen tang quang cao?** Meta Ads / TikTok Ads / Google Ads / Zalo OA.
3. **Doi tuong muc tieu?** Gioi tinh, do tuoi, noi dau chinh. Cold (chua biet) hay Warm (da tuong tac)?
4. **Muc tieu quang cao?** Tin nhan / Lead / Traffic / Chuyen doi.

<!-- #/SECTION -->

<!-- #SECTION
id: copy_principles
type: logic
priority: 1
modes: [all]
industries: [all]
tags: [125_chars, emotion_triggers, tofu_mofu_bofu]
-->

## Nguyen tac Cot loi

### Quy tac 125 ky tu

Tren Meta Ads, chi **125 ky tu dau** hien thi truoc nut "Xem them". Dong 1 phai:
- Gay to mo hoac cham noi dau
- Chua USP hoac con so cu the
- Tu hoan chinh ve nghia (khong cat giua cau)

**Tot:**
> "Da ban len mun 3 nam chua het? 1 lieu trinh 28 ngay — cam ket sau sach." *(74 ky tu)*

**Xau:**
> "Chao ban, cam on ban da quan tam den dich vu cua chung toi. Hom nay minh muon gioi thieu..." *(cat giua — nguoi doc bo qua)*

### Thu vien cam xuc trigger

| # | Trigger | Mo ta | Vi du |
|---|---------|-------|-------|
| 1 | **Noi dau (Pain)** | Cham vao van de dang gap | "Met moi vi da mun? Ban khong co loi..." |
| 2 | **Khat vong (Aspiration)** | Ve hinh anh tuong lai | "Tuong tuong da ban dep tu tin khong can filter" |
| 3 | **FOMO** | So bo lo, gioi han | "Chi con 12 slot thang nay — 89 nguoi da dat" |
| 4 | **Bang chung xa hoi** | Nguoi khac da thanh cong | "1,200 chi da trai nghiem — 4.8/5 sao" |
| 5 | **Uy tin (Authority)** | Chuyen gia, chung nhan | "10 nam kinh nghiem — bac si da lieu truc tiep" |
| 6 | **To mo (Curiosity)** | Gay thac mac | "Co 1 thu 90% nguoi dung skincare sai — ban biet chua?" |

**Quy tac chon trigger theo pheu:**
- TOFU: To mo (6), Noi dau (1), Khat vong (2)
- MOFU: Bang chung (4), Uy tin (5), Noi dau (1)
- BOFU: FOMO (3), Bang chung (4), Noi dau (1)

<!-- #/SECTION -->

<!-- #SECTION
id: frameworks
type: template
priority: 1
modes: [all]
industries: [all]
tags: [framework, AIDA, PAS, BAB, 4P, FAB, SSS, negative_example]
-->

## 6 Framework Copy

### Chon framework theo nhiet do audience

| Nhiet do | Framework uu tien | Ly do |
|---------|------------------|-------|
| **Cold** | AIDA, Star·Story·Solution | Dan dat logic tu dau, khong lo quang cao |
| **Warm** | PAS, 4P | Nhac lai noi dau, tang trust bang proof |
| **Hot** | FAB, BAB | Rap dap loi ich cu the, visual transformation |
| **Retarget** | PAS hoac BAB | Nhan manh hau qua hoac bien doi |

### Tom tat 6 frameworks

| Framework | Cau truc | Dung khi | Platform |
|-----------|---------|---------|---------|
| **AIDA** | Attention → Interest → Desire → Action | Cold, launch san pham moi | Meta, TikTok, YouTube |
| **PAS** | Problem → Agitate → Solution | Warm, nganh co pain point ro | Meta, LinkedIn, Google |
| **BAB** | Before → After → Bridge | Transformation (spa, fitness, giao duc) | Meta Reels, TikTok |
| **4P** | Promise → Picture → Proof → Push | High-ticket, can trust cao | LinkedIn, Google, Meta |
| **FAB** | Features → Advantages → Benefits | Khach co intent, dang so sanh | Google, Meta retarget |
| **Star·Story·Solution** | Star → Story → Solution | Storytelling, UGC-style | TikTok, Reels, Shorts |

**Sai lam pho bien:** Viet tu do (gioi thieu → tinh nang → CTA) thay vi dung framework → copy nhat, CTR thap. Moi bien the trong 6 bien the phai dung **1 framework khac nhau**.

### Negative Examples — Framework copy xau vs tot

#### PAS (Problem → Agitate → Solution)

**Copy xau:**
> "Ban dang gap van de voi da? Da la van de kho chua. Nhung dung lo vi chung toi co giai phap. San pham cua chung toi rat hieu qua va duoc nhieu nguoi tin dung. Lien he ngay."

*Tai sao sai:* Problem chung chung, Agitate khong co, Solution khong cu the, CTA nhat.

**Copy tot:**
> "Da ban len mun sau 30 tuoi du da dung du thu? Cang dung nhieu san pham, mun cang nhieu hon — vi ban dang bo qua 1 buoc co ban. Lieu trinh tri mun sinh hoc 28 ngay cua chung toi fix dung nguyen nhan goc re — 847 khach da het mun hoan toan. Nhan tin nhan lich tu van mien phi."

*Tai sao tot:* Problem cu the (sau 30 tuoi, da dung du thu), Agitate day cam giac bat luc (cang dung cang toi), Solution ro rang (28 ngay, fix goc re), social proof (847 khach), CTA cu the.

---

#### AIDA (Attention → Interest → Desire → Action)

**Copy xau:**
> "Chao mung den voi spa cua chung toi! Chung toi co nhieu dich vu cham soc da dep. Gia ca phai chang, chat luong tot. Hay den trai nghiem ngay!"

*Tai sao sai:* Attention khong co, Interest khong co tension, Desire khong co, Action yeu.

**Copy tot:**
> "97% nguoi di spa van bi mun vi nhan vien khong biet dieu nay. [Attention]
> Quy trinh lam sach thong thuong chi xu ly be mat — khong cham toi nang mun an sau da. Do la ly do mun cu tai di tai lai du ban lam da thuong xuyen. [Interest]
> Cong nghe Hydra-Clean 3D cua [Ten spa] di sau 3 lop bieu bi — sach hoan toan, khong squeezing, khong ton thuong. Ket qua giu duoc 3-4 thang. [Desire]
> Con 5 slot cuoi thang nay. Nhan tin de dat lich — tu van mien phi." [Action]

<!-- #/SECTION -->

<!-- #SECTION
id: andromeda_compliance
type: reference
priority: 2
modes: [all]
industries: [all]
tags: [andromeda, compliance, policy, meta, ad_rejection]
-->

## Andromeda Warning — Khong clone ads

Meta 2026: He thong Andromeda cluster quang cao co **Creative Similarity Score > 60%** → giam delivery tu dong.

| Similarity Score | Trang thai | Hanh dong |
|-----------------|-----------|-----------|
| < 40% | An toan | Tiep tuc chay |
| 40–60% | Canh bao | Kiem tra lai |
| > 60% | Nguy hiem | Giam delivery tu dong |

**5 chieu da dang tranh Andromeda:**
1. **Hook khac nhau** — Pain vs To mo vs Aspiration (thay goc nhin, khong chi thay text)
2. **Format khac nhau** — Video doc 9:16 vs Anh vuong 1:1 vs Carousel
3. **Nhan vat khac nhau** — Founder vs Khach hang review vs Bac si/KOC
4. **Am nhac khac nhau** — Trending VN vs Nhac cam trang vs Voiceover
5. **Boi canh khac nhau** — Studio vs Ngoai canh vs UGC phong khach

## Compliance Checklist

| Quy tac | Chi tiet | Vi pham = bi tu choi |
|---------|---------|---------------------|
| Khong cam ket tuyet doi | Tranh "dam bao", "100%", "chac chan" | Co |
| Khong "mien phi" trong headline | Dung trong body, khong trong headline | Co |
| Khong nhac den dac diem ca nhan | Tranh "Ban bi mun?" — dung "Nhieu nguoi gap..." | Co |
| Truoc/sau phai thuc te | Khong chinh sua qua muc | Co |
| Khong hinh anh nhay cam | Khong close-up mun, da bi thuong | Co |
| Disclaimer y te | Thuc pham chuc nang, clinic → can disclaimer | Co |

<!-- #/SECTION -->

<!-- #SECTION
id: platform_rules
type: reference
priority: 2
modes: [all]
industries: [all]
tags: [platform, meta, tiktok, google, zalo, CTA, char_limit]
-->

## Quy tac theo Nen tang

| Quy tac | Meta Ads | TikTok Ads | Google Ads | Zalo OA |
|---------|----------|-----------|------------|---------|
| Primary text | 125 char dong 1, 300–500 char toan bo | 80–100 char | Khong co | 500 char, xuat hien day du |
| Headline | Toi da 40 char | Khong co | 30 char × 3 | Tieu de 50 char |
| Description | Toi da 30 char | Khong co | 90 char × 2 | Khong co |
| Giong van | Chuyen nghiep, gan gui | Tre, tu nhien, nhu noi chuyen | Truc tiep, keyword | Than mat, ca nhan hoa |
| CTA button | Chon tu danh sach Meta | Trong text | Trong headline | Nut "Xem them" hoac link |
| Ti le hinh | 1:1 feed, 9:16 story | 9:16 bat buoc | Khong ap dung | 16:9 hoac 1:1 |

### Zalo OA — Dac thu rieng

Zalo OA la kenh retention, khong phai acquisition. Giong van va muc tieu khac hoan toan voi Meta/TikTok.

| Yeu to | Zalo OA |
|--------|---------|
| Tone | Than mat, nhu nhan tin ca nhan — KHONG nhu quang cao |
| Muc tieu chinh | Nhac lich, giu chan, upsell khach cu |
| Gioi han | Toi da 3 broadcast/tuan — qua → unfollow tang |
| Mau tin hieu qua | [Ten khach], [noi dung ngan], [CTA 1 buoc] |
| Tranh | Chay chu, nhieu anh, giong van thuong mai |

**Template Zalo OA (3 loai):**

*Nhac lich:*
> "Chi [Ten] oi, da [X] tuan tu buoi lam da lan truoc cua chi roi. Da chi giai doan nay can duoc cham soc de giu ket qua. Em co the giu lich cho chi vao [ngay] khong a?"

*Tin cam on + follow-up:*
> "Chi [Ten] oi, cam on chi da tin tuong [Ten spa] nhe. Sau buoi hom nay da chi co gi thay doi khong a? Neu chi thay kho chiu gi nho nhan tin em ngay. Em luon o day ho tro chi."

*Offer exclusive:*
> "Chi [Ten], thang nay [Ten spa] co uu dai dac biet danh rieng cho khach than thiet — [offer cu the]. Chi la 1 trong [X] khach duoc em gui rieng tin nay. Hieu luc den [ngay], chi muon em giu cho chi slot khong a?"

### CTA — Thu tu uu tien

| Muc do | CTA | Khi nao |
|--------|-----|---------|
| Manh nhat | "Nhan tin ngay de dat lich" | Tin nhan, BOFU |
| Manh | "Dat lich tu van mien phi" | Lead, MOFU/BOFU |
| Trung binh | "Xem bang gia chi tiet" | Traffic, MOFU |
| Nhe | "Tim hieu them" | Awareness, TOFU |

**Tranh:** "Click vao day", "Lien he ngay" — khong ro hanh dong.

<!-- #/SECTION -->

<!-- #SECTION
id: output_format
type: output_template
priority: 1
modes: [all]
industries: [all]
tags: [output, telegram, excel, 6_variants, AB_test]
-->

## Cau truc Output

### Telegram (bullet tom tat)

```
San pham: [ten]
Nen tang: [Meta / TikTok / Google / Zalo OA]
Muc tieu: [Tin nhan / Lead / Traffic]
Doi tuong: [mo ta ngan]

Top hook duoc chon:
• TOFU: "[125 char]"
• BOFU: "[125 char]"

Watch-out:
• [Compliance note neu co]
• [Creative note quan trong]

→ File Excel day du: [link hoac ten file]
```

### Full — Excel (6 bien the)

#### Thong tin chung

```
San pham / Dich vu: [ten]
Nen tang: [Meta Ads / TikTok Ads / Google Ads / Zalo OA]
Muc tieu: [Tin nhan / Lead / Traffic / Chuyen doi]
Doi tuong: [mo ta ngan]
USP chinh: [1 cau]
```

#### TOFU — Thu hut (Cold audience)

**Bien the 1 — [Ten goc do, VD: Cham noi dau]**

| Thanh phan | Noi dung |
|------------|---------|
| Framework | [AIDA / Star·Story·Solution] |
| Trigger | [Pain / Curiosity / Aspiration] |
| Primary text (125 char) | [Dong 1 — hien truoc "Xem them"] |
| Primary text (day du) | [300–500 char] |
| Headline | [Toi da 40 char] |
| Description | [Toi da 30 char] |
| CTA button | [Tim hieu them / Gui tin nhan] |
| Creative note | [Mo ta hinh anh/video di kem] |

**Bien the 2 — [Ten goc do, VD: Gay to mo]**
*(Cung cau truc, khac framework va trigger)*

---

#### MOFU — Thuyet phuc (Warm audience)

**Bien the 3 — [Ten goc do, VD: Social proof]**

| Thanh phan | Noi dung |
|------------|---------|
| Framework | [PAS / 4P] |
| Trigger | [Social proof / Authority] |
| Primary text (125 char) | [Dong 1] |
| Primary text (day du) | [Nhan manh bang chung, review, so lieu] |
| Headline | [Toi da 40 char] |
| Description | [Toi da 30 char] |
| CTA button | [Gui tin nhan / Dat lich] |
| Creative note | [Nen dung review / truoc-sau] |

**Bien the 4 — [Ten goc do, VD: Chuyen gia]**
*(Cung cau truc, goc do khac)*

---

#### BOFU — Chot don (Hot audience + Retarget)

**Bien the 5 — [Ten goc do, VD: FOMO]**

| Thanh phan | Noi dung |
|------------|---------|
| Framework | [FAB / BAB] |
| Trigger | [FOMO / Social proof] |
| Primary text (125 char) | [Nhan manh khan cap, gioi han] |
| Primary text (day du) | [Deadline, so luong, uu dai cu the] |
| Headline | [Toi da 40 char] |
| Description | [Toi da 30 char] |
| CTA button | [Dat lich ngay / Mua ngay] |
| Creative note | [Co so lieu, countdown] |

**Bien the 6 — Retarget**
*(Danh rieng cho nguoi da nhan tin hoac da xem chua mua)*

| Thanh phan | Noi dung |
|------------|---------|
| Framework | [PAS hoac BAB] |
| Trigger | [Pain + FOMO] |
| Primary text (125 char) | ["Hom truoc ban hoi ve [dich vu]..."] |
| Primary text (day du) | [Nhac lai noi dau, bo sung bang chung moi] |
| Headline | [Toi da 40 char] |
| Description | [Toi da 30 char] |
| CTA button | [Gui tin nhan / Dat lich] |
| Creative note | [Creative KHAC lan 1 — tranh ad fatigue] |

---

#### Bang tong hop 6 bien the

| # | Tang | Goc do | Framework | Trigger | Hook 125 char | CTA |
|---|------|--------|-----------|---------|--------------|-----|
| 1 | TOFU | | | | | |
| 2 | TOFU | | | | | |
| 3 | MOFU | | | | | |
| 4 | MOFU | | | | | |
| 5 | BOFU | | | | | |
| 6 | BOFU | Retarget | | | | |

#### Huong dan A/B test

| Test | Bien the A | Bien the B | Chi so | Thoi gian |
|------|-----------|-----------|--------|----------|
| Hook | Bien the 1 | Bien the 2 | CTR, CPMess | 3–5 ngay |
| CTA | Bien the 3 | Bien the 4 | Ti le chuyen doi | 3–5 ngay |
| Offer | Bien the 5 | Bien the 6 | ROAS, CPA | 5–7 ngay |

**Quy tac test:**
- Chi test 1 yeu to/lan
- Budget toi thieu 200K/ngay/bien the
- Du lieu toi thieu 1,000 impression hoac 50 click truoc khi ket luan
- Chenh lech >20% = co y nghia thong ke

<!-- #/SECTION -->

<!-- #SECTION
id: personal_brand_mode
type: template
priority: 3
modes: [full]
industries: [all]
tags: [personal_brand, mode_B, awareness, trust, soft_sell, A1_A2_T1_T2_S1_S2]
-->

## Personal Brand Mode (Mode B)

### Khac biet so voi Mode A

| Yeu to | Mode A (San pham) | Mode B (Personal Brand) |
|--------|------------------|------------------------|
| Pheu | TOFU/MOFU/BOFU (sell) | Awareness / Trust / Soft sell |
| Muc tieu | Conversion | Follower, engagement, inbound DM |
| Tone | Direct, USP | Authentic, story-led, expert |
| CTA | "Inbox", "Mua ngay" | "Follow them", "Share neu thay dung" |
| Proof | Review, before-after | Track record ca nhan, case study |

### 6 bien the Personal Brand

**2 Awareness (Cold audience — gioi thieu ban than)**

*Bien the A1 — Founder angle:*
| Thanh phan | Noi dung |
|------------|---------|
| Primary text | "[Ten], [X] nam [linh vuc]. Tuan nay minh share [X] bai hoc dat gia nhat sau [X] lan that bai. [link]" |
| Headline | "[X] lan that bai dat tien" |
| Description | "Tu [chuc danh] [so nam] nam" |
| CTA | "Doc them" |

*Bien the A2 — Coach/Expert angle:*
| Thanh phan | Noi dung |
|------------|---------|
| Primary text | "Sau khi [coach/tu van/lam viec voi] [X] [khach/doi ngu/founder], minh nhan ra 1 dieu: [insight bat ngo]. Minh viet day du o day. [link]" |
| Headline | "1 dieu [X]% [doi tuong] sai" |
| Description | "Sau [X] [ca/du an/nam]" |
| CTA | "Tim hieu" |

**2 Trust (Warm audience — da follow 1–2 tuan)**

*Bien the T1 — Personal story + lesson:*
| Thanh phan | Noi dung |
|------------|---------|
| Primary text | "Thang truoc minh [hanh dong sai/quyet dinh kho]. Hom nay nhin lai, day la dieu minh hoc duoc — va no thay doi cach minh [lam gi] mai mai. [link]" |
| Headline | "Bai hoc dat gia nhat thang nay" |
| Description | "[1 cau mo ta lesson chinh]" |
| CTA | "Doc chuyen cua minh" |

*Bien the T2 — Industry insight + framework:*
| Thanh phan | Noi dung |
|------------|---------|
| Primary text | "Sau [X] nam trong nganh [linh vuc], day la [X] dieu minh thay nguoi moi bat dau hay sai nhat — va cach fix tung cai. Khong ai day dieu nay trong sach. [link]" |
| Headline | "[X] loi sai nguoi moi trong nganh hay mac" |
| Description | "Chia se tu kinh nghiem thuc chien" |
| CTA | "Tim hieu ngay" |

**2 Soft Sell (Warm-to-Hot — da co trust)**

*Bien the S1 — Free resource:*
| Thanh phan | Noi dung |
|------------|---------|
| Primary text | "Minh vua hoan thanh [tai lieu/template/checklist] tom tat [X] nam kinh nghiem cua minh ve [chu de]. Mien phi — minh chi muon no den tay nguoi thuc su can. Comment '[tu khoa]' de minh gui." |
| Headline | "Mien phi: [ten tai lieu]" |
| Description | "[X] trang / [X] buoc thuc te" |
| CTA | "Nhan ngay" |

*Bien the S2 — Waitlist / Cohort:*
| Thanh phan | Noi dung |
|------------|---------|
| Primary text | "[Ten chuong trinh] — cohort [so] se mo dang ky trong [X] ngay. [X] nguoi dang trong danh sach cho. Neu ban dang [mo ta van de doi tuong], day co the la chuong trinh danh cho ban. Link waitlist trong bio." |
| Headline | "Cohort [so] — [X] slot con lai" |
| Description | "Mo dang ky [ngay]" |
| CTA | "Xem chi tiet" |

### 3 canh bao truoc khi chay ads Personal Brand

1. **Chua du 500 follower huu co:** Ads khong convert vi thieu social proof. Fix: tang follower organic truoc.
2. **Niche chua ro:** Target sai, dot ngan sach. Fix: chay skill 23 personal-brand-strategy truoc.
3. **Dung AI avatar:** Phai disclose theo Nghi dinh 147/2024 — tham khao `references/ai-video-disclosure-vn.md`.

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
| Script video di kem copy ads | `04-script-video` |
| Brief chien dich day du | `02-brief-chien-dich` |
| Insight khach de viet copy chinh xac | `09-insight-khach-hang` |

## Checklist Chat Luong

- [ ] Co du 6 bien the: 2 TOFU + 2 MOFU + 2 BOFU (gom 1 retarget)
- [ ] Dong 1 moi bien the khong vuot 125 ky tu
- [ ] Headline khong vuot 40 ky tu
- [ ] Moi bien the dung 1 framework khac nhau
- [ ] Moi bien the dung trigger cam xuc khac nhau
- [ ] CTA cu the, hanh dong duoc — khong chung chung
- [ ] Khong vi pham compliance (xem checklist)
- [ ] Khong dung "mien phi" trong headline
- [ ] Khong nhac den dac diem ca nhan ("Ban bi...", "Ban thua...")
- [ ] Co ghi chu creative di kem moi bien the
- [ ] Giong van phu hop nen tang (Meta vs TikTok vs Google vs Zalo OA)
- [ ] Retarget copy dung creative KHAC lan 1
- [ ] Khong co 2 bien the nao cung framework + cung hook → Andromeda risk
- [ ] Telegram output: da tom tat bullet + watch-out
- [ ] Full output: Excel day du 6 bien the + A/B guide

<!-- #/SECTION -->
