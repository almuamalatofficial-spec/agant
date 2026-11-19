#!/usr/bin/env python3
"""Hujjatlarni agentlar qidira oladigan .md matnga aylantiradi.

Qo'llab-quvvatlanadi: PDF (matnli va skanerlangan - OCR), DOCX, DOC, RTF, ODT, TXT,
XLSX, XLS, PPTX, VSDX, PNG, JPG.

Foydalanish:
    python3 scripts/bazani_tayyorla.py                      # bilim/ va korxonalar/ hammasi
    python3 scripts/bazani_tayyorla.py korxonalar/01_Xalq_bank
    python3 scripts/bazani_tayyorla.py hujjatlar/shartnoma.docx
    python3 scripts/bazani_tayyorla.py --ocrsiz              # skanerlangan PDF'larni o'tkazib yuborish

Har bir `fayl.pdf` yonida `fayl.pdf.md` yaratiladi. Fayl o'zgarmagan bo'lsa qayta ishlanmaydi.
"""
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMATLAR = {".pdf", ".docx", ".doc", ".rtf", ".odt", ".txt", ".html", ".htm", ".xlsx", ".xls",
             ".pptx", ".vsdx", ".png", ".jpg", ".jpeg"}
OCR_TILLAR = "uzb+uzb_cyrl+rus+eng"
OCR = "--ocrsiz" not in sys.argv


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=1800, **kw)


def ocr_rasm(p: Path) -> str:
    import os
    env = dict(os.environ, OMP_THREAD_LIMIT="1")  # parallel jarayonlarda oqimlar to'qnashmasin
    return subprocess.run(["tesseract", str(p), "-", "-l", OCR_TILLAR, "--psm", "3"],
                          capture_output=True, text=True, timeout=600, env=env).stdout


def pdf_matn(p: Path) -> str:
    matn = run(["pdftotext", "-layout", str(p), "-"]).stdout
    sahifalar = max(1, matn.count("\f"))
    if len(matn.strip()) / sahifalar > 200:  # matnli PDF
        return matn
    if not OCR:
        return "> OGOHLANTIRISH: skanerlangan PDF — OCR o'tkazib yuborildi (--ocrsiz).\n\n" + matn
    with tempfile.TemporaryDirectory() as d:  # skanerlangan PDF -> OCR
        run(["pdftoppm", "-r", "150", "-gray", "-png", str(p), f"{d}/s"])
        qismlar = []
        for i, rasm in enumerate(sorted(Path(d).glob("s-*.png")), 1):
            qismlar.append(f"\n\n<!-- sahifa {i} -->\n" + ocr_rasm(rasm))
    return "> Eslatma: matn OCR orqali olingan — raqam va atamalarda xato bo'lishi mumkin, asl PDF bilan solishtiring.\n" + "".join(qismlar)


def html_matn(p: Path) -> str:
    """Veb-sahifa (lex.uz va boshqalar) -> matn. lex.uz da faqat hujjat matni olinadi."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(p.read_bytes(), "lxml")
    for t in soup(["script", "style", "noscript", "nav", "header", "footer", "form", "button"]):
        t.decompose()
    for t in soup.select(".lx_no_select, .COMMENT, .INDEXES_ON_REF, .CHANGES_ORIGINS, .dropdown-menu"):
        t.decompose()
    bandlar = soup.select(".ACT_TEXT, .ACT_TITLE, .CLAUSE_DEFAULT, .TEXT_HEADER_DEFAULT, .ACT_FORM, .ACT_EMBLEM_TITLE, .BY_DEFAULT, .ACT_TITLE_APPL")
    if not bandlar:
        bandlar = [t for t in soup.select(".lx_elem") if not t.find_parent(class_="lx_elem")]
    if bandlar:
        qatorlar = [b.get_text(" ", strip=True) for b in bandlar]
    else:
        qatorlar = [ln.strip() for ln in (soup.body or soup).get_text("\n").splitlines()]
    tugma = re.compile(r"(Ҳужжатга таклиф юбориш|Аудиони тинглаш|Ҳужжат элементидан ҳавола олиш|Hujjatga taklif yuborish|Audioni tinglash|Hujjat elementidan havola olish)\s*")
    qatorlar = [tugma.sub("", q).strip() for q in qatorlar]
    return "\n\n".join(q for q in qatorlar if q)


def docx_matn(p: Path) -> str:
    out = run(["pandoc", "-f", "docx", str(p), "-t", "gfm", "--wrap=none", "--track-changes=all"])
    if out.returncode != 0:
        raise RuntimeError(out.stderr[:300])
    return out.stdout


def soffice(p: Path, fmt: str, d: str) -> Path:
    run(["soffice", f"-env:UserInstallation=file://{d}/lo", "--headless",
         "--convert-to", fmt, "--outdir", d, str(p)])
    natija = [f for f in Path(d).glob(f"*.{fmt.split(':')[0]}")]
    if not natija:
        raise RuntimeError(f"soffice {fmt} ga aylantira olmadi")
    return natija[0]


def xlsx_matn(p: Path) -> str:
    import openpyxl
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    qism = []
    for ws in wb.worksheets:
        qism.append(f"\n## Varaq: {ws.title}\n")
        for row in ws.iter_rows(values_only=True):
            cells = ["" if c is None else str(c).replace("\n", " ").replace("|", "/") for c in row]
            if any(cells):
                qism.append("| " + " | ".join(cells) + " |")
    return "\n".join(qism)


def pptx_matn(p: Path) -> str:
    from pptx import Presentation
    qism = []
    for i, slide in enumerate(Presentation(p).slides, 1):
        qism.append(f"\n## Slayd {i}\n")
        for sh in slide.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip():
                qism.append(sh.text_frame.text)
    return "\n".join(qism)


def aylantir(p: Path):
    chiqish = p.with_name(p.name + ".md")
    if chiqish.exists() and chiqish.stat().st_mtime >= p.stat().st_mtime:
        if not (OCR and "OCR o'tkazib yuborildi" in chiqish.read_text(encoding="utf-8", errors="ignore")[:3000]):
            return None
    ext = p.suffix.lower()
    with tempfile.TemporaryDirectory() as d:
        if ext == ".pdf":
            matn = pdf_matn(p)
        elif ext == ".docx":
            matn = docx_matn(p)
        elif ext in (".doc", ".rtf", ".odt"):
            bosh = p.read_bytes()[:4096]
            if bosh.startswith(b"PK") and ext == ".doc":  # aslida .docx
                matn = docx_matn(p)
            elif b"<html" in bosh.lower() or b"<!doctype html" in bosh.lower():  # lex.uz HTML eksporti
                out = run(["pandoc", "-f", "html", "-t", "gfm-raw_html", "--wrap=none", str(p)])
                if out.returncode != 0:
                    raise RuntimeError(out.stderr[:300])
                matn = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", out.stdout)
            else:
                matn = docx_matn(soffice(p, "docx", d))
        elif ext in (".html", ".htm"):
            matn = html_matn(p)
        elif ext == ".txt":
            matn = p.read_text(encoding="utf-8", errors="replace")
        elif ext == ".xlsx":
            matn = xlsx_matn(p)
        elif ext == ".xls":
            matn = xlsx_matn(soffice(p, "xlsx", d))
        elif ext == ".pptx":
            matn = pptx_matn(p)
        elif ext == ".vsdx":
            matn = pdf_matn(soffice(p, "pdf", d))
        else:  # rasm
            matn = "> Eslatma: rasm OCR orqali o'qildi.\n\n" + ocr_rasm(p) if OCR else ""
    chiqish.write_text(f"<!-- manba: {rel(p)} -->\n# {p.stem}\n\n{matn}", encoding="utf-8")
    return len(matn.strip())


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    nishonlar = [Path(a).resolve() for a in args] or [ROOT / "bilim", ROOT / "korxonalar"]
    fayllar = []
    for n in nishonlar:
        if n.is_file():
            fayllar.append(n)
        elif n.is_dir():
            fayllar += sorted(f for f in n.rglob("*") if f.is_file() and f.suffix.lower() in FORMATLAR)
    yangi = xato = 0
    boshlar = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        ishlar = {ex.submit(aylantir, f): f for f in fayllar}
        for fut in as_completed(ishlar):
            f = ishlar[fut]
            try:
                n = fut.result()
                if n is not None:
                    yangi += 1
                    print(f"  + {rel(f)}", flush=True)
                    if n < 50:
                        boshlar.append(f)
            except Exception as e:  # bitta buzuq fayl butun jarayonni to'xtatmasin
                xato += 1
                print(f"  ! {rel(f)}: {e}", file=sys.stderr, flush=True)
    print(f"Jami: {len(fayllar)} fayl, {yangi} ta yangilandi, {xato} ta xato.")
    for f in boshlar:
        print(f"  (matn deyarli yo'q) {rel(f)}")


if __name__ == "__main__":
    main()
