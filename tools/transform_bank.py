"""
QuickBooks bank and credit card accounts -> BC bank accounts and opening bank journal (D-009, D-021).

Two packages, applied in order (a journal line cannot refer to a bank account that does not exist yet, I-012):
  python tools/transform_bank.py accounts <QCS-10-BANK-ACCOUNTS_export-template.xlsx>
  python tools/transform_bank.py journal  <QCS-11-OPEN-BANK_export-template.xlsx> [extract folder]
  python tools/transform_bank.py rec      <QCS-12-OPEN-BANK-REC_export-template.xlsx> [extract folder]
The opening reconciliation (statement no. 0, dated 9/30/2026) closes each opening entry, so the first real
statement (no. 1) starts from the 9/30 statement balance (D-021). It is imported because the Docker demo
license rejects dates outside November-February typed in the client (I-019).
Rules: one opening entry per bank account at 9/30/2026 against 25900 Opening Balance Clearing;
balance = trial balance (debit positive; the credit card is a credit, so negative); Reason Code MIGRATION.
"""
import csv, sys
from pathlib import Path
from rapidstart_excel import read, write

ROOT = Path(__file__).resolve().parent.parent
def load(p): return list(csv.DictReader(open(p, encoding="utf-8")))
banks = load(ROOT / "mapping/bank-accounts.csv")
mode, template = sys.argv[1], sys.argv[2]
D = read(template)

if mode == "accounts":
    s = "Bank Account"; h = D[s]["hdr"]; D[s]["rows"] = []
    for b in banks:
        v = {"No.": b["BC Bank Account No."], "Name": b["Name"], "Bank Acc. Posting Group": b["Bank Acc. Posting Group"]}
        D[s]["rows"].append([v[x] for x in h])
    write(template, ROOT / "packages/QCS-10-BANK-ACCOUNTS_import.xlsx", D)
    print(f"bank accounts: {len(banks)}")

elif mode == "journal":
    extract = Path(sys.argv[3]) if len(sys.argv) > 3 else ROOT / "source/qbo-exports/extract-v2"
    tb = {r["Account"]: r for r in load(extract / "qbo_trial_balance_2026-09-30.csv")}
    s = "Gen. Journal Line"; h = D[s]["hdr"]; D[s]["rows"] = []
    total = 0.0
    for i, b in enumerate(banks, start=1):
        t = tb[b["QBO Account"]]
        amount = round(float(t["Debit"] or 0) - float(t["Credit"] or 0), 2)
        total += amount
        v = {"Journal Template Name": "GENERAL", "Journal Batch Name": "OB-BANK", "Line No.": str(i * 10000),
             "Account Type": "Bank Account", "Account No.": b["BC Bank Account No."], "Posting Date": "2026-09-30",
             "Document Type": "", "Document No.": "OB-BANK-20260930", "Document Date": "2026-09-30",
             "Description": f"Opening balance, QB {b['QBO Account']} at 9/30/2026", "Amount": f"{amount:.2f}",
             "Bal. Account Type": "G/L Account", "Bal. Account No.": "25900", "Reason Code": "MIGRATION", "Tax Liable": "false"}
        D[s]["rows"].append([v.get(x, "") for x in h])
        print(f"  {b['BC Bank Account No.']:<11} {amount:>12,.2f}")
    write(template, ROOT / "packages/QCS-11-OPEN-BANK_import.xlsx", D)
    print(f"lines: {len(banks)} | net {total:,.2f}")

elif mode == "rec":
    extract = Path(sys.argv[3]) if len(sys.argv) > 3 else ROOT / "source/qbo-exports/extract-v2"
    tb = {r["Account"]: r for r in load(extract / "qbo_trial_balance_2026-09-30.csv")}
    head = next(k for k in D if k.startswith("Bank Acc. Reconciliation") and "Li" not in k[25:])
    lines = next(k for k in D if k != head)
    hh, hl = D[head]["hdr"], D[lines]["hdr"]; D[head]["rows"], D[lines]["rows"] = [], []
    for b in banks:
        t = tb[b["QBO Account"]]
        amount = f"{float(t['Debit'] or 0) - float(t['Credit'] or 0):.2f}"
        h = {"Statement Type": "Bank Reconciliation", "Bank Account No.": b["BC Bank Account No."], "Statement No.": "0",
             "Statement Ending Balance": amount, "Statement Date": "2026-09-30"}
        l = {"Statement Type": "Bank Reconciliation", "Bank Account No.": b["BC Bank Account No."], "Statement No.": "0",
             "Statement Line No.": "10000", "Transaction Date": "2026-09-30",
             "Description": "Opening balance 9/30/2026 (statement balance = book balance, D-021)", "Statement Amount": amount}
        D[head]["rows"].append([h[x] for x in hh]); D[lines]["rows"].append([l[x] for x in hl])
        print(f"  {b['BC Bank Account No.']:<11} statement 0, ending balance {float(amount):>12,.2f}")
    write(template, ROOT / "packages/QCS-12-OPEN-BANK-REC_import.xlsx", D)
