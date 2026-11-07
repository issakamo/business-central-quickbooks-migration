# Reconciliation Report: Trial Run 1

**Company:** Queen City Supply Co. (BC 28.3, Docker container)
**Cutover:** balances as of 9/30/2026, go-live 10/1/2026
**Source:** QuickBooks Online extract v2 (after corrections I-013, I-014, I-015)

## 1. Trial balance, account by account

Produced by `tools/reconcile_trial_balance.py` from the BC Chart of Accounts export and the QuickBooks trial balance mapped through `mapping/account-mapping.csv`. Detail: `reconciliation/trial-balance-reconciliation-trial-run-1.csv`.

| Result | Count |
|---|---|
| BC accounts compared | 55 |
| Matching to the cent | 53 |
| Differences | 2 (both explained by I-018) |
| BC total of all balances | 0.00 |
| Balance sheet / income statement side agrees with QuickBooks | All accounts |

| BC account | QuickBooks | BC | Difference | Explanation |
|---|---|---|---|---|
| 14140 Inventory Asset | 164,831.46 | 164,831.55 | +0.09 | I-018: item journal recalculates cost from the unit amount rounded to 0.001 |
| 25900 Opening Balance Clearing | 0.00 | -0.09 | -0.09 | Mirror of the inventory difference |

## 2. Subledgers

| Check | QuickBooks | BC | Status |
|---|---|---|---|
| Aged Accounts Receivable at 9/30/2026 | 169,777.55 | 169,777.55 | Match |
| C00100 Dilworth Dental Group, PLLC (merged, I-002/I-016) | 8,945.74 | 8,945.74 | Match |
| Aged Accounts Payable at 9/30/2026 | 81,160.02 | 81,160.02 | Match |
| Inventory Valuation at 9/30/2026 | 164,831.46 | 164,831.55 | +0.09 (I-018) |
| Bank accounts (4), opening reconciliations posted | 139,720.18 | 139,720.18 | Match; all opening entries closed |

## 3. Opening balance clearing account

All five loads (AR, AP, stock, bank, G/L) posted against 25900 Opening Balance Clearing. Final balance: **-0.09**, fully explained by I-018. Expected 0.00 in trial run 2 with the corrected stock transformation.

## 4. Open items before production cutover

- I-018: prove the corrected stock method in trial run 2.
- I-006, I-007, I-011: 1099 TINs, W-9 review, and Jan–Sep 1099 amounts (accountant).
- I-019: September/October dates cannot be typed in the Docker demo license; trial run 2 to be run in BC online.

## Sign-off

| Role | Name | Date | Signature |
|---|---|---|---|
| Client accountant | | | |
| Migration consultant | Issaka Mohammed | | |
