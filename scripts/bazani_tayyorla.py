#!/usr/bin/env python3
"""PDF/DOCX/DOC/RTF/ODT/TXT fayllarni agentlar qidira oladigan .md matnga aylantiradi.

Foydalanish:
    python3 scripts/bazani_tayyorla.py              # butun bilim/ bazasi
    python3 scripts/bazani_tayyorla.py hujjatlar/   # boshqa papka yoki bitta fayl

Har bir `fayl.pdf` yonida `fayl.pdf.md` yaratiladi. Fayl o'zgarmagan bo'lsa qayta ishlanmaydi.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMATLAR = {".pdf", ".docx", ".doc", ".rtf", ".odt", ".txt"}


def pdf_matn(p: Path) -> str:
    out = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True)
    matn = out.stdout
    if len(matn.strip()) < 50:
        matn += "\n\n> OGOHLANTIRISH: PDF skanerlangan rasm bo'lishi mumkin — matn topilmadi, OCR kerak.\n"
    return matn


def docx_matn(p: Path) -> str:
    out = subprocess.run(["pandoc", str(p), "-t", "gfm", "--wrap=none"], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr)
    return out.stdout


def eski_format_matn(p: Path) -> str:  # .doc, .rtf, .odt -> docx -> md
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["soffice", "--headless", "--convert-to", "docx", "--outdir", d, str(p)],
                       capture_output=True, check=True)
        return docx_matn(next(Path(d).glob("*.docx")))


def aylantir(p: Path) -> bool:
    chiqish = p.with_name(p.name + ".md")
    if chiqish.exists() and chiqish.stat().st_mtime >= p.stat().st_mtime:
        return False
    ext = p.suffix.lower()
    if ext == ".pdf":
        matn = pdf_matn(p)
    elif ext == ".docx":
        matn = docx_matn(p)
    elif ext == ".txt":
        matn = p.read_text(encoding="utf-8", errors="replace")
    else:
        matn = eski_format_matn(p)
    chiqish.write_text(f"<!-- manba: {p.relative_to(ROOT)} -->\n# {p.stem}\n\n{matn}", encoding="utf-8")
    return True


def main() -> None:
    nishon = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "bilim"
    fayllar = [nishon] if nishon.is_file() else sorted(
        f for f in nishon.rglob("*") if f.is_file() and f.suffix.lower() in FORMATLAR)
    yangi = xato = 0
    for f in fayllar:
        try:
            if aylantir(f):
                yangi += 1
                print(f"  + {f.relative_to(ROOT)}")
        except Exception as e:  # bitta buzuq fayl butun jarayonni to'xtatmasin
            xato += 1
            print(f"  ! {f.relative_to(ROOT)}: {e}", file=sys.stderr)
    print(f"Jami: {len(fayllar)} fayl, {yangi} ta yangilandi, {xato} ta xato.")
    for papka in sorted((ROOT / "bilim").rglob("*")):
        if papka.is_dir() and not any(x for x in papka.rglob("*.md") if x.name != "README.md"):
            if not any(c.is_dir() for c in papka.iterdir()):
                print(f"  (bo'sh) {papka.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
