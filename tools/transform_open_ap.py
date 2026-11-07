"""
QuickBooks A/P Aging Detail (extract v2) -> opening AP journal lines (package QCS-08-OPEN-AP).

Rules (D-017, D-018, I-017):
  Posting Date 9/30/2026 | Document Date, Due Date = QuickBooks originals
  Document No. = OB-AP-0001... (QuickBooks bills have no own number) | External Document No. = vendor's invoice no.
  Amount: bills negative (credit to vendor), vendor credits positive | Tax Liable = No | Reason Code MIGRATION
  balancing account 25900 Opening Balance Clearing
  2% 10 Net 30 bills keep the discount if the discount date is on/after go-live
  1099 contractors' bills carry IRS 1099 period/form/box so post-go-live payments are counted (I-017)
Checks: every vendor resolves through mapping/vendor-xref.csv; no duplicate external document no. per vendor;
total equals the trial balance A/P.
Usage:
  python tools/transform_open_ap.py <QCS-08-OPEN-AP_export-template.xlsx> [extract folder]
"""
import csv, sys
from datetime import date, timedelta
from pathlib import Path
from rapidstart_excel import read, write

ROOT = Path(__file__).resolve().parent.parent
EXTRACT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "source/qbo-exports/extract-v2"
POSTING_DATE, GO_LIVE = "2026-09-30", date(2026, 10, 1)
CLEARING = "25900"                                  # 25900 Opening Balance Clearing
IRS_1099 = {"V00010", "V00060", "V00100", "V00190"}  # IRS 1099 Vendor Form Box Setup: NEC / NEC-01
def load(p): return list(csv.DictReader(open(p, encoding="utf-8")))

ap = load(EXTRACT / "qbo_ap_aging_detail_2026-09-30.csv")
tb = {r["Account"]: r for r in load(EXTRACT / "qbo_trial_balance_2026-09-30.csv")}
xref = {r["QBO Vendor"]: r["BC No."] for r in load(ROOT / "mapping/vendor-xref.csv")}
terms = {r["Vendor"]: r["Terms"] for r in load(ROOT / "source/qbo-exports/qbo_vendors.csv")}

D = read(sys.argv[1]); sheet = "Gen. Journal Line"; hdr = D[sheet]["hdr"]; D[sheet]["rows"] = []
problems, notes, per_vendor, seen = [], [], {}, set()
for i, r in enumerate(ap, start=1):
    no = xref.get(r["Vendor"])
    if not no: problems.append(f"{r['Num']}: vendor '{r['Vendor']}' not in cross-reference"); continue
    if (no, r["Num"]) in seen: problems.append(f"{r['Num']}: duplicate external document no. for {no}")
    seen.add((no, r["Num"]))
    is_bill = r["Transaction Type"] == "Bill"
    open_bal = float(r["Open Balance"])                   # bills positive, vendor credits negative in QuickBooks
    amount = -open_bal                                    # BC: vendor invoice = credit (negative)
    disc_date, disc_pct = "", "0"
    if is_bill and terms[r["Vendor"]] == "2% 10 Net 30":
        d = date.fromisoformat(r["Date"]) + timedelta(days=10)
        if d >= GO_LIVE and r["Open Balance"] == r["Amount"]:
            disc_date, disc_pct = d.isoformat(), "2"; notes.append(f"{r['Num']} {r['Vendor']}: 2% until {d}")
    irs = no in IRS_1099 and is_bill
    if irs: notes.append(f"{r['Num']} {r['Vendor']} ({no}): 1099 NEC / NEC-01")
    v = {"Journal Template Name": "GENERAL", "Journal Batch Name": "OB-AP", "Line No.": str(i * 10000),
         "Account Type": "Vendor", "Account No.": no, "Posting Date": POSTING_DATE,
         "Document Type": "Invoice" if is_bill else "Credit Memo", "Document No.": f"OB-AP-{i:04d}",
         "Description": f"Opening balance, QB {r['Transaction Type'].lower()} {r['Num']}",
         "Bal. Account No.": CLEARING, "Amount": f"{amount:.2f}", "Document Date": r["Date"], "Due Date": r["Due Date"],
         "Pmt. Discount Date": disc_date, "Payment Discount %": disc_pct, "Reason Code": "MIGRATION",
         "Bal. Account Type": "G/L Account", "External Document No.": r["Num"], "Tax Liable": "false",
         "IRS 1099 Reporting Period": "2026" if irs else "", "IRS 1099 Form No.": "NEC" if irs else "",
         "IRS 1099 Form Box No.": "NEC-01" if irs else ""}
    D[sheet]["rows"].append([v[h] for h in hdr])
    per_vendor[no] = round(per_vendor.get(no, 0) + amount, 2)

total = round(sum(per_vendor.values()), 2)
target = -round(float(tb["Accounts Payable (A/P)"]["Credit"] or 0), 2)
if abs(total - target) > 0.005: problems.append(f"journal total {total:,.2f} <> trial balance A/P {target:,.2f}")
if problems: sys.exit("Stopped:\n  " + "\n  ".join(problems))
write(sys.argv[1], ROOT / "packages/QCS-08-OPEN-AP_import.xlsx", D)
with open(ROOT / "mapping/reconciliation-targets-ap.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["BC Vendor No.", "Expected balance at 9/30/2026"])
    w.writerows(sorted(per_vendor.items())); w.writerow(["TOTAL", f"{total:.2f}"])
print(f"lines: {len(D[sheet]['rows'])} | vendors: {len(per_vendor)} | total {total:,.2f} = trial balance A/P {target:,.2f}")
print("notes:"); [print("  " + n) for n in notes or ["none"]]
