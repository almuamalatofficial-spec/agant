#!/usr/bin/env python3
"""U20: islomiy atamalarni foydalanuvchi ro'yxati shakliga keltirish (docx w:t matnida).
python3 scripts/atama_standart.py tekshir fayl.docx [...]
python3 scripts/atama_standart.py tuzat kirish.docx chiqish.docx
"vakolat" (huquqiy vakolat) tegilmaydi. delText (o'chirilgan matn) o'zgarmaydi."""
import re, sys, zipfile
QOIDALAR = [
    (re.compile(r"\b([Vv])akola(?!t)"), r"\1akala"),
    (re.compile(r"\b([Ii])stisno"), r"\1stisna"),
    (re.compile(r"\b([Ii])bra[’'ʼ`]"), r"\1bra"),
    (re.compile(r"\b([Jj])iddiyya"), r"\1iddiya"),
    (re.compile(r"\b([Hh])amis\s+([Jj])iddiya"), r"\1amish \2iddiya"),
    (re.compile(r"\b([Mm])urabaha"), r"\1urobaha"),
    (re.compile(r"\b([Mm])usharaka"), r"\1ushoraka"),
]
WT = re.compile(r'(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)')
def ozgart(t):
    n = 0
    for p, r in QOIDALAR:
        t, k = p.subn(r, t); n += k
    return t, n
def tekshir(f):
    x = zipfile.ZipFile(f).read('word/document.xml').decode()
    t = ''.join(m.group(2) for m in WT.finditer(x))
    return {p.pattern: len(p.findall(t)) for p, _ in QOIDALAR if p.findall(t)}
def tuzat(a, b):
    zi = zipfile.ZipFile(a); zo = zipfile.ZipFile(b, 'w', zipfile.ZIP_DEFLATED); jami = 0
    for it in zi.infolist():
        d = zi.read(it.filename)
        if it.filename.startswith('word/') and it.filename.endswith('.xml'):
            def r(m):
                nonlocal jami
                t, k = ozgart(m.group(2)); jami += k; return m.group(1) + t + m.group(3)
            d = WT.sub(r, d.decode()).encode()
        zo.writestr(it, d)
    zo.close(); return jami
if __name__ == '__main__':
    if sys.argv[1] == 'tekshir':
        for f in sys.argv[2:]:
            r = tekshir(f)
            if r: print(f, r)
    else:
        print('almashtirildi', tuzat(sys.argv[2], sys.argv[3]))
