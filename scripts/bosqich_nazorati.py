#!/usr/bin/env python3
"""Majburiy bosqichlar nazorati: tasniflovchi KERAK degan bosqich bajarilmay keyingi qadamga o'tilmaydi.

    python3 scripts/bosqich_nazorati.py I/ --gacha 10      # ziddiyatlar/savollar oldidan (10 dan oldingi bosqichlar)
    python3 scripts/bosqich_nazorati.py I/ --gacha 11      # yakuniy-muharrir oldidan

Natija: har bir KERAK bosqich — BAJARILDI / YO'Q / O'TKAZILDI (foydalanuvchi qarori bilan).
Chiqish kodi 1 — kamida bitta KERAK bosqich natijasi yo'q va foydalanuvchi uni o'tkazib yuborishga rozilik bermagan.

Bosqichni o'tkazib yuborish faqat foydalanuvchining yozma qarori bilan: I/NN_qarorlar.md ga qator
    BOSQICH_OTKAZILDI: 9 | sabab: AAOIFI matni bazada yo'q | foydalanuvchi roziligi: 2026-11-23
Orkestrator bunday qatorni o'zi qaror qilib yozmaydi — faqat foydalanuvchi aniq aytgandan keyin.
"""
import argparse
import re
import sys
from pathlib import Path

ILDIZ = Path(__file__).resolve().parent.parent

# bosqich -> natija fayli naqshlari (kamida bittasi bo'lishi kerak)
NATIJA = {
    "0": ["00_tasnif.md"],
    "1": ["01_ozgarishlar.md"],
    "2": ["02_huquqiy.md"],
    "3": ["03_shariat_audit.md"],
    "3.5": ["03_5_fatvo_xotirasi.md"],
    "4": ["04_terminologiya.md"],
    "5": ["05_tuzilma.md"],
    "5.5": ["05_5_mijoz_himoyasi.md"],
    "6.1": ["06_1_*.md"], "6.2": ["06_2_*.md"], "6.3": ["06_3_*.md"], "6.4": ["06_4_*.md"],
    "6.5": ["06_5_*.md"], "6.6": ["06_6_*.md"], "6.7": ["06_7_*.md"], "6.8": ["06_8_*.md"], "6.9": ["06_9_*.md"],
    "7": ["07_metodologiya.md"],
    "7.2": ["07_2_hisob*.md"],
    "7.5": ["07_takrorlar.md"],
    "8": ["08_ichki_normativ.md"],
    "8.2": ["08_2_paket*.md"],
    "8.5": ["08_5_mohiyat.md"],
    "9": ["09_aaoifi_nazorat.md"],
    "9.5": ["09_5_iqtiboslar.md"],
    "9.7": ["09_7_orinlilik.md"],
    "10": ["10_savollar.json"],
    "10.5": ["10_5_kengash_xulosasi.md"],
    "11": ["11_tahrirlar.json"],
}

AGENT_BOSQICH = {
    "tasniflovchi": "0", "shariat-moslashtiruvchi": "1", "huquqiy-tekshiruvchi": "2", "shariat-auditor": "3",
    "fatvo-xotirasi": "3.5", "terminolog": "4", "tuzilma-tekshiruvchi": "5", "mijoz-himoyasi": "5.5",
    "soha-risk": "6.1", "soha-komplayens": "6.2", "soha-audit": "6.3", "soha-buxgalteriya": "6.4",
    "soha-gazna": "6.5", "soha-soliq": "6.6", "soha-operatsion": "6.7", "soha-garov-sugurta": "6.8",
    "soha-prudensial": "6.9", "metodolog": "7", "hisob-tekshiruvchi": "7.2", "takror-tozalovchi": "7.5",
    "ichki-normativ-tekshiruvchi": "8", "paket-muvofiqligi": "8.2", "mohiyat-tekshiruvchi": "8.5",
    "aaoifi-nazoratchi": "9", "iqtibos-tekshiruvchi": "9.5", "orinlilik-nazoratchi": "9.7", "savol-yiguvchi": "10", "kengash-xulosachi": "10.5",
    "yakuniy-muharrir": "11",
}


def kerakli(tasnif: Path):
    """Tasnif jadvalidan KERAK bosqichlar. Bosqich raqami bo'lmasa — agent nomidan aniqlanadi."""
    out = {}
    for q in tasnif.read_text(encoding="utf-8").splitlines():
        if not q.strip().startswith("|"):
            continue
        c = [x.strip() for x in q.strip().strip("|").split("|")]
        holat = next((x for x in c if re.fullmatch(r"(?i)kerak( emas)?", x)), None)
        if not holat or holat.lower() != "kerak":
            continue
        agent = next((x for x in c if x.strip("` *") in AGENT_BOSQICH), None)
        b = next((x for x in c if re.fullmatch(r"\d+(?:\.\d+)?", x)), None)
        if agent:
            b = b or AGENT_BOSQICH[agent.strip("` *")]
        if b:
            out[b] = (agent or "").strip("` *")
    return list(out.items())


def otkazilganlar(I: Path):
    f = I / "NN_qarorlar.md"
    if not f.exists():
        return {}
    d = {}
    for q in f.read_text(encoding="utf-8").splitlines():
        m = re.search(r"BOSQICH_OTKAZILDI:\s*([\d.]+)\s*\|(.*)", q)
        if m:
            d[m.group(1)] = m.group(2).strip()
    return d


def aaoifi_holati():
    """AAOIFI standartlari matni bazada bormi (mundarija emas, standart matni)."""
    p = ILDIZ / "bilim/00-umumiy/aaoifi"
    standart = [f for f in p.rglob("*.md") if re.match(r"(SS|FAS|GS|AS|ES)-\d+", f.stem)]
    return len(standart)


def kalit(b):
    return tuple(int(x) for x in b.split("."))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ish_papkasi")
    ap.add_argument("--gacha", default="99", help="shu raqamdan OLDINGI bosqichlarni tekshir")
    a = ap.parse_args()
    I = Path(a.ish_papkasi)
    tasnif = I / "00_tasnif.md"
    if not tasnif.exists():
        print("YO'Q: 00_tasnif.md — avval tasniflovchi ishga tushirilsin")
        sys.exit(1)
    otk = otkazilganlar(I)
    gacha = kalit(a.gacha)
    xato = 0
    print(f"# Bosqichlar nazorati: {I.name} (--gacha {a.gacha})\n")
    print("| Bosqich | Agent | Holat | Izoh |\n|---|---|---|---|")
    for b, agent in sorted(kerakli(tasnif), key=lambda x: kalit(x[0])):
        if kalit(b) >= gacha:
            continue
        naqsh = NATIJA.get(b, [])
        bor = [f.name for n in naqsh for f in I.glob(n)]
        if bor:
            holat, izoh = "BAJARILDI", ", ".join(bor[:3])
        elif b in otk:
            holat, izoh = "O'TKAZILDI", otk[b]
        else:
            holat, izoh = "YO'Q", "natija fayli yo'q: " + ", ".join(naqsh)
            if b == "9" and aaoifi_holati() == 0:
                izoh += " — AAOIFI standartlari matni bilim bazasida yo'q (bilim/00-umumiy/aaoifi/README.md): foydalanuvchiga ayt"
            xato += 1
        print(f"| {b} | {agent} | {holat} | {izoh} |")
    print()
    if xato:
        print(f"⛔ {xato} ta KERAK bosqich bajarilmagan. Keyingi qadamga o'tilmaydi: ularni bajar yoki foydalanuvchidan "
              f"o'tkazib yuborishga rozilik ol va I/NN_qarorlar.md ga 'BOSQICH_OTKAZILDI: N | sabab | rozilik sanasi' yoz.")
        sys.exit(1)
    print("✅ Barcha KERAK bosqichlar bajarilgan yoki foydalanuvchi roziligi bilan o'tkazilgan.")


if __name__ == "__main__":
    main()
