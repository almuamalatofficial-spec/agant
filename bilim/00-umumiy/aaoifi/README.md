# 00-umumiy/aaoifi

AAOIFI standartlari (SS, FAS, GS, AS, Ethics) — BARCHA agentlar foydalanadi.

## Holat (2026-11-25, yangilandi)
| Papka | Mazmuni | Manba |
|---|---|---|
| `SS/` | 61 bo'lak: CPSS-A01 va SS 1–62 (SS 2, 33 yo'q) — PDF + to'liq matn (`.md`), `SS/README.md` jadvali | AAOIFI CPSS study text 2024 (foydalanuvchi 15 qismga bo'lgan) |
| `GS/` | GS 1 (2024), 4–22 va GS 13 yo'riqnomasi; GS 1 eski tahriri va GS 2 (almashtirilgan, faqat tarix uchun) | alohida fayllar |
| `AS/` | AS 1–6 (audit) | alohida fayllar |
| `ES/` | Islomiy moliya mutaxassislari odob-axloq kodeksi | alohida fayl |
| `FAS/` | 28 bo'lak: Kontseptual asos (2020) va FAS 1, 3, 4, 7, 10, 14, 21, 23, 24, 26–28, 30–44 — PDF + to'liq matn, `FAS/README.md` | AAOIFI CPFAS study text 2024 (foydalanuvchi 8 qismga bo'lgan) |
Bo'laklar Drive'da: AAOIFI → "Boblar (SS — CPSS 2024 bo'yicha)" va "Boblar (FAS — CPFAS 2024 bo'yicha)". `manba/AS_merged_full.pdf` — AS 1–6, GS 1, 10–22 va Odob-axloq kodeksining birlashgan nashri (GS/AS/ES dagilar bilan bir xil). **2026-11-25:** SS, FAS, GS, AS, ES matnlari (`.md`) foydalanuvchi yuborgan Obsidian Markdown nashriga almashtirildi — sarlavhalar, jadvallar va band raqamlari tozaroq; oldingi pdftotext matnlari `manba/eski_matn/` da, kitob mundarijalari `manba/kitob_haqida/`, rasmlar `manba/rasmlar/`. SS 17 va SS 62 eski alohida fayllarda qoldi (kitobda ular birlashtirilgan: `manba/kitob_haqida/CPSS - 56 - …`). PDF fayllar o'zgarmadi. Eski kesilgan matnlar: `manba/eski_kesilgan/` (ishlatilmaydi).

## Qanday to'ldiriladi (birortasi yetarli)
1. Har bir PDF 10 MB dan kichik qismlarga bo'linib, Drive'ga shu papkaga qo'yiladi (masalan, "Split PDF" bilan 2 qism)
   → orkestrator ularni Drive ulanishi orqali yuklab oladi.
2. Foydalanuvchi fayllarga vaqtincha "havolasi bor har kim — ko'ruvchi" ruxsatini beradi → yuklab olingach yopadi.
   (Ruxsatni orkestrator o'zi o'zgartira olmaydi — bu sessiya xavfsizlik qoidasi bilan bloklangan.)
3. Foydalanuvchi kompyuteri Remote Control orqali ulanadi va fayllar o'sha yerdan olinadi.

PDF olingach: `python3 scripts/aaoifi_bolish.py KITOB.pdf --chiqish bilim/00-umumiy/aaoifi/SS --tur SS`
(FAS, GS uchun `--tur` mos ravishda) → `SS-08.pdf` + `SS-08.md` va `README.md` jadvali; bo'laklar Drive'ga
`00_Umumiy/AAOIFI/Boblar/` ga yuklanadi.

## Qoida
Standart matni bu papkada bo'lmasa, 9-bosqich (aaoifi-nazoratchi) boshlanmaydi va foydalanuvchiga ishning boshida
aytiladi (CLAUDE.md 15-qoida). AAOIFI'ga tayangan topilmalar "AAOIFI tekshiruvi kutilmoqda" belgisi bilan qoladi.
