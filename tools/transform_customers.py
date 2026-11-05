"""
QuickBooks customers -> BC Customer (package QCS-04-CUSTOMERS).

Inputs (never edited by hand):
  source/qbo-exports/qbo_customers.csv
Rules and approved corrections:
  mapping/customer-corrections.csv, mapping/city-tax-area.csv, mapping/payment-terms.csv
Outputs:
  mapping/customer-xref.csv                     QuickBooks name -> BC No. (used again for open AR)
  packages/QCS-04-CUSTOMERS_import.xlsx         filled from BC's own exported template
Usage:
  python tools/transform_customers.py <path to QCS-04-CUSTOMERS_export-template.xlsx>
"""
import csv, sys
from pathlib import Path
from rapidstart_excel import read, write

ROOT = Path(__file__).resolve().parent.parent
def load(p): return list(csv.DictReader(open(ROOT / p, encoding="utf-8")))

src = load("source/qbo-exports/qbo_customers.csv")
corr = load("mapping/customer-corrections.csv")
tax = {(r["City"], r["State"]): r["Tax Area Code"] for r in load("mapping/city-tax-area.csv")}
terms = {r["QBO Terms"]: r["BC Payment Terms Code"] for r in load("mapping/payment-terms.csv")}

merge = {c["QBO Customer"]: c["Corrected Value"] for c in corr if c["Field"] == "Merge Into"}
exclude = {c["QBO Customer"] for c in corr if c["Field"] == "Exclude"}
fixes = {(c["QBO Customer"], c["Field"]): c["Corrected Value"] for c in corr if c["Field"] not in ("Merge Into", "Exclude")}

# 1. records that become BC customers (merged names are not separate customers)
keep = [r for r in src if r["Customer"] not in exclude and r["Customer"] not in merge]
keep.sort(key=lambda r: r["Customer"].lower())
bc_no = {r["Customer"]: f"C{(i + 1) * 10:05d}" for i, r in enumerate(keep)}

# 2. cross-reference: every QuickBooks name -> BC No. (or why it has none)
xref = []
for r in src:
    name = r["Customer"]
    if name in exclude:
        xref.append([name, "", "Not migrated", "I-003"])
    elif name in merge:
        xref.append([name, bc_no[merge[name]], f"Merged into {merge[name]}", "I-002"])
    else:
        xref.append([name, bc_no[name], "Migrated", ""])
with open(ROOT / "mapping/customer-xref.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["QBO Customer", "BC No.", "Status", "Issue"]); w.writerows(sorted(xref))

# 3. BC customer records
template = sys.argv[1]
D = read(template)
hdr = D["Customer"]["hdr"]; D["Customer"]["rows"] = []
problems = []
for r in keep:
    name = r["Customer"]
    zipc = fixes.get((name, "Shipping ZIP"), r["Shipping ZIP"])
    area = tax.get((r["Shipping City"], r["Shipping State"]))
    if not area: problems.append(f"{name}: no tax area for {r['Shipping City']}, {r['Shipping State']}")
    if not zipc: problems.append(f"{name}: missing ZIP")
    if r["Terms"] not in terms: problems.append(f"{name}: unmapped terms {r['Terms']}")
    exempt = r["Tax Exempt"] == "Yes"
    v = {"No.": bc_no[name], "Name": name, "Address": r["Shipping Street"], "City": r["Shipping City"],
         "Phone No.": r["Phone"], "Customer Posting Group": "DOMESTIC", "Payment Terms Code": terms.get(r["Terms"], ""),
         "Country/Region Code": "US", "Location Code": "MAIN", "Gen. Bus. Posting Group": "DOMESTIC",
         "ZIP Code": zipc, "State": r["Shipping State"], "Email": r["Email"], "Tax Area Code": area or "",
         "Tax Liable": "false" if exempt else "true", "Tax Exemption No.": r["Exemption Certificate No."] if exempt else ""}
    D["Customer"]["rows"].append([v[h] for h in hdr])
if problems:
    sys.exit("Stopped, unresolved data problems:\n  " + "\n  ".join(problems))
(ROOT / "packages").mkdir(exist_ok=True)
write(template, ROOT / "packages/QCS-04-CUSTOMERS_import.xlsx", D)
print(f"QuickBooks rows: {len(src)} | BC customers: {len(keep)} | merged: {len(merge)} | excluded: {len(exclude)}")
