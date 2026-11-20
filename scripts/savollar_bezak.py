# -*- coding: utf-8 -*-
"""Savollar.docx ni guruhlarga bo'lish, Manba ustuni, AAOIFI belgisi, ilovalar."""
import copy, json, re, sys
from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

docx_yol, json_yol, kochir_yol = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.loads(Path(json_yol).read_text(encoding="utf-8"))
S = d["savollar"]
doc = Document(docx_yol)
body = doc.element.body


def soya(cell, rang):
    tcPr = cell._tc.get_or_add_tcPr()
    for e in tcPr.findall(qn("w:shd")):
        tcPr.remove(e)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), rang)
    tcPr.append(shd)


def para_after(el, text, style=None, bold=False, size=None):
    p = doc.add_paragraph(style=style)
    if text:
        r = p.add_run(text); r.bold = bold
        if size: r.font.size = Pt(size)
    el.addnext(p._p)
    return p._p


t = doc.tables[0]
# Bosqich -> Manba
hdr = t.rows[0].cells
for c in hdr:
    if c.text.strip() == "Bosqich":
        for r in c.paragraphs[0].runs:
            r.text = "Manba" if r.text.strip() == "Bosqich" else r.text
i_manba = [c.text.strip() for c in hdr].index("Manba")

# AAOIFI belgisi: Manba katagini och to'q sariq rangga bo'yash
for row, s in zip(t.rows[1:], S):
    if s["aaoifi_kutilmoqda"]:
        soya(row.cells[i_manba], "F8CBAD")

# Kirish matni (jadvaldan oldin)
oldingi = t._tbl.getprevious()
kirish = [
    ("Savollar besh guruhga bo‘lingan: 1) IMK (shariat) qarori kerak; 2) yurist qarori kerak; 3) bank (muallif) ma’lumoti kerak; "
     "4) boshqa hujjatlarga ta’sir, bank tasdiqlashi kerak; 5) bazada yo‘q hujjatlar, bank taqdim etishi kerak. "
     "Har guruh ichida avval KRITIK va YUQORI savollar berilgan.", False),
    ("«Manba» ustunida qizg‘ish rangdagi kataklar AAOIFI standartiga tayangan savollar. AAOIFI bo‘yicha alohida tekshiruv hali o‘tkazilmagan: "
     "bu savollarga hozir javob berish mumkin, lekin javob keyin AAOIFI matni bilan solishtiriladi.", False),
    ("Tavsiya ustunidagi taklif maslahat xarakterida. Shariat masalasida yakuniy qarorni Bank IMK, huquqiy masalada yurist beradi.", False),
]
el = oldingi
for txt, b in kirish:
    el = para_after(el, txt, bold=b)

# Jadvalni guruhlar bo'yicha bo'lish
guruhlar = []
for idx, s in enumerate(S, 1):
    if not guruhlar or guruhlar[-1][0] != s["guruh"]:
        guruhlar.append([s["guruh"], []])
    guruhlar[-1][1].append(idx)

asl = t._tbl
ENI = [0.8, 1.0, 1.6, 1.8, 1.4, 5.0, 4.5, 4.0, 3.2, 4.2]
grid = asl.find(qn("w:tblGrid"))
for gc, w in zip(grid.findall(qn("w:gridCol")), ENI):
    gc.set(qn("w:w"), str(int(w * 567)))
tblPr = asl.find(qn("w:tblPr"))
lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
joy = asl
for nom, qatorlar in guruhlar:
    h = doc.add_heading(f"{nom} ({len(qatorlar)} ta savol)", level=2)
    joy.addnext(h._p); joy = h._p
    yangi = copy.deepcopy(asl)
    trs = yangi.findall(qn("w:tr"))
    for k, tr in enumerate(trs):
        if k == 0 or k in qatorlar:
            continue
        yangi.remove(tr)
    joy.addnext(yangi); joy = yangi
asl.getparent().remove(asl)

# ----- Ilova 1: Ko'chirishlar (qisqa)
oxir = joy
p = doc.add_heading("Ilova 1. Boshqa hujjatlarga ko‘chiriladigan qoidalar (qisqa ro‘yxat)", level=2)
oxir.addnext(p._p); oxir = p._p
oxir = para_after(oxir, "Bu qoidalar shu hujjatga kiritilmaydi. Tasdiqdan keyin bankning o‘zgartirish navbatiga tushadi. "
                         "To‘liq ro‘yxat va havola matnlari «10_kochirishlar.md» faylida.")
def kochir_qatorlar(matn):
    """10_kochirishlar.md jadvallaridan (№, Mazmun, Qaysi hujjatga, Tasdiqlovchi organ) qatorlari.
    Ustunlar sarlavha bo'yicha topiladi; qator raqami K1/M1 yoki oddiy 1 bo'lishi mumkin."""
    out, sarl = [], None
    for l in matn.splitlines():
        if not l.strip().startswith("|"):
            sarl = None
            continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if set("".join(c)) <= set("-: "):
            continue
        if sarl is None:
            past = [x.lower() for x in c]
            def top(*soz):
                for i, x in enumerate(past):
                    if any(w in x for w in soz):
                        return i
                return None
            sarl = (top("mazmun", "nima"), top("qaysi hujjat", "hujjatga", "qabul qiluvchi"), top("tasdiqlovchi", "organ"))
            continue
        if not re.match(r"^(?:[KM]\d+|\d+)$", c[0]):
            continue
        nom = c[0]
        g = lambda i: c[i] if i is not None and i < len(c) else ""
        out.append((nom, g(sarl[0]), g(sarl[1]), g(sarl[2])))
    return out


qq = kochir_qatorlar(Path(kochir_yol).read_text(encoding="utf-8"))
tab = doc.add_table(rows=1, cols=4)
tab.style = "Table Grid"
for i, s in enumerate(["№", "Mazmun", "Qaysi hujjatga", "Tasdiqlovchi organ"]):
    tab.rows[0].cells[i].text = ""
    tab.rows[0].cells[i].paragraphs[0].add_run(s).bold = True
    soya(tab.rows[0].cells[i], "D9E2F3")
tozala = lambda x: re.sub(r"`([^`]*)`", r"\1", x).replace("**", "")
for r in qq:
    row = tab.add_row()
    for i, v in enumerate(r):
        row.cells[i].text = tozala(v)
oxir.addnext(tab._tbl); oxir = tab._tbl

# ----- Ilova 2: Bazadan javob topildi
p = doc.add_heading("Ilova 2. Bazadan javob topilgan masalalar (savol berilmadi)", level=2)
oxir.addnext(p._p); oxir = p._p
for txt in d["bazadan_javob"]:
    oxir = para_after(oxir, "• " + txt)

oxir = para_after(oxir, "")
oxir = para_after(oxir, "Eslatma: ushbu savollar va takliflar maslahat xarakterida. Yakuniy fatvo Bank Islomiy moliya kengashi (IMK), "
                         "yakuniy huquqiy xulosa litsenziyali yurist tomonidan beriladi.")
doc.save(docx_yol)
print("guruhlar:", [(g, len(q)) for g, q in guruhlar], "kochirish:", len(qq))
