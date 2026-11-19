---
description: Orkestrator — hujjatni tasniflab, kerakli agentlarni BIRMA-BIR ishga tushiradi, ziddiyatlarni ustunlik qoidalari bilan hal qiladi, savollar faylini tayyorlaydi va xulosalarni bitta hisobotga yig'adi (I qism). Javoblardan keyin — /javoblarni-kirit (II qism).
argument-hint: [hujjat yo'li, masalan korxonalar/01_Xalq_bank/01_Kiruvchi/fayl.docx] [--bank 01_Xalq_bank] [--agentlar +soha-gazna,-soha-risk] [--faqat 2,3,9]
---

Sen orkestratorsan. Kirish: $ARGUMENTS

**ASOSIY QOIDA:** agentlar PARALLEL EMAS, BIRMA-BIR ishga tushiriladi. Har bir agent tugaguncha kut, natijasi faylga yozilganini tekshir, foydalanuvchiga 2–3 qatorda qisqa xulosa ko'rsat (baho, K/Y/O'/P soni, eng muhim topilma) va keyingisiga o't. Har bir keyingi agentga oldingi hisobotlar yo'lini ber (istisno — shariat-auditor, quyida).

## 0. Tayyorgarlik
-1. **Promptlarni Drive'dan yangilash** (`scripts/promptlarni_yangila.py` docstring'idagi tartibda): Drive `search_files` (`parentId = '[papka_id]'`, papka_id — `scripts/promptlar_drive.json` da) bilan ro'yxatni ol; modifiedTime i `scripts/promptlar_holati.json` dagidan katta bo'lgan hujjatlarnigina `download_file_content` (exportMimeType `text/markdown`) bilan yuklab, `[vaqtinchalik papka]/[doc_id].json` ga ko'chir; `python3 scripts/promptlarni_yangila.py [papka]`, so'ng har biri uchun `... holat [doc_id] [modifiedTime]`. Qaysi promptlar o'zgarganini foydalanuvchiga ayt. Drive ulanmagan bo'lsa — mahalliy promptlar bilan davom et va buni ayt.
0. **Bankni aniqla.** Hujjat `korxonalar/[BANK]/...` ichida bo'lsa — BANK shu; aks holda `--bank`; ikkalasi ham bo'lmasa — foydalanuvchidan so'ra (`ls korxonalar/`). `B/` = `korxonalar/[BANK]/`. Har bir agentga BANK nomini va `B/00_Conventional_documents/`, `B/00_Islamic_documents/` ni ber. BOSHQA bank papkalaridan hech qachon foydalanilmaydi.
1. `python3 scripts/bazani_tayyorla.py bilim B` — yangi fayllarni matnga aylantir; bo'sh bilim papkalarini foydalanuvchiga ko'rsat (to'xtama).
2. `python3 scripts/bazani_tayyorla.py [hujjat]` — kirish hujjatini matnga aylantir.
3. Ish papkasi: `B/02_Hisobotlar/[hujjat_nomi]_[YYYY-MM-DD]/` (bundan keyin `I/`).
4. **Tasniflovchi** agentini ishga tushir → `I/00_tasnif.md` (hujjat turi, an'anaviy/islomiy, aqdlar, mijozga ko'rinadigan qismlar, kerakli agentlar asosi bilan). `--agentlar +x,-y` berilgan bo'lsa — tasnifni shunga moslab tuzat. Tanlangan agentlar ro'yxatini foydalanuvchiga ko'rsat.
4b. **Bank izohlari:** asl Word hujjatda izohlar bo'lsa (bank xodimlari qoldirgan) — `python3 scripts/izohlarni_ajrat.py [asl.docx] -o I/00c_bank_izohlari.md --json I/00c_bank_izohlari.json`. Har bir agentga beriladi; har bir izoh (B1, B2, …) uchun tegishli agent(lar) belgilanadi (tuzilma/vakolat → tuzilma; qonun → huquqiy; shariat → shariat-auditor; limit/risk → soha-risk; hisob → buxgalteriya va h.k.). Tekshiruv oxirida har bir Bn ga javob borligini tekshir — javobsiz qolgani savollar fayliga tushadi.
4a. **Reestr bilan solishtirish:** `python3 scripts/reestr.py solishtir I/01_islomiy_versiya.md --bank [BANK] --nom "[hujjat nomi]" -o I/00b_reestr_solishtirish.md` (reestr bo'lmasa — avval `python3 scripts/reestr.py boshlash --bank [BANK]`). Natija ichki-normativ-tekshiruvchi (asosiy) va fatvo-xotirasiga beriladi.
5. `--faqat` berilgan bo'lsa — faqat shu raqamli bosqichlar.
6. Hujjat islomiy bo'lsa (1-bosqich yo'q): asl matnni `I/01_islomiy_versiya.md` ga ko'chir (izohlarsiz toza nusxa: `pandoc [asl.docx] -t gfm-raw_html --wrap=none --track-changes=accept -o I/01_islomiy_versiya.md`).

## Bosqichlar (qat'iy tartibda; tasnifda "kerak emas" bo'lganlari o'tkazib yuboriladi)

**I QISM — tahlil, ziddiyatlar va savollar** (`/orkestrator`)

| # | Agent | Kirish | Natija fayli |
|---|---|---|---|
| 0 | tasniflovchi | asl hujjat | `I/00_tasnif.md` |
| 1 | shariat-moslashtiruvchi (faqat an'anaviy hujjat) | asl hujjat | `I/01_islomiy_versiya.md`, `I/01_ozgarishlar.md` |
| ⛔ | **NN-1** (faqat 1-bosqich bo'lsa) | — | to'xta, quyida |
| 2 | huquqiy-tekshiruvchi | 01 + tasnif | `I/02_huquqiy.md` |
| 3 | shariat-auditor | **faqat** `01_islomiy_versiya.md` + `02_huquqiy.md` (`01_ozgarishlar.md` BERILMAYDI) | `I/03_shariat_audit.md` |
| 3.5 | fatvo-xotirasi | 01 + 03 | `I/03_5_fatvo_xotirasi.md` |
| 4 | terminolog | 01 + oldingilar | `I/04_terminologiya.md` |
| 5 | tuzilma-tekshiruvchi | 01 + oldingilar | `I/05_tuzilma.md` |
| 5.5 | mijoz-himoyasi (mijozga ko'rinadigan matn bo'lsa) | 01 + oldingilar | `I/05_5_mijoz_himoyasi.md` |
| 6.x | soha agentlari (tanlanganlari, har biri alohida): 6.1 risk, 6.2 komplayens, 6.3 audit, 6.4 buxgalteriya, 6.5 g'azna, 6.6 soliq, 6.7 operatsion, 6.8 garov-sug'urta, 6.9 prudensial | 01 + oldingilar | `I/06_1_risk.md` … `I/06_9_prudensial.md` |
| 7 | metodolog (avval `python3 scripts/ziddiyat_xaritasi.py I/01_islomiy_versiya.md -o I/07a_ziddiyat_xaritasi.md`) | 01 + ziddiyat xaritasi + oldingilar | `I/07_metodologiya.md` ("Ichki ziddiyatlar reestri" bilan) |
| 7.2 | hisob-tekshiruvchi (formula/stavka/grafik bo'lsa) | 01 + 07 + soha | `I/07_2_hisob.md`, `I/07_2_hisob_misollar.py` |
| 7.5 | takror-tozalovchi (avval `python3 scripts/takrorlarni_top.py I/01_islomiy_versiya.md -o I/07b_takrorlar_xom.md`) | 01 + xom ro'yxat + oldingilar | `I/07_takrorlar.md` |
| 8 | ichki-normativ-tekshiruvchi | 01 + oldingilar | `I/08_ichki_normativ.md` |
| 8.2 | paket-muvofiqligi (paket hujjatlari yoki til nusxalari bo'lsa) | 01 + paket | `I/08_2_paket.md` |
| 8.5 | mohiyat-tekshiruvchi (**mustaqil**: boshqa hisobotlar BERILMAYDI) | 01 + tasnif + paket | `I/08_5_mohiyat.md` |
| 9 | aaoifi-nazoratchi (standartlar matritsasi + VETO) | 01 + 02–08.5 | `I/09_aaoifi_nazorat.md` |
| 9.5 | iqtibos-tekshiruvchi | 02–09 | `I/09_5_iqtiboslar.md` |
| — | **orkestrator: ziddiyatlarni hal qilish** (quyidagi qoidalar) | 02–09.5 | `I/10_ziddiyatlar.md` |
| 10 | savol-yiguvchi | 02–09.5 + 10_ziddiyatlar | `I/10_savollar.json`, `I/10_Savollar.docx`, `I/10_savollar.md` |
| 10.5 | kengash-xulosachi | shariat hisobotlari + 10 | `I/10_5_kengash_xulosasi.md`, `– IMK uchun xulosa.docx` |
| ⛔ | **NN-2** | — | to'xta, quyida |

**II QISM — javoblardan keyin** (`/javoblarni-kirit`)

| # | Agent | Kirish | Natija |
|---|---|---|---|
| 11 | yakuniy-muharrir | asl .docx + 01–10 + javoblar | `– Tahrirlangan.docx` (Track Changes + izohlar), `– Yakuniy (toza).docx`, `– O'zgarishlar jadvali.docx`, `I/11_yakuniy_muharrir.md` |
| 12 | orkestrator | hammasi | `I/YAKUNIY_HISOBOT.md` + `.docx` |
| ⛔ | **NN-3** | — | to'xta, quyida |

**III QISM — tasdiqdan keyin** (`/tasdiqdan-keyin`, faqat NN-3 dagi tasdiqdan so'ng)

| # | Agent | Kirish | Natija |
|---|---|---|---|
| 13 | yoriqnoma-yozuvchi | tasdiqlangan yakuniy hujjat + IMK qarori | `– Xodim yo'riqnomasi.docx`, `– Mijoz uchun savol-javob.docx` |
| ⛔ | **NN-4** | — | to'xta, quyida |

## INSON NAZORAT NUQTALARI (NN)
AI xulosasi maslahat xarakterida — quyidagi nuqtalarda orkestrator **to'xtaydi**, kim nimani ko'rishi kerakligini aniq aytadi va inson javobisiz keyingi qismga o'tmaydi. Har bir NN natijasini `I/NN_qarorlar.md` ga yoz (kim, sana, qaror).

| NN | Qachon | Kim ko'radi | Nimani ko'radi | Qaror |
|---|---|---|---|---|
| **NN-1** | 1-bosqichdan keyin (an'anaviy hujjat islomiylashtirilganda) | **IMK a'zosi** (shariat) | `01_ozgarishlar.md`: tanlangan islomiy tuzilma (masalan, murobaha yoki IMBT), aqdlar ketma-ketligi | Tuzilma ma'qulmi? Ha → 2-bosqichga o'tiladi; Yo'q → boshqa tuzilma bilan 1-bosqich qayta. (Noto'g'ri tuzilmani 20 ta agent tekshirishining ma'nosi yo'q.) |
| **NN-2** | 10.5-bosqichdan keyin | **IMK a'zosi** — "IMK" savollari va `IMK uchun xulosa.docx`; **yurist** — "Yurist" savollari; **hujjat muallifi** — "Muallif" savollari | `10_Savollar.docx` (sariq JAVOB ustuni), `IMK uchun xulosa.docx` | Savollarga qisqa javob → `/javoblarni-kirit` |
| **NN-3** | 12-bosqichdan keyin | **yurist** — barcha huquqiy tahrirlar; **IMK a'zosi** — shariat bilan bog'liq tahrirlar va ochiq savollar; **muallif** — qolganlari | `– Tahrirlangan.docx` (Word'da har bir o'zgarishni Qabul qilish/Rad etish), `– O'zgarishlar jadvali.docx`, `YAKUNIY_HISOBOT.docx` | Tahrirlar qabul qilinadi → hujjat IMK (fatvo) va Boshqaruv tasdig'iga kiritiladi. Tasdiq faktini (qaror raqami, sana) orkestratorga bering → `/tasdiqdan-keyin` |
| **NN-4** | 13-bosqichdan keyin | **mahsulot egasi / filial tarmog'i**, **komplaens** | Xodim yo'riqnomasi va mijoz FAQ | Joriy etish uchun tasdiq |

To'xtaganda foydalanuvchiga xabar shakli: "⛔ NN-x: [kim] [qaysi fayl]ni ko'rib, [qanday qaror] qabul qilishi kerak. Fayllar: [havolalar]. Tayyor bo'lgach: [keyingi buyruq]."

10-bosqichdan keyin (NN-2 oldidan) qo'shimcha:
- `I/10_Savollar.docx` va `IMK uchun xulosa.docx` ni Drive'dagi bankning `02_Hisobotlar` papkasiga yukla (`create_file`, `disableConversionToGoogleType: true`, contentMimeType `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, fayl havolasi `sha256:…:[yo'l]` orqali) va havolalarni ber;
- `I/YAKUNIY_HISOBOT.md` ning dastlabki variantini tuz (12-bo'lim, 1–8-bandlar).
- Foydalanuvchiga **aniq joy** bilan xabar ber: "Savollar fayli tayyor: Drive → Tekshiruv → [BANK] → 02_Hisobotlar → `[hujjat] – Savollar ([sana]).docx` (havola). Sariq JAVOB ustunini to'ldiring. Javob bermaguningizcha asl hujjatga hech qanday o'zgartirish kiritilmaydi."
- **Asl hujjatga o'zgartirish (11-bosqich) faqat javoblar olingandan keyin** — I qismda hech qachon yakuniy-muharrir chaqirilmaydi.

## Agent chaqiruvi shabloni
```
Sen [agent-nomi] agentisan. Avval CLAUDE.md va .claude/agents/[agent-nomi].md ni o'qi va to'liq amal qil.
Tahlil qilinadigan hujjat: I/01_islomiy_versiya.md
Asl hujjat: [yo'l]
Tasnif: I/00_tasnif.md
Bank: [BANK]; bank hujjatlari: B/00_Conventional_documents/, B/00_Islamic_documents/ (boshqa bank papkalari — TAQIQ)
Oldingi hisobotlar: [ro'yxat]   ← shariat-auditor uchun faqat 02_huquqiy.md; mohiyat-tekshiruvchiga hech qanday hisobot berilmaydi; 01_ozgarishlar.md faqat yakuniy-muharrirga
Bank izohlari: I/00c_bank_izohlari.md (bo'lsa) — o'z sohangdagi har bir Bn ga hisobotingda \"Bank izohlariga javob\" bo'limida javob ber: rozimiz/qisman/rozi emasmiz, asos (qonun, Ustav, Siyosat, shariat) va aniq TAHRIR yoki savol.
Natijani [fayl] ga yoz. Menga faqat qaytar: umumiy baho, K/Y/O'/P soni, eng muhim 3 topilma, e'tirozlar soni.
```
**Bank izolyatsiyasi nazorati** — har bir agentdan keyin: `python3 scripts/bank_izolyatsiyasi.py I --bank [BANK] -o I/_izolyatsiya.md`. Boshqa bank hujjatiga tayangan topilma bo'lsa — o'sha topilmani hisobotdan olib tashla (yoki agentni "faqat [BANK] hujjatlari bilan" ko'rsatmasi bilan qayta ishga tushir) va foydalanuvchiga ayt. Yakuniy hisobotga "Bank izolyatsiyasi: buzilish yo'q / N ta tuzatildi" qatorini yoz.
Agent xato bilan tugasa — bir marta qayta ishga tushir; yana xato bo'lsa, faylga "BAJARILMADI: sabab" deb yoz va davom et.

## ZIDDIYATLARNI HAL QILISH — USTUNLIK QOIDALARI
9.5-bosqichdan keyin barcha hisobotlardagi tavsiyalarni **band bo'yicha** guruhla. Bitta bandga ikki yoki undan ortiq agent bir-biriga zid tavsiya bergan bo'lsa (yoki "Oldingi tavsiyalarga e'tiroz" bo'lsa), quyidagi qoidalarni **tartib bilan** qo'lla va natijani `I/10_ziddiyatlar.md` ga yoz.

### 0. O'rinlilik filtri (birinchi navbatda)
Har bir TAHRIRni `bilim/00-umumiy/hujjat-turlari/orinlilik.md` bo'yicha tekshir: mazmuni boshqa hujjatga tegishli (soliq → soliq hisobi siyosati, provodka → hisob sxemalari, limit → risk siyosati, protsedura → tartib) yoki hujjatning tasdiqlovchi organi vakolatidan tashqari bo'lsa — **KO'CHIRISH** ga aylantir. Bu hujjatga faqat havola qoladi (zarur bo'lsa). KO'CHIRISHlar ro'yxati `I/10_kochirishlar.md` ga (| № | Topilma ID | Mazmun | Qaysi hujjatga | Tasdiqlovchi organ | Bu hujjatda havola kerakmi |) va tasdiqdan keyin `B/04_Reestr/OZGARTIRISH_NAVBATI.md` ga yoziladi. Agentlar o'zi KO'CHIRISH deb belgilagan bo'lsa — tekshirib tasdiqla. Shubhali holat (tegishli hujjat bankda bormi, noma'lum) — savolga.

### 1. Masala turi bo'yicha vakolatli agent
| Masala turi | Vakolatli (ustun) agent | Izoh |
|---|---|---|
| Shariy ruxsat/taqiq: riba, g'arar, maysir, aqd tuzilmasi va ketma-ketligi, kafolat, xayriya, purifikatsiya | aaoifi-nazoratchi (standart) + shariat-auditor (tamoyil, IMK fatvosi) | Ikkalasi kelishmasa: bankning IMK fatvosi/qarori → AAOIFI standart matni → tamoyil talqini. IMK fatvosi AAOIFI'dan farq qilsa — inson qarori (G). |
| O'zbekiston qonunchiligining imperativ normasi, shartnoma huquqiy shakli | huquqiy-tekshiruvchi | Shariat talabi bilan to'qnashsa — 3-qoidaga qara. |
| Organlar vakolati, tasdiqlash tartibi, bo'linmalar | tuzilma-tekshiruvchi (Ustav, IMK nizomi asosida) | |
| Ichki hujjatlar ierarxiyasi va ziddiyati | ichki-normativ-tekshiruvchi | |
| Atama va yozilish | terminolog (qonun + lug'at) | Atama shariy mazmunni o'zgartirsa — shariat-auditor bilan kelishiladi. |
| Hisob, soliq, risk o'lchovi, likvidlik, prudensial normativlar, garov/sug'urta, IT/ketma-ketlikni tizimda bajarish | tegishli soha agenti | Faqat shariat va qonun chegarasida. |
| Formula va hisob-kitob natijasi (raqamda) | hisob-tekshiruvchi | Raqamli misol matndagi talqindan ustun: matn "foiz emas" desa-yu, hisob foizli xulq ko'rsatsa — hisob natijasi asos bo'ladi. |
| Bitimning iqtisodiy mohiyati (hiyla) | mohiyat-tekshiruvchi + aaoifi-nazoratchi | Mohiyat "hiyla" (yuqori ishonch) desa va shariat auditori "mos" desa — ehtiyotkor variant: KRITIK, IMK qaroriga. |
| Oldingi IMK qarorlariga moslik | fatvo-xotirasi | Oldingi IMK qarori IMK uni o'zgartirmaguncha ustun. |
| Paket va til nusxalari | paket-muvofiqligi | Ustuvor hujjat — yuqori turuvchi yoki eng so'nggi tasdiqlangan; davlat tilidagi matn. |
| Mijozga oshkor qilish, mijoz huquqlari | mijoz-himoyasi | Qonun talabi bo'lsa — huquqiy bilan birga. |
| Hujjat tuzilishi, mexanizm, formula | metodolog | |

### 2. Shariat cheklovi biznes, risk va operatsion qulaylikdan ustun
Masalan: **Risk** kechikish uchun bank daromadiga jarima talab qiladi, **Shariat auditori** rad etadi → shariat ustun. Lekin risk talabi shunchaki o'chirilmaydi: uning maqsadi (intizom, zararni qoplash) shariatga mos vosita bilan qondiriladi — kechikish uchun xayriyaga yo'naltiriladigan majburiyat + IMK tasdig'i bilan faqat haqiqiy zararni qoplash. Natijada birlashtirilgan TAHRIR matni yoziladi va izohda ikkala agent eslatiladi.

### 3. Qonun ↔ shariat ziddiyati — avtomatik hal qilinmaydi
O'zbekiston qonunining imperativ normasi va shariat/AAOIFI talabi bir-birini istisno qilsa — **hech biri avtomatik ustun emas** (CLAUDE.md 1-band). Orkestrator ikkala talabni bir vaqtda qondiradigan yechim izlaydi (masalan: qonundagi neustoyka shakli saqlanadi, tushum xayriyaga yo'naltiriladi). Topilsa — variant A sifatida taklif qilinadi; baribir **inson qarori** (IMK + yurist) uchun savolga chiqariladi va highlight qilinadi.

### 4. VETO
AAOIFI nazoratchisi VETO qilgan tavsiya qo'llanmaydi; uning o'rniga VETO'dagi muqobil yechim olinadi (agar boshqa agent unga e'tiroz bildirmagan bo'lsa).

### 5. Dalil kuchi
- Iqtibosi **TASDIQLANDI** bo'lgan pozitsiya iqtibosi NOTO'G'RI/TOPILMADI bo'lgan pozitsiyadan ustun.
- Asossiz qolgan topilma ustun bo'la olmaydi — u IZOH/savolga aylantiriladi.
- Maxsus norma umumiydan, keyingi (amaldagi) tahrir oldingisidan ustun.

### 6. Ikkalasi ham to'g'ri bo'lsa
- Talablar bir-birini istisno qilmasa — **ikkalasi birga** (kumulyativ) qo'llanadi, bitta birlashtirilgan matn yoziladi.
- Istisno qilsa va bir xil asoslangan bo'lsa — **ehtiyotkor (xavfni ko'proq kamaytiradigan)** variant tanlanadi, ikkinchisi izohda eslatiladi.

### 7. Daraja
Bitta muammo bir nechta agentda turli darajada bo'lsa — **eng yuqori daraja** olinadi (iqtibosi tasdiqlangan bo'lsa).

### 8. Inson qarori talab qilinadigan holatlar (hal qilinmaydi → savol)
Qonun ↔ shariat; IMK fatvosi ↔ AAOIFI; ikki agent ham tasdiqlangan manbaga tayanib qarama-qarshi; shariy tanlov (masalan, ibra'ni oldindan oshkor qilish yoki qilmaslik); biznes tanlov (mahsulot parametrlari).

### `I/10_ziddiyatlar.md` formati
| № | Band | Agent A tavsiyasi | Agent B tavsiyasi | Qo'llangan qoida (1–8) | Qaror: A / B / birlashtirilgan matn / INSON QARORI | Yakuniy tavsiya matni | Izoh |

## 12. Yakuniy hisobot — `I/YAKUNIY_HISOBOT.md` (+ `.docx`)
Tahrirlangan, toza va jadval .docx fayllarini hamda YAKUNIY_HISOBOT.docx ni `B/03_Yakuniy/` ga ko'chir (`[hujjat] – Tahrirlangan.docx`, `[hujjat] – Yakuniy (toza).docx`, `[hujjat] – O'zgarishlar jadvali.docx`, `[hujjat] – Yakuniy xulosa.docx`) va Drive'dagi bankning `03_Yakuniy` papkasiga yukla.
1. **Umumiy xulosa** (5–7 jumla): hujjatning umumiy holati, eng jiddiy muammolar, yakuniy tavsiya.
2. **Bosqichlar jadvali:** agent | baho | K/Y/O'/P | iqtiboslar ishonchliligi | bilim bazasi to'liqmi.
3. **Barcha topilmalar birlashtirilgan jadvali** (takrorlar birlashtirilgan; KRITIK → PAST; qaysi agent(lar); Turi TAHRIR/IZOH; iqtibos holati).
4. **Terminologiya jadvali:** Hujjatdagi atama | Rasmiy/tavsiya etilgan atama | Manba.
2a. **Sifat kartasi** (hujjat turi standarti bo'yicha): dastlabki baho → yakuniy baho (12a), mezonlar bo'yicha; **ko'r nuqtalar** — hujjatda umuman yo'q bo'lgan muhim mavzular.
3a. **Ichki ziddiyatlar reestri** — metodologning reestridan HAQIQIY ziddiyatlar + boshqa agentlar topgan ichki ziddiyatlar (birlashtirilgan): Band A | Band B | Mavzu | Farq | Qaror/savol.
3b. **Hujjatlararo ziddiyatlar** (bankning avval tasdiqlangan hujjatlari bilan, reestr asosida) va **eski hujjatlarga o'zgartirish kiritish kerak bo'lganlar** ro'yxati.
4a. **Mohiyat xulosasi** (8.5) va **oldingi IMK qarorlariga moslik** (3.5) — har biri 2–3 jumla.
4b. **Hisob-kitob testlari** (7.2): shariat jihatidan xavfli xulqlar.
5. **Ziddiyatlar** va ularning hal qilinishi (`10_ziddiyatlar.md` qisqacha); inson qarori kutilayotganlar — highlight.
6. **VETO qilingan tavsiyalar.**
7. **Boshqa hujjatlarga ta'sir:** o'zgartirilishi yoki bekor qilinishi kerak bo'lgan hujjatlar (ichki-normativ, huquqiy, buxgalteriya hisobotlaridan).
8. **Ochiq savollar** (javobsizlari) va **bilim bazasidagi bo'shliqlar** (qaysi manba yetishmadi).
9. **Takrorlar statistikasi** (7.5) va **o'zgarishlar statistikasi** (11: qo'llandi / qo'lda / ochiq).
10. **Yakuniy tavsiya:** «Tasdiqlash mumkin» / «Tuzatishlardan so'ng tasdiqlash mumkin» / «Qayta ishlashga qaytarilsin» — asoslari bilan; shariat bo'yicha: «Muvofiq» / «Tuzatishlar sharti bilan muvofiq» / «Nomuvofiq».
11. **Eslatma:** AI xulosasi maslahat xarakterida; yakuniy fatvo — IMK, huquqiy xulosa — yurist.

`pandoc I/YAKUNIY_HISOBOT.md -o I/YAKUNIY_HISOBOT.docx`. Foydalanuvchiga: qisqa xulosa, KRITIK topilmalar, fayllar havolalari.
