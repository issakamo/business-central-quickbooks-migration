# Reconciliation Report: Trial Run 2

**Company:** Queen City Supply Co. (Business Central online, Dev sandbox, BC 29.0)
**Cutover:** balances as of 9/30/2026, go-live 10/1/2026
**Source:** QuickBooks Online extract v2 (after corrections I-013, I-014, I-015)
**Method:** the runbook from trial run 1, with its fixes (I-001, I-018) and one new fix found in this run (I-021)

## 1. Trial balance, account by account

Produced by `tools/reconcile_trial_balance.py` from the BC Chart of Accounts export (`reconciliation/bc-chart-of-accounts-trial-run-2.xlsx`) and the QuickBooks trial balance mapped through `mapping/account-mapping.csv`. Detail: `reconciliation/trial-balance-reconciliation-trial-run-2.csv`.

| Result | Trial run 1 | Trial run 2 |
|---|---|---|
| BC accounts with a balance, compared to QuickBooks | 55 | 54 |
| Matching to the cent | 53 | **54** |
| Differences | 2 (I-018) | **0** |
| 25900 Opening Balance Clearing | -0.09 | **0.00** |
| BC total of all balances | 0.00 | 0.00 |
| Balance sheet / income statement side agrees with QuickBooks | All accounts | All accounts |

Trial run 2 compares one account fewer because 25900 Opening Balance Clearing now has a zero balance and no QuickBooks source, so there is nothing to compare.

## 2. Subledgers

| Check | QuickBooks | BC | Status |
|---|---|---|---|
| Aged Accounts Receivable at 9/30/2026 | 169,777.55 | 169,777.55 | Match |
| C00100 Dilworth Dental Group, PLLC (merged, I-002/I-016) | 8,945.74 | 8,945.74 | Match |
| Aged Accounts Payable at 9/30/2026 | 81,160.02 | 81,160.02 | Match |
| Inventory Valuation at 9/30/2026 | 164,831.46 | 164,831.46 | **Match** (I-018 fixed) |
| Bank accounts (4), opening reconciliations posted | 139,720.18 | 139,720.18 | Match; all opening entries closed |

## 3. Opening balance clearing account

All five loads (AR, AP, stock, bank, G/L) posted against 25900 Opening Balance Clearing. Final balance: **0.00**.

## 4. What trial run 2 proved

| Issue | Trial run 1 | Trial run 2 |
|---|---|---|
| I-001 System timestamps in packages | 16 records "modified" in QCS-03 | 1 modified (only the intended change) |
| I-018 Opening stock rounding | Inventory +0.09 | Exact (corrected transformation) |
| I-019 Demo-license date restriction | Dates in Sep/Oct could not be typed | Not applicable online |
| I-021 Item Units of Measure (BC 29.0) | Created by BC automatically | Not created; found in this run and loaded explicitly (QCS-06B, QCS-06C) |

The packages and scripts were built against BC 28.3 and ran unchanged on BC 29.0, except for I-021, which was found by a check and fixed with two new packages that work on both versions.

## 5. Open items before production cutover

- Phase 3 of trial run 2: blocking unused accounts, the period lock, day-one tests dated in October, and the 1099 check (I-011, I-017).
- I-006, I-007, I-011: 1099 TINs, W-9 review, and Jan–Sep 1099 amounts (accountant).
- I-020: zero-rate tax details created automatically by BC (check Tax Setup).

## Sign-off

| Role | Name | Date | Signature |
|---|---|---|---|
| Client accountant | | | |
| Migration consultant | Issaka Mohammed | | |
