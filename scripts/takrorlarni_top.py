#!/usr/bin/env python3
"""Hujjatdagi takrorlangan (aynan yoki deyarli bir xil) jumlalarni topadi.

    python3 scripts/takrorlarni_top.py <hujjat.md> [-o natija.md] [--chegara 0.85] [--min-soz 6]

Har bir jumla uchun joyi (qator va eng yaqin sarlavha/band) aniqlanadi. Natija — guruhlar jadvali:
har guruhda bir xil (yoki o'xshashlik >= chegara) jumlalar va ularning joylari. Bu xom ro'yxat:
qaysi takrorni olib tashlash kerakligini `takror-tozalovchi` agenti hal qiladi.
"""
import argparse
import re
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

SARLAVHA = re.compile(r"^\s*(#{1,6})\s+(.*)")
BAND = re.compile(r"^\s*(\d+(?:\.\d+)*)[.)]?\s")


def norm(s: str) -> str:
    s = s.lower().replace("ʻ", "'").replace("‘", "'").replace("’", "'").replace("ʼ", "'")
    s = re.sub(r"[*_`|>#\[\]()\"«»“”]", " ", s)
    s = re.sub(r"\b\d+(\.\d+)*\b", "#", s)  # raqamlar farqi takrorni yashirmasin
    return re.sub(r"\s+", " ", s).strip(" .;:,")


def jumlalar(matn: str):
    joy = "—"
    for i, qator in enumerate(matn.splitlines(), 1):
        m = SARLAVHA.match(qator)
        if m:
            joy = re.sub(r"\s+", " ", m.group(2))[:70]
            continue
        b = BAND.match(qator)
        band = b.group(1) if b else None
        toza = qator.strip().strip("|").strip()
        if not toza or set(toza) <= set("-|: "):
            continue
        qismlar = [toza] if toza.count("|") >= 2 else re.split(r"(?<=[.!?;])\s+(?=[A-ZА-ЯЎҚҒҲO‘])", toza)
        for j in qismlar:
            if toza.count("|") >= 2:
                for kat in [c.strip() for c in toza.split("|")]:
                    if len(kat.split()) >= 6:
                        yield i, (f"{band} " if band else "") + joy, kat
            else:
                yield i, (f"{band} " if band else "") + joy, j.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hujjat")
    ap.add_argument("-o", "--chiqish")
    ap.add_argument("--chegara", type=float, default=0.85)
    ap.add_argument("--min-soz", type=int, default=6)
    a = ap.parse_args()

    j = [(q, joy, t, norm(t)) for q, joy, t in jumlalar(Path(a.hujjat).read_text(encoding="utf-8"))]
    j = [x for x in j if len(x[3].split()) >= a.min_soz]

    # 1) aynan takrorlar
    aynan = defaultdict(list)
    for x in j:
        aynan[x[3]].append(x)
    guruhlar = [(1.0, v) for v in aynan.values() if len(v) > 1]
    yakka = [v[0] for v in aynan.values() if len(v) == 1]

    # 2) deyarli bir xil: umumiy 4-so'zli bo'laklar orqali nomzodlar, so'ng SequenceMatcher
    indeks = defaultdict(set)
    for k, x in enumerate(yakka):
        w = x[3].split()
        for s in {" ".join(w[i:i + 4]) for i in range(max(1, len(w) - 3))}:
            indeks[s].add(k)
    juft = defaultdict(int)
    for ids in indeks.values():
        if 1 < len(ids) <= 30:
            ids = sorted(ids)
            for p in range(len(ids)):
                for r in range(p + 1, len(ids)):
                    juft[(ids[p], ids[r])] += 1
    ota = list(range(len(yakka)))

    def top(x):
        while ota[x] != x:
            ota[x] = ota[ota[x]]
            x = ota[x]
        return x

    oxshash = {}
    for (p, r), n in juft.items():
        if n < 2:
            continue
        sp, sr = yakka[p][3], yakka[r][3]
        if min(len(sp), len(sr)) / max(len(sp), len(sr)) < a.chegara - 0.1:
            continue
        k = SequenceMatcher(None, sp, sr, autojunk=False).ratio()
        if k >= a.chegara:
            ota[top(p)] = top(r)
            oxshash[top(r)] = min(oxshash.get(top(r), 1.0), k)
    tuda = defaultdict(list)
    for k in range(len(yakka)):
        tuda[top(k)].append(k)
    for ildiz, ks in tuda.items():
        if len(ks) > 1:
            guruhlar.append((round(min(oxshash.get(top(ildiz), 1.0), 0.99), 2), [yakka[k] for k in ks]))

    guruhlar.sort(key=lambda g: (-len(g[1]), g[1][0][0]))
    chiq = [f"# Takrorlar ro'yxati (avtomatik): {Path(a.hujjat).name}\n",
            f"Jami guruh: {len(guruhlar)} (aynan: {sum(1 for g in guruhlar if g[0] == 1.0)}, "
            f"deyarli bir xil ≥{a.chegara}: {sum(1 for g in guruhlar if g[0] < 1.0)}). "
            f"Raqamlar farqi hisobga olinmaydi.\n"]
    for n, (k, v) in enumerate(guruhlar, 1):
        chiq.append(f"\n## T{n} — {'aynan' if k == 1.0 else f'o‘xshash ({k:.0%})'}, {len(v)} marta\n")
        for q, joy, t, _ in sorted(v):
            chiq.append(f"- qator {q} · {joy}: {t[:400]}")
    natija = "\n".join(chiq) + "\n"
    if a.chiqish:
        Path(a.chiqish).write_text(natija, encoding="utf-8")
        print(f"{len(guruhlar)} ta guruh -> {a.chiqish}")
    else:
        print(natija)


if __name__ == "__main__":
    main()
