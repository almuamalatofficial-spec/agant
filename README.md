# Islomiy hujjatlarni ko'p agentli tekshirish tizimi

Claude Code asosidagi 29 ta ixtisoslashgan AI agent va orkestrator. Har bir hujjat kerakli
"mutaxassislar" tomonidan birma-bir tekshiriladi, ziddiyatlar ustunlik qoidalari bilan hal
qilinadi, ochiq savollar Word faylga yig'iladi, javoblardan keyin asl Word hujjatga Track Changes
bilan o'zgartirish kiritiladi va toza yakuniy hujjat chiqariladi.

## Ish tartibi

```
I QISM  /orkestrator [hujjat]
 0   tasniflovchi ............ hujjat turi + qaysi agentlar kerak
 1   shariat-moslashtiruvchi . (faqat an'anaviy hujjat) islomiy versiya
 ⛔ NN-1  IMK a'zosi tuzilmani tasdiqlaydi
 2   huquqiy-tekshiruvchi .... yurist: A–I, TAHRIR/IZOH
 3   shariat-auditor ......... tamoyillar, Shariat Governance (moslashtiruvchi izohlarini ko'rmaydi)
 3.5 fatvo-xotirasi .......... bankning oldingi IMK qarorlari va tasdiqlangan hujjatlari
 4   terminolog .............. qonunchilik + lug'atlar
 5   tuzilma-tekshiruvchi .... org struktura, Ustav, IMK vakolatlari
 5.5 mijoz-himoyasi
 6.x soha: risk, komplayens, audit, buxgalteriya, g'azna, soliq, operatsion/IT, garov-sug'urta, prudensial
 7   metodolog ............... ichki ziddiyat, mexanizm, formulalar yozilishi
 7.2 hisob-tekshiruvchi ...... formulalarni raqamli misollarda sinash
 7.5 takror-tozalovchi
 8   ichki-normativ
 8.2 paket-muvofiqligi ....... shartnoma/pasport/tarif/oferta va til nusxalari
 8.5 mohiyat-tekshiruvchi .... mustaqil "qizil jamoa": shakli islomiy, mohiyati kreditmi?
 9   aaoifi-nazoratchi ....... standartlar bandma-band + VETO
 9.5 iqtibos-tekshiruvchi
 —   orkestrator: ziddiyatlar (ustunlik qoidalari)
10   savol-yiguvchi .......... Savollar.docx
10.5 kengash-xulosachi ....... IMK uchun 1–2 betlik xulosa
 ⛔ NN-2  IMK a'zosi, yurist, muallif savollarga javob yozadi
II QISM  /javoblarni-kirit
11   yakuniy-muharrir ........ Tahrirlangan (Track Changes) + Yakuniy (toza) + O'zgarishlar jadvali
12   yakuniy hisobot
 ⛔ NN-3  yurist va IMK tahrirlarni qabul/rad etadi → IMK va Boshqaruv tasdig'i
III QISM /tasdiqdan-keyin
13   yoriqnoma-yozuvchi ...... filial xodimi yo'riqnomasi + mijoz uchun savol-javob
 ⛔ NN-4  mahsulot egasi va komplaens joriy etishni tasdiqlaydi
```

Sifat va izchillik:
- `bilim/00-umumiy/hujjat-turlari/` — 9 ta hujjat turi (siyosat, nizom, tartib, yo'riqnoma, metodika, shartnoma, oferta, mahsulot pasporti, TT) bo'yicha chuqurlik darajasi, majburiy bo'limlar, 0–3 balllik mezonlar va "ko'r nuqtalar" → metodolog **Sifat kartasi** (boshida va yakunda).
- `scripts/ziddiyat_xaritasi.py` — zanjirdan olib tashlangan (2026-11-23: aniqligi 0–5 %); faqat `scripts/reestr.py` parametr ajratish kutubxonasi sifatida ishlatadi.
- `scripts/bosqich_nazorati.py` — tasnifdagi KERAK bosqichlar bajarilganini tekshiradi (bajarilmasa zanjir to'xtaydi).
- `korxonalar/[BANK]/04_Reestr/` + `scripts/reestr.py` — **bank qoidalari reestri**: har tasdiqlangan hujjat parametrlari va sifatli qoidalari saqlanadi; har yangi hujjat avvalgilari bilan solishtiriladi (bir oy oldingi hujjatga ziddiyat darhol ko'rinadi); tasdiqdan keyin eski hujjatlarga o'zgartirish navbati (`OZGARTIRISH_NAVBATI.md`).

Bilim fayllari: `bilim/00-umumiy/aqdlar/` — 7 ta aqd (murobaha, ijara, mushoraka, muzoraba, vakolat, salam, istisno') bo'yicha nazorat ro'yxatlari; shariat agentlari hujjatdagi aqd turiga qarab keraklisini yuklaydi.

## Ustunlik qoidalari (qisqacha)
Shariy ruxsat/taqiq → AAOIFI nazoratchisi va shariat auditori; qonun → huquqiy; vakolat → tuzilma;
atama → terminolog; soha texnikasi → soha agenti (shariat va qonun chegarasida).
Shariat cheklovi biznes/risk qulayligidan ustun (risk maqsadi shariatga mos vosita bilan qondiriladi).
Qonun ↔ shariat ziddiyati avtomatik hal qilinmaydi — inson (IMK + yurist) qaroriga. To'liq qoidalar:
`.claude/commands/orkestrator.md`.

## Papkalar
- `bilim/00-umumiy/aaoifi/` — AAOIFI standartlari (barcha agentlar)
- `bilim/02-qonunchilik/` — O'zbekiston qonunlari, kodekslar, MB nizomlari (lex.uz)
- `bilim/04-terminologiya/` — Atamalar lug'ati (yozilish standarti), soha lug'atlari
- `bilim/06-soha/[risk|gazna|...]/` — har bir soha agentining alohida bazasi; `manbalar/` — havolalardan yuklangan matnlar
- `bilim/0X-.../` — boshqa bosqichlar bazasi
- `korxonalar/[BANK]/` — har bir bank alohida (00_Conventional, 00_Islamic, 01_Kiruvchi, 02_Hisobotlar, 03_Yakuniy). **Maxfiy — git'ga yuklanmaydi.**
- `scripts/` — konvertor (PDF/DOCX/DOC/HTML/XLSX/PPTX/OCR), takrorlar, iqtiboslar, Word vositalari, Drive prompt sinxroni

## Foydalanish
```
/orkestrator korxonalar/01_Xalq_bank/01_Kiruvchi/hujjat.docx
/orkestrator hujjatlar/kredit_shartnomasi.docx --bank 02_Aloqa_bank --agentlar +soha-gazna
/javoblarni-kirit korxonalar/01_Xalq_bank/02_Hisobotlar/hujjat_2026-11-20
```
`/hujjat-tekshir` — `/orkestrator` ning qisqa nomi. Tasdiqdan keyin: `/tasdiqdan-keyin [I] [IMK qarori]`.

## Promptlarni tahrirlash
Har bir agentning prompti Google Drive'dagi `Tekshiruv/Agent_promptlari` papkasida Google Doc sifatida turadi.
"PROMPT" sarlavhasidan pastini tahrirlang — keyingi tekshiruv oldidan avtomatik olinadi (faqat inson
tahrirlagan hujjatlar; `scripts/promptlar_holati.json`).

## Yangi agent qo'shish
`.claude/agents/` ga yangi `.md` (mavjudlaridan birini nusxa qilib), `name`, `description` va vazifani
o'zgartiring; `tasniflovchi.md` dagi tanlash qoidalariga va `orkestrator.md` bosqichlar jadvaliga qo'shing.

## Muhim eslatma
AI xulosasi maslahat xarakterida. Yakuniy fatvo — Shariat kengashi (IMK), yakuniy huquqiy xulosa —
litsenziyali yurist. AAOIFI standartlari mualliflik huquqi bilan himoyalangan — faqat litsenziyali nusxadan foydalaning.
