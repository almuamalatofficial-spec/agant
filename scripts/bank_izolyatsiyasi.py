#!/usr/bin/env python3
"""Bank izolyatsiyasi nazorati: hisobotlarda BOSHQA bank hujjatlariga havola bormi?

    python3 scripts/bank_izolyatsiyasi.py [I papkasi] --bank 02_Aloqa_bank [-o natija.md]

Tekshiradi:
  1) boshqa bank papka nomlari (01_Xalq_bank, 03_OTP_bank, …) va bank nomlari (Xalq banki, OTP, Asia Alliance, …);
  2) faqat boshqa bankda mavjud bo'lgan fayl nomlari (korxonalar/[BOSHQA]/** dagi noyob nomlar).
Topilsa — qaysi hisobot, qaysi qator. Orkestrator har bosqichdan keyin ishga tushiradi; topilma bo'lsa agent
hisobotini qayta ishlatadi yoki o'sha topilmalarni olib tashlaydi.
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK_NOMLARI = {
    "01_Xalq_bank": [r"xalq\s*bank", r"xalqbank"],
    "02_Aloqa_bank": [r"aloqa\s*bank", r"aloqabank"],
    "03_OTP_bank": [r"\botp\s*bank", r"otpbank"],  # yolg'iz "OTP" — bir martalik parol ham bo'lishi mumkin
    "04_Asia_Alliance_bank": [r"asia\s*alliance", r"\baab\b"],
}


def nom(f):
    s = f.name
    for e in (".docx.md", ".doc.md", ".pdf.md", ".xlsx.md", ".pptx.md", ".md"):
        if s.endswith(e):
            s = s[: -len(e)]
            break
    return re.sub(r"\.(docx|doc|pdf|xlsx|xls|pptx|vsdx|rtf)$", "", s, flags=re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("papka")
    ap.add_argument("--bank", required=True)
    ap.add_argument("-o", "--chiqish")
    a = ap.parse_args()

    banklar = [d.name for d in (ROOT / "korxonalar").iterdir() if d.is_dir()]
    oz = {nom(f).lower() for f in (ROOT / "korxonalar" / a.bank).rglob("*") if f.is_file()}
    begona = {}
    for b in banklar:
        if b == a.bank:
            continue
        for f in (ROOT / "korxonalar" / b).rglob("*"):
            n = nom(f).lower()
            if f.is_file() and len(n) >= 14 and n not in oz and not re.fullmatch(r"[\d\s._()-]+", n):
                begona[n] = b
    naqsh = [(b, re.compile(rx, re.I)) for b, rxs in BANK_NOMLARI.items() if b != a.bank for rx in rxs]
    naqsh += [(b, re.compile(re.escape(b), re.I)) for b in banklar if b != a.bank]

    topildi = []
    for f in sorted(Path(a.papka).glob("*.md")):
        if f.name.startswith("_") or f.name.startswith("01_") or "xom" in f.name or f.name.startswith("00b_"):
            continue
        for i, q in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            ql = q.lower()
            for b, rx in naqsh:
                if rx.search(q) and not re.search(r"(ishlatilmadi|chiqarib tashlan|foydalanilmadi|olinmadi|TAQIQ|o'qilmadi|o‘qilmadi)", q, re.I):
                    topildi.append((f.name, i, b, rx.pattern, q.strip()[:200]))
            for n, b in begona.items():
                if n in ql:
                    topildi.append((f.name, i, b, f"fayl: {n[:60]}", q.strip()[:200]))
    chiq = [f"# Bank izolyatsiyasi nazorati: {Path(a.papka).name} (bank: {a.bank})\n",
            f"Tekshirilgan hisobotlar: {len([f for f in Path(a.papka).glob('*.md')])}. "
            f"Boshqa banklarning noyob fayl nomlari: {len(begona)}. Topilmalar: {len(topildi)}.\n"]
    if topildi:
        chiq.append("| Hisobot | Qator | Boshqa bank | Belgi | Matn |\n|---|---|---|---|---|")
        for r in topildi:
            chiq.append("| " + " | ".join(str(x).replace("|", "/") for x in r) + " |")
    else:
        chiq.append("✅ Boshqa bank hujjatlariga havola topilmadi.")
    natija = "\n".join(chiq) + "\n"
    if a.chiqish:
        Path(a.chiqish).write_text(natija, encoding="utf-8")
    print(natija if len(natija) < 3000 else natija[:3000] + "\n…")


if __name__ == "__main__":
    main()
