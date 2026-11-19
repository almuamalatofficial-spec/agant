# Islomiy hujjatlarni ko'p agentli tekshirish tizimi

Claude Code asosidagi 21 ta ixtisoslashgan AI agent va orkestrator. Har bir hujjat kerakli
"mutaxassislar" tomonidan birma-bir tekshiriladi, ziddiyatlar ustunlik qoidalari bilan hal
qilinadi, ochiq savollar Word faylga yig'iladi, javoblardan keyin asl Word hujjatga Track Changes
bilan o'zgartirish kiritiladi va toza yakuniy hujjat chiqariladi.

## Ish tartibi

```
hujjat (korxonalar/[BANK]/01_Kiruvchi/)
 0   tasniflovchi ............ hujjat turi + qaysi agentlar kerak
 1   shariat-moslashtiruvchi . (faqat an'anaviy hujjat) islomiy versiya
 2   huquqiy-tekshiruvchi .... yurist: A–I savollar, TAHRIR/IZOH
 3   shariat-auditor ......... tamoyillar, IMK fatvolari, Shariat Governance (moslashtiruvchi izohlarini ko'rmaydi)
 4   terminolog .............. qonunchilik + lug'atlar
 5   tuzilma-tekshiruvchi .... org struktura, Ustav, IMK vakolatlari
 5.5 mijoz-himoyasi .......... (mijozga ko'rinadigan matn bo'lsa)
 6.x soha agentlari .......... risk, komplayens, audit, buxgalteriya, g'azna, soliq, operatsion/IT
 7   metodolog ............... ichki ziddiyat, mexanizm, formulalar
 7.5 takror-tozalovchi ....... takrorlangan jumlalar
 8   ichki-normativ .......... bankning boshqa ichki hujjatlari
 9   aaoifi-nazoratchi ....... AAOIFI standartlari bandma-band + VETO
 9.5 iqtibos-tekshiruvchi .... har bir modda/band/standart havolasini manba bilan solishtiradi
 —   orkestrator ............. ziddiyatlarni ustunlik qoidalari bilan hal qiladi
10   savol-yiguvchi .......... Savollar.docx (sariq JAVOB ustuni)
     ── siz javob yozasiz → /javoblarni-kirit ──
11   yakuniy-muharrir ........ Tahrirlangan.docx (Track Changes) + Yakuniy (toza).docx + O'zgarishlar jadvali.docx
12   yakuniy hisobot
```

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
`/hujjat-tekshir` — `/orkestrator` ning qisqa nomi.

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
