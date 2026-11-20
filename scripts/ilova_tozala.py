# -*- coding: utf-8 -*-
"""Ilova 1 jadvalidagi texnik belgilarni (agent kodlari, qator raqamlari) Word matnidan olib tashlash."""
import re, sys
from docx import Document

yol = sys.argv[1]
doc = Document(yol)
t = doc.tables[-1]
assert t.rows[0].cells[0].text.strip() == "№"

KOD = r"(?:(?:HS|IN|OM|NB|ML|MS) )?(?:\d{2}(?:_\d)?#\w+|\d{2}(?:_\d)? §\d+|[HTLGKMPN]\d+|Ⓘ\d+|Ⓐ|\d+-qator|05)"
ALM = [
    (r"\s*\((?:IBD Hisob siyosati|HS) Ⓘ\d+ bilan bitta savol\)", " (IBD Hisob siyosati bo‘yicha xuddi shu savol bilan birga)"),
    (r",\s*Ⓘ\d+ dan keyin", ", IMK qaroridan keyin"),
    (r"\s*\(H\d+:\s*", " ("),
    (r"\s*\(0\d-T\d+\)", ""),
    (r"\s*\((?:IBD Hisob siyosati|HS) [KLMP]\d+(?:,\s*[KLMP]\d+)*\)", ""),
    (r"\s*\((?:IBD Hisob siyosati|HS) [KLMP]\d+(?:,\s*[KLMP]\d+)* bilan bitta(?: [^)]*)?\)", " (IBD Hisob siyosati bo‘yicha xuddi shu taklif bilan birga)"),
    (r";\s*(?:IBD Hisob siyosati|HS) [KLMP]\d+(?:,\s*[KLMP]\d+)* bilan bitta bo'lim", "; IBD Hisob siyosati bo‘yicha xuddi shu taklif bilan bitta bo‘lim"),
    (r"\s*\((?:IBD Hisob siyosati|HS) [KLMP]\d+; HSY da bajarilmagan\)", " (IBD Hisob siyosatining yakuniy tahririda hali bajarilmagan)"),
    (r"\bHSY\b", "IBD Hisob siyosatining yakuniy tahriri"),
    (r"\s*\(0\d(?:_\d)?#\w+ savolidan keyin\)", " (savolga javobdan keyin)"),
    (r"\b0\d(?:_\d)? tuzatishi:\s*", ""),
    (r"\s*—\s*0\d(?:_\d)? qo'shgan", ""),
    (r"\s*—\s*0\d(?:_\d)? qo‘shgan", ""),
    (r"\bOM\b", "Omonatlar siyosati"),
    (r",\s*T7\)", ")"),
    (r"\s*—\s*05#14 taklifi:", ":"),
    (r"\s*\(03#S9, 08_5#13, 07#17 satrlari bilan\)", ""),
    (r"15\.4 — L1", "15.4 — ustuvorlik bo‘yicha qaror"),
    (r"\s*\(03_Yakuniy matni\)", " (yakuniy matn)"),
    (r"\s*—\s*08 §4 tuzatishi: qabul qiluvchi MS 3-ilovasi emas, skrining metodikasi", ""),
    (r"\s*—\s*T1 yoki 06_5 varianti", " — savollar bo‘yicha javobga ko‘ra"),
    (r"\s*—\s*02#14 javobiga moslanadi", " — maxsus bo‘linma bo‘yicha javobga moslanadi"),
    (r"\s*—\s*T7 savoli", " — savolga javobga ko‘ra"),
    (r"L1 qarori \(HS 17-qator\)", "ustuvorlik bo‘yicha qaror"),
    (r"Ⓘ\d+ qaroriga", "IMK qaroriga"),
    (r"\s*—\s*Ⓘ\d+", " — IMK qaroriga ko‘ra"),
    (r"\(Ⓘ\d+ dan keyin\)", "(IMK qaroridan keyin)"),
    (r"\(Ⓘ\d+\)", "(IMK qarori)"),
    (r";\s*888 holati reestrda tekshirilsin\s*—\s*08#11", ""),
    (r"\s*—\s*973 IBDga tatbiq etilsa \(08#6 savoli\)", ", agar 973 IBDga tatbiq etilsa"),
    (r"04_Reestr/hujjatlar_reestri", "Ichki hujjatlar reestri"),
    (r"\bIN (?=\d|IV|ga\b)", "IBD Investitsiya siyosati "),
    (r"\bIN\b", "IBD Investitsiya siyosati"),
    (r"\bHS\b", "IBD Hisob siyosati"),
    (r"\bMS\b", "Muvofiqlik siyosati"),
    (r"\bNB\b", "Narx belgilash siyosati"),
    (r"\bML\b", "Moliyalashtirish siyosati"),
    (r"siyosati ga\b", "siyosatiga"),
    (r"siyosati da\b", "siyosatida"),
]


def tozala(s):
    for a, b in ALM:
        s = re.sub(a, b, s)
    # faqat kodlardan iborat qavslar: "(08#3)", "(H1)", "(05#10)", "(33-qator)", "(9-qator)"
    s = re.sub(r"\s*\((?:" + KOD + r")(?:[;,] *" + KOD + r")*\)", "", s)
    # qavs ichidagi kod qo'shimchalari: "(H4; 10.2c ... — 02 §6)" -> qavs qoladi, kod olinadi
    s = re.sub(r"\s*—\s*" + KOD + r"(?=\))", "", s)
    s = re.sub(r"\(" + KOD + r";\s*", "(", s)
    s = re.sub(r"\s*\(\s*\)", "", s)
    s = re.sub(r"  +", " ", s)
    return s.strip()


n = 0
for row in t.rows[1:]:
    for cell in row.cells[1:]:
        for p in cell.paragraphs:
            eski = p.text
            yangi = tozala(eski)
            if yangi != eski:
                for r in p.runs[1:]:
                    r._r.getparent().remove(r._r)
                p.runs[0].text = yangi
                n += 1
doc.save(yol)
print("tozalandi:", n)
for row in t.rows[1:]:
    for c in row.cells[1:]:
        if re.search(r"#|Ⓘ|§|\b[HTLGKMPN]\d|qator|\b(?:HS|IN|OM|NB|ML|MS)\b|\b0\d(?:_\d)? ", c.text):
            print("QOLDI:", row.cells[0].text, c.text[:200])
