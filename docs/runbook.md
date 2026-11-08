# Migration Runbook: Queen City Supply Co.

Steps run in order for every trial run and for the production cutover.

## Phase 1: Company and setup

| Step | Action | Method | Check |
|---|---|---|---|
| 1.1 | Create company "Queen City Supply Co." from Production – Setup data only, modules per D-002 | Wizard | Customers, vendors, items empty |
| 1.2 | Company information: address, phone, email (bank fields blank) | Manual | Printed on a test invoice |
| 1.3 | Apply package QCS-01-COA, then Indent Chart of Accounts | RapidStart | 364 accounts; 40330 category Income |
| 1.4 | Apply package QCS-02-POSTING | RapidStart | 17 inserted, 21 modified, 0 errors |
| 1.5 | Apply package QCS-03-TAX-TERMS | RapidStart | 37 inserted, 0 errors |
| 1.6 | Inventory Setup: Location Mandatory = Yes; Prevent Negative Inventory = Yes | Manual | Fields set |
| 1.7 | General Ledger Setup: Payment Tolerance Warning = Yes | Manual | Field set |
| 1.8 | Apply package QCS-04-CUSTOMERS (built by tools/transform_customers.py) | RapidStart | 40 inserted, 0 errors; C00370 tax area NC-UNION |
| 1.9 | No. Series CUST: Last No. Used = C00400 | Manual | Next new customer is C00410 |
| 1.10 | Apply package QCS-05-VENDORS (built by tools/transform_vendors.py) | RapidStart | 22 inserted, 0 errors; V00050 state GA |
| 1.11 | No. Series VEND: Last No. Used = V00220 | Manual | Next new vendor is V00230 |
| 1.12 | Apply package QCS-06-ITEMS (built by tools/transform_items.py) | RapidStart | 65 inserted, 0 errors; EQ-3010 base unit PCS; Item Units of Measure created |
| 1.13 | IRS Forms: reporting period 2026 (1/1–12/31/2026); IRS Forms Guide creates forms and boxes; Vendor Setup: V00010, V00060, V00100, V00190 on 1099-NEC box 1 (I-007 vendors pending W-9 review); set NEC-01 and MISC-01 minimums to 2,000.00 (D-019). | Manual (guide) | Must be done BEFORE importing opening AP (QCS-08) |
| 1.14 | Apply QCS-10-BANK-ACCOUNTS (tools/transform_bank.py accounts) | RapidStart | 4 bank accounts, balance 0.00, posting groups per bank-accounts.csv |
| 2.1 | Apply QCS-07-OPEN-AR (tools/transform_open_ar.py, extract v2); Preview Posting; post batch OB-AR | RapidStart + journal | 37 lines; preview shows only 15110/25900 and no tax; Aged AR at 9/30 = 169,777.55; C00100 = 8,945.74; 25900 = -169,777.55 |
| 2.2 | Apply QCS-08-OPEN-AP (tools/transform_open_ap.py, extract v2); Preview Posting; post batch OB-AP | RapidStart + journal | 27 lines; only 22100/25900, no tax; Aged AP at 9/30 = 81,160.02; V00030 = -14,484.66; 25900 = -88,617.53; contractor bills carry NEC/NEC-01 |
| 2.3 | Apply QCS-09-OPEN-STOCK (tools/transform_open_stock.py, extract v2); Preview Posting; post batch OB-STOCK | RapidStart + item journal | 59 lines; only 14140/25900, nothing on 50140; Inventory Valuation at 9/30 = 164,831.46; CH-1001 qty 83; 25900 = -253,448.99; 59 items (107 lines, 48 split per I-018); Inventory Valuation at 9/30 = 164,831.46 |
| 2.4 | Apply QCS-11-OPEN-BANK (tools/transform_bank.py journal, extract v2); Preview Posting; post batch OB-BANK; opening bank reconciliation per bank account dated 9/30/2026 (D-021) | RapidStart + journal + bank reconciliation | Bank balances: OPERATING 85,562.55, PAYROLL 6,000.00, SAVINGS 50,000.00, CREDITCARD -1,842.37; all opening entries closed; Balance Last Statement = 9/30 balance |
| 2.5 | Apply QCS-13-OPEN-GL (tools/transform_open_gl.py, extract v2); Preview Posting; post batch OB-GL | RapidStart + journal | 47 lines; only G/L entries, no tax; 25900 Opening Balance Clearing = 0.00 (trial run 1: -0.09, I-018) |
| 2.5 | ... | ... | 47 lines; only G/L entries, no tax; Gen. Posting Type empty on all lines; 25900 Opening Balance Clearing = -0.09 (I-018; 0.00 expected in trial run 2) |
| 2.6 | Final reconciliation: BC Chart of Accounts balances vs QuickBooks trial balance per BC account (tools/reconcile_trial_balance.py) | Script | Every account matches; trial run 1 exceptions: 14140 +0.09, 25900 -0.09 (I-018) |
| 2.7 | Day-one tests (work date 11/10/2026, I-019): sales invoices to C00010 (NC-MECK), C00060 (SC-YORK), C00070 (exempt) with CH-1001 x2, PP-2001 x1, DELIVERY x1 | Manual | Tax 13.42 / 11.39 / 0.00; totals 176.11 / 174.08 / 162.69; tax to 23100 and 23110; delivery to 40390; CH-1001 inventory 77 |
| 2.8 | Apply QCS-14-BLOCK-ACCOUNTS (tools/block_accounts.py, D-022) | RapidStart | 176 modified, 0 inserted; client accounts and 40920 not blocked |
| 2.9 | Day-one process tests after blocking: purchase order (receive + invoice), sales order (ship + invoice), payment applied to an opening invoice | Manual | No "blocked" errors |
| 2.10 | After reconciliation sign-off: block 25900 Opening Balance Clearing and the MIGRATION General Posting Setup rows | Manual | Migration-only setup can no longer be used |

After posting each opening batch, delete the empty line BC leaves in it



## Phase 3: Trial run 2

| Step | Action | Method | Check |
|---|---|---|---|
| 3.1 | Create a new company and run every step of Phases 1 and 2 again, using the corrected tools | Runbook | Every check passes with no manual corrections; 25900 Opening Balance Clearing = 0.00 exactly |

