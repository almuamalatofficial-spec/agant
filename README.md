# Islomiy hujjatlarni ko'p agentli tekshirish tizimi

Claude Code asosidagi 13 ta ixtisoslashgan AI agentdan iborat tizim. Har bir hujjat bir nechta
mustaqil "mutaxassis" tomonidan tekshiriladi, oxirida AAOIFI nazoratchisi barcha xulosalarni
filtrlaydi va bitta yakuniy hisobot chiqadi.

## Tizim sxemasi

```
                 hujjat
                   │
     ┌─────────────▼──────────────┐
     │ 1. shariat-moslashtiruvchi │  (ichki hujjatni shariatga moslab tuzatadi)
     └─────────────┬──────────────┘
                   │ tuzatilgan versiya
   ┌───────────────┼──────────────────────────── PARALLEL ─────────────┐
   │ 2. huquqiy-tekshiruvchi   (O'zbekiston qonunchiligi)              │
   │ 3. shariat-auditor        (mustaqil shariat auditi)               │
   │ 4. terminolog             (atamalar)                              │
   │ 5. tuzilma-tekshiruvchi   (korxona tuzilmasi, vakolatlar)         │
   │ 6. soha-risk / soha-komplayens / soha-audit /                     │
   │    soha-buxgalteriya / soha-gazna   (hujjat sohasiga qarab)        │
   │ 7. metodolog              (metodologiya)                          │
   │ 8. ichki-normativ-tekshiruvchi (korxonaning o'z ichki hujjatlari) │
   └───────────────┬───────────────────────────────────────────────────┘
                   │ barcha xulosalar
     ┌─────────────▼──────────────┐
     │   aaoifi-nazoratchi (VETO) │  hech narsa AAOIFI'dan chetga chiqmasin
     └─────────────┬──────────────┘
                   ▼
       hisobotlar/<hujjat>_hisobot_<sana>.md
```

## O'rnatish

1. Claude Code o'rnating: https://code.claude.com
2. Ushbu papkani oching va `claude` ni ishga tushiring.
3. **Bilim bazasini to'ldiring** (eng muhim qadam — agentlar faqat shu yerdagi manbalarga iqtibos keltiradi):
   - `bilim/aaoifi/` — AAOIFI standartlari (rasmiy saytdan litsenziyali nusxa, matn yoki PDF)
   - `bilim/qonunchilik/` — lex.uz dan: Fuqarolik kodeksi, bank faoliyati, islomiy moliya bo'yicha
     qonun va MB nizomlari, Soliq kodeksi, AML/CFT qonuni
   - `bilim/korxona/` — tashkiliy tuzilma, vakolatlar matritsasi, bo'linma nizomlari
   - `bilim/ichki-normativ/` — ustav, siyosatlar, tartiblar, Shariat kengashi qarorlari
   - `bilim/glossariy.md` — tasdiqlangan atamalar

## Foydalanish

Hujjatni `hujjatlar/` ga joylang va:

```
/hujjat-tekshir hujjatlar/murobaha_shartnomasi.docx
/hujjat-tekshir hujjatlar/risk_siyosati.pdf --soha risk,komplayens
/hujjat-tekshir hujjatlar/nizom.docx --moslashtirmasdan
```

Bitta agentni alohida chaqirish ham mumkin:
`shariat-auditor agenti bilan hujjatlar/ijara.docx ni tekshir`.

## Yangi agent qo'shish

`.claude/agents/` ga yangi `.md` fayl qo'shing (masalan `soha-takaful.md`) — mavjudlaridan
birini nusxa qilib, `name`, `description` va vazifani o'zgartiring. Keyin
`.claude/commands/hujjat-tekshir.md` dagi soha tanlash ro'yxatiga qo'shing.

## Muhim eslatma

AI xulosasi maslahat xarakterida. Yakuniy fatvo — Shariat kengashi, yakuniy huquqiy xulosa —
litsenziyali yurist tomonidan beriladi. AAOIFI standartlari mualliflik huquqi bilan himoyalangan —
faqat litsenziyali nusxadan foydalaning.
