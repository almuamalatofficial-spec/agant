#!/usr/bin/env python3
"""Bank qoidalari reestri — hujjatlar o'rtasida VAQT BO'YICHA izchillikni saqlash.

Har bir tasdiqlangan (yoki amaldagi) hujjatning raqamli parametrlari (muddat, %, summa, chegara) va vakolatlari
(kim tasdiqlaydi/qaror qiladi) band raqami bilan `korxonalar/[BANK]/04_Reestr/reestr.jsonl` ga yoziladi.
Yangi hujjat tekshirilganda u reestrdagi BARCHA oldingi hujjatlar bilan solishtiriladi — bir oy oldin
tasdiqlangan hujjatga zid qoida darhol ko'rinadi. Sifatli (raqamsiz) qoidalar — `04_Reestr/QOIDALAR.md` da
(orkestrator tasdiqdan keyin to'ldiradi).

Buyruqlar:
  qosh      python3 scripts/reestr.py qosh [hujjat.md] --bank 02_Aloqa_bank --nom "IBD Hisob siyosati"
                      [--holat tasdiqlangan|amalda|loyiha] [--sana 2026-11-25] [--asos "IMK qarori №12"]
            (shu nomdagi hujjatning eski yozuvlari "almashtirilgan" deb belgilanadi)
  solishtir python3 scripts/reestr.py solishtir [yangi.md] --bank 02_Aloqa_bank [--nom "..."] -o natija.md
            (yangi hujjat ↔ reestrdagi boshqa hujjatlar: ehtimoliy ziddiyatlar, eski hujjat bo'yicha guruhlangan)
  royxat    python3 scripts/reestr.py royxat --bank 02_Aloqa_bank
  boshlash  python3 scripts/reestr.py boshlash --bank 02_Aloqa_bank   (00_Islamic_documents va 03_Yakuniy dagi
            barcha .md matnlardan dastlabki reestr; holati "mavjud")
"""
import argparse
import datetime as dt
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import ziddiyat_xaritasi as zx  # noqa: E402


def yol(bank):
    d = ROOT / "korxonalar" / bank / "04_Reestr"
    d.mkdir(parents=True, exist_ok=True)
    return d / "reestr.jsonl"


def oqi(bank):
    p = yol(bank)
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def yoz(bank, yozuvlar):
    yol(bank).write_text("".join(json.dumps(y, ensure_ascii=False) + "\n" for y in yozuvlar), encoding="utf-8")


def qosh(fayl, bank, nom, holat="tasdiqlangan", sana=None, asos=""):
    matn = Path(fayl).read_text(encoding="utf-8")
    sana = sana or dt.date.today().isoformat()
    eski = oqi(bank)
    for y in eski:
        if y["hujjat"] == nom and y.get("holat") != "almashtirilgan":
            y["holat"] = "almashtirilgan"
            y["almashtirildi"] = sana
    yangi = []
    for tur, qiymat, band, qator, kontekst, sozlar in zx.parametrlar(matn):
        yangi.append({"hujjat": nom, "fayl": str(Path(fayl)), "band": band, "tur": tur, "qiymat": qiymat,
                      "kontekst": kontekst[:300], "sozlar": sorted(sozlar), "holat": holat, "sana": sana, "asos": asos})
    yoz(bank, eski + yangi)
    print(f"{nom}: {len(yangi)} parametr reestrga qo'shildi ({holat}, {sana})")


def solishtir(fayl, bank, nom=None, chiqish=None, chegara=0.3):
    matn = Path(fayl).read_text(encoding="utf-8")
    yangi = zx.parametrlar(matn)
    def asos(n):
        import re as _re
        return _re.sub(r"[^a-z0-9]", "", _re.sub(r"\s*[–-]\s*(tahrirlangan|yakuniy.*|toza)\b.*$", "", (n or "").lower()))
    reestr = [y for y in oqi(bank) if y.get("holat") != "almashtirilgan" and (not nom or asos(y["hujjat"]) != asos(nom))]
    # bandlar bo'yicha organlar to'plami (bir bandda bir nechta organ — "tayyorlaydi/tasdiqlaydi" — ziddiyat emas)
    yangi_org = defaultdict(set)
    for tur, qiymat, band, *_ in yangi:
        if tur == "vakolat":
            yangi_org[band].add(qiymat.replace(" (ota banddan)", ""))
    eski_org = defaultdict(set)
    for y in reestr:
        if y["tur"] == "vakolat":
            eski_org[(y["hujjat"], y["band"])].add(y["qiymat"].replace(" (ota banddan)", ""))
    guruh = defaultdict(list)
    for tur, qiymat, band, qator, kontekst, sozlar in yangi:
        for y in reestr:
            r = zx.juftlik_mosmi(tur, qiymat, sozlar, y["tur"], y["qiymat"], set(y["sozlar"]), chegara)
            if r and tur == "vakolat":
                yo, eo = yangi_org[band], eski_org[(y["hujjat"], y["band"])]
                if yo & eo:  # bir xil organ ikkala bandda ham bor — farq rollar taqsimotida, ziddiyat emas
                    r = None
            if r:
                guruh[y["hujjat"]].append((r[0], tur, band, qiymat, kontekst, y, r[1]))
    jami = sum(len(v) for v in guruh.values())
    chiq = [f"# Hujjatlararo ziddiyat nomzodlari: {Path(fayl).name} ↔ {bank} reestri\n",
            f"Reestrda: {len({y['hujjat'] for y in reestr})} ta hujjat, {len(reestr)} parametr. Yangi hujjatda: {len(yangi)} parametr. "
            f"Nomzodlar: {jami}.\n",
            "Har bir nomzodni ichki-normativ-tekshiruvchi tekshiradi: HAQIQIY ZIDDIYAT / FARQLI MAVZU / ATAYLAB O'ZGARTIRISH "
            "(yangi hujjat eski qoidani o'zgartiradi — unda eski hujjatga o'zgartirish kiritish kerak).\n"]
    for hujjat, items in sorted(guruh.items(), key=lambda kv: -len(kv[1])):
        y0 = items[0][5]
        chiq.append(f"\n## {hujjat} ({y0.get('holat')}, {y0.get('sana')}{', ' + y0['asos'] if y0.get('asos') else ''}) — {len(items)} ta\n")
        items.sort(key=lambda x: -x[0])
        for n, (oxs, tur, band, qiymat, kon, y, umumiy) in enumerate(items, 1):
            chiq.append(f"- **{tur}**, o'xshashlik {oxs:.0%}: YANGI **{band}** → **{qiymat}** ↔ ESKI **{y['band']}** → **{y['qiymat']}**  \n"
                        f"  yangi: …{' '.join(kon.split())[:200]}…  \n  eski: …{' '.join(y['kontekst'].split())[:200]}…")
    natija = "\n".join(chiq) + "\n"
    if chiqish:
        Path(chiqish).write_text(natija, encoding="utf-8")
        print(f"{jami} ta nomzod ({len(guruh)} ta hujjat bilan) -> {chiqish}")
    else:
        print(natija)


def royxat(bank):
    r = oqi(bank)
    d = defaultdict(lambda: [0, "", "", ""])
    for y in r:
        k = (y["hujjat"], y.get("holat"))
        d[k][0] += 1
        d[k][1], d[k][2], d[k][3] = y.get("sana", ""), y.get("asos", ""), y.get("fayl", "")
    print(f"{bank} reestri: {len(r)} yozuv")
    for (h, holat), (n, sana, asos, f) in sorted(d.items(), key=lambda kv: kv[1][1]):
        print(f"  {sana}  {holat:14} {n:4}  {h}  {asos}")


def boshlash(bank):
    b = ROOT / "korxonalar" / bank
    fayllar = sorted(list((b / "00_Islamic_documents").glob("*.md")) + list((b / "03_Yakuniy").glob("*.md")))
    fayllar = [f for f in fayllar if f.name != "README.md" and "Hisobot" not in f.name and "xulosa" not in f.name.lower()]
    for f in fayllar:
        nom = f.name.replace(".docx.md", "").replace(".doc.md", "").replace(".pdf.md", "").replace(".md", "")
        qosh(f, bank, nom, holat="mavjud", sana=dt.date.fromtimestamp(f.stat().st_mtime).isoformat(), asos=f.parent.name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("buyruq", choices=["qosh", "solishtir", "royxat", "boshlash"])
    ap.add_argument("fayl", nargs="?")
    ap.add_argument("--bank", required=True)
    ap.add_argument("--nom")
    ap.add_argument("--holat", default="tasdiqlangan")
    ap.add_argument("--sana")
    ap.add_argument("--asos", default="")
    ap.add_argument("-o", "--chiqish")
    ap.add_argument("--chegara", type=float, default=0.3)
    a = ap.parse_args()
    if a.buyruq == "qosh":
        qosh(a.fayl, a.bank, a.nom or Path(a.fayl).stem, a.holat, a.sana, a.asos)
    elif a.buyruq == "solishtir":
        solishtir(a.fayl, a.bank, a.nom, a.chiqish, a.chegara)
    elif a.buyruq == "royxat":
        royxat(a.bank)
    else:
        boshlash(a.bank)
