"""
List G/L accounts that are safe candidates for blocking after the migration.

A candidate is a posting account that: has a zero balance in BC, is not in mapping/account-mapping.csv
(used by the client or required by posting groups), and is not referenced by an active row of the setup
packages we loaded (posting groups, general/inventory posting setup, bank posting groups, tax jurisdictions).
Setup tables outside our packages (payment methods, currencies, ...) are NOT checked here: spot-check with
BC's Where-Used List, then test day-one processes after blocking.
Usage:
  python tools/block_candidates.py <BC chart of accounts export.xlsx> <QCS-02 import.xlsx> <QCS-06 import.xlsx>
"""
import csv, sys
from pathlib import Path
import openpyxl
from rapidstart_excel import read

ROOT = Path(__file__).resolve().parent.parent
ws = openpyxl.load_workbook(sys.argv[1], data_only=True).worksheets[0]
rows = list(ws.iter_rows(values_only=True)); bc = {str(r[0]): r for r in rows[1:]}
mapped = {r["BC No."] for r in csv.DictReader(open(ROOT / "mapping/account-mapping.csv", encoding="utf-8")) if r["BC No."]}
refs = {"23100": {"Tax Jurisdiction"}, "23110": {"Tax Jurisdiction"}}
for pkg in sys.argv[2:4]:
    for sheet, t in read(pkg).items():
        if sheet.startswith(("14 ", "Location")): continue          # addresses, not accounts
        for r in t["rows"]:
            d = dict(zip(t["hdr"], r))
            if d.get("Blocked") == "true": continue                  # blocked setup rows are never used
            for k, v in d.items():
                if v.isdigit() and len(v) == 5 and v in bc: refs.setdefault(v, set()).add(f"{sheet} {r[0]} {k}")
cands = [n for n, r in sorted(bc.items()) if not (r[4] or 0) and n not in mapped and n not in refs]
with open(ROOT / "mapping/block-candidates.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["BC Account", "Name", "Reason"])
    for n in cands: w.writerow([n, bc[n][1].strip(), "Zero balance; not used by the client; not in any loaded setup"])
print(f"posting accounts {len(bc)} | candidates {len(cands)}")
for n, w in sorted(refs.items()):
    if n not in mapped: print(f"  kept, referenced by setup: {n} {bc[n][1].strip()} <- {sorted(w)[0]}")
