# Tizimni yangi sessiyada tiklash

Yangi Claude Code sessiyasida (claude.ai/code) shu matnni yozing:

> TIKLASH.md bo'yicha tizimni tikla.

Claude quyidagilarni bajaradi:

1. **Kod** — GitHub repozitoriysidan (sessiyada tanlangan bo'lsa) yoki Google Drive'dagi
   `Tekshiruv/islomiy-hujjat-agentlar_kod_*.zip` dan (eng yangisi) ochiladi.
2. **Bank hujjatlari va qonunchilik bazasi** — Google Drive'dan qayta yuklanadi:
   - ro'yxat: `scripts/drive_manifest.jsonl` (har qatorda: Drive `id`, `title`, `fileSize`, `target` — loyiha ichidagi yo'l);
   - yuklash: Drive `download_file_content(fileId=id)` → saqlangan faylni `target` ga ko'chirish
     (5 ta parallel yordamchi agentga bo'lib berish tezroq, ~5 daqiqa);
   - 10 MB dan katta fayllar: `scripts/drive_katta_fayllar.jsonl` (bo'laklarga bo'lingan versiyalari Drive'ga qo'yilgan bo'lsa — ularni yuklash).
   - Drive papkasida yangi fayllar paydo bo'lgan bo'lsa — `Tekshiruv` papkasini `parentId` bo'yicha qayta ro'yxatlab, manifestga qo'shish.
3. **Lug'atlar** (Atamalar lug'ati, G'azna va Risk lug'atlari/manbalari) — `Tekshiruv/00_Umumiy` yoki foydalanuvchi qayta yuboradi; joylari:
   `bilim/04-terminologiya/Atamalar_lugati.xlsx`, `bilim/04-terminologiya/soha/`, `bilim/06-soha/gazna/`, `bilim/06-soha/risk/`.
4. **Havolalardagi manbalar** (lex.uz, BIS, IFSB…): `python3 scripts/havolalarni_yukla.py scripts/havolalar.json`.
5. **Matnga aylantirish:** `python3 scripts/bazani_tayyorla.py --ocrsiz`, so'ng fonda `python3 scripts/bazani_tayyorla.py` (OCR; kerak bo'lsa
   `apt-get install -y tesseract-ocr tesseract-ocr-uzb tesseract-ocr-uzb-cyrl tesseract-ocr-rus`).
6. **Bank qoidalari reestri:** Drive'dagi har bir bankning `04_Reestr` papkasidan `QOIDALAR.md`, `OZGARTIRISH_NAVBATI.md`, `reestr.jsonl` ni `korxonalar/[BANK]/04_Reestr/` ga yukla; papka bo'lmasa — `python3 scripts/reestr.py boshlash --bank [BANK]` (amaldagi islomiy hujjatlar va 03_Yakuniy dan qayta quriladi).
7. **Promptlar** — `scripts/promptlar_drive.json` dagi Google Doc'lar bilan sinxron (orkestratorning -1 qadami).

Tekshiruv: `ls .claude/agents | wc -l` (29), `find bilim korxonalar -name "*.*.md" | wc -l`.
