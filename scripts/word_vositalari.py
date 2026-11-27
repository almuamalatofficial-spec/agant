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

4) Toza yakuniy versiya (barcha o'zgarishlar qabul qilingan, izohlarsiz):
   python3 scripts/word_vositalari.py toza tahrirlangan.docx toza.docx
5) O'zgarishlar jadvali (Word):
   python3 scripts/word_vositalari.py jadval tahrirlar.json Ozgarishlar_jadvali.docx

3) Asl Word hujjatga tahrir rejimida (Track Changes) o'zgartirish kiritish:
   python3 scripts/word_vositalari.py tahrir asl.docx tahrirlar.json natija.docx [--muallif "Ism Familiya"]  (standart: scripts/sozlamalar.json)
   tahrirlar.json: [{"id": "E1", "band": "10.6", "eski": "hujjatdagi aniq matn", "yangi": "yangi matn ('' = o'chirish)",
                     "izoh": "Word'dagi qisqa, insoniy izoh (1–2 jumla)", "asos": "to'liq texnik asos (jadval uchun)",
                     "manba": "03#2; S5=B", "sariq": false}]
   "sariq": true — o'zgarish sariq fon bilan belgilanadi (izohida ZIDDIYAT / "manba yo'q" bo'lsa — avtomatik).
   "qiyinlik": 1–10 (ixtiyoriy) — izoh vaqti oldingisidan shuncha daqiqa keyin; vaqt tartibi: Metodolog → Yurist → qolganlar (--boshlanish "2026-11-27T09:00"); "vaqt": aniq ISO vaqt.
   "muallif": "Yurist" (ixtiyoriy) — shu tahrir va izoh muallifi; berilmasa --muallif yoki sozlamalar.json dagi standart.
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
_SOZ = json.loads((Path(__file__).resolve().parent / "sozlamalar.json").read_text(encoding="utf-8")) \
    if (Path(__file__).resolve().parent / "sozlamalar.json").exists() else {}
MUALLIF = _SOZ.get("word_muallif", "Reviewer")
INITSIAL = _SOZ.get("word_initsial", "RV")


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
    sarlavha = ["№", "ID", "Kimga", "Bosqich", "Band", "Savol", "Kontekst / nega muhim", "Variantlar", "Tavsiya", JAVOB_USTUNI]
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
        self.initsial = INITSIAL

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
        self._izoh([Run(r, p) for r in tanlangan], izoh)
        return True

    def _izoh(self, runlar, izoh):
        c = self.doc.add_comment(runlar, text=izoh, author=self.muallif, initials=self.initsial)
        try:
            c._comment_elm.set(qn("w:date"), self.sana)
        except Exception:
            pass
        return c

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
                self._izoh(izoh_runlari, izoh)
            except Exception:
                pass
        return True


MUALLIF_TARTIBI = ("Metodolog", "Yurist")  # izohlar vaqt bo'yicha: avval Metodolog, keyin Yurist, oxirida qolganlar


def vaqt_jadvali(royxat, boshlanish=None):
    """"qiyinlik" (1–10) bo'lsa — har izoh oldingisidan qiyinlik daqiqa keyin; mualliflar ketma-ketligi
    MUALLIF_TARTIBI bo'yicha, har muallif ichida ro'yxat tartibida. Natija: {indeks: ISO vaqt}."""
    if not any("qiyinlik" in e for e in royxat):
        return {}
    t0 = dt.datetime.fromisoformat(boshlanish) if boshlanish else dt.datetime.now().replace(second=0, microsecond=0) - dt.timedelta(hours=6)
    def guruh(e):
        m = e.get("muallif") or MUALLIF
        return MUALLIF_TARTIBI.index(m) if m in MUALLIF_TARTIBI else len(MUALLIF_TARTIBI)
    tartib = sorted(range(len(royxat)), key=lambda k: (guruh(royxat[k]), k))
    natija, joriy = {}, t0
    for k in tartib:
        q = max(1, min(10, int(royxat[k].get("qiyinlik", 1) or 1)))
        joriy = joriy + dt.timedelta(minutes=q)
        natija[k] = joriy.strftime("%Y-%m-%dT%H:%M:00Z")
    return natija


def izsiz(doc, oxirgi_muallif=None):
    """AI/skript izlarini olib tashlash: hujjat xossalari."""
    cp = doc.core_properties
    for maydon in ("comments", "keywords", "subject"):
        if "python-docx" in (getattr(cp, maydon) or ""):
            setattr(cp, maydon, "")
    if oxirgi_muallif:
        cp.last_modified_by = oxirgi_muallif
    cp.modified = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)


def tahrir(asl, tahrir_json, chiqish, muallif=None, boshlanish=None):
    doc = Document(asl)
    t = Tahrirchi(doc, muallif or MUALLIF)
    t.initsial = INITSIAL if not muallif else "".join(w[0] for w in muallif.split()[:2]).upper()
    royxat = json.loads(Path(tahrir_json).read_text(encoding="utf-8"))
    hisobot = {"qollandi": [], "topilmadi": []}
    asosiy_muallif, asosiy_initsial = t.muallif, t.initsial
    vaqtlar = vaqt_jadvali(royxat, boshlanish)
    for k, e in enumerate(royxat):
        t.sana = e.get("vaqt") or vaqtlar.get(k) or t.sana
        ok = False
        # ixtiyoriy: tahrir bo'yicha muallif (masalan, lavozim: "Metodolog", "Yurist")
        if e.get("muallif"):
            t.muallif = e["muallif"]
            t.initsial = e.get("initsial") or "".join(w[0] for w in e["muallif"].split()[:2]).upper()
        else:
            t.muallif, t.initsial = asosiy_muallif, asosiy_initsial
        for p in _paragraflar(doc):
            izoh = (e.get("izoh") or "").strip()  # Word izohi: qisqa, insoniy; ID va texnik asos bu yerga yozilmaydi
            t.sariq = bool(e.get("sariq")) or bool(SARIQ_SOZLAR.search(izoh + " " + e.get("asos", "")))
            bajar = t.izoh_qoy(p, e["eski"], izoh) if e.get("faqat_izoh") else t.qol(p, e["eski"], e.get("yangi", ""), izoh)
            if bajar:
                ok = True
                break
        (hisobot["qollandi"] if ok else hisobot["topilmadi"]).append(e.get("id"))
    oxirgi = max(((v, (royxat[k].get("muallif") or asosiy_muallif)) for k, v in vaqtlar.items()), default=(None, t.muallif))[1]
    izsiz(doc, oxirgi)
    doc.save(chiqish)
    Path(str(chiqish) + ".hisobot.json").write_text(json.dumps(hisobot, ensure_ascii=False, indent=1), encoding="utf-8")
    holat = {i: "qo'llandi" for i in hisobot["qollandi"]}
    holat.update({i: "TOPILMADI — qo'lda kiritish kerak" for i in hisobot["topilmadi"]})
    Path(str(Path(tahrir_json).with_suffix("")) + "_holat.json").write_text(json.dumps(holat, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"qo'llandi: {len(hisobot['qollandi'])}, topilmadi: {len(hisobot['topilmadi'])} -> {chiqish}")
    if hisobot["topilmadi"]:
        print("topilmadi:", ", ".join(map(str, hisobot["topilmadi"])))


# ---------------------------------------------------------------- toza versiya va o'zgarishlar jadvali
def toza(kirish, chiqish):
    """Barcha tracked changes ni qabul qiladi (ins -> oddiy matn, del -> o'chiriladi), izohlarni olib tashlaydi."""
    doc = Document(kirish)
    W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    qismlar = [doc.part] + [r.target_part for r in doc.part.rels.values()
                            if "header" in r.reltype or "footer" in r.reltype]
    for part in qismlar:
        root = part.element
        for d in list(root.iter(W + "del")) + list(root.iter(W + "moveFrom")):
            if d.getparent() is not None:
                d.getparent().remove(d)
        for tag in ("ins", "moveTo"):
            for e in list(root.iter(W + tag)):
                ota = e.getparent()
                if ota is None:
                    continue
                i = ota.index(e)
                for bola in list(e):
                    ota.insert(i, bola)
                    i += 1
                ota.remove(e)
        for tag in ("commentRangeStart", "commentRangeEnd"):
            for e in list(root.iter(W + tag)):
                e.getparent().remove(e)
        for e in list(root.iter(W + "commentReference")):
            r = e.getparent()
            r.getparent().remove(r) if r.tag == W + "r" else r.remove(e)
        for e in list(root.iter(W + "rPrChange")) + list(root.iter(W + "pPrChange")):
            e.getparent().remove(e)
    # izohlar qismini bo'shatish
    for rel in list(doc.part.rels.values()):
        if rel.reltype.endswith("/comments"):
            cel = rel.target_part.element if hasattr(rel.target_part, "element") else None
            if cel is not None:
                for c in list(cel):
                    cel.remove(c)
    doc.save(chiqish)
    print(f"toza versiya -> {chiqish}")


def jadval(tahrir_json, chiqish, sarlavha="O'zgarishlar jadvali"):
    royxat = json.loads(Path(tahrir_json).read_text(encoding="utf-8"))
    hp = Path(str(Path(tahrir_json).with_suffix("")) + "_holat.json")
    holat = json.loads(hp.read_text(encoding="utf-8")) if hp.exists() else {}
    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = sec.page_height, sec.page_width
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, m, Cm(1.5))
    doc.styles["Normal"].font.size = Pt(9)
    doc.add_heading(sarlavha, level=1)
    ust = ["№", "ID", "Band", "Turi", "Eski matn", "Yangi matn", "Asos / manba", "Holati"]
    t = doc.add_table(rows=1, cols=len(ust))
    t.style = "Table Grid"
    for i, u in enumerate(ust):
        t.rows[0].cells[i].text = ""
        t.rows[0].cells[i].paragraphs[0].add_run(u).bold = True
        _soya(t.rows[0].cells[i], "D9E2F3")
    for n, e in enumerate(royxat, 1):
        tur = "Izoh" if e.get("faqat_izoh") else ("O'chirish" if not e.get("yangi") else "Tahrir")
        q = [str(n), e.get("id", ""), e.get("band", ""), tur, e.get("eski", ""), "" if e.get("faqat_izoh") else e.get("yangi", ""),
             ((e.get("asos") or e.get("izoh", "")) + (f" [{e['manba']}]" if e.get("manba") else "")).strip(), holat.get(e.get("id", ""), "")]
        row = t.add_row()
        for i, v in enumerate(q):
            row.cells[i].text = v
        if SARIQ_SOZLAR.search(q[6]) or e.get("sariq"):
            for c in row.cells:
                _soya(c, "FFF2CC")
    eni = [0.8, 1.2, 1.6, 1.6, 6.0, 6.0, 5.5, 2.3]
    for row in t.rows:
        for i, w in enumerate(eni):
            row.cells[i].width = Cm(w)
    doc.save(chiqish)
    print(f"{len(royxat)} qatorli jadval -> {chiqish}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("savollar", "javoblar", "tahrir", "toza", "jadval"):
        print(__doc__)
        sys.exit(1)
    if a[0] == "savollar":
        savollar(a[1], a[2])
    elif a[0] == "javoblar":
        javoblar(a[1], a[2])
    elif a[0] == "toza":
        toza(a[1], a[2])
    elif a[0] == "jadval":
        jadval(a[1], a[2])
    else:
        m = a[a.index("--muallif") + 1] if "--muallif" in a else None
        b = a[a.index("--boshlanish") + 1] if "--boshlanish" in a else None
        tahrir(a[1], a[2], a[3], m, b)
