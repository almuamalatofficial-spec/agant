#!/usr/bin/env python3
"""U20: islomiy atamalarni foydalanuvchi ro'yxati shakliga keltirish (docx w:t matnida va .md da).
python3 scripts/atama_standart.py tekshir fayl.docx|fayl.md [...]
python3 scripts/atama_standart.py tuzat kirish.docx chiqish.docx   (yoki .md)
python3 scripts/atama_standart.py sinov

Manba: bilim/04-terminologiya/islomiy_atamalar_standart.md (Atamalar_lugati.xlsx asosidagi to'liq jadval).
Himoya:
- oddiy so'zlar tegilmaydi: "vakolat", "istisno" (bundan mustasno), "istisnolar", "jiddiylik", "hadya" (FK);
- w:delText (o'chirilgan matn) o'zgarmaydi;
- o'zgarishlar jadvalida ("Eski matn" sarlavhali jadval) faqat "Yangi matn" ustuni o'zgaradi
  (eski matn va asos/manba ustunidagi iqtiboslar buzilmaydi);
- bank hujjatlarining rasmiy nomlari ("Nomuvofiqlik riski siyosati",
  "...nomuvofiqlik riskini boshqarish siyosati") va qo'shtirnoq ichidagi so'z-misollar ("hovuz") o'zgarmaydi;
- 824-3 yangi alifbosi (ş, ö, ğ, ç) saqlanadi: faqat atamaning o'zi tuzatiladi (Muşaraka -> Muşoraka).
"""
import re, sys, zipfile

AQD = r"(?:shartnoma|narx|asosida|daromad|debitor|tannarx|aktiv|moliyalashtirish|bitim|aqd|mahsulot)"
ATAMALAR = r"(?:[Ii]jara|[Ss]alam|[Mm]urobaha|[Mm]ushoraka|[Mm]uzoraba|[Vv]akala)"


def _risk(m):
    """nomuvofiqlik riski -> nomuvofiqlik tavakkalchiligi (19.11.2026 qarori)."""
    bosh, qoshimcha = m.group(1), m.group(2)
    if qoshimcha.startswith('lar'):
        return bosh + 'tavakkalchilik' + qoshimcha
    if qoshimcha.startswith('i'):
        return bosh + 'tavakkalchilig' + qoshimcha
    if qoshimcha == '':
        return bosh + 'tavakkalchilik'
    return bosh + 'tavakkalchilik' + qoshimcha   # riskga, riskdan, riskda


QOIDALAR = [
    # U22 (2026-11-27, foydalanuvchi): Vadiya, Ujara, Sarf
    (re.compile(r"\b([Vv])adia(?=\w*)\b|\b([Vv])adi'a"), lambda m: (m.group(1) or m.group(2))+'adiya'),
    (re.compile(r"\b([Uu])jra\b|\b([Uu])jra(?=[a-z‘'’]{1,6}\b)"), lambda m: (m.group(1) or m.group(2))+'jara'),
    # Vakala (Vakola, Wakala). "vakolat" — boshqa so'z
    (re.compile(r"\b([Vv])akola(?!t)"), r"\1akala"),
    (re.compile(r"\bWakala"), "Vakala"),
    (re.compile(r"\bwakala"), "vakala"),
    # Istisna (foydalanuvchi tuzatishi 2026-11-26). Oddiy "istisno" (bundan mustasno) tegilmaydi:
    # faqat aqd konteksti, "Parallel istisno" va atamalar sanog'i ichida
    (re.compile(r"\b([Pp]arallel )istisno"), r"\1istisna"),
    (re.compile(r"\b([Ii])stisno(?=\w{0,6}\s+" + AQD + ")"), r"\1stisna"),
    (re.compile(r"\b(" + ATAMALAR + r"(?:,| va| yoki)\s)([Ii])stisno\b"), r"\1\2stisna"),
    (re.compile(r"\b([Ii])stisno(?=(?:,| va| yoki)\s" + ATAMALAR + ")"), r"\1stisna"),
    (re.compile(r"\b([Ii])stisna[’'ʼ`]"), r"\1stisna"),
    # Ibra (Ibra')
    (re.compile(r"\b([Ii])bra[’'ʼ`]"), r"\1bra"),
    # Hamish jiddiyya (U29, 2026-11-27: MB Murobaha standarti loyihasidagi shakl; jiddiya, jiddiyah; Hamis). "jiddiylik" tegilmaydi
    (re.compile(r"\b([Jj])iddiy(?:ah\b|a\b|a(?=[a-z‘’']))"), r"\1iddiyya"),
    (re.compile(r"\b([Hh])amis(\s+[Jj]iddiyya)"), r"\1amish\2"),
    # Murobaha (Murabaha, Murabahah)
    (re.compile(r"\b([Mm])urabaha(?:h\b)?"), r"\1urobaha"),
    # Mushoraka (Musharaka, Musharakah; yangi alifboda Muşaraka -> Muşoraka)
    (re.compile(r"\b([Mm])u(sh|ş)araka(?:h\b)?"), r"\1u\2oraka"),
    # Muzoraba ("Yozilish variantlari": Mudoraba, Mudaraba, Mudarabah) va Muzorib (Mudorib, Mudarib)
    (re.compile(r"\b([Mm])ud[oa]raba(?:h\b)?"), r"\1uzoraba"),
    (re.compile(r"\b([Mm])ud[oa]rib"), r"\1uzorib"),
    # Hiba (Hibah)
    (re.compile(r"\b([Hh])ibah\b"), r"\1iba"),
    # Tavarruq (Tawarruq, Tavarruk)
    (re.compile(r"\b([Tt])awarruq"), r"\1avarruq"),
    (re.compile(r"\b([Tt])avarruk(?!\w*q)"), r"\1avarruq"),
    # Ribo (Riba) — faqat alohida so'z
    (re.compile(r"\b([Rr])iba\b"), r"\1ibo"),
    # Takaful (Takoful)
    (re.compile(r"\b([Tt])akoful"), r"\1akaful"),
    # Sukuk (Sukuk')
    (re.compile(r"\b([Ss])ukuk[’'ʼ`]"), r"\1ukuk"),
    # U14: hovuz -> fond (qo'shtirnoqdagi so'z-misol "hovuz" tegilmaydi)
    (re.compile(r"(?<![“\"«'‘„])\bhovuz(?!\w*[”\"»'’])"), "fond"),
    (re.compile(r"(?<![“\"«'‘„])\bHovuz(?!\w*[”\"»'’])"), "Fond"),
    # 19.11.2026: nomuvofiqlik riski -> nomuvofiqlik tavakkalchiligi; hujjat nomlari tegilmaydi
    (re.compile(r"\b([Nn]omuvofiqlik\s+)risk(\w*)(?!\w*\s+(?:boshqarish\s+)?siyosat)(?!\w*\s*\.docx)"), _risk),
]

# Bank bo'yicha qoidalar (CLAUDE.md 4: boshqa bank atamasi asos qilinmaydi).
# Aloqabank: "Komplaens" (lug'at "Yozilish variantlari", Aloqabank reestri).
# Xalq banki: "komplayens" — bankning rasmiy bo'linma nomi ("Ichki nazorat va komplayens departamenti"), tegilmaydi.
BANK_QOIDALARI = {
    '02_Aloqa_bank': [(re.compile(r"\b([Kk])omplayens"), r"\1omplaens")],
}

WT = re.compile(r'(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)')
TIKLASH = [  # avvalgi versiyaning xatosini qaytarish: oddiy so'z "istisno" (bundan mustasno)
    (re.compile(r"\b([Ii])stisnalar"), r"\1stisnolar"),
    (re.compile(r"\b([Ii])stisna(?=\s+(tariqasida|holat|qilin|etil|tashqari|sifatida))"), r"\1stisno"),
    (re.compile(r"(bundan|bundan tashqari|qonunchilikda nazarda tutilgan)\s+istisna\b"), r"\1 istisno"),
]
# O'zgarishlar jadvalida o'zgarmaydigan ustunlar (sarlavha boshlanishi)
HIMOYA_USTUN = ('eski matn', 'asos', 'manba', 'joriy matn', 'amaldagi matn', "o'chirildi", 'o‘chirildi')


def qoidalar(yol=''):
    q = list(QOIDALAR)
    for bank, r in BANK_QOIDALARI.items():
        if bank in yol:
            q += r
    return q


def ozgart(t, yol='', hisob=None):
    for p, r in TIKLASH:
        t = p.sub(r, t)
    n = 0
    for p, r in qoidalar(yol):
        if hisob is not None:
            for m in p.finditer(t):
                hisob[(p.pattern, m.group(0))] = hisob.get((p.pattern, m.group(0)), 0) + 1
        t, k = p.subn(r, t)
        n += k
    return t, n


def _himoya_oraliqlari(x):
    """O'zgarishlar jadvalidagi himoyalangan ustun kataklarining (bosh, oxir) oraliqlari."""
    oraliq = []
    for tbl in re.finditer(r'<w:tbl>.*?</w:tbl>', x, re.S):
        tx = tbl.group(0)
        qatorlar = list(re.finditer(r'<w:tr[ >].*?</w:tr>', tx, re.S))
        if not qatorlar:
            continue
        sarlavha = [''.join(m[1] for m in WT.findall(c)).strip().lower()
                    for c in re.findall(r'<w:tc>.*?</w:tc>', qatorlar[0].group(0), re.S)]
        if not any(s.startswith('eski matn') for s in sarlavha):
            continue
        himoya = {i for i, s in enumerate(sarlavha) if s.startswith(HIMOYA_USTUN)}
        for q in qatorlar[1:]:
            for i, c in enumerate(re.finditer(r'<w:tc>.*?</w:tc>', q.group(0), re.S)):
                if i in himoya:
                    b = tbl.start() + q.start() + c.start()
                    oraliq.append((b, b + len(c.group(0))))
    return oraliq


def _xml_tuzat(x, yol, hisob):
    oraliq = _himoya_oraliqlari(x)
    jami = 0
    def r(m):
        nonlocal jami
        if any(a <= m.start() < b for a, b in oraliq):
            return m.group(0)
        t, k = ozgart(m.group(2), yol, hisob); jami += k
        return m.group(1) + t + m.group(3)
    return WT.sub(r, x), jami


def tekshir(f):
    hisob = {}
    if f.endswith('.md'):
        ozgart(open(f, encoding='utf-8').read(), f, hisob)
    else:
        z = zipfile.ZipFile(f)
        for n in z.namelist():
            if n.startswith('word/') and n.endswith('.xml'):
                _xml_tuzat(z.read(n).decode(), f, hisob)
    return hisob


def tuzat(a, b, hisob=None):
    if a.endswith('.md'):
        t, n = ozgart(open(a, encoding='utf-8').read(), a, hisob)
        open(b, 'w', encoding='utf-8').write(t)
        return n
    zi = zipfile.ZipFile(a); zo = zipfile.ZipFile(b, 'w', zipfile.ZIP_DEFLATED); jami = 0
    for it in zi.infolist():
        d = zi.read(it.filename)
        if it.filename.startswith('word/') and it.filename.endswith('.xml'):
            x, k = _xml_tuzat(d.decode(), a, hisob); jami += k
            d = x.encode()
        zo.writestr(it, d)
    zo.close(); return jami


SINOV = [  # (kirish, kutilgan, bank yo'li)
    ("Vakola shartnomasi", "Vakala shartnomasi", ''),
    ("vakolatli organ vakolati", "vakolatli organ vakolati", ''),
    ("Wakala asosida", "Vakala asosida", ''),
    ("Istisno shartnomasi", "Istisna shartnomasi", ''),
    ("Parallel istisno", "Parallel istisna", ''),
    ("Murobaha, Ijara, Istisno va Salam", "Murobaha, Ijara, Istisna va Salam", ''),
    ("istisno tariqasida", "istisno tariqasida", ''),
    ("Istisno tariqasida", "Istisno tariqasida", ''),
    ("bundan istisno", "bundan istisno", ''),
    ("istisno holatlar", "istisno holatlar", ''),
    ("istisno qilinadi", "istisno qilinadi", ''),
    ("istisnolar ro'yxati", "istisnolar ro'yxati", ''),
    ("istisno faqat mulk sug'urtasida", "istisno faqat mulk sug'urtasida", ''),
    ("fors-major istisno qilingan", "fors-major istisno qilingan", ''),
    ("istisna’ va salam", "istisna va salam", ''),
    ("Ibra’ berish", "Ibra berish", ''),
    ("hamiş jiddiyah", "hamiş jiddiyya", ''),
    ("hamish jiddiya", "hamish jiddiyya", ''),
    ("hamis jiddiya", "hamish jiddiyya", ''),
    ("hamish jiddiyani", "hamish jiddiyyani", ''),
    ("jiddiylik puli", "jiddiylik puli", ''),
    ("Murabaha", "Murobaha", ''),
    ("muşaraka böyiça", "muşoraka böyiça", ''),
    ("Musharakah", "Mushoraka", ''),
    ("mudoraba va muşoraka", "muzoraba va muşoraka", ''),
    ("Mudorabada", "Muzorabada", ''),
    ("Mudaribning uluşi", "Muzoribning uluşi", ''),
    ("Mudarabah", "Muzoraba", ''),
    ("hibah", "hiba", ''),
    ("hadya qilish", "hadya qilish", ''),
    ("manfaat — riba", "manfaat — ribo", ''),
    ("ribavoy", "ribavoy", ''),
    ("tavarruq", "tavarruq", ''),
    ("Tawarruq", "Tavarruq", ''),
    ("“hovuz” o‘rniga", "“hovuz” o‘rniga", ''),
    ("umumiy hovuzdan", "umumiy fonddan", ''),
    ("nomuvofiqlik riskini boshqarish siyosati", "nomuvofiqlik riskini boshqarish siyosati", ''),
    ("Nomuvofiqlik riski siyosati 24-band", "Nomuvofiqlik riski siyosati 24-band", ''),
    ("Nomuvofiqlik riski siyosatida", "Nomuvofiqlik riski siyosatida", ''),
    ("nomuvofiqlik riskini kamaytirish", "nomuvofiqlik tavakkalchiligini kamaytirish", ''),
    ("nomuvofiqlik riski yuzaga", "nomuvofiqlik tavakkalchiligi yuzaga", ''),
    ("komplayens departamenti", "komplayens departamenti", 'korxonalar/01_Xalq_bank/x.docx'),
    ("komplayens xizmati", "komplaens xizmati", 'korxonalar/02_Aloqa_bank/x.docx'),
]


def sinov():
    xato = 0
    for k, kut, y in SINOV:
        t, _ = ozgart(k, y)
        if t != kut:
            xato += 1; print('XATO:', repr(k), '->', repr(t), 'kutilgan', repr(kut))
    print(f'sinov: {len(SINOV) - xato}/{len(SINOV)} to\'g\'ri')
    return xato


if __name__ == '__main__':
    if sys.argv[1] == 'tekshir':
        for f in sys.argv[2:]:
            r = tekshir(f)
            if r: print(f, {k[1]: v for k, v in r.items()})
    elif sys.argv[1] == 'sinov':
        sys.exit(1 if sinov() else 0)
    else:
        print('almashtirildi', tuzat(sys.argv[2], sys.argv[3]))
