"""
QuickBooks Inventory Valuation (extract v2) -> opening stock item journal (package QCS-09-OPEN-STOCK).

Rules (D-006, D-016, D-017):
  Entry Type Positive Adjmt. | Location MAIN | Posting Date 9/30/2026 | Gen. Bus. Posting Group MIGRATION
  Quantity in the item's base unit (as counted in QuickBooks) | Amount = QuickBooks asset value (not a rounded unit cost)
  items with quantity 0 are skipped | Reason Code MIGRATION
  BC rounds the Unit Amount to G/L Setup "Unit-Amount Rounding Precision" (0.001) and posts Quantity x Unit Amount.
  Where that would not reproduce the QuickBooks value, the item is split into two lines (I-018):
  (quantity - 1) units at the rounded unit amount, and 1 unit carrying the exact remainder.
Checks: every item resolves through mapping/item-xref.csv; no negative quantity; BC's posting is simulated per line
and the simulated total must equal trial balance Inventory Asset.
Usage:
  python tools/transform_open_stock.py <QCS-09-OPEN-STOCK_export-template.xlsx> [extract folder]
"""
import csv, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from rapidstart_excel import read, write

ROOT = Path(__file__).resolve().parent.parent
EXTRACT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "source/qbo-exports/extract-v2"
UNIT_PRECISION = Decimal("0.001")   # General Ledger Setup: Unit-Amount Rounding Precision ($)
def load(p): return list(csv.DictReader(open(p, encoding="utf-8")))
def rnd(x, p): return x.quantize(p, rounding=ROUND_HALF_UP)
def bc_posts(qty, amount):
    """What BC posts as cost for one item journal line: Quantity x Unit Amount rounded to the precision."""
    return rnd(qty * rnd(amount / qty, UNIT_PRECISION), Decimal("0.01"))
def split(qty, value):
    """Lines (qty, amount) whose posted costs add up to value exactly."""
    if bc_posts(qty, value) == value: return [(qty, value)]
    unit = rnd(value / qty, UNIT_PRECISION)
    first = rnd((qty - 1) * unit, Decimal("0.01"))
    lines = [(qty - 1, first), (Decimal(1), value - first)]
    assert sum(bc_posts(q, a) for q, a in lines) == value, (qty, value)
    return lines

inv = load(EXTRACT / "qbo_inventory_valuation_2026-09-30.csv")
tb = {r["Account"]: r for r in load(EXTRACT / "qbo_trial_balance_2026-09-30.csv")}
item_no = {r["QBO Item"]: r["BC No."] for r in load(ROOT / "mapping/item-xref.csv")}

D = read(sys.argv[1]); sheet = "Item Journal Line"; hdr = D[sheet]["hdr"]; D[sheet]["rows"] = []
problems, skipped, targets, splits, simulated, line = [], [], [], [], [], 0
for r in inv:
    no = item_no.get(r["Product/Service"])
    qty, value = Decimal(r["Qty On Hand"]), Decimal(r["Asset Value"])
    if not no: problems.append(f"'{r['Product/Service']}' not in item cross-reference"); continue
    if qty < 0: problems.append(f"{no}: negative quantity {qty}"); continue
    if qty == 0:
        skipped.append(f"{no} {r['Product/Service']} (quantity 0, value {value:.2f})")
        if value != 0: problems.append(f"{no}: quantity 0 but value {value:.2f}")
        continue
    parts = split(qty, value)
    if len(parts) > 1: splits.append(no)
    for q, a in parts:
        line += 1
        v = {"Journal Template Name": "ITEM", "Journal Batch Name": "OB-STOCK", "Line No.": str(line * 10000),
             "Item No.": no, "Posting Date": "2026-09-30", "Entry Type": "Positive Adjmt.", "Location Code": "MAIN",
             "Quantity": f"{q:f}".rstrip("0").rstrip("."), "Amount": f"{a:.2f}", "Gen. Bus. Posting Group": "MIGRATION",
             "Document No.": "OB-STOCK-20260930", "Description": r["Product/Service"], "Reason Code": "MIGRATION",
             "Document Date": "2026-09-30"}
        D[sheet]["rows"].append([v[h] for h in hdr])
        simulated.append(bc_posts(q, a))
    targets.append([no, f"{qty:f}".rstrip("0").rstrip("."), f"{value:.2f}"])

total = sum(simulated, Decimal(0))
target = Decimal(tb["Inventory Asset"]["Debit"] or "0")
if total != target: problems.append(f"simulated BC posting {total:,.2f} <> trial balance Inventory Asset {target:,.2f}")
if problems: sys.exit("Stopped:\n  " + "\n  ".join(problems))
write(sys.argv[1], ROOT / "packages/QCS-09-OPEN-STOCK_import.xlsx", D)
with open(ROOT / "mapping/reconciliation-targets-stock.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["BC Item No.", "Expected quantity at MAIN", "Expected value at 9/30/2026"])
    w.writerows(targets); w.writerow(["TOTAL", "", f"{total:.2f}"])
print(f"items: {len(targets)} | lines: {line} ({len(splits)} items split) | simulated BC posting {total:,.2f} = trial balance Inventory Asset {target:,.2f}")
print("skipped:"); [print("  " + s) for s in skipped]
