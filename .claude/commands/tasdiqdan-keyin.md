---
description: III qism — IMK va Boshqaruv tasdiqlagan hujjat asosida xodim yo'riqnomasi va mijoz uchun savol-javob tayyorlash (13-bosqich, NN-4)
argument-hint: [ish papkasi I] [tasdiq: IMK qarori raqami/sanasi; Boshqaruv qarori] [tasdiqlangan hujjat fayli yoki Drive havolasi — bo'lmasa "– Yakuniy (toza).docx"]
---

Sen orkestratorsan (III qism). Kirish: $ARGUMENTS

1. Ish papkasi `I/` va bankni aniqla. **Tasdiq faktini tekshir:** IMK qarori (raqam/sana) va Boshqaruv/vakolatli organ qarori berilganmi? Berilmagan bo'lsa — to'xta va so'ra (tasdiqlanmagan hujjat bo'yicha yo'riqnoma yozilmaydi). `I/NN_qarorlar.md` ga yoz.
2. Tasdiqlangan hujjatni ol (mahalliy yoki Drive'dan yuklab) → `korxonalar/[BANK]/03_Yakuniy/` ga; NN-3 da inson rad etgan/o'zgartirgan tahrirlar bo'lsa — aynan tasdiqlangan versiyadan foydalan.
2a. **Bank qoidalari reestrini yangilash** (keyingi hujjatlar shu hujjatga zid bo'lmasligi uchun):
   - matn: `pandoc "[tasdiqlangan.docx]" -t gfm --wrap=none -o I/13_tasdiqlangan.md`;
   - `python3 scripts/reestr.py qosh I/13_tasdiqlangan.md --bank [BANK] --nom "[hujjat nomi]" --holat tasdiqlangan --sana [tasdiq sanasi] --asos "[IMK qarori №, sana]"` (shu hujjatning eski versiyasi avtomatik "almashtirilgan" bo'ladi);
   - `korxonalar/[BANK]/04_Reestr/QOIDALAR.md` ga shu hujjatdagi 10–30 ta asosiy **sifatli qoidani** qo'sh (raqamsiz qoidalar: shariy pozitsiyalar, taqiqlar, vakolatlar): | Mavzu | Qoida (bir jumla) | Hujjat, band | Tasdiq (IMK qarori, sana) | Holat |. Eski qoida o'zgargan bo'lsa — eski qatorni "almashtirilgan" deb belgilab, yangisini yoz;
   - **Ta'sir:** `python3 scripts/reestr.py solishtir I/13_tasdiqlangan.md --bank [BANK] --nom "[hujjat nomi]" -o I/13_tasir.md` — nomzodlardan ATAYLAB O'ZGARTIRISHlarni ajrat va `korxonalar/[BANK]/04_Reestr/OZGARTIRISH_NAVBATI.md` ga yoz: | Eski hujjat | Band | Nima o'zgarishi kerak | Sabab (yangi hujjat, band) | Mas'ul | Holat |. Shu faylga `I/10_kochirishlar.md` dagi KO'CHIRISHlarni ham qo'sh (Eski hujjat = qaysi hujjatga, Sabab = topilma ID). Foydalanuvchiga: "Quyidagi oldingi hujjatlarga o'zgartirish kiritish kerak" ro'yxatini ber.
   - `korxonalar/[BANK]/04_Reestr/` dagi uchala faylni (reestr.jsonl, QOIDALAR.md, OZGARTIRISH_NAVBATI.md) Drive'dagi bankning `04_Reestr` papkasiga yukla (papka yo'q bo'lsa — yarat; eski versiyasi bo'lsa — yangisi bilan almashtirish o'rniga sana qo'shilgan nom bilan yukla). Bu — yangi sessiyada reestr yo'qolmasligi uchun.
3. **13-bosqich:** `yoriqnoma-yozuvchi` agentini ishga tushir (tasdiqlangan hujjat, tasdiq ma'lumoti, `10_5_kengash_xulosasi.md`, `11_javoblar.json`, BANK).
4. Natijalarni `B/03_Yakuniy/` ga ko'chir va Drive'dagi bankning `03_Yakuniy` papkasiga yukla.
5. **⛔ NN-4:** foydalanuvchiga ayt — mahsulot egasi/filial tarmog'i va komplaens yo'riqnoma va FAQ ni ko'rib, joriy etishni tasdiqlasin; "[mas'ul bo'linma aniqlashtirsin]" belgili joylar ro'yxatini ber.
