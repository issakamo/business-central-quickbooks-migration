"""
QuickBooks vendors -> BC Vendor (package QCS-05-VENDORS).

Inputs (never edited by hand): source/qbo-exports/qbo_vendors.csv
Rules: mapping/payment-terms.csv
Outputs:
  mapping/vendor-xref.csv                    QuickBooks name -> BC No. (used again for open AP and 1099)
  packages/QCS-05-VENDORS_import.xlsx        filled from BC's own exported template
Not loaded on purpose: tax ID (masked in the export; entered from W-9s by the client, I-006),
tax settings (use tax out of scope, D-011), 1099 setup (IRS Forms setup, separate step).
Usage:
  python tools/transform_vendors.py <path to QCS-05-VENDORS_export-template.xlsx>
"""
import csv, sys
from pathlib import Path
from rapidstart_excel import read, write

ROOT = Path(__file__).resolve().parent.parent
def load(p): return list(csv.DictReader(open(ROOT / p, encoding="utf-8")))

src = load("source/qbo-exports/qbo_vendors.csv")
terms = {r["QBO Terms"]: r["BC Payment Terms Code"] for r in load("mapping/payment-terms.csv")}

keep = sorted(src, key=lambda r: r["Vendor"].lower())
bc_no = {r["Vendor"]: f"V{(i + 1) * 10:05d}" for i, r in enumerate(keep)}

with open(ROOT / "mapping/vendor-xref.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["QBO Vendor", "BC No.", "Status", "QBO 1099", "Issue"])
    for r in keep:
        issue = "I-007" if r["Vendor"] in ("Freight Way Properties LLC", "Wilkes & Partners CPA", "Triad Truck & Van Repair") else ""
        w.writerow([r["Vendor"], bc_no[r["Vendor"]], "Migrated", r["Track Payments for 1099"], issue])

D = read(sys.argv[1]); hdr = D["Vendor"]["hdr"]; D["Vendor"]["rows"] = []
problems = []
for r in keep:
    if r["Terms"] not in terms: problems.append(f"{r['Vendor']}: unmapped terms {r['Terms']}")
    if not r["ZIP"]: problems.append(f"{r['Vendor']}: missing ZIP")
    v = {"No.": bc_no[r["Vendor"]], "Name": r["Vendor"], "Address": r["Street"], "City": r["City"],
         "Phone No.": r["Phone"], "Vendor Posting Group": "DOMESTIC", "Payment Terms Code": terms.get(r["Terms"], ""),
         "Country/Region Code": "US", "Gen. Bus. Posting Group": "DOMESTIC", "ZIP Code": r["ZIP"],
         "State": r["State"], "Email": r["Email"], "Location Code": "MAIN"}
    D["Vendor"]["rows"].append([v[h] for h in hdr])
if problems:
    sys.exit("Stopped, unresolved data problems:\n  " + "\n  ".join(problems))
write(sys.argv[1], ROOT / "packages/QCS-05-VENDORS_import.xlsx", D)
print(f"QuickBooks rows: {len(src)} | BC vendors: {len(keep)}")
