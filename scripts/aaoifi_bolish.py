#!/usr/bin/env python3
"""AAOIFI kitobini standartlar (boblar) bo'yicha alohida PDF va matn fayllariga bo'lish.

    python3 scripts/aaoifi_bolish.py KITOB.pdf --chiqish bilim/00-umumiy/aaoifi/SS [--tur SS|FAS|GS] [--max-mb 9]

Har bir sahifaning boshidagi sarlavhadan standart boshlanishi aniqlanadi ("Shari'ah Standard No. (8)",
"Financial Accounting Standard No. 28", "Governance Standard No. 13"). Kirish/mundarija qismi "00_Kirish"
bo'ladi. Har bir bo'lak: SS-08.pdf + SS-08.md (pdftotext). Bo'lak --max-mb dan katta bo'lsa — qismlarga bo'linadi
(Drive 10 MB chegarasidan pastda qolishi uchun). Natijada README.md: standart → sahifalar → fayl.
"""
import argparse
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader, PdfWriter

NAQSH = {
    "SS": re.compile(r"Shari.?a(?:h)?\s+Standard\s+No\.?\s*\(?\s*(\d{1,3})\s*\)?", re.I),
    "FAS": re.compile(r"Financial\s+Accounting\s+Standard\s+(?:No\.?\s*)?\(?\s*(\d{1,3})\s*\)?", re.I),
    "GS": re.compile(r"Governance\s+Standard\s+(?:No\.?\s*)?\(?\s*(\d{1,3})\s*\)?", re.I),
}


def boshlar(reader, tur, bosh_qator=12):
    """Har sahifa boshidagi (birinchi qatorlar) standart raqami — sarlavha shu yerda bo'ladi."""
    rx = NAQSH[tur]
    natija = []
    for i, p in enumerate(reader.pages):
        try:
            t = p.extract_text() or ""
        except Exception:
            t = ""
        # takrorlangan harflarni (matn qatlami ikki marta) soddalashtirish
        t = re.sub(r"\b(\w+) \1\b", r"\1", t)
        head = "\n".join(t.splitlines()[:bosh_qator])
        m = rx.search(head)
        natija.append(int(m.group(1)) if m else None)
    return natija


def bolaklar(raqamlar):
    """Sahifa sarlavhalaridan standart chegaralari: raqam o'zgargan joyda yangi bo'lak."""
    joriy, bosh, out = "00", 0, []
    for i, r in enumerate(raqamlar):
        if r is not None and f"{r:02d}" != joriy:
            out.append((joriy, bosh, i - 1))
            joriy, bosh = f"{r:02d}", i
    out.append((joriy, bosh, len(raqamlar) - 1))
    return [b for b in out if b[2] >= b[1]]


def yoz(reader, bosh, oxir, yol):
    w = PdfWriter()
    for i in range(bosh, oxir + 1):
        w.add_page(reader.pages[i])
    with open(yol, "wb") as f:
        w.write(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--chiqish", required=True)
    ap.add_argument("--tur", default="SS", choices=list(NAQSH))
    ap.add_argument("--max-mb", type=float, default=9.0)
    a = ap.parse_args()
    out = Path(a.chiqish)
    out.mkdir(parents=True, exist_ok=True)
    r = PdfReader(a.pdf)
    bl = bolaklar(boshlar(r, a.tur))
    jadval = [f"# {Path(a.pdf).name} — {a.tur} bo'yicha bo'lingan ({len(r.pages)} sahifa)\n",
              "| Standart | Sahifalar (PDF) | Fayllar |", "|---|---|---|"]
    for raq, b, e in bl:
        nom = f"{a.tur}-{raq}" if raq != "00" else "00_Kirish"
        fayllar = []
        qism_b = b
        while qism_b <= e:
            qism_e = e
            yol = out / (f"{nom}.pdf" if qism_b == b else f"{nom}_q{len(fayllar)+1}.pdf")
            yoz(r, qism_b, qism_e, yol)
            # juda katta bo'lsa — sahifalarni ikkiga bo'lib qisqartir
            while yol.stat().st_size > a.max_mb * 1024 * 1024 and qism_e > qism_b:
                qism_e = qism_b + (qism_e - qism_b) // 2
                yoz(r, qism_b, qism_e, yol)
            subprocess.run(["pdftotext", "-layout", str(yol), str(yol.with_suffix(".md"))], check=False)
            md = yol.with_suffix(".md")
            if md.exists():
                md.write_text(f"<!-- manba: {Path(a.pdf).name}, PDF sahifalar {qism_b+1}-{qism_e+1} -->\n" + md.read_text(errors="ignore"))
            fayllar.append(yol.name)
            qism_b = qism_e + 1
        jadval.append(f"| {nom} | {b+1}–{e+1} | {', '.join(fayllar)} |")
    (out / "README.md").write_text("\n".join(jadval) + "\n")
    print("\n".join(jadval))


if __name__ == "__main__":
    main()
