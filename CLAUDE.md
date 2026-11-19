# Islomiy hujjatlarni ko'p agentli tekshirish tizimi

Bu loyiha islomiy moliya hujjatlarini (shartnoma, nizom, ichki tartib, mahsulot pasporti, buyruq, siyosat va h.k.)
bir nechta ixtisoslashgan AI agent orqali tekshiradi. Asosiy buyruq: `/hujjat-tekshir [fayl]`.

## Barcha agentlar uchun umumiy qoidalar

1. **AAOIFI ustuvorligi.** Hech bir xulosa AAOIFI Shariat standartlari, FAS (moliyaviy hisobot),
   Governance va Ethics standartlaridan chetga chiqmasligi kerak. Agar O'zbekiston qonunchiligi bilan
   AAOIFI o'rtasida ziddiyat bo'lsa — buni yashirmang, "ZIDDIYAT" deb belgilang va inson (Shariat kengashi
   + yurist) qaroriga qoldiring.
2. **Manbasiz iqtibos yo'q.** Standart raqami, band, qonun moddasini faqat `bilim/` papkasidagi matnda
   topgan bo'lsangiz aniq keltiring. Topilmasa: "manba bilim bazasida yo'q — tekshirish kerak" deb yozing.
   Hech qachon modda yoki band raqamini o'ylab topmang.
3. **Bilim bazasi** — har bir bosqichning o'z papkasi bor (`bilim/01-...` – `bilim/09-...`),
   AAOIFI standartlari esa umumiy: `bilim/00-umumiy/aaoifi/`. Har bir agent o'z papkasini
   agent faylidagi "Sening bilim bazang" bo'limida ko'radi. PDF/DOCX ning matni yonidagi `.md` faylda
   (`python3 scripts/bazani_tayyorla.py` yaratadi).
4. **Natija formati** (har bir agent shu formatda qaytaradi):

   ```
   ## [Agent nomi] xulosasi
   Umumiy baho: MOS / SHARTLI MOS / MOS EMAS
   | # | Band/joy | Muammo | Daraja | Manba | Tavsiya (aniq matn) |
   Daraja: KRITIK (hujjatni bekor qiladi / harom) · YUQORI · O'RTA · PAST
   Aniqlanmagan savollar: ...
   ```
5. **Til:** hisobotlar o'zbek tilida (lotin). Arabcha atamalar transliteratsiya + qavsda arabcha yozuv.
6. **Mas'uliyat:** AI xulosasi maslahat xarakterida. Yakuniy fatvo — Shariat kengashi, yakuniy huquqiy
   xulosa — litsenziyali yurist tomonidan beriladi. Har bir hisobot oxirida shu eslatma bo'lsin.
