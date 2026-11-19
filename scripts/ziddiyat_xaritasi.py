#!/usr/bin/env python3
"""Ziddiyat xaritasi: hujjat ichidagi ehtimoliy ziddiyatlarni avtomatik topadi.

    python3 scripts/ziddiyat_xaritasi.py [hujjat.md] -o [I]/07a_ziddiyat_xaritasi.md [--chegara 0.35]

Ikki turdagi parametrlar band raqami bilan ajratiladi:
  1) RAQAMLI: muddat (kun, ish kuni, oy, yil, soat), foiz/ulush (%), summa (so'm, mln, mlrd), koeffitsiyent, "X marta";
  2) VAKOLAT: kim tasdiqlaydi / qaror qabul qiladi / belgilaydi / kelishadi (organ yoki bo'linma).
     Kichik bandda organ yozilmagan bo'lsa ("10.5.3. ... tasdiqlaydi"), ota band ("10.5. Bank Boshqaruvi:") dan meros olinadi.
So'ng bir xil mavzudagi (kontekst so'zlari o'xshash) lekin QIYMATI yoki ORGANI farq qiladigan juftliklar
"ehtimoliy ziddiyat" sifatida chiqariladi. Bu xom ro'yxat: haqiqiy ziddiyatmi — metodolog agenti hal qiladi.
"""
import argparse
import re
from collections import defaultdict
from pathlib import Path

BAND = re.compile(r"^\s*(?:\*\*)?(\d{1,3}(?:\.\d{1,3}){0,4})\.?(?:\*\*)?\s+(.*)")
SARLAVHA = re.compile(r"^\s*#{1,6}\s+(.*)")

BIRLIK = [
    ("muddat", r"(\d+(?:[.,]\d+)?)\s*(?:\(\s*[^)]{1,30}\)\s*)?(ish\s+kuni|kalendar\s+kuni|bank\s+kuni|kun|oy|yil|soat|hafta|daqiqa)\w*"),
    ("foiz", r"(\d+(?:[.,]\d+)?)\s*(%|foiz\b)"),
    ("summa", r"(\d[\d\s]*(?:[.,]\d+)?)\s*(mlrd|mln|million|milliard|ming)?\s*(so['‘’ʻ]m|AQSh dollari|USD|EUR|BHM|bazaviy hisoblash miqdori)"),
    ("marta", r"(\d+(?:[.,]\d+)?)\s*(marta|baravar)"),
    ("koeffitsiyent", r"(koeffitsiyent\w*|nisbat\w*|chegara\w*|limit\w*)\D{0,25}?(\d+(?:[.,]\d+)?)"),
]
ORGANLAR = [
    "aksiyadorlar umumiy yig['‘’ʻ]ilishi", "umumiy yig['‘’ʻ]ilish", "kuzatuv kengashi", "audit qo['‘’ʻ]mitasi",
    "boshqaruv", "bank imk", "markaziy bank imk", "imk", "islomiy moliya kengashi", "kredit qo['‘’ʻ]mitasi",
    "apbq", "alco", "risk\\w* qo['‘’ʻ]mitasi", "bosh buxgalter", "bhhd", "ichki audit\\w*", "islomiy audit\\w*",
    "komplaens\\w*|komplayens\\w*", "islomiy muvofiqlik bo['‘’ʻ]limi", "ibd departamenti|islomiy bank darchasi departamenti",
    "g['‘’ʻ]aznachilik\\w*", "risk\\w* departamenti", "yuridik\\w*", "rais\\w*", "boshqaruv raisi",
]
FEL = r"(tasdiqla\w*|qaror qabul qil\w*|belgila\w*|kelishi\w*|ma['‘’ʻ]qulla\w*|ruxsat ber\w*|tomonidan)"
ORGAN_RX = re.compile(r"(" + "|".join(ORGANLAR) + r")", re.I)
STOP = set("""va bilan uchun bo'yicha bo‘yicha asosida tomonidan hamda yoki ham bu shu ushbu u ular
qilinadi qiladi etiladi bo'ladi bo‘ladi kerak mumkin emas har bir barcha hisob hisobga bank bankning
oid ichida kabi orqali sifatida holda holatda keyin oldin dan gacha ga da ni ning""".split())


def toza(s):
    s = s.lower().replace("ʻ", "'").replace("‘", "'").replace("’", "'").replace("ʼ", "'")
    return re.sub(r"[*_`|>#\[\]()\"«»“”:;,.]", " ", s)


HUJJAT_TURI = ("metodik", "siyosat", "nizom", "reglam", "tartib", "hisobot", "chegara", "limit", "zaxira",
               "koeffit", "stavka", "muddat", "rejasi", "yo'riqn", "kapital", "fond", "taqsim", "ulush", "ajratm")


def sozlar(s):
    """Kontekst so'zlarining o'zaklari (6 harf) — 'metodikani/metodikada' bitta o'zak."""
    return {w[:6] for w in re.findall(r"[a-zа-яўқғҳ'\-]{4,}", toza(s)) if w not in STOP}


def oxshashlik(a, b):
    umumiy = a & b
    if not umumiy:
        return 0.0, umumiy
    return len(umumiy) / max(1, min(len(a), len(b))), umumiy


def bandlar(matn):
    joriy, ota_matn, sar = "—", {}, "—"
    for i, q in enumerate(matn.splitlines(), 1):
        m = SARLAVHA.match(q)
        if m:
            sar = m.group(1)[:60]
            continue
        b = BAND.match(q)
        if b and re.search(r"[A-Za-zА-Яа-я]", b.group(2)):
            joriy = b.group(1)
            ota_matn[joriy] = b.group(2)
            yield i, joriy, b.group(2), sar, ota_matn
        elif q.strip().startswith("|"):
            hujayra = [h.strip() for h in q.strip().strip("|").split("|")]
            if set("".join(hujayra)) <= set("-: "):
                continue
            # jadval qatori: "sarlavha/joriy band" + qator matni (birinchi ustun odatda mavzu)
            yield i, f"{joriy} (jadval, {sar[:30]})", " ; ".join(h for h in hujayra if h), sar, ota_matn
        elif q.strip():
            yield i, joriy, q.strip(), sar, ota_matn


ORGAN_SINONIM = [
    (r"^(bank imk|imk|islomiy moliya kengashi|bankning islomiy moliya kengashi)$", "IMK"),
    (r"^(markaziy bank imk)$", "MB IMK"),
    (r"^(aksiyadorlar umumiy yig['‘’ʻ]ilishi|umumiy yig['‘’ʻ]ilish)$", "Aksiyadorlar umumiy yig'ilishi"),
    (r"^(boshqaruv)$", "Boshqaruv"),
    (r"^(kuzatuv kengashi)$", "Kuzatuv kengashi"),
    (r"^(apbq|alco)$", "APBQ"),
    (r"^(bosh buxgalter|bhhd)$", "BHHD (Bosh buxgalter)"),
    (r"^(komplaens\w*|komplayens\w*)$", "Komplaens"),
    (r"^(ichki audit\w*)$", "Ichki audit"),
    (r"^(islomiy audit\w*)$", "Islomiy audit"),
]


def organ_norm(o):
    meros = " (ota banddan)" if o.endswith(" (ota banddan)") else ""
    t = o.replace(" (ota banddan)", "").strip().lower()
    for rx, nom in ORGAN_SINONIM:
        if re.match(rx, t):
            return nom + meros
    return t + meros


def meros_organ(band, ota_matn):
    q = band.split(".")
    while len(q) > 1:
        q = q[:-1]
        ota = ".".join(q)
        t = ota_matn.get(ota, "")
        if t:
            m = ORGAN_RX.search(t)
            if m and (t.rstrip().endswith(":") or len(t) < 160):
                return m.group(1)
    return None


def parametrlar(matn):
    """Hujjatdan raqamli va vakolat parametrlarini ajratadi: [(tur, qiymat, band, qator, kontekst, so'zlar_to'plami)]."""
    yozuvlar = []  # (tur, qiymat, band, qator, kontekst, sozlar)
    for qator, band, t, sar, ota_matn in bandlar(matn):
        # raqamli parametrlar
        for tur, rx in BIRLIK:
            for m in re.finditer(rx, t, re.I):
                if tur == "koeffitsiyent":
                    qiymat = m.group(2)
                else:
                    qiymat = re.sub(r"\s+", " ", " ".join(g for g in m.groups() if g)).strip().lower()
                bosh, oxir = max(0, m.start() - 120), min(len(t), m.end() + 120)
                kontekst = t[bosh:oxir]
                yozuvlar.append((tur, qiymat, band, qator, kontekst, sozlar(kontekst) - sozlar(m.group(0))))
        # vakolat: faqat TASDIQLOVCHI/QAROR QILUVCHI organ (maslahatchi organlar — "IMK xulosasi asosida", "kelishuvi bilan" — chiqariladi)
        if re.search(FEL, t, re.I):
            organlar = set()
            for m in ORGAN_RX.finditer(t):
                keyin = t[m.end():m.end() + 40].lower()
                if re.match(r"\W*(xulosa|tavsiya|taqdim|kelishuv|fikr|ko['‘’ʻ]rib)", keyin):
                    continue  # maslahatchi
                if re.match(r"\W*(tomonidan|tasdi|qaror|belgila|ma['‘’ʻ]qulla|ruxsat)", keyin) or re.match(r"\W*\w*\s*(tasdi)", keyin):
                    organlar.add(m.group(1).lower())
            if not organlar:
                o = meros_organ(band, ota_matn)
                if o and re.search(r"(tasdiqlaydi|qaror qabul qiladi|belgilaydi|ma['‘’ʻ]qullaydi)", t, re.I):
                    organlar = {o.lower() + " (ota banddan)"}
            organlar = {organ_norm(o) for o in organlar}
            for o in organlar:
                obyekt = re.sub(ORGAN_RX, " ", t)
                yozuvlar.append(("vakolat", o, band, qator, t[:260], sozlar(obyekt)))

    return yozuvlar


def juftlik_mosmi(ti, vi, si, tj, vj, sj, chegara):
    """Ikki parametr bir mavzuda, lekin qiymati farqlimi? (o'xshashlik, umumiy so'zlar) yoki None."""
    if tj != ti or not si or not sj:
        return None
    if re.sub(r" \(ota banddan\)", "", vi) == re.sub(r" \(ota banddan\)", "", vj):
        return None
    j_k, umumiy = oxshashlik(si, sj)
    hujjat_turi = any(u.startswith(h[:6]) for u in umumiy for h in HUJJAT_TURI)
    kerak = 2 if (ti == "vakolat" and hujjat_turi) else (99 if ti == "vakolat" else 3)
    if j_k >= chegara and len(umumiy) >= kerak:
        return round(j_k, 2), sorted(umumiy)[:8]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hujjat")
    ap.add_argument("-o", "--chiqish")
    ap.add_argument("--chegara", type=float, default=0.3)
    a = ap.parse_args()
    matn = Path(a.hujjat).read_text(encoding="utf-8")

    yozuvlar = parametrlar(matn)

    org = defaultdict(set)
    for tur, qiymat, band, *_ in yozuvlar:
        if tur == "vakolat":
            org[band].add(qiymat.replace(" (ota banddan)", ""))
    # juftliklar: bir xil tur, farqli qiymat, o'xshash kontekst
    nomzod = []
    for i in range(len(yozuvlar)):
        ti, vi, bi, qi, ki, si = yozuvlar[i]
        if not si:
            continue
        for j in range(i + 1, len(yozuvlar)):
            tj, vj, bj, qj, kj, sj = yozuvlar[j]
            if tj != ti or bi == bj or not sj:
                continue
            vi_n = re.sub(r" \(ota banddan\)", "", vi)
            vj_n = re.sub(r" \(ota banddan\)", "", vj)
            if vi_n == vj_n:
                continue
            if ti == "muddat" and vi.split()[-1:] != vj.split()[-1:] and not {"kun", "oy"} & set((vi + " " + vj).split()):
                pass
            if ti == "vakolat" and org[bi] & org[bj]:
                continue
            j_k, umumiy = oxshashlik(si, sj)
            hujjat_turi = any(u.startswith(h[:6]) for u in umumiy for h in HUJJAT_TURI)
            kerak = 2 if (ti == "vakolat" and hujjat_turi) else (99 if ti == "vakolat" else 3)
            if j_k >= a.chegara and len(umumiy) >= kerak:
                nomzod.append((round(j_k, 2), ti, (bi, qi, vi, ki), (bj, qj, vj, kj), sorted(umumiy)[:8]))
    nomzod.sort(key=lambda x: (-x[0], x[1]))

    # bir xil band juftliklari takrorlanmasin
    korilgan, natija = set(), []
    for n in nomzod:
        k = (n[1], n[2][0], n[3][0])
        if k in korilgan:
            continue
        korilgan.add(k)
        natija.append(n)

    chiq = [f"# Ziddiyat xaritasi (avtomatik): {Path(a.hujjat).name}\n",
            f"Ajratilgan parametrlar: {len(yozuvlar)} (vakolat: {sum(1 for y in yozuvlar if y[0]=='vakolat')}). "
            f"Ehtimoliy ziddiyatlar: {len(natija)} (kontekst o'xshashligi ≥ {a.chegara}).\n",
            "Bu xom ro'yxat — har bir juftlikni metodolog tekshiradi: haqiqiy ziddiyat / farqli mavzu / qonuniy farq.\n"]
    for n, (oxs, tur, A, B, umumiy) in enumerate(natija, 1):
        chiq.append(f"\n## Z{n} — {tur}, o'xshashlik {oxs:.0%} — umumiy so'zlar: {', '.join(umumiy)}\n")
        for band, qator, qiymat, kon in (A, B):
            chiq.append(f"- **{band}** (qator {qator}) → **{qiymat}** — …{re.sub(r'\\s+', ' ', kon)[:300]}…")
    natija_matn = "\n".join(chiq) + "\n"
    if a.chiqish:
        Path(a.chiqish).write_text(natija_matn, encoding="utf-8")
        print(f"{len(yozuvlar)} parametr, {len(natija)} ehtimoliy ziddiyat -> {a.chiqish}")
    else:
        print(natija_matn)


if __name__ == "__main__":
    main()
