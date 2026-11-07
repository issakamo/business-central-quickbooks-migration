"""
QuickBooks Trial Balance (extract v2) -> opening G/L journal (package QCS-13-OPEN-GL).

Every trial balance account whose load method in mapping/account-mapping.csv is "G/L journal" becomes one line
(D-004, D-005, D-017): Posting Date 9/30/2026 | Amount = debit - credit | balancing account 25900 Opening Balance Clearing
Gen. Posting Type blank and Tax Liable = No, so year-to-date income and cost balances are not treated as new sales
or purchases (no tax). Reason Code MIGRATION.
Coverage check: every trial balance account must have a load method; "Not migrated" accounts must be zero.
Usage:
  python tools/transform_open_gl.py <QCS-13-OPEN-GL_export-template.xlsx> [extract folder]
"""
import csv, sys
from decimal import Decimal
from pathlib import Path
from rapidstart_excel import read, write

ROOT = Path(__file__).resolve().parent.parent
EXTRACT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "source/qbo-exports/extract-v2"
def load(p): return list(csv.DictReader(open(p, encoding="utf-8")))

tb = [r for r in load(EXTRACT / "qbo_trial_balance_2026-09-30.csv") if r["Account"] != "TOTAL"]
mapping = {r["QBO Account"]: r for r in load(ROOT / "mapping/account-mapping.csv")}
qbo_type = {r["Account"]: r["Type"] for r in load(ROOT / "source/qbo-exports/qbo_chart_of_accounts.csv")}
PNL = {"Income", "Other Income", "Cost of Goods Sold", "Expenses", "Other Expense"}

D = read(sys.argv[1]); s = "Gen. Journal Line"; h = D[s]["hdr"]; D[s]["rows"] = []
problems, by_method, line = [], {}, 0
gl_total = Decimal(0)
for r in tb:
    acct = r["Account"]; m = mapping.get(acct)
    bal = Decimal(r["Debit"] or "0") - Decimal(r["Credit"] or "0")
    if not m: problems.append(f"'{acct}' has no row in account-mapping.csv"); continue
    method = m["Load Method"]
    by_method[method] = by_method.get(method, Decimal(0)) + bal
    if method == "Not migrated":
        if bal != 0: problems.append(f"'{acct}' is not migrated but has balance {bal}")
        continue
    if method != "G/L journal": continue
    line += 1; gl_total += bal
    ytd = qbo_type.get(acct) in PNL
    v = {"Journal Template Name": "GENERAL", "Journal Batch Name": "OB-GL", "Line No.": str(line * 10000),
         "Account Type": "G/L Account", "Account No.": m["BC No."], "Posting Date": "2026-09-30", "Document Type": "",
         "Document No.": "OB-GL-20260930", "Document Date": "2026-09-30",
         "Description": (f"YTD 1/1-9/30/2026, QB {acct}" if ytd else f"Opening balance, QB {acct} at 9/30/2026")[:100],
         "Amount": f"{bal:.2f}", "Bal. Account Type": "G/L Account", "Bal. Account No.": "25900",
         "Reason Code": "MIGRATION", "Gen. Posting Type": "", "Tax Liable": "false"}
    D[s]["rows"].append([v[x] for x in h])

others = sum((v for k, v in by_method.items() if k not in ("G/L journal", "Not migrated")), Decimal(0))
if gl_total + others != 0: problems.append(f"trial balance does not balance: G/L {gl_total} + subledgers {others}")
if problems: sys.exit("Stopped:\n  " + "\n  ".join(problems))
write(sys.argv[1], ROOT / "packages/QCS-13-OPEN-GL_import.xlsx", D)
print(f"lines: {line} | G/L journal net {gl_total:,.2f}")
for k, v in sorted(by_method.items()): print(f"  {k:<22} {v:>16,.2f}")
print(f"expected 25900 after posting (QuickBooks figures): {-(others + gl_total):,.2f}")
