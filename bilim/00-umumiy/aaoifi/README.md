# 00-umumiy/aaoifi

AAOIFI standartlari (SS, FAS, GS, AS, Ethics) — BARCHA agentlar foydalanadi.

## Holat (2026-11-23)
Kitoblar foydalanuvchi tomonidan berilgan: Google Drive → `00_Umumiy/AAOIFI/` (5 ta PDF):
Shariaa-Standards-ENG, AAOIFI CPSS study text, AAOIFI CPFAS study text, AAOIFI-GS-13-Waqf-Governance-merged,
Auditing_standard_No_1…merged. Har biri 11–15 MB.

**Muammo:** Drive ulanishi 10 MB dan katta faylni yuklab bermaydi, matnni o'qish esa ~200 ming belgida uziladi.
Shu papkadagi `*.pdf.md` fayllar — kesilgan matn (asosan mundarija va dastlabki standartlar). Ular AAOIFI tekshiruvi
uchun YETARLI EMAS: `scripts/bosqich_nazorati.py` standart matnini faqat `SS-NN.md`, `FAS-NN.md`, `GS-NN.md`,
`AS-NN.md` nomli fayllar bo'yicha hisoblaydi.

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
