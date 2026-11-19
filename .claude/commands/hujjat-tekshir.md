---
description: An'anaviy yoki ichki hujjatni islomiylashtirib, barcha agentlar orqali BIRMA-BIR (ketma-ket) tahlil qilish va yakuniy hujjat + hisobot chiqarish
argument-hint: <hujjat yo'li, masalan korxonalar/01_Xalq_bank/01_Kiruvchi/fayl.docx> [--bank 01_Xalq_bank] [--soha risk,komplayens,audit,buxgalteriya,gazna] [--moslashtirmasdan] [--faqat 2,3,7]
---

Sen orkestratorsan. Kirish: $ARGUMENTS

ASOSIY QOIDA: agentlar PARALLEL EMAS, BIRMA-BIR ishga tushiriladi. Har bir agent tugaguncha kut,
uning natijasini faylga yoz, foydalanuvchiga 2–3 qatorda qisqa xulosa ko'rsat va keyin keyingisiga o'tasan.
Har bir keyingi agentga oldingi barcha hisobotlar yo'lini ber.

## 0. Tayyorgarlik
-1. **Promptlarni Drive'dan yangilash** (`scripts/promptlarni_yangila.py` docstring'idagi tartibda):
   Drive `search_files` (`parentId = '[papka_id]'`, papka_id — `scripts/promptlar_drive.json` da) bilan ro'yxatni ol;
   modifiedTime i `scripts/promptlar_holati.json` dagidan katta bo'lgan hujjatlarnigina `download_file_content`
   (exportMimeType `text/markdown`) bilan yuklab, `[vaqtinchalik papka]/[doc_id].json` ga ko'chir;
   `python3 scripts/promptlarni_yangila.py [papka]`, so'ng har biri uchun `... holat [doc_id] [modifiedTime]`.
   Qaysi promptlar o'zgarganini foydalanuvchiga ayt. Drive ulanmagan bo'lsa — mahalliy promptlar bilan davom et va buni ayt.
0. **Bankni aniqla.** Hujjat `korxonalar/[BANK]/...` ichida bo'lsa — BANK shu; aks holda `--bank` dan ol;
   ikkalasi ham bo'lmasa, foydalanuvchidan so'ra (`ls korxonalar/` ro'yxatini ko'rsat). Bundan keyin
   `B/` = `korxonalar/[BANK]/`. Har bir agentga promptda BANK nomini va quyidagi papkalarni ber:
   - `B/00_Conventional_documents/` — bankning amaldagi ichki hujjatlari (ustav, nizomlar, siyosatlar, tuzilma)
   - `B/00_Islamic_documents/` — bankning islomiy hujjatlari (IMK reglamenti, nomuvofiqlik siyosati va h.k.)
   - `B/02_Hisobotlar/`, `B/03_Yakuniy/` — avvalgi tekshiruvlar (uslub va izchillik uchun namuna)
   BOSHQA bank papkalaridan hech qachon foydalanma.
1. `python3 scripts/bazani_tayyorla.py` — bilim bazasidagi yangi fayllarni matnga aylantir.
   Bo'sh papkalar ro'yxatini foydalanuvchiga ko'rsat (to'xtama, davom et).
2. `python3 scripts/bazani_tayyorla.py [hujjat]` — kirish hujjatini matnga aylantir va o'qi.
3. Ish papkasi: `B/02_Hisobotlar/[hujjat_nomi]_<YYYY-MM-DD>/` (keyingi hamma fayllar shu yerda, `I/` deb belgilanadi).
4. Aniqla va `I/00_tasnif.md` ga yoz: hujjat turi (shartnoma/nizom/siyosat/tartib...), an'anaviy yoki islomiy,
   an'anaviy mahsulot nomi, soha(lar). Soha agentlari: `--soha` berilgan bo'lsa shular, aks holda mazmunga qarab
   (risk → soha-risk, AML/KYC → soha-komplayens, audit → soha-audit, hisob/provodka → soha-buxgalteriya,
   likvidlik/sukuk/valyuta → soha-gazna). Hech biri mos kelmasa — soha bosqichi o'tkazib yuboriladi.
5. `--faqat` berilgan bo'lsa, faqat shu raqamli bosqichlarni bajar (1 va 9 kerak bo'lsa ular ham ko'rsatilishi kerak).

## Bosqichlar (qat'iy tartibda)

**I QISM — tahlil va savollar** (shu buyruq bilan)

| # | Agent | Kirish | Natija fayli |
|---|---|---|---|
| 1 | shariat-moslashtiruvchi (A rejim) | asl hujjat | `I/01_islomiy_versiya.md` + `I/01_ozgarishlar.md` |
| 2 | huquqiy-tekshiruvchi | 01 versiya | `I/02_huquqiy.md` |
| 3 | shariat-auditor | 01 versiya | `I/03_shariat_audit.md` |
| 4 | terminolog | 01 versiya | `I/04_terminologiya.md` |
| 5 | tuzilma-tekshiruvchi | 01 versiya | `I/05_tuzilma.md` |
| 6.x | soha-* (tanlanganlar, har biri alohida, ketma-ket) | 01 versiya | `I/06_1_risk.md`, `I/06_2_komplayens.md`, ... |
| 7 | metodolog | 01 versiya | `I/07_metodologiya.md` |
| 7.5 | takror-tozalovchi (avval `python3 scripts/takrorlarni_top.py I/01_islomiy_versiya.md -o I/07b_takrorlar_xom.md`) | 01 versiya + xom ro'yxat | `I/07_takrorlar.md` |
| 8 | ichki-normativ-tekshiruvchi | 01 versiya | `I/08_ichki_normativ.md` |
| 9 | aaoifi-nazoratchi | 01 versiya + 02–08 hamma hisobotlar | `I/09_aaoifi_nazorat.md` |
| 10 | savol-yiguvchi | 02–09 hamma hisobotlar | `I/10_savollar.json`, `I/10_Savollar.docx`, `I/10_savollar.md` |

10-bosqichdan keyin **TO'XTA**:
- `I/10_Savollar.docx` ni Drive'dagi bankning `02_Hisobotlar` papkasiga yukla (Drive `create_file`, `disableConversionToGoogleType: true`,
  contentMimeType `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, fayl havolasi orqali) va havolani foydalanuvchiga ber;
- `I/YAKUNIY_HISOBOT.md` ning dastlabki variantini tuz (quyidagi 12-bo'lim, 1–7-bandlar);
- foydalanuvchiga ayt: "Savollar faylidagi sariq JAVOB ustunini to'ldiring, so'ng `/javoblarni-kirit` deb yozing".

**II QISM — javoblardan keyin** (`/javoblarni-kirit` buyrug'i bilan)

| # | Agent | Kirish | Natija fayli |
|---|---|---|---|
| 11 | yakuniy-tahrirchi | asl .docx + 02–09 + javoblar | `I/[hujjat] – Tahrirlangan.docx`, `I/11_tahrirlar.json`, `I/11_yakuniy_tahrir.md` |
| 12 | (orkestrator) | hammasi | `I/YAKUNIY_HISOBOT.md` + `.docx` |

`--moslashtirmasdan` bo'lsa 1-bosqich o'rniga asl hujjat matni `I/01_islomiy_versiya.md` ga ko'chiriladi.

Har bir Agent chaqiruvi prompti shu shablonda:
```
Tahlil qilinadigan hujjat: I/01_islomiy_versiya.md
Asl (an'anaviy) hujjat: [yo'l]
Hujjat tasnifi: I/00_tasnif.md
Bank: [BANK]; bank hujjatlari: B/00_Conventional_documents/, B/00_Islamic_documents/
Oldingi agentlar hisobotlari: [ro'yxat]
Avval o'z bilim bazangni o'rgan, keyin tahlil qil. CLAUDE.md dagi formatda qaytar.
```
Agent qaytargan matnni o'zgartirmasdan natija fayliga yoz (agent o'zi yozgan bo'lsa — tekshir).
Agent xato bilan tugasa — bir marta qayta ishga tushir; yana xato bo'lsa, faylga "BAJARILMADI: sabab" deb yoz va davom et.

## 12. Yakuniy hisobot — `I/YAKUNIY_HISOBOT.md`
(Tahrirlangan .docx va YAKUNIY_HISOBOT.docx ni `B/03_Yakuniy/` ga ham ko'chir: `[hujjat] – Tahrirlangan.docx`, `[hujjat] – Yakuniy xulosa.docx`; Drive'dagi bankning `03_Yakuniy` papkasiga ham yukla.)
1. Xulosa: umumiy baho (MOS / SHARTLI MOS / MOS EMAS), KRITIK topilmalar soni, tanlangan islomiy tuzilma.
2. Bosqichlar jadvali: agent, baho, topilmalar soni (K/Y/O'/P), bilim bazasi to'liqmi.
3. Barcha topilmalar birlashtirilgan jadvali (takrorlar birlashtirilgan, KRITIK → PAST, qaysi agent topgani).
4. ZIDDIYATLAR (shariat/AAOIFI ↔ qonun, agentlar o'rtasida) — inson qarori uchun.
5. VETO qilingan tavsiyalar.
6. Savollar va ularga berilgan javoblar (javobsizlari alohida).
6a. Takrorlar statistikasi (7.5-bosqich).
7. Bilim bazasidagi bo'shliqlar (qaysi bosqichga qaysi hujjat yetishmadi).
8. Eslatma: AI xulosasi maslahat xarakterida; yakuniy fatvo — Shariat kengashi, huquqiy xulosa — yurist.

So'ng `pandoc I/YAKUNIY_HISOBOT.md -o I/YAKUNIY_HISOBOT.docx` bilan Word versiyasini yarat.
Foydalanuvchiga: qisqa xulosa, KRITIK topilmalar va ish papkasi yo'lini ko'rsat.
