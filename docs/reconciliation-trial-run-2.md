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

## 5. Go-live configuration and day-one tests (Phase 3)

| Step | Test | Result |
|---|---|---|
| 3.1 | Block 176 unused template accounts (QCS-14) | 176 modified; no client account blocked |
| 3.2 | Period lock: Allow Posting From 10/1/2026 | A journal line dated 9/30/2026 was refused; October postings allowed |
| 3.3 | Day-one tests dated 10/5/2026: sales invoices to NC (C00010), SC (C00060) and an exempt customer (C00070); purchase order; sales order; payment applied to opening invoice 4410 | All results as predicted: tax 13.42 / 11.39 / 0.00; FIFO cost from the opening layer; C00100 balance 7,716.46; units of measure filled in on every line (I-021) |
| 3.4 | 1099: Jan–Sep amounts entered as IRS 1099 adjustments; October payment on opening bill OB-AP-0018 | BC's 2026 NEC-01 amount for V00010 Andre Coleman = 15,787.24 (14,200.00 + 1,587.24), as predicted (I-011, I-017) |
| 3.5 | Automatic tax details (I-020) and Tax Setup default accounts (I-022) | Automatic 0% rows explained and kept (D-023); Tax Setup defaults moved off a blocked account |
| 3.6 | Block 25900 Opening Balance Clearing and the MIGRATION posting setup rows | An item journal line with MIGRATION was refused |

## 6. Open items before production cutover

These are client decisions or data, not defects in the migration method:

- I-006, I-007: 1099 contractors' TINs from W-9s; W-9 review of Freight Way Properties LLC, Wilkes & Partners CPA and Triad Truck & Van Repair (accountant).
- I-011: at cutover, the accountant confirms the Jan–Sep 1099 amounts from QuickBooks before they are entered as adjustments.
- D-019: accountant reviews the remaining MISC box minimums against the 2026 IRS instructions.
- D-023: behavior when a taxable (SUPPLIES) rate is missing for a jurisdiction is untested; accountant to review the tax setup.
- Payment methods: vendor payment lines highlight Payment Method Code; the client decides which methods to use.

## Sign-off

| Role | Name | Date | Signature |
|---|---|---|---|
| Client accountant | | | |
| Migration consultant | Issaka Mohammed | | |
