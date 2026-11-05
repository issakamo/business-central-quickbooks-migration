"""
QuickBooks products/services -> BC Item, plus the setup items depend on (package QCS-06-ITEMS).

Inputs (never edited by hand): source/qbo-exports/qbo_products_services.csv
Rules and approved corrections:
  mapping/item-corrections.csv, mapping/income-account-posting-group.csv, mapping/vendor-xref.csv
Outputs:
  mapping/item-xref.csv                   QuickBooks item -> BC item No. (used again for opening stock)
  packages/QCS-06-ITEMS_import.xlsx       filled from BC's own exported template
Usage:
  python tools/transform_items.py <path to QCS-06-ITEMS_export-template.xlsx>
"""
import csv, re, sys
from pathlib import Path
from rapidstart_excel import read, write

ROOT = Path(__file__).resolve().parent.parent
def load(p): return list(csv.DictReader(open(ROOT / p, encoding="utf-8")))

src = load("source/qbo-exports/qbo_products_services.csv")
corr = load("mapping/item-corrections.csv")
pg_by_income = {r["QBO Income Account"]: r["BC Gen. Prod. Posting Group"] for r in load("mapping/income-account-posting-group.csv")}
vendor_no = {r["QBO Vendor"]: r["BC No."] for r in load("mapping/vendor-xref.csv")}
sku_fix = {c["QBO Item"]: c["Corrected Value"] for c in corr if c["Field"] == "SKU"}
pg_fix = {c["QBO Item"]: c["Corrected Value"] for c in corr if c["Field"] == "Gen. Prod. Posting Group"}


def base_uom(name):
    """D-016: base unit of measure from the pack type in the QuickBooks item name."""
    n = name.lower()
    if "(case of" in n: return "CASE"
    if "pail" in n: return "PAIL"
    if re.search(r"\d+\s*lb bag", n): return "BAG"   # "50 lb bag", not "Cart with Bag"
    if "(pack of" in n: return "PACK"
    if re.search(r"\d+\s*lb box", n): return "BOX"   # "25 lb box", not "flat box" (sold by case)
    return "PCS"


D = read(sys.argv[1])
log, problems, xref = [], [], []

# --- supporting setup (processed before items) ---
def add(sheet, values):
    h = D[sheet]["hdr"]; r = [""] * len(h)
    for k, v in values.items(): r[h.index(k)] = v
    D[sheet]["rows"].append(r)
add("204 Unit of Measure", {"Code": "CASE", "Description": "Case", "International Standard Code": "CS"})
add("204 Unit of Measure", {"Code": "PAIL", "Description": "Pail", "International Standard Code": "PL"})
add("251 Gen. Product Posting Group", {"Code": "DELIVERY", "Description": "Delivery charges", "Auto Insert Default": "true"})
gps = "252 General Posting Setup"; gh = D[gps]["hdr"]
tmpl = dict(zip(gh, next(r for r in D[gps]["rows"] if r[0] == "DOMESTIC" and r[1] == "CHEMICALS")))
row = {k: "" for k in gh}
row.update({"Gen. Bus. Posting Group": "DOMESTIC", "Gen. Prod. Posting Group": "DELIVERY",
            "Sales Account": "40390", "Sales Credit Memo Account": "40390",
            "Sales Line Disc. Account": "40910", "Sales Inv. Disc. Account": "40910",
            "Description": "Domestic trade, delivery charges (service item, sales only)",
            "View All Accounts on Lookup": "false", "Blocked": "false"})
add(gps, row)

# --- items ---
ih = D["Item"]["hdr"]; D["Item"]["rows"] = []
for r in src:
    name = r["Product/Service Name"]
    service = r["Type"] == "Service"
    sku = "DELIVERY" if service and name == "Delivery Charge" else (r["SKU"] or sku_fix.get(name, ""))
    if not sku: problems.append(f"{name}: no SKU and no approved correction"); continue
    pg = pg_fix.get(sku) or pg_by_income.get(r["Income Account"])
    if not pg: problems.append(f"{sku}: unmapped income account {r['Income Account']}")
    vend = vendor_no.get(r["Preferred Vendor"], "") if r["Preferred Vendor"] else ""
    if r["Preferred Vendor"] and not vend: problems.append(f"{sku}: preferred vendor not in vendor-xref")
    uom = "PCS" if service else base_uom(name)
    v = {"No.": sku, "Description": name, "Base Unit of Measure": uom, "Type": "Service" if service else "Inventory",
         "Inventory Posting Group": "" if service else "RESALE", "Unit Price": r["Sales Price/Rate"],
         "Costing Method": "FIFO", "Unit Cost": r["Purchase Cost"] or "0", "Vendor No.": vend,
         "Gen. Prod. Posting Group": pg or "", "Tax Group Code": "SUPPLIES" if r["Taxable"] == "Yes" else "NONTAXABLE",
         "Sales Unit of Measure": uom, "Purch. Unit of Measure": uom}
    D["Item"]["rows"].append([v[h] for h in ih])
    note = "I-008" if name in sku_fix else ("I-009" if sku in pg_fix else ("D-015" if service else ""))
    xref.append([name, r["SKU"], sku, uom, pg, note])
if problems:
    sys.exit("Stopped, unresolved data problems:\n  " + "\n  ".join(problems))
with open(ROOT / "mapping/item-xref.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["QBO Item", "QBO SKU", "BC No.", "Base UOM", "Gen. Prod. Posting Group", "Issue/Decision"])
    w.writerows(xref)
write(sys.argv[1], ROOT / "packages/QCS-06-ITEMS_import.xlsx", D)
print(f"QuickBooks rows: {len(src)} | BC items: {len(D['Item']['rows'])}")
