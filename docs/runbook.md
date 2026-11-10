# Migration Runbook: Queen City Supply Co.

The steps for every trial run and for the production cutover, in order. This version reflects trial run 2 (BC online, BC 29.0), which ran end to end with no manual corrections.

**For every RapidStart package:** Import Package (`packages/rapidstart/…rapidstart`, the definition) → Import from Excel (`packages/…_import.xlsx`, the reviewed data built by our scripts; it overwrites the package data) → check No. of Package Records and No. of Package Errors (0) → Apply → compare the inserted/modified counts with the prediction. Import each package just before applying it: a package can only be imported after the records it refers to exist (I-012).

**After posting each opening batch,** delete the empty line BC leaves in it.

## Phase 0: Build the load files (before the run)

| Step | Action | Method | Check |
|---|---|---|---|
| 0.1 | Receive the final QuickBooks extract after the period is locked; compare it with the previous extract | `tools/compare_extracts.py` | Differences are only the approved corrections; A/R, A/P and Inventory Asset equal their detail reports |
| 0.2 | Rebuild every import file from the extract and the mapping files | `tools/build_package_0*.py`, `tools/transform_*.py`, `tools/block_accounts.py` | Every script finishes without "Stopped" |

## Phase 1: Company and setup

| Step | Action | Method | Check |
|---|---|---|---|
| 1.1 | Create company "Queen City Supply Co.", Production – Setup data only, modules per D-002 | Wizard | Template baseline: 350 accounts, 18 General Posting Setup rows, 11 payment terms, 5 tax groups; customers, vendors, items empty |
| 1.2 | Company information: address, phone, email (bank fields blank) | Manual | |
| 1.3 | Work Date 10/1/2026 | Manual | |
| 1.4 | QCS-01-COA, then Indent Chart of Accounts | RapidStart | 364 package records; 14 inserted, 45 modified; 40330 category Income; 25900 exists; nothing blocked |
| 1.5 | QCS-02-POSTING | RapidStart | 17 inserted, 21 modified; 9 active General Posting Setup rows, template rows blocked |
| 1.6 | QCS-03-TAX-TERMS | RapidStart | 37 inserted, 1 modified (I-001) |
| 1.7 | Tax Setup: Tax Account (Sales) = 23100 Sales Tax Payable, NC; Tax Account (Purchases) and Reverse Charge (Purchases) empty (I-022) | Manual | |
| 1.8 | Inventory Setup: Location Mandatory = Yes, Prevent Negative Inventory = Yes. G/L Setup: Payment Tolerance Warning = Yes (D-013). Confirm unchanged template values: Automatic Cost Posting on, Expected Cost Posting off, Automatic Cost Adjustment Always, FIFO; Payment Tolerance 0.1% / 1.00; Unit-Amount Rounding Precision 0.001 (I-018) | Manual | |
| 1.9 | QCS-04-CUSTOMERS, then No. Series CUST Last No. Used = C00400 | RapidStart + manual | 40 inserted; C00370 tax area NC-UNION; 62 contacts after 1.10 |
| 1.10 | QCS-05-VENDORS, then No. Series VEND Last No. Used = V00220 | RapidStart + manual | 22 inserted; V00050 state GA |
| 1.11 | QCS-06-ITEMS | RapidStart | 65 inserted, 0 modified; EQ-3010 base unit PCS; PP-2006 posting group PAPER |
| 1.12 | QCS-06B-ITEM-UOM (`tools/transform_item_uom.py 06B`) | RapidStart | 61 inserted; CH-1001 has a CASE Item Unit of Measure (I-021) |
| 1.13 | QCS-06C-ITEM-S-P-UOM (`tools/transform_item_uom.py 06C`), after 1.12 | RapidStart | 61 modified; CH-1001 Sales and Purch. Unit of Measure = CASE |
| 1.14 | IRS Forms: reporting period 2026 (1/1–12/31/2026); IRS Forms Guide creates forms and boxes; NEC-01 and MISC-01 minimums 600.00 → 2,000.00 (D-019); Vendor Setup V00010, V00060, V00100, V00190 on NEC / NEC-01 | Manual (guide) | Must be done before importing QCS-08 (I-017) |
| 1.15 | Reason Code MIGRATION; journal batches OB-AR, OB-AP, OB-BANK, OB-GL (template GENERAL) and OB-STOCK (template ITEM): no number series, no balancing account, Copy Tax Setup off, Suggest Balancing Amount off, Allow Tax Difference off, Copy to Posted Jnl. Lines on, Item Tracking on Lines off | Manual | |
| 1.16 | QCS-10-BANK-ACCOUNTS | RapidStart | 4 inserted; balances 0.00 |

## Phase 2: Opening balances

| Step | Action | Method | Check |
|---|---|---|---|
| 2.1 | QCS-07-OPEN-AR; Preview Posting; post OB-AR | RapidStart + journal | 37 lines; 4401 due date 7/11/2026; preview only 15110 and 25900, no tax; Aged AR at 9/30 = 169,777.55; C00100 = 8,945.74; 25900 = -169,777.55 |
| 2.2 | QCS-08-OPEN-AP; Preview Posting; post OB-AP | RapidStart + journal | 27 lines; OB-AP-0018 carries 2026 / NEC / NEC-01; preview only 22100 and 25900, no tax; Aged AP at 9/30 = 81,160.02; V00030 = -14,484.66; 25900 = -88,617.53 |
| 2.3 | QCS-09-OPEN-STOCK (corrected method, I-018); Preview Posting; post OB-STOCK | RapidStart + item journal | 107 lines (59 items, 48 split); preview 14140 = +164,831.46 exactly, nothing on 50140; Inventory Valuation at 9/30 = 164,831.46; 25900 = -253,448.99 |
| 2.4 | QCS-11-OPEN-BANK, post OB-BANK; QCS-12-OPEN-BANK-REC, match and post each reconciliation (D-021) | RapidStart + journal + bank reconciliation | OPERATING 85,562.55, PAYROLL 6,000.00, SAVINGS 50,000.00, CREDITCARD -1,842.37; opening entries closed; Balance Last Statement = 9/30 balance; 25900 = -393,169.17 |
| 2.5 | QCS-13-OPEN-GL; Preview Posting; post OB-GL | RapidStart + journal | 47 lines (94 G/L entries); Gen. Posting Type empty on all lines; no tax; **25900 Opening Balance Clearing = 0.00** |
| 2.6 | Final reconciliation: BC Chart of Accounts export vs the QuickBooks trial balance per BC account | `tools/reconcile_trial_balance.py` | Every account matches; BC total 0.00; sides agree. Report: docs/reconciliation-<run>.md |

## Phase 3: Go-live configuration and tests

| Step | Action | Method | Check |
|---|---|---|---|
| 3.1 | Review the single-record setup pages (Tax Setup, G/L Setup, Sales & Receivables, Purchases & Payables, Inventory Setup) for references to block candidates (I-022); then QCS-14-BLOCK-ACCOUNTS (D-022) | Manual + RapidStart | 176 modified; client accounts, 40920, 18100 and 25900 not blocked |
| 3.2 | G/L Setup: Allow Posting From 10/1/2026; User Setup has no overriding dates | Manual | A journal line dated 9/30/2026 is refused |
| 3.3 | Day-one tests dated after go-live: sales invoices to C00010 (NC-MECK), C00060 (SC-YORK), C00070 (exempt) with CH-1001 x2, PP-2001 x1, DELIVERY x1; purchase order V00030 CH-1001 x10 at 28.40; sales order C00100 CH-1001 x3; cash receipt C00100 applied to invoice 4410 | Manual | Tax 13.42 / 11.39 / 0.00; totals 176.11 / 174.08 / 162.69; FIFO COGS 84.85 from the opening layer; C00100 = 7,716.46; units of measure fill in on every line |
| 3.4 | IRS 1099 adjustments for Jan–Sep, amounts confirmed by the accountant (I-011); in trial runs, pay V00010's opening bill and create the 2026 forms | Manual | Trial run 2: V00010 NEC-01 = 15,787.24 (I-017) |
| 3.5 | Tax Details: only the reviewed rates plus BC's automatic 0% rows for blank and NONTAXABLE (D-023, I-020) | Manual | |
| 3.6 | After reconciliation sign-off: block 25900 Opening Balance Clearing (balance 0.00) and the three MIGRATION General Posting Setup rows | Manual | An item journal line with MIGRATION is refused |

## Run record

| Run | Environment | Result | Deviations from this runbook |
|---|---|---|---|
| Trial run 1 | Docker container, BC 28.3 | All loads posted; 53 of 55 accounts matched; 25900 = -0.09 (I-018) | Demo license allowed only November–February dates in the client (I-019): opening bank reconciliation imported, period lock not tested, day-one tests dated 11/10/2026. QCS-06B/06C not needed on 28.3. Tax Setup step (1.7) not yet in the runbook. |
| Trial run 2 | BC online, Dev sandbox, BC 29.0 | All checks passed; 54 of 54 accounts matched; 25900 = 0.00 | None. Findings fixed during the run: I-021 (item units of measure), I-022 (Tax Setup default account) |
