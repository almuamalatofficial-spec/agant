---
description: Savollar.docx ga yozilgan javoblarni o'qib, asl Word hujjatga Track Changes bilan o'zgartirish kiritish (11–12-bosqichlar)
argument-hint: [ish papkasi I, masalan korxonalar/01_Xalq_bank/02_Hisobotlar/TT_IBD_UZ_2026-11-19] [to'ldirilgan Savollar.docx yo'li yoki Drive havolasi]
---

Sen orkestratorsan (II qism). Kirish: $ARGUMENTS

1. Ish papkasi `I/` ni aniqla (berilmagan bo'lsa — `korxonalar/*/02_Hisobotlar/*/10_Savollar.docx` bor eng oxirgi papka; noaniq bo'lsa so'ra).
2. To'ldirilgan savollar faylini ol: mahalliy yo'l, yoki Drive havolasi/ID (Drive `download_file_content`; Google Doc bo'lsa
   exportMimeType `application/vnd.openxmlformats-officedocument.wordprocessingml.document`). Uni `I/10_Savollar_javoblar.docx` ga ko'chir.
3. `python3 scripts/word_vositalari.py javoblar I/10_Savollar_javoblar.docx I/11_javoblar.json` — nechta javob berilgani va
   nechtasi javobsiz qolganini foydalanuvchiga ayt. Javob noaniq bo'lsa (masalan, variantlarda yo'q harf) — shu savollarni ko'rsat va so'ra.
4. **11-bosqich:** `yakuniy-muharrir` agentini ishga tushir (asl .docx yo'li, I/ papka, 02–09 hisobotlar, 10_savollar.json, 11_javoblar.json, 10_ziddiyatlar.md, 09_aaoifi_nazorat.md, 09_5_iqtiboslar.md).
5. **12-bosqich:** `orkestrator.md` dagi 12-bo'lim bo'yicha yakuniy hisobotni tuz; fayllarni `B/03_Yakuniy/` ga va Drive'ga joyla.
6. Foydalanuvchiga: qo'llangan / qo'lda kiritish kerak / ochiq qolgan o'zgarishlar soni va fayllar havolalari.
