#!/usr/bin/env python3
"""Asl Word hujjatdagi (bank tomonidan qoldirilgan) izohlarni ajratadi: muallif, sana, izoh matni, izoh qo'yilgan matn.

    python3 scripts/izohlarni_ajrat.py [asl.docx] -o [I]/00c_bank_izohlari.md [--json [I]/00c_bank_izohlari.json]

Izohlar B1, B2, ... deb raqamlanadi. Har biriga tekshiruvda javob berilishi shart (orkestrator nazorat qiladi).
Muallifi sozlamalardagi `word_muallif` (bizning sharhlovchi) bo'lgan izohlar chiqarib tashlanadi.
"""
import argparse, json, zipfile
from pathlib import Path
from lxml import etree

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx"); ap.add_argument("-o", "--chiqish", required=True); ap.add_argument("--json")
    a = ap.parse_args()
    soz = Path(__file__).resolve().parent / "sozlamalar.json"
    biz = json.loads(soz.read_text()).get("word_muallif", "") if soz.exists() else ""
    z = zipfile.ZipFile(a.docx)
    if "word/comments.xml" not in z.namelist():
        Path(a.chiqish).write_text("# Bank izohlari\n\nAsl hujjatda izoh yo'q.\n", encoding="utf-8"); print("izoh yo'q"); return
    com = etree.fromstring(z.read("word/comments.xml")); doc = etree.fromstring(z.read("word/document.xml"))
    izoh = {c.get(W + "id"): (c.get(W + "author") or "", (c.get(W + "date") or "")[:10], " ".join(t.text or "" for t in c.iter(W + "t")).strip())
            for c in com.iter(W + "comment")}
    langar, ochiq = {}, set()
    for el in doc.iter():
        if el.tag == W + "commentRangeStart":
            ochiq.add(el.get(W + "id")); langar.setdefault(el.get(W + "id"), "")
        elif el.tag == W + "commentRangeEnd":
            ochiq.discard(el.get(W + "id"))
        elif el.tag == W + "t" and ochiq:
            for i in ochiq:
                langar[i] += el.text or ""
    par = {}
    for p in doc.iter(W + "p"):
        txt = "".join(t.text or "" for t in p.iter(W + "t"))
        for e in p.iter(W + "commentRangeStart"):
            par[e.get(W + "id")] = txt
    qator, js = [], []
    for i, (m, d, t) in sorted(izoh.items(), key=lambda x: int(x[0])):
        if biz and m == biz:
            continue
        n = f"B{len(js) + 1}"
        js.append({"id": n, "muallif": m, "sana": d, "izoh": t, "langar": langar.get(i, "").strip(), "xatboshi": par.get(i, "").strip()})
        qator.append(f"| {n} | {m} | {d} | {t} | {langar.get(i, '').strip()[:200]} | {par.get(i, '').strip()[:250]} |".replace("\n", " "))
    md = ["# Bank izohlari (asl hujjatdagi Word izohlari)\n",
          "Har bir izohga tekshiruvda javob berilishi shart: tegishli agent o'z hisobotida \"Bank izohlariga javob\" bo'limida "
          "(Bn → javob: TAHRIR / IZOH / savol). Savol-yig'uvchi hal qilinmaganlarini savollar fayliga oladi; yakuniy muharrir har biriga Word'da qisqa javob izohi qo'yadi.\n",
          "| № | Muallif | Sana | Izoh | Izoh qo'yilgan matn | Xatboshi |", "|---|---|---|---|---|---|"] + qator
    Path(a.chiqish).write_text("\n".join(md) + "\n", encoding="utf-8")
    if a.json:
        Path(a.json).write_text(json.dumps(js, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(js)} ta bank izohi -> {a.chiqish}")


if __name__ == "__main__":
    main()
