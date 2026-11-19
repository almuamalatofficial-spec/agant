#!/usr/bin/env python3
"""Google Drive'dagi `Agent_promptlari` hujjatlaridan agent promptlarini yangilaydi.

Ish tartibi (orkestrator bajaradi):
  0. Drive `search_files` (parentId = papka_id) bilan hujjatlar ro'yxatini ol va har birining modifiedTime ini
     scripts/promptlar_holati.json dagi qiymat bilan solishtir. FAQAT modifiedTime kattaroq (inson tahrirlagan)
     hujjatlarni yuklab ol — qolganlarida mahalliy versiya to'g'ri (u Drive'dan yangiroq bo'lishi mumkin).
  1. scripts/promptlar_drive.json dagi har bir Google Doc'ni Drive `read_file_content` bilan o'qiydi
     va natijani (JSON yoki matn) <papka>/<doc_id>.json ga saqlaydi.
  2. python3 scripts/promptlarni_yangila.py <papka>
  3. Har bir qo'llangan hujjat uchun: python3 scripts/promptlarni_yangila.py holat <doc_id> <modifiedTime>
Skript har bir hujjatdagi "# PROMPT" sarlavhasidan keyingi matnni oladi va mos faylga yozadi.
Agent fayllaridagi texnik qism (name/description/tools) o'zgarmaydi. O'zgargan fayllar ro'yxati chiqariladi.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def matn(f: Path) -> str:
    s = f.read_text(encoding="utf-8")
    try:
        return json.loads(s)["fileContent"]
    except Exception:
        return s

def tozala(s: str) -> str:
    s = s.split("# PROMPT", 1)[1].lstrip("\n") if "# PROMPT" in s else s
    s = re.sub(r"\\([\\`*_\[\]{}()#+\-.!<>|~])", r"\1", s)      # markdown escape'larini qaytarish
    return s.strip() + "\n"

def main():
    if sys.argv[1] == "holat":
        hp = ROOT / "scripts/promptlar_holati.json"
        h = json.loads(hp.read_text()) if hp.exists() else {}
        h[sys.argv[2]] = sys.argv[3]
        hp.write_text(json.dumps(h, indent=1)); print("holat saqlandi"); return
    papka = Path(sys.argv[1])
    xarita = json.loads((ROOT / "scripts/promptlar_drive.json").read_text())["hujjatlar"]
    for fayl, doc_id in xarita.items():
        f = papka / f"{doc_id}.json"
        if not f.exists():
            continue
        yangi = tozala(matn(f))
        p = ROOT / fayl
        eski = p.read_text(encoding="utf-8")
        fm = re.match(r"^---\n.*?\n---\n\n?", eski, re.S)
        bosh = fm.group(0) if fm else ("# " + eski.split("\n", 1)[0].lstrip("# ") + "\n\n" if fayl == "CLAUDE.md" else "")
        natija = bosh + yangi
        if re.sub(r"\s+", " ", natija) != re.sub(r"\s+", " ", eski):
            p.write_text(natija, encoding="utf-8"); print(f"  ✎ yangilandi: {fayl}")
        else:
            print(f"  = o'zgarmagan: {fayl}")

if __name__ == "__main__":
    main()
