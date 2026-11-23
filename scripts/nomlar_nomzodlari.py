#!/usr/bin/env python3
"""Yakuniy (toza) .docx dan atama, hujjat nomi, metodika, qisqartma nomzodlarini band raqami bilan yig'ish.

    python3 scripts/nomlar_nomzodlari.py HUJJAT.docx CHIQISH.json

Natija nomzodlar ro'yxati — to'liqlik uchun xom material. Yakuniy ro'yxatni agent/inson tozalaydi.
"""
import json
import re
import sys
from collections import defaultdict

from docx import Document

TUR = (r"(?:siyosat|tartib|nizom|metodika|metodologiya|metodolog|yo[‘'’`ʻ]?riqnoma|reglament|qoidalar|qoida|reja|dastur|"
       r"standart|kodeks|qonun|qaror|buyruq|farmoyish|farmon|ko[‘'’`ʻ]?rsatma|shartnoma|pasport|reestr|matritsa|katalog|"
       r"bayonot|xulosa|fatvo|nizomi|ilova|shakl|deklaratsiya|strategiya|konsepsiya|ICAAP|ILAAP)\w*")
RX_TUR = re.compile(r"((?:[«\"“][^»\"”]{3,200}[»\"”])|(?:(?:[A-ZЁЎҚҒҲА-Я\w‘'’ʻ-]+\s+){1,12}" + TUR + r"))", re.U)
RX_QUOTE = re.compile(r"[«“\"]([^»”\"]{3,250})[»”\"]")
RX_ACR = re.compile(r"\b([A-ZЁЎҚҒҲА-Я]{2,}[A-ZЁЎҚҒҲА-Я0-9\-]*)\b")
RX_ARAB = re.compile(r"([\w‘'’ʻ\- ]{2,40})\s*\(([؀-ۿ][؀-ۿ\s]*)\)")
RX_TARIF = re.compile(r"^\s*(?:\d+(?:\.\d+)*\.?\s*)?([^\s—–:-][^—–:]{1,80}?)\s*[—–-]\s+(?:bu\s|deganda|tushuniladi|)", re.U)
RX_BAND = re.compile(r"^\s*((?:\d+\.)+\d*|\d+\)|[a-z]\))\s")


def paragraflar(doc):
    def ichki(c):
        for el in c.element.body.iterchildren() if hasattr(c, "element") and hasattr(c.element, "body") else []:
            yield el
    for p in doc.paragraphs:
        yield p.text
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    yield p.text


def main():
    doc = Document(sys.argv[1])
    band = "boshi"
    kand = defaultdict(lambda: {"tur": set(), "bandlar": [], "soni": 0})

    def qosh(nom, tur):
        nom = re.sub(r"\s+", " ", nom).strip(" ,.;:()")
        if len(nom) < 2:
            return
        k = kand[nom]
        k["tur"].add(tur)
        k["soni"] += 1
        if band not in k["bandlar"]:
            k["bandlar"].append(band)

    for matn in paragraflar(doc):
        if not matn.strip():
            continue
        m = RX_BAND.match(matn)
        if m:
            band = m.group(1)
        for q in RX_QUOTE.findall(matn):
            qosh(q, "qo'shtirnoq")
        for m in RX_TUR.finditer(matn):
            qosh(m.group(1), "hujjat_turi_sozi")
        for a in RX_ACR.findall(matn):
            qosh(a, "qisqartma")
        for t, ar in RX_ARAB.findall(matn):
            qosh(f"{t.strip()} ({ar.strip()})", "arabcha")
        m = RX_TARIF.match(matn)
        if m and len(m.group(1).split()) <= 8:
            qosh(m.group(1), "ta'rif_boshi")
    out = [{"nom": k, "tur": sorted(v["tur"]), "soni": v["soni"], "bandlar": v["bandlar"][:60]} for k, v in kand.items()]
    out.sort(key=lambda x: (-x["soni"], x["nom"]))
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"{len(out)} nomzod -> {sys.argv[2]}")


if __name__ == "__main__":
    main()
