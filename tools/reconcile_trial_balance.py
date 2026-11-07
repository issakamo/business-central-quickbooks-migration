"""
Final reconciliation: BC balance per G/L account vs the QuickBooks trial balance mapped to BC accounts.

Inputs:
  BC export of Chart of Accounts (No., Name, Income/Balance, Account Category, Balance) -- all entries are dated
  9/30/2026, so current balances are balances at the cutover
  source/qbo-exports/extract-v2/qbo_trial_balance_2026-09-30.csv, mapping/account-mapping.csv
Checks:
  1. every BC account: BC balance = sum of the QuickBooks accounts mapped to it
  2. any BC account with a balance but no QuickBooks source is reported (25900 must be 0.00)
  3. balance sheet / income statement side agrees between QuickBooks type and BC Income/Balance
  4. BC accounts in total balance (debits = credits)
Output: reconciliation/trial-balance-reconciliation-<run>.csv and a printed summary.
Usage:
  python tools/reconcile_trial_balance.py <BC chart of accounts export.xlsx> <run name> [known exceptions issue]
"""
import csv, sys
from decimal import Decimal
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
bc_file, run = sys.argv[1], sys.argv[2]
def load(p): return list(csv.DictReader(open(p, encoding="utf-8")))

tb = [r for r in load(ROOT / "source/qbo-exports/extract-v2/qbo_trial_balance_2026-09-30.csv") if r["Account"] != "TOTAL"]
mapping = {r["QBO Account"]: r for r in load(ROOT / "mapping/account-mapping.csv")}
qtype = {r["Account"]: r["Type"] for r in load(ROOT / "source/qbo-exports/qbo_chart_of_accounts.csv")}
PNL = {"Income", "Other Income", "Cost of Goods Sold", "Expenses", "Other Expense"}

ws = openpyxl.load_workbook(bc_file, data_only=True).worksheets[0]
rows = list(ws.iter_rows(values_only=True)); hdr = list(rows[0])
bc = {}
for r in rows[1:]:
    d = dict(zip(hdr, r))
    if d["No."]: bc[str(d["No."])] = {"name": d["Name"], "side": d["Income/Balance"], "bal": Decimal(str(d["Balance"] or 0)).quantize(Decimal("0.01"))}

expected, sources, side = {}, {}, {}
for r in tb:
    m = mapping[r["Account"]]
    if not m["BC No."]: continue
    amt = Decimal(r["Debit"] or "0") - Decimal(r["Credit"] or "0")
    expected[m["BC No."]] = expected.get(m["BC No."], Decimal(0)) + amt
    sources.setdefault(m["BC No."], []).append(r["Account"])
    side[m["BC No."]] = "Income Statement" if qtype.get(r["Account"]) in PNL else "Balance Sheet"

out, diffs, side_errors = [], [], []
for no in sorted(set(expected) | {n for n, v in bc.items() if v["bal"] != 0}):
    exp = expected.get(no, Decimal(0)); got = bc.get(no, {}).get("bal", Decimal(0)); diff = got - exp
    status = "OK" if diff == 0 else "DIFFERENCE"
    if diff: diffs.append((no, bc.get(no, {}).get("name", "?"), exp, got, diff))
    if no in side and no in bc and bc[no]["side"] != side[no]:
        side_errors.append(f"{no}: QuickBooks side {side[no]}, BC {bc[no]['side']}")
    out.append([no, bc.get(no, {}).get("name", "(not in BC export)"), "; ".join(sources.get(no, ["(none)"])),
                f"{exp:.2f}", f"{got:.2f}", f"{diff:.2f}", status])

(ROOT / "reconciliation").mkdir(exist_ok=True)
path = ROOT / f"reconciliation/trial-balance-reconciliation-{run}.csv"
with open(path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["BC Account", "BC Name", "QuickBooks source account(s)", "QuickBooks 9/30/2026",
                                    "BC 9/30/2026", "Difference", "Status"]); w.writerows(out)
total_bc = sum(v["bal"] for v in bc.values())
print(f"accounts compared: {len(out)} | matching: {len(out) - len(diffs)} | differences: {len(diffs)}")
for d in diffs: print(f"  {d[0]} {d[1]}: QuickBooks {d[2]:,.2f}  BC {d[3]:,.2f}  difference {d[4]:+,.2f}")
print(f"BC total of all balances (must be 0.00): {total_bc:,.2f}")
print("side check:", "all agree" if not side_errors else side_errors)
print(f"written: {path.relative_to(ROOT)}")
