#!/usr/bin/env python3
"""Agent hisobotlaridan barcha iqtiboslarni (qonun moddasi, MB nizomi, AAOIFI standarti, ichki hujjat bandi) ajratib oladi.

    python3 scripts/iqtiboslarni_ajrat.py [I]/02_huquqiy.md [I]/03_*.md ... -o [I]/09b_iqtiboslar_xom.md

Har bir jadval qatoridan "Manba" ustuni (bo'lmasa — butun qator) olinadi va undagi iqtiboslar ajratiladi.
Natija — iqtibos turlari bo'yicha guruhlangan ro'yxat: qaysi hisobot, qaysi topilma (#), iqtibos matni.
Bir xil iqtibos bir necha hisobotda bo'lsa — bitta qatorda birlashtiriladi (tekshirish bir marta).
Tekshirishning o'zini `iqtibos-tekshiruvchi` agenti manba matni bilan bajaradi.
"""
import argparse
import re
from collections import OrderedDict
from pathlib import Path

NAQSH = [
    ("AAOIFI", re.compile(r"\b(?:SS|FAS|GS|ASIFI)\s*[-№]?\s*\d+(?:\s*\(?\s*(?:band|para(?:graph)?|§)?\s*[\d/.]+\)?)?", re.I)),
    ("Qonun/kodeks moddasi", re.compile(r"(?:[A-ZА-ЯЎҚҒҲ][\w‘’'ʻ\- ]{0,40}?(?:kodeks\w*|Qonun\w*|FK|FPK|SK|MK|ІПК|IPK)[^|;]{0,60}?)?\b\d+[¹²³⁴⁵⁶⁷⁸⁹⁰]*(?:-\d+)?\s*-?\s*modda(?:si|ning)?(?:\s+\w+\s*-?\s*qism\w*)?(?:\s+\d+\s*-?\s*band\w*)?", re.U)),
    ("O‘RQ / PF / PQ / VMQ", re.compile(r"\b(?:O['‘’ʻ]?RQ|PF|PQ|VMQ)\s*-?\s*\d+", re.U)),
    ("MB nizomi (ro'yxat raqami)", re.compile(r"\b\d{3,4}\s*-?\s*(?:son\w*|сон\w*)\s+(?:Nizom|nizom|Низом)\w*|(?:ro['‘’ʻ]yxatga olingan raqami|AVda)\D{0,15}\d{3,4}", re.U)),
    ("Ichki hujjat bandi", re.compile(r"(?:Ustav|Siyosat|Reglament|Nizom|Tartib|Tuzilma|Yo['‘’ʻ]riqnoma)\w*\s*,?\s*\d+(?:[.\d]*)\s*-?\s*band\w*(?:\s*[«\"“]?[a-zа-я]\)?[»\"”]?\s*kichik\s*band\w*)?", re.U)),
]


def qatorlar(matn):
    sarlavha, manba_i, n_i = None, None, None
    for q in matn.splitlines():
        if not q.strip().startswith("|"):
            sarlavha = None
            yield None, q
            continue
        hujayra = [h.strip() for h in q.strip().strip("|").split("|")]
        if sarlavha is None:
            sarlavha = [h.lower() for h in hujayra]
            manba_i = next((i for i, h in enumerate(sarlavha) if "manba" in h or "asos" in h), None)
            n_i = 0 if sarlavha and sarlavha[0] in ("#", "№", "n") else None
            continue
        if set("".join(hujayra)) <= set("-: "):
            continue
        raqam = hujayra[n_i] if n_i is not None and n_i < len(hujayra) else "?"
        matn_q = hujayra[manba_i] if manba_i is not None and manba_i < len(hujayra) else " ".join(hujayra)
        yield raqam, matn_q


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hisobotlar", nargs="+")
    ap.add_argument("-o", "--chiqish")
    a = ap.parse_args()
    guruh = OrderedDict((t, OrderedDict()) for t, _ in NAQSH)
    for f in a.hisobotlar:
        q = Path(f).stem.split("_")
        nom = "_".join(q[:2]) if len(q) > 1 and q[1].isdigit() else q[0]
        for raqam, matn in qatorlar(Path(f).read_text(encoding="utf-8")):
            if raqam is None:
                continue
            for tur, rx in NAQSH:
                for m in rx.finditer(matn):
                    k = re.sub(r"\s+", " ", m.group(0)).strip(" ,;.")
                    if len(k) < 3:
                        continue
                    guruh[tur].setdefault(k, set()).add(f"{nom}#{raqam}")
    chiq = ["# Iqtiboslar ro'yxati (avtomatik ajratilgan)\n",
            "Har bir iqtibos manba matni bilan solishtirilishi kerak. Holat: TASDIQLANDI / NOTO'G'RI / TOPILMADI / MANBA BAZADA YO'Q.\n"]
    jami = 0
    for tur, d in guruh.items():
        if not d:
            continue
        chiq.append(f"\n## {tur} ({len(d)})\n\n| № | Iqtibos | Qayerda (hisobot#topilma) |\n|---|---|---|")
        for i, (k, joy) in enumerate(d.items(), 1):
            chiq.append(f"| {i} | {k} | {', '.join(sorted(joy))} |")
        jami += len(d)
    natija = "\n".join(chiq) + f"\n\nJami noyob iqtiboslar: {jami}\n"
    if a.chiqish:
        Path(a.chiqish).write_text(natija, encoding="utf-8")
        print(f"{jami} ta noyob iqtibos -> {a.chiqish}")
    else:
        print(natija)


if __name__ == "__main__":
    main()
