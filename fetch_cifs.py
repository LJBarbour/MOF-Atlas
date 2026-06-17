#!/usr/bin/env python3
"""
fetch_cifs.py — download crystal structure files for entries in mofs.json
that have a `cod_id` recorded. CIFs come from the Crystallography Open
Database (CC0). Run from the same directory as mof-atlas.html.

    python3 fetch_cifs.py            # download all
    python3 fetch_cifs.py MOF-5      # download a single entry by id

Once populated, the cif/ folder sits next to mof-atlas.html and the app
auto-loads cif/{id}.cif when you open a record.
"""
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = ROOT / "mofs.json"
CIF_DIR = ROOT / "cif"
COD_URL = "https://www.crystallography.net/cod/{cod_id}.cif"


def fetch_one(mof, force=False):
    if not mof.get("cod_id"):
        print(f"  · {mof['id']:<22}  skipped (no cod_id)")
        return False
    out = CIF_DIR / f"{mof['id']}.cif"
    if out.exists() and not force:
        print(f"  ✓ {mof['id']:<22}  already present  →  {out.name}")
        return True
    url = COD_URL.format(cod_id=mof["cod_id"])
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MOF-Atlas/1.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read().decode("utf-8", errors="replace")
        if len(data) < 200 or "data_" not in data:
            print(f"  ✗ {mof['id']:<22}  unexpected response (len={len(data)})")
            return False
        out.write_text(data)
        print(f"  ✓ {mof['id']:<22}  fetched COD {mof['cod_id']}  ({len(data)//1024 or 1} kB)")
        return True
    except urllib.error.HTTPError as e:
        print(f"  ✗ {mof['id']:<22}  HTTP {e.code}")
    except urllib.error.URLError as e:
        print(f"  ✗ {mof['id']:<22}  network: {e.reason}")
    except Exception as e:
        print(f"  ✗ {mof['id']:<22}  {type(e).__name__}: {e}")
    return False


def main():
    if not DB.exists():
        print(f"Could not find {DB}. Run this from the folder containing mofs.json.")
        sys.exit(1)
    CIF_DIR.mkdir(exist_ok=True)
    db = json.loads(DB.read_text())
    by_id = {m["id"]: m for m in db}

    targets = []
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg not in by_id:
                print(f"Unknown id: {arg}")
                sys.exit(2)
            targets.append(by_id[arg])
    else:
        targets = db

    with_cod = [m for m in targets if m.get("cod_id")]
    print(f"\nFetching CIFs from COD into {CIF_DIR}/")
    print(f"Targets with cod_id: {len(with_cod)} / {len(targets)} requested\n")

    ok = sum(fetch_one(m) for m in targets)
    print(f"\nDone — {ok} CIF{'s' if ok != 1 else ''} now available.")
    print("Reload mof-atlas.html and open any populated entry to see its 3D structure.\n")


if __name__ == "__main__":
    main()
