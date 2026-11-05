"""
Compare two QuickBooks extracts and list every difference, then check each extract is internally consistent.

Usage: python tools/compare_extracts.py source/qbo-exports source/qbo-exports/extract-v2
A new extract must differ from the previous one ONLY by the approved corrections.
"""
import csv, sys
from pathlib import Path

A, B = Path(sys.argv[1]), Path(sys.argv[2])
FILES = {"qbo_trial_balance_2026-09-30.csv": "Account", "qbo_ar_aging_detail_2026-09-30.csv": "Num",
         "qbo_inventory_valuation_2026-09-30.csv": "Product/Service", "qbo_1099_contractor_summary_2026-01-01_2026-09-30.csv": "Vendor"}

def rows(p): return list(csv.DictReader(open(p, encoding="utf-8")))

for name, key in FILES.items():
    a = {r[key]: r for r in rows(A / name)}; b = {r[key]: r for r in rows(B / name)}
    diffs = [f"  removed: {k}" for k in a if k not in b] + [f"  added:   {k}" for k in b if k not in a]
    diffs += [f"  changed: {k}: " + ", ".join(f"{c} {a[k][c]} -> {b[k][c]}" for c in a[k] if a[k][c] != b[k][c])
              for k in a if k in b and a[k] != b[k]]
    print(f"{name}: {len(diffs)} difference(s)"); print("\n".join(diffs)) if diffs else None

# A/P lines have no unique key (that was the problem), so compare them as whole lines
name = "qbo_ap_aging_detail_2026-09-30.csv"
la = [tuple(r.values()) for r in rows(A / name)]; lb = [tuple(r.values()) for r in rows(B / name)]
extra = [l for l in la if la.count(l) > lb.count(l)]
print(f"{name}: {len(la) - len(lb)} line(s) fewer in the new extract"); [print("  removed:", l) for l in dict.fromkeys(extra)]

# internal consistency: control accounts = detail reports
for folder in (A, B):
    tb = {r["Account"]: r for r in rows(folder / "qbo_trial_balance_2026-09-30.csv")}
    bal = lambda acct: round(float(tb[acct]["Debit"] or 0) - float(tb[acct]["Credit"] or 0), 2) if acct in tb else 0.0
    ar = round(sum(float(r["Open Balance"]) for r in rows(folder / "qbo_ar_aging_detail_2026-09-30.csv")), 2)
    ap = round(sum(float(r["Open Balance"]) for r in rows(folder / name)), 2)
    inv = round(sum(float(r["Asset Value"]) for r in rows(folder / "qbo_inventory_valuation_2026-09-30.csv")), 2)
    checks = [("A/R", bal("Accounts Receivable (A/R)"), ar), ("A/P", -bal("Accounts Payable (A/P)"), ap),
              ("Inventory", bal("Inventory Asset"), inv)]
    total = tb["TOTAL"]
    print(f"{folder}: TB debits {total['Debit']} = credits {total['Credit']}: {total['Debit'] == total['Credit']}")
    for label, t, d in checks:
        print(f"  {label}: trial balance {t:,.2f} vs detail {d:,.2f} -> {'OK' if abs(t - d) < 0.005 else 'MISMATCH'}")
