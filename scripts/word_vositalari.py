#!/usr/bin/env python3
"""Word bilan ishlash vositalari.

1) Savollar faylini yaratish (javob uchun bo'sh ustun bilan):
   python3 scripts/word_vositalari.py savollar savollar.json Savollar.docx
   savollar.json: {"hujjat": "...", "bank": "...", "sana": "...",
                   "savollar": [{"id": "S1", "bosqich": "03 Shariat", "band": "10.6",
                                 "savol": "...", "kontekst": "...", "variantlar": ["A ...", "B ..."],
                                 "tavsiya": "...", "kimga": "IMK|Yurist|Muallif"}]}

2) To'ldirilgan savollar faylidan javoblarni o'qish:
   python3 scripts/word_vositalari.py javoblar Savollar_javoblar.docx javoblar.json

3) Asl Word hujjatga tahrir rejimida (Track Changes) o'zgartirish kiritish:
   python3 scripts/word_vositalari.py tahrir asl.docx tahrirlar.json natija.docx [--muallif "Al Muamalat AI"]
   tahrirlar.json: [{"id": "E1", "eski": "hujjatdagi aniq matn", "yangi": "yangi matn ('' = o'chirish)",
                     "izoh": "sabab va manba", "band": "10.6"}]
   "sariq": true — o'zgarish sariq fon bilan belgilanadi (izohida ZIDDIYAT / "manba yo'q" bo'lsa — avtomatik).
   "faqat_izoh": true bo'lsa — matn o'zgarmaydi, faqat izoh biriktiriladi (masalan, ochiq savol).
   Har bir tahrir: eski matn o'chirilgan (qizil), yangi matn qo'shilgan (yashil) ko'rinadi, yoniga izoh qo'yiladi.
   Topilmagan tahrirlar natija.docx.hisobot.json da ko'rsatiladi.
"""
import copy
import datetime as dt
import json
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

JAVOB_USTUNI = "JAVOB"


# ---------------------------------------------------------------- savollar
def _soya(cell, rang):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), rang)
    tcPr.append(shd)


def savollar(json_yol, docx_yol):
    d = json.loads(Path(json_yol).read_text(encoding="utf-8"))
    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = sec.page_height, sec.page_width
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, m, Cm(1.5))
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(10)

    doc.add_heading("Aniqlashtirish uchun savollar", level=1)
    doc.add_paragraph(f"Hujjat: {d.get('hujjat', '')}\nBank: {d.get('bank', '')}\nSana: {d.get('sana', dt.date.today().isoformat())}")
    yo = doc.add_paragraph()
    yo.add_run("Qanday to'ldiriladi: ").bold = True
    yo.add_run(f"har bir savol uchun faqat sariq «{JAVOB_USTUNI}» ustuniga qisqa javob yozing — variant harfi (masalan, «A»), "
               "«ha/yo'q», raqam yoki bir-ikki jumla. Boshqa ustunlarni o'zgartirmang. Javob berilmagan savol "
               "bo'yicha hujjatga o'zgartirish kiritilmaydi va u izoh sifatida qoladi.")
    sarlavha = ["№", "ID", "Kimga", "Bosqich", "Band", "Savol", "Kontekst / nega muhim", "Variantlar", "AI tavsiyasi", JAVOB_USTUNI]
    eni = [0.8, 1.0, 1.6, 1.8, 1.4, 5.0, 4.5, 4.0, 3.2, 4.2]
    t = doc.add_table(rows=1, cols=len(sarlavha))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, s in enumerate(sarlavha):
        c = t.rows[0].cells[i]
        c.text = ""
        r = c.paragraphs[0].add_run(s)
        r.bold = True
        _soya(c, "FFE699" if s == JAVOB_USTUNI else "D9E2F3")
    for n, s in enumerate(d["savollar"], 1):
        qiymat = [str(n), s.get("id", f"S{n}"), s.get("kimga", ""), s.get("bosqich", ""), s.get("band", ""),
                  s.get("savol", ""), s.get("kontekst", ""), "\n".join(s.get("variantlar", []) or []),
                  s.get("tavsiya", ""), ""]
        row = t.add_row()
        for i, v in enumerate(qiymat):
            row.cells[i].text = v
            if sarlavha[i] == JAVOB_USTUNI:
                _soya(row.cells[i], "FFF2CC")
    for row in t.rows:
        for i, w in enumerate(eni):
            row.cells[i].width = Cm(w)
    # sarlavha qatori har sahifada takrorlansin
    trPr = t.rows[0]._tr.get_or_add_trPr()
    h = OxmlElement("w:tblHeader")
    h.set(qn("w:val"), "true")
    trPr.append(h)
    doc.save(docx_yol)
    print(f"{len(d['savollar'])} ta savol -> {docx_yol}")


def javoblar(docx_yol, json_yol):
    doc = Document(docx_yol)
    natija, bosh = {}, 0
    for t in doc.tables:
        sar = [c.text.strip() for c in t.rows[0].cells]
        if "ID" not in sar or JAVOB_USTUNI not in sar:
            continue
        i_id, i_j, i_s = sar.index("ID"), sar.index(JAVOB_USTUNI), sar.index("Savol") if "Savol" in sar else None
        for row in t.rows[1:]:
            cells = row.cells
            sid, jav = cells[i_id].text.strip(), cells[i_j].text.strip()
            if not sid:
                continue
            if jav:
                natija[sid] = {"javob": jav, "savol": cells[i_s].text.strip() if i_s is not None else ""}
            else:
                bosh += 1
    Path(json_yol).write_text(json.dumps(natija, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(natija)} ta javob o'qildi, {bosh} ta savol javobsiz -> {json_yol}")


# ---------------------------------------------------------------- tahrir (track changes)
def _norm(s):
    return (s.replace("ʻ", "‘").replace("'", "’").replace("ʼ", "’").replace("`", "‘")
            .replace(" ", " ").replace("“", "\"").replace("”", "\"").replace("«", "\"").replace("»", "\""))


def _paragraflar(doc):
    def ichki(container):
        for p in container.paragraphs:
            yield p
        for t in getattr(container, "tables", []):
            for row in t.rows:
                for cell in row.cells:
                    yield from ichki(cell)
    yield from ichki(doc)


def _runlar(p):
    """Paragrafdagi oddiy matnli runlar (w:r ichida w:t) — tartib bilan."""
    return [r for r in p._p.iter(qn("w:r")) if r.find(qn("w:t")) is not None and r.getparent().tag != qn("w:del")]


def _run_matn(r):
    return "".join(t.text or "" for t in r.findall(qn("w:t")))


def _bol(r, pos):
    """Runni pos belgidan ikkiga bo'lish; o'ng qismni qaytaradi."""
    matn = _run_matn(r)
    chap, ong = matn[:pos], matn[pos:]
    r2 = copy.deepcopy(r)
    for t in r.findall(qn("w:t"))[1:]:
        r.remove(t)
    for t in r2.findall(qn("w:t"))[1:]:
        r2.remove(t)
    t1, t2 = r.find(qn("w:t")), r2.find(qn("w:t"))
    t1.text, t2.text = chap, ong
    for t in (t1, t2):
        t.set(qn("xml:space"), "preserve")
    r.addnext(r2)
    return r2


SARIQ_SOZLAR = re.compile(r"ZIDDIYAT|manba(si)? (bilim bazasida )?yo['’]q|bazada manba yo['’]q|qonunchilikda topilmadi|tekshirish kerak", re.I)


def _sariq(r):
    """Run (w:r) ga sariq fon (highlight) berish."""
    rpr = r.find(qn("w:rPr"))
    if rpr is None:
        rpr = OxmlElement("w:rPr")
        r.insert(0, rpr)
    for h in rpr.findall(qn("w:highlight")):
        rpr.remove(h)
    h = OxmlElement("w:highlight")
    h.set(qn("w:val"), "yellow")
    rpr.append(h)


class Tahrirchi:
    def __init__(self, doc, muallif):
        self.doc, self.muallif = doc, muallif
        self.sana = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.rid = 9000
        self.sariq = False

    def _id(self):
        self.rid += 1
        return str(self.rid)

    def izoh_qoy(self, p, matn_qism, izoh):
        """Matnni o'zgartirmasdan, unga izoh biriktirish."""
        from docx.text.run import Run
        runs = _runlar(p)
        matn = "".join(_run_matn(r) for r in runs)
        i = _norm(matn).find(_norm(matn_qism))
        if i < 0 or not matn_qism:
            return False
        pos, tanlangan = 0, []
        for r in runs:
            n = len(_run_matn(r))
            if pos + n > i and pos < i + len(matn_qism):
                tanlangan.append(r)
            pos += n
        if self.sariq:
            for r in tanlangan:
                _sariq(r)
        self.doc.add_comment([Run(r, p) for r in tanlangan], text=izoh, author=self.muallif, initials="AI")
        return True

    def qol(self, p, eski, yangi, izoh):
        runs = _runlar(p)
        matn = "".join(_run_matn(r) for r in runs)
        i = _norm(matn).find(_norm(eski))
        if i < 0 or not eski:
            return False
        j = i + len(eski)
        # chegaralarda runlarni bo'lish
        pos, tanlangan = 0, []
        for r in list(runs):
            n = len(_run_matn(r))
            bosh, oxir = pos, pos + n
            pos = oxir
            if oxir <= i or bosh >= j:
                continue
            if bosh < i:
                r = _bol(r, i - bosh)
                bosh = i
            if oxir > j:
                _bol(r, j - bosh)
            tanlangan.append(r)
        if not tanlangan:
            return False
        birinchi = tanlangan[0]
        # o'chirish
        dl = OxmlElement("w:del")
        dl.set(qn("w:id"), self._id())
        dl.set(qn("w:author"), self.muallif)
        dl.set(qn("w:date"), self.sana)
        birinchi.addprevious(dl)
        for r in tanlangan:
            for t in r.findall(qn("w:t")):
                t.tag = qn("w:delText")
            dl.append(r)
        oxirgi = dl
        # qo'shish
        if yangi:
            ins = OxmlElement("w:ins")
            ins.set(qn("w:id"), self._id())
            ins.set(qn("w:author"), self.muallif)
            ins.set(qn("w:date"), self.sana)
            r = OxmlElement("w:r")
            rpr = birinchi.find(qn("w:rPr"))
            if rpr is not None:
                r.append(copy.deepcopy(rpr))
            t = OxmlElement("w:t")
            t.text = yangi
            t.set(qn("xml:space"), "preserve")
            r.append(t)
            if self.sariq:
                _sariq(r)
            ins.append(r)
            dl.addnext(ins)
            oxirgi = ins
        # izoh
        if izoh:
            try:
                from docx.text.run import Run
                izoh_runlari = [Run(x, p) for x in oxirgi.iter(qn("w:r"))] or [Run(birinchi, p)]
                self.doc.add_comment(izoh_runlari, text=izoh, author=self.muallif, initials="AI")
            except Exception:
                pass
        return True


def tahrir(asl, tahrir_json, chiqish, muallif="Al Muamalat AI"):
    doc = Document(asl)
    t = Tahrirchi(doc, muallif)
    royxat = json.loads(Path(tahrir_json).read_text(encoding="utf-8"))
    hisobot = {"qollandi": [], "topilmadi": []}
    for e in royxat:
        ok = False
        for p in _paragraflar(doc):
            izoh = f'[{e.get("id", "")}] {e.get("izoh", "")}'.strip()
            t.sariq = bool(e.get("sariq")) or bool(SARIQ_SOZLAR.search(izoh))
            bajar = t.izoh_qoy(p, e["eski"], izoh) if e.get("faqat_izoh") else t.qol(p, e["eski"], e.get("yangi", ""), izoh)
            if bajar:
                ok = True
                break
        (hisobot["qollandi"] if ok else hisobot["topilmadi"]).append(e.get("id"))
    doc.save(chiqish)
    Path(str(chiqish) + ".hisobot.json").write_text(json.dumps(hisobot, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"qo'llandi: {len(hisobot['qollandi'])}, topilmadi: {len(hisobot['topilmadi'])} -> {chiqish}")
    if hisobot["topilmadi"]:
        print("topilmadi:", ", ".join(map(str, hisobot["topilmadi"])))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("savollar", "javoblar", "tahrir"):
        print(__doc__)
        sys.exit(1)
    if a[0] == "savollar":
        savollar(a[1], a[2])
    elif a[0] == "javoblar":
        javoblar(a[1], a[2])
    else:
        m = a[a.index("--muallif") + 1] if "--muallif" in a else "Al Muamalat AI"
        tahrir(a[1], a[2], a[3], m)
