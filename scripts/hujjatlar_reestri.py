#!/usr/bin/env python3
"""Bankning ichki hujjatlar reestri: hujjatda tilga olingan ichki hujjat nomlarini rasmiy reestr bilan solishtirish.

Har bir bankning rasmiy reestri o'z papkasida: korxonalar/[BANK]/04_Reestr/hujjatlar_reestri.jsonl (+ .md).
Faqat SHU bank reestri ishlatiladi (CLAUDE.md 4-band) — islomiy hujjatlar ro'yxati banklarda o'xshash bo'lsa ham.

    python3 scripts/hujjatlar_reestri.py import  reestr.xlsx --bank 01_Xalq_bank
    python3 scripts/hujjatlar_reestri.py tekshir [I]/01_islomiy_versiya.md --bank 01_Xalq_bank -o [I]/00d_hujjat_nomlari.md

import: varaqlarni o'qiydi. Asosiy reestr varag'i (sarlavhada "Ҳужжат номи"/"Hujjat nomi" va "тури"/"turi")
— holati "amalda"; nomida "кучини йўқот"/"kuchini yo'qot" bo'lgan varaq — "kuchini yo'qotgan"; qolgan oddiy
ro'yxat (masalan IBD varag'i) — "ro'yxatda (rekvizitsiz)". Kirill nomlar lotinga o'giriladi (solishtirish uchun).
tekshir: hujjatdagi qo'shtirnoqli va "... siyosati/tartibi/nizomi/..." ko'rinishidagi havolalarni ajratadi va reestrdan
eng yaqin yozuvni topadi: MOS / NOMI FARQ QILADI (rasmiy nomi berilgan) / KUCHINI YO'QOTGAN / REESTRDA YO'Q.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KIR = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo", "ж": "j", "з": "z", "и": "i",
       "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
       "у": "u", "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sh", "ъ": "'", "ы": "i", "ь": "",
       "э": "e", "ю": "yu", "я": "ya", "ў": "o'", "қ": "q", "ғ": "g'", "ҳ": "h"}
SHABLON = [r"o'?zbekiston respublikasi", r"aksiyadorlik tijorat", r"\"?xalq\s*banki?\"?(\s*atb)?", r"atb", r"bankning",
           r"bank\b", r"markaziy apparati(ning)?", r"tizimida", r"qoshidagi", r"tomonidan", r"to'g'risida(gi)?",
           r"bo'yicha", r"\bva\b", r"\bning\b", r"ga kiritil\w*", r"o'zgartirish\w*", r"qo'shimcha\w*"]
TURLAR = r"siyosat|tartib|nizom|yo'riqnoma|metodika|metodologiya|reglament|qoidalar|strategiya|standart|dastur|konsepsiya|yo'l xaritasi"


def lotin(s):
    s = str(s or "")
    out = []
    for ch in s:
        lo = ch.lower()
        if lo in KIR:
            t = KIR[lo]
            out.append(t.capitalize() if ch != lo and t else t)
        else:
            out.append(ch)
    return "".join(out)


def norm(s):
    s = lotin(s).lower()
    s = re.sub(r"[‘’`ʻʼ´]", "'", s)
    s = re.sub(r"[«»“”„\"]", " ", s)
    for p in SHABLON:
        s = re.sub(p, " ", s)
    s = re.sub(r"[^a-z0-9' ]", " ", s)
    return " ".join(s.split())


def ildizlar(s):
    return {w.replace("'", "")[:6] for w in norm(s).split() if len(w.replace("'", "")) >= 4}


def yol(bank):
    d = ROOT / "korxonalar" / bank / "04_Reestr"
    d.mkdir(parents=True, exist_ok=True)
    return d / "hujjatlar_reestri.jsonl"


def import_xlsx(fayl, bank):
    import openpyxl
    wb = openpyxl.load_workbook(fayl, read_only=True, data_only=True)
    yozuvlar = []
    for ws in wb.worksheets:
        rows = [r for r in ws.iter_rows(values_only=True)]
        sarl = " ".join(str(c) for r in rows[:6] for c in r if c).lower()
        kuchsiz = bool(re.search(r"кучини йўқот|kuchini yo'qot|kuchini yo‘qot", ws.title.lower()))
        toliq = ("ҳужжат номи" in sarl or "hujjat nomi" in sarl) and ("тури" in sarl or "turi" in sarl)
        for r in rows:
            if not r or not isinstance(r[0], (int, float)) or not r[1]:
                continue
            nom = " ".join(str(r[1]).split()).strip(" \"“”")
            if toliq:
                y = {"nom": nom, "nom_lotin": lotin(nom), "turi": lotin(r[2]).strip(), "raqami": str(r[3] or "").strip(),
                     "sana": str(r[4] or "").strip(), "organ": lotin(" ".join(str(r[5] or "").split())),
                     "qaror": " ".join(str(r[6] or "").split()), "ozgartirishlar": r[7] or 0,
                     "asos": lotin(" ".join(str(r[8] or "").split())), "bolinma": " ".join(str(r[9] or "").split())}
            else:
                y = {"nom": nom, "nom_lotin": lotin(nom)}
            y["holat"] = "kuchini yo'qotgan" if kuchsiz else ("amalda" if toliq else "ro'yxatda (rekvizitsiz)")
            y["varaq"] = ws.title
            yozuvlar.append(y)
    p = yol(bank)
    p.write_text("".join(json.dumps(y, ensure_ascii=False) + "\n" for y in yozuvlar), encoding="utf-8")
    md = [f"# {bank}: ichki hujjatlar reestri (manba: {Path(fayl).name})\n",
          "| № | Hujjat nomi (lotin) | Turi | Raqami | Sana | Organ | Holat | Bo'linma |", "|---|---|---|---|---|---|---|---|"]
    for i, y in enumerate(yozuvlar, 1):
        md.append("| " + " | ".join(str(x).replace("|", "/") for x in [i, y["nom_lotin"], y.get("turi", ""), y.get("raqami", ""),
                  y.get("sana", ""), y.get("organ", ""), y["holat"], y.get("bolinma", "")]) + " |")
    p.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    from collections import Counter
    print(f"{len(yozuvlar)} yozuv -> {p}", dict(Counter(y["holat"] for y in yozuvlar)))


def havolalar(matn):
    """Hujjatdagi ichki hujjat nomlari: qo'shtirnoq ichidagilar va '... [tur]i' ko'rinishidagilar."""
    topil = []
    for m in re.finditer(r"[«“\"]([^«»“”\"\n]{12,250})[»”\"]", matn):
        if re.search(TURLAR, lotin(m.group(1)).lower().replace("‘", "'").replace("’", "'")):
            topil.append((m.start(), m.group(1).strip()))
    lot = matn.replace("‘", "'").replace("’", "'").replace("ʻ", "'")
    for m in re.finditer(r"(?:Bankning|Bank|IBD(?:ning)?)\s+((?:[A-ZO'G'][\w'‑-]*\s+){0,2}(?:[\w'‑-]+\s+){1,9}?(?:siyosati|tartibi|nizomi|yo'riqnomasi|metodikasi|metodologiyasi|reglamenti|qoidalari|strategiyasi))\b", lot):
        topil.append((m.start(), m.group(1).strip()))
    # bir xil nomlarni birlashtirish
    ko = {}
    for pos, n in topil:
        k = norm(n)
        if k and k not in ko:
            ko[k] = (pos, n)
    return sorted(ko.values())


def tekshir(fayl, bank, chiqish=None):
    p = yol(bank)
    if not p.exists():
        print(f"OGOHLANTIRISH: {p} yo'q — avval bankning rasmiy hujjatlar reestrini import qiling.")
        return
    reestr = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    for y in reestr:
        y["_i"] = ildizlar(y["nom"])
    matn = Path(fayl).read_text(encoding="utf-8")
    qatorlar = matn[:]
    natija = []
    for pos, n in havolalar(matn):
        q = qatorlar.count("\n", 0, pos) + 1
        hi = ildizlar(n)
        if len(hi) < 2 or re.search(r"banklarida|markaziy bank|vazirlar mahkamasi|qonun", norm(n)):
            continue  # tashqi normativ hujjat (MB, VM, qonun) — bu reestrda emas
        eng = []
        for y in reestr:
            if not y["_i"]:
                continue
            k = len(hi & y["_i"])
            s = k / len(hi | y["_i"]) if hi | y["_i"] else 0
            qamrov = k / len(hi)
            eng.append((s, qamrov, y))
        eng.sort(key=lambda t: -(t[0] + 0.5 * t[1]))
        s, qamrov, y = eng[0] if eng else (0, 0, None)
        ball = s
        if s >= 0.75:
            hukm = "KUCHINI YO'QOTGAN" if y["holat"] == "kuchini yo'qotgan" else "MOS"
        elif s >= 0.4 or qamrov >= 0.7:
            hukm = "KUCHINI YO'QOTGAN (ehtimol)" if y["holat"] == "kuchini yo'qotgan" else "NOMI FARQ QILADI"
        else:
            hukm, y = "REESTRDA YO'Q", None
        natija.append((q, n, hukm, ball, y))
    tartib = {"KUCHINI YO'QOTGAN": 0, "KUCHINI YO'QOTGAN (ehtimol)": 1, "REESTRDA YO'Q": 2, "NOMI FARQ QILADI": 3, "MOS": 4}
    natija.sort(key=lambda t: (tartib[t[2]], t[0]))
    from collections import Counter
    c = Counter(t[2] for t in natija)
    chiq = [f"# Hujjatda keltirilgan ichki hujjatlar ↔ {bank} rasmiy reestri\n",
            f"Reestr: {len(reestr)} yozuv ({p.relative_to(ROOT)}). Hujjatda topilgan havolalar: {len(natija)}. "
            + ", ".join(f"{k}: {v}" for k, v in c.items()) + ".\n",
            "Skript nomzod beradi; har birini ichki-normativ-tekshiruvchi tekshiradi. NOMI FARQ QILADI — rasmiy nomni "
            "TAHRIR qilish kerakmi ko'r (bir xil hujjat bo'lsa). REESTRDA YO'Q — hujjat hali qabul qilinmagan, boshqa nom bilan "
            "qabul qilingan yoki xato (IZOH). KUCHINI YO'QOTGAN — amaldagi hujjatga almashtirilsin.\n",
            "| Qator | Hujjatdagi nom | Hukm | O'xshashlik | Reestrdagi nom | Turi, raqami, sana, organ | Holat |",
            "|---|---|---|---|---|---|---|"]
    for q, n, hukm, ball, y in natija:
        rek = ", ".join(x for x in [y.get("turi", ""), y.get("raqami", ""), y.get("sana", ""), y.get("organ", "")] if x) if y else ""
        chiq.append("| " + " | ".join(str(x).replace("|", "/") for x in [q, n[:150], hukm, f"{ball:.0%}",
                    (y["nom_lotin"][:160] if y else "—"), rek, (y["holat"] if y else "—")]) + " |")
    out = "\n".join(chiq) + "\n"
    if chiqish:
        Path(chiqish).write_text(out, encoding="utf-8")
        print(f"{len(natija)} havola ({dict(c)}) -> {chiqish}")
    else:
        print(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("buyruq", choices=["import", "tekshir"])
    ap.add_argument("fayl")
    ap.add_argument("--bank", required=True)
    ap.add_argument("-o", "--chiqish")
    a = ap.parse_args()
    import_xlsx(a.fayl, a.bank) if a.buyruq == "import" else tekshir(a.fayl, a.bank, a.chiqish)
