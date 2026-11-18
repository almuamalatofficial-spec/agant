---
description: Islomiy hujjatni barcha agentlar orqali to'liq tekshirish (moslashtirish → parallel tekshiruv → AAOIFI darvozasi → yakuniy hisobot)
argument-hint: <hujjat yo'li> [--moslashtirmasdan] [--soha risk,komplayens,audit,buxgalteriya,gazna]
---

Sen orkestratorsan. Tekshiriladigan hujjat: $ARGUMENTS

## 0. Tayyorgarlik
- Hujjatni o'qi (PDF/DOCX bo'lsa matnini chiqar). Hujjat turi, aqd turi va sohasini aniqla.
- Soha agentlarini tanla: `--soha` berilgan bo'lsa shularni, aks holda mazmuniga qarab
  (risk → soha-risk, AML/KYC/komplayens → soha-komplayens, audit → soha-audit,
  hisob/provodka/hisobot → soha-buxgalteriya, likvidlik/sukuk/valyuta → soha-gazna). Bir nechtasi bo'lishi mumkin.

## 1. Moslashtirish (ketma-ket)
`--moslashtirmasdan` berilmagan bo'lsa, `shariat-moslashtiruvchi` agentini ishga tushir.
Keyingi bosqichlar uning yozgan `hisobotlar/<hujjat>_moslashtirilgan.md` fayli ustida ishlaydi.

## 2. Mustaqil tekshiruv (PARALLEL — bitta xabarda barcha Agent chaqiruvlari)
huquqiy-tekshiruvchi, shariat-auditor, terminolog, tuzilma-tekshiruvchi, metodolog,
ichki-normativ-tekshiruvchi + tanlangan soha-* agentlari.
Har biriga: hujjat yo'li, hujjat turi va "CLAUDE.md dagi formatda qaytar" deb yoz.

## 3. AAOIFI darvozasi
`aaoifi-nazoratchi` ga hujjat yo'lini VA 2-bosqichdagi barcha agentlar xulosalarini ber.
U VETO qilgan tavsiyalar yakuniy hisobotga kirmaydi (alohida bo'limda ko'rsatiladi).

## 4. Yakuniy hisobot
`hisobotlar/<hujjat>_hisobot_<YYYY-MM-DD>.md` faylini yoz:
1. Xulosa: umumiy baho (MOS / SHARTLI MOS / MOS EMAS), KRITIK topilmalar soni.
2. Agentlar bo'yicha baholar jadvali.
3. Barcha topilmalar birlashtirilgan jadvali (takrorlarni birlashtir, KRITIK → PAST tartibida, qaysi agent(lar) topgani).
4. ZIDDIYATLAR: shariat/AAOIFI ↔ qonunchilik, agentlar orasidagi kelishmovchiliklar — inson qarori uchun.
5. VETO qilingan tavsiyalar.
6. Shariat kengashi va yuristga savollar.
7. Eslatma: AI xulosasi maslahat xarakterida; yakuniy fatvo — Shariat kengashi, huquqiy xulosa — yurist.

Foydalanuvchiga qisqa xulosa va hisobot fayl yo'lini ko'rsat.
