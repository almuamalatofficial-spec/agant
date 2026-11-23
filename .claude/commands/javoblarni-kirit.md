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
3b. **Javoblarni qarorlar fayliga yoz.** Inson bergan har bir javobni `korxonalar/[BANK]/04_Reestr/FOYDALANUVCHI_QARORLARI.md` ga qo'sh (sana, hujjat, masala, qaror) — keyingi hujjatlarda qayta so'ralmasin (CLAUDE.md 14-qoida).
3c. **Tavsiyadan olingan javob.** Foydalanuvchi "tavsiya bo'yicha yoz" desa: `qaror_turi: "inson"` (IMK, Yurist, Boshqaruv) savollari, shartli yoki misolli tavsiyalar va "____" qiymatlari matnga KIRITILMAYDI — faqat Word izohi bo'ladi. Buni foydalanuvchiga oldindan ayt (nechta savol shunday). Bunday javoblar `FOYDALANUVCHI_QARORLARI.md` ga yozilmaydi, `I/NN_qarorlar.md` da "tavsiyadan olingan" deb belgilanadi. Izohlarda "Kelishilganidek" deb yozilmaydi.
3a. Javoblar fayli olinmagan yoki unda birorta ham javob bo'lmasa — TO'XTA, foydalanuvchiga ayt; 11-bosqichni boshlama.
4. **11-bosqich:** `yakuniy-muharrir` agentini ishga tushir (asl .docx yo'li, I/ papka, 02–09 hisobotlar, 10_savollar.json, 11_javoblar.json, 10_ziddiyatlar.md, 09_aaoifi_nazorat.md, 09_5_iqtiboslar.md).
4a. **12a-bosqich (sifat):** `metodolog` agentini baholash rejimida ishga tushir — yakuniy (toza) hujjat bo'yicha Sifat kartasi → `I/12a_sifat_yakuniy.md` (dastlabki baho bilan solishtirish).
5. **12-bosqich:** `orkestrator.md` dagi 12-bo'lim bo'yicha yakuniy hisobotni tuz; fayllarni `B/03_Yakuniy/` ga va Drive'ga joyla.
6. Foydalanuvchiga: qo'llangan / qo'lda kiritish kerak / ochiq qolgan o'zgarishlar soni va fayllar havolalari.
7. **⛔ NN-3 — to'xta.** Foydalanuvchiga ayt: yurist (huquqiy tahrirlar), IMK a'zosi (shariat tahrirlari va ochiq savollar) va muallif `– Tahrirlangan.docx` ni Word'da ko'rib, har bir o'zgarishni qabul/rad etsin; so'ng hujjat IMK va Boshqaruv tasdig'iga kiritiladi. Tasdiqdan keyin: `/tasdiqdan-keyin [I] [IMK qarori raqami/sanasi]`. `I/NN_qarorlar.md` ga NN-2 javoblari kim tomonidan berilganini yoz.

