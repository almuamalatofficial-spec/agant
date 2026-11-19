#!/usr/bin/env python3
"""Excel lug'at/manba ro'yxatlaridagi havolalarni bo'lim papkasiga yuklab oladi.

    python3 scripts/havolalarni_yukla.py <havolalar.json>
havolalar.json: [{"soha": "risk|gazna|...", "url": ..., "nom": ...}, ...]
Natija: bilim/06-soha/<soha>/manbalar/<nom>.<html|pdf> + manbalar/ROYXAT.md (holati bilan).
"""
import json, re, subprocess, sys, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def slug(s, n=80):
    s = re.sub(r"[^\w\s.-]", "", s, flags=re.U).strip()
    return re.sub(r"\s+", "_", s)[:n] or "manba"

def main():
    items = json.load(open(sys.argv[1]))
    royxat = {}
    for it in items:
        d = ROOT / "bilim/06-soha" / it["soha"] / "manbalar"; d.mkdir(parents=True, exist_ok=True)
        base = f'{slug(it["nom"])}_{hashlib.md5(it["url"].encode()).hexdigest()[:6]}'
        old = list(d.glob(base + ".*"))
        if any(p.suffix in (".pdf", ".html") for p in old):
            holat = "oldin yuklangan"; fayl = [p for p in old if p.suffix in (".pdf", ".html")][0].name
        else:
            tmp = d / (base + ".tmp")
            r = subprocess.run(["curl", "-sSL", "-m", "90", "-A", "Mozilla/5.0", "-o", str(tmp),
                                "-w", "%{http_code} %{content_type}", it["url"]], capture_output=True, text=True)
            kod, _, tur = r.stdout.partition(" ")
            if r.returncode or not kod.startswith("2") or not tmp.exists() or tmp.stat().st_size < 500:
                holat = f"YUKLANMADI ({kod or r.stderr.strip()[:60]})"; fayl = "—"; tmp.unlink(missing_ok=True)
            else:
                ext = ".pdf" if ("pdf" in tur or tmp.read_bytes()[:4] == b"%PDF") else ".html"
                tmp.rename(d / (base + ext)); fayl = base + ext; holat = "yuklandi"
        royxat.setdefault(it["soha"], []).append(f'| {it["nom"][:90]} | {it["url"]} | {fayl} | {holat} |')
        print(it["soha"], holat, it["url"], flush=True)
    for soha, rows in royxat.items():
        (ROOT / "bilim/06-soha" / soha / "manbalar/ROYXAT.md").write_text(
            f"# {soha} — havolalar bo'yicha manbalar\n\n| Manba | Havola | Fayl | Holati |\n|---|---|---|---|\n" + "\n".join(rows) + "\n")

if __name__ == "__main__":
    main()
