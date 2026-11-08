"""
Set Blocked = Yes on the accounts in mapping/block-candidates.csv (package QCS-14-BLOCK-ACCOUNTS, D-022).
Every other row of BC's export is written back unchanged.
Usage: python tools/block_accounts.py <QCS-14-BLOCK-ACCOUNTS_export-template.xlsx>
"""
import csv, sys
from pathlib import Path
from rapidstart_excel import read, write

ROOT = Path(__file__).resolve().parent.parent
cands = {r["BC Account"] for r in csv.DictReader(open(ROOT / "mapping/block-candidates.csv", encoding="utf-8"))}
D = read(sys.argv[1]); s = next(iter(D)); h = D[s]["hdr"]; ino, ib = h.index("No."), h.index("Blocked")
found = set(); changed = 0
for r in D[s]["rows"]:
    if r[ino] in cands:
        found.add(r[ino])
        if r[ib] != "true": r[ib] = "true"; changed += 1
missing = cands - found
if missing: sys.exit(f"Stopped: candidates not in the export: {sorted(missing)}")
write(sys.argv[1], ROOT / "packages/QCS-14-BLOCK-ACCOUNTS_import.xlsx", D)
print(f"accounts in package: {len(D[s]['rows'])} | set to blocked: {changed} | already blocked: {len(cands) - changed}")
