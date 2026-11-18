# Islomiy hujjatlarni ko'p agentli tekshirish tizimi

Claude Code asosidagi 13 ta ixtisoslashgan AI agentdan iborat tizim. Har bir hujjat bir nechta
mustaqil "mutaxassis" tomonidan tekshiriladi, oxirida AAOIFI nazoratchisi barcha xulosalarni
filtrlaydi va bitta yakuniy hisobot chiqadi.

## Tizim sxemasi (ketma-ket)

```
an'anaviy hujjat namunasi
   │
   1. shariat-moslashtiruvchi ── islomiy versiya (01)
   2. huquqiy-tekshiruvchi      ─┐
   3. shariat-auditor            │ har biri birma-bir,
   4. terminolog                 │ oldingilarning hisobotini
   5. tuzilma-tekshiruvchi       │ o'qib, faqat yangi
   6. soha-risk/komplayens/      │ topilmalarni yozadi
      audit/buxgalteriya/gazna   │
   7. metodolog                  │
   8. ichki-normativ-tekshiruvchi┘
   9. aaoifi-nazoratchi  ── VETO: hech narsa AAOIFI'dan chetga chiqmaydi
  10. shariat-moslashtiruvchi ── tasdiqlangan tavsiyalar qo'llangan yakuniy hujjat
   │
   ▼  hisobotlar/<hujjat>_<sana>/YAKUNIY_HISOBOT.md (+ .docx)
```

## Bilim bazasi — har bir bosqichning o'z papkasi

| Papka | Agent | Nima joylanadi |
|---|---|---|
| `bilim/00-umumiy/aaoifi/` | hammasi | AAOIFI standartlari |
| `bilim/01-moslashtirish/` | shariat-moslashtiruvchi | islomiy shablonlar, avval moslashtirilgan hujjatlar |
| `bilim/02-qonunchilik/` | huquqiy-tekshiruvchi | qonunlar, kodekslar, MB nizomlari |
| `bilim/03-shariat-audit/` | shariat-auditor | audit metodikasi, checklistlar, fatvolar |
| `bilim/04-terminologiya/` | terminolog | glossariy, atamalar standarti |
| `bilim/05-tuzilma/` | tuzilma-tekshiruvchi | tuzilma, vakolatlar matritsasi |
| `bilim/06-soha/risk/` … `gazna/` | soha-* | har bir sohaning siyosat va tartiblari |
| `bilim/07-metodologiya/` | metodolog | hujjat yozish qoidalari, shablonlar |
| `bilim/08-ichki-normativ/` | ichki-normativ-tekshiruvchi | ustav, ichki hujjatlar, Shariat kengashi qarorlari |
| `bilim/09-aaoifi-nazorat/` | aaoifi-nazoratchi | AAOIFI talqinlari, kengash pozitsiyalari |

Fayllarni (PDF, DOCX, DOC, RTF, ODT, TXT) joylagandan keyin:

```
python3 scripts/bazani_tayyorla.py
```

Skanerlangan (rasm) PDF'lar uchun avval OCR kerak — skript bunday fayllar haqida ogohlantiradi.

## O'rnatish

1. Claude Code o'rnating: https://code.claude.com
2. Ushbu papkani oching va `claude` ni ishga tushiring.
3. Bilim bazasini yuqoridagi jadval bo'yicha to'ldiring.

## Foydalanish

An'anaviy hujjat namunasini `hujjatlar/` ga joylang va:

```
/hujjat-tekshir hujjatlar/kredit_shartnomasi.docx
/hujjat-tekshir hujjatlar/depozit_siyosati.pdf --soha gazna,buxgalteriya
/hujjat-tekshir hujjatlar/murobaha_nizomi.docx --moslashtirmasdan     # hujjat allaqachon islomiy bo'lsa
/hujjat-tekshir hujjatlar/shartnoma.docx --faqat 1,2,3,9               # faqat tanlangan bosqichlar
```

Har bir agent tugagach, terminalda uning qisqa xulosasi chiqadi, to'liq hisobot esa
`hisobotlar/<hujjat>_<sana>/` papkasida `01_...md` – `10_...md` fayllari sifatida saqlanadi.

## Yangi agent qo'shish

`.claude/agents/` ga yangi `.md` fayl qo'shing (masalan `soha-takaful.md`) — mavjudlaridan
birini nusxa qilib, `name`, `description` va vazifani o'zgartiring. Keyin
`.claude/commands/hujjat-tekshir.md` dagi soha tanlash ro'yxatiga qo'shing.

## Muhim eslatma

AI xulosasi maslahat xarakterida. Yakuniy fatvo — Shariat kengashi, yakuniy huquqiy xulosa —
litsenziyali yurist tomonidan beriladi. AAOIFI standartlari mualliflik huquqi bilan himoyalangan —
faqat litsenziyali nusxadan foydalaning.
