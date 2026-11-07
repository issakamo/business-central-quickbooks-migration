"""
QuickBooks A/R Aging Detail (extract v2) -> opening AR journal lines (package QCS-07-OPEN-AR).

Rules (D-017, D-018):
  Posting Date 9/30/2026 | Document Date, Due Date = QuickBooks originals | Document No. = QuickBooks Num
  open balance only | Tax Liable = No | Reason Code MIGRATION | balancing account 25900 Opening Balance Clearing
  2% 10 Net 30 invoices keep the discount only if the discount date is on/after go-live and nothing was paid yet
Checks: every customer resolves through mapping/customer-xref.csv; total equals the trial balance A/R.
Usage:
  python tools/transform_open_ar.py <QCS-07-OPEN-AR_export-template.xlsx> [extract folder]
"""
import csv, sys
from datetime import date, timedelta
from pathlib import Path
from rapidstart_excel import read, write

ROOT = Path(__file__).resolve().parent.parent
EXTRACT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "source/qbo-exports/extract-v2"
POSTING_DATE, GO_LIVE = "2026-09-30", date(2026, 10, 1)
CLEARING = "25900"   # 25900 Opening Balance Clearing
def load(p): return list(csv.DictReader(open(p, encoding="utf-8")))

ar = load(EXTRACT / "qbo_ar_aging_detail_2026-09-30.csv")
tb = {r["Account"]: r for r in load(EXTRACT / "qbo_trial_balance_2026-09-30.csv")}
xref = {r["QBO Customer"]: r for r in load(ROOT / "mapping/customer-xref.csv")}
terms = {r["Customer"]: r["Terms"] for r in load(ROOT / "source/qbo-exports/qbo_customers.csv")}

D = read(sys.argv[1]); sheet = "Gen. Journal Line"; hdr = D[sheet]["hdr"]; D[sheet]["rows"] = []
problems, discounts, per_customer = [], [], {}
for i, r in enumerate(ar, start=1):
    x = xref.get(r["Customer"])
    if not x or not x["BC No."]:
        problems.append(f"{r['Num']}: customer '{r['Customer']}' has no BC number ({x['Status'] if x else 'not in cross-reference'})"); continue
    amount, original = float(r["Open Balance"]), float(r["Amount"])
    doc_date = date.fromisoformat(r["Date"])
    disc_date, disc_pct = "", "0"
    if terms[r["Customer"]] == "2% 10 Net 30" and r["Transaction Type"] == "Invoice":
        d = doc_date + timedelta(days=10)
        if d >= GO_LIVE and amount == original:
            disc_date, disc_pct = d.isoformat(), "2"
            discounts.append(f"{r['Num']} {r['Customer']} {amount:,.2f}: 2% until {d.isoformat()}")
        elif d >= GO_LIVE:
            discounts.append(f"{r['Num']} {r['Customer']}: discount window open but partially paid -> no discount")
    desc = f"Opening balance, QB {r['Transaction Type'].lower()} {r['Num']}"
    if amount != original: desc += f" (original {original:,.2f})"
    v = {"Journal Template Name": "GENERAL", "Journal Batch Name": "OB-AR", "Line No.": str(i * 10000),
         "Account Type": "Customer", "Account No.": x["BC No."], "Posting Date": POSTING_DATE,
         "Document Type": "Invoice" if r["Transaction Type"] == "Invoice" else "Credit Memo",
         "Document No.": r["Num"], "Description": desc, "Bal. Account No.": CLEARING, "Amount": f"{amount:.2f}",
         "Document Date": r["Date"], "Due Date": r["Due Date"], "Pmt. Discount Date": disc_date,
         "Payment Discount %": disc_pct, "Reason Code": "MIGRATION", "Bal. Account Type": "G/L Account", "Tax Liable": "false"}
    D[sheet]["rows"].append([v[h] for h in hdr])
    per_customer[x["BC No."]] = round(per_customer.get(x["BC No."], 0) + amount, 2)

total = round(sum(per_customer.values()), 2)
target = round(float(tb["Accounts Receivable (A/R)"]["Debit"] or 0), 2)
if abs(total - target) > 0.005: problems.append(f"journal total {total:,.2f} <> trial balance A/R {target:,.2f}")
if problems: sys.exit("Stopped:\n  " + "\n  ".join(problems))
write(sys.argv[1], ROOT / "packages/QCS-07-OPEN-AR_import.xlsx", D)
with open(ROOT / "mapping/reconciliation-targets-ar.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["BC Customer No.", "Expected balance at 9/30/2026"])
    w.writerows(sorted(per_customer.items())); w.writerow(["TOTAL", f"{total:.2f}"])
print(f"lines: {len(D[sheet]['rows'])} | customers: {len(per_customer)} | total {total:,.2f} = trial balance A/R {target:,.2f}")
print("payment discounts:"); [print("  " + d) for d in discounts or ["none"]]
