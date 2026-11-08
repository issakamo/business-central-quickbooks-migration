# Trial Run 2 Plan

**Where:** Business Central online, Dev sandbox (BC 29.0), new company "Queen City Supply Co."
**Why online:** no demo-license date restriction (I-019); newer version than trial run 1 (28.3), which tests that the packages and scripts are portable.
**Goal:** run the whole runbook with no manual corrections, ending with 25900 Opening Balance Clearing = 0.00 exactly (I-018 fixed).
**Trial run 1** (Docker container) is kept unchanged as evidence.

## How packages move to the new company

The exported `.rapidstart` files (in `packages/rapidstart/`) carry each package's tables, fields and processing order. They also carry data:

- **Setup and master data packages (QCS-01 to QCS-06, QCS-10, QCS-14)** contain the **container's current records** (for example, all 364 G/L accounts as they are now, including the 176 blocked by QCS-14). This is *not* the data trial run 2 should load.
- **Journal packages (QCS-07, 08, 09, 11, 12, 13)** contain one empty record only (the field definitions).

So for **every** package, trial run 2 does four actions:

1. **Import Package** (`packages/rapidstart/…rapidstart`): creates the package definition
2. **Import from Excel** (the matching `packages/*_import.xlsx`, built by our scripts from extract v2): loads the reviewed data
3. **Check No. of Package Records** against the table below. If the number is higher, the Excel import added to the container's data instead of replacing it: delete the extra package records before applying
4. **Apply**

| Package | Import file | Expected package records |
|---|---|---|
| QCS-01-COA | QCS-01-COA_import.xlsx | G/L Account 364 |
| QCS-02-POSTING | QCS-02-POSTING_import.xlsx | Location 1; Customer Posting Group 3; Vendor Posting Group 3; Inventory Posting Group 2; Gen. Business Posting Group 4; Gen. Product Posting Group 10; General Posting Setup 27; Bank Account Posting Group 6; Inventory Posting Setup 2 |
| QCS-03-TAX-TERMS | QCS-03-TAX-TERMS_import.xlsx (rebuilt in step 0.4, no timestamp columns) | Payment Terms 13; Tax Area 6; Tax Area Line 12; Tax Jurisdiction 8; Tax Group 5; Tax Detail 9 |
| QCS-04-CUSTOMERS | QCS-04-CUSTOMERS_import.xlsx | Customer 40 |
| QCS-05-VENDORS | QCS-05-VENDORS_import.xlsx | Vendor 22 |
| QCS-06-ITEMS | QCS-06-ITEMS_import.xlsx | Item 61; Unit of Measure 21; Gen. Product Posting Group 11; General Posting Setup 28 |
| QCS-07-OPEN-AR | QCS-07-OPEN-AR_import.xlsx | Gen. Journal Line 37 |
| QCS-08-OPEN-AP | QCS-08-OPEN-AP_import.xlsx | Gen. Journal Line 27 |
| QCS-09-OPEN-STOCK | QCS-09-OPEN-STOCK_import.xlsx (corrected, I-018) | Item Journal Line 107 |
| QCS-10-BANK-ACCOUNTS | QCS-10-BANK-ACCOUNTS_import.xlsx | Bank Account 4 |
| QCS-11-OPEN-BANK | QCS-11-OPEN-BANK_import.xlsx | Gen. Journal Line 4 |
| QCS-12-OPEN-BANK-REC | QCS-12-OPEN-BANK-REC_import.xlsx | Bank Acc. Reconciliation 4; Bank Acc. Reconciliation Line 4 |
| QCS-13-OPEN-GL | QCS-13-OPEN-GL_import.xlsx | Gen. Journal Line 47 |
| QCS-14-BLOCK-ACCOUNTS | QCS-14-BLOCK-ACCOUNTS_import.xlsx | G/L Account 364 (176 blocked) |

Import each package **just before applying it**, never all at once: a package can only be imported after the records it refers to exist (I-012).

## Phase 0: Prepare in the Docker container (complete)

| Step | Action | Status |
|---|---|---|
| 0.1 | QCS-03: untick Last Modified Date Time on Payment Terms, Tax Group and Tax Area (I-001) | Done; verified in the re-exported package (no timestamp fields) |
| 0.2 | QCS-09: no package data to delete (0 package records) | Done |
| 0.3 | Export Package QCS-01 to QCS-14 into packages/rapidstart/ | Done; QCS-03 re-exported after 0.1 |
| 0.4 | Rebuild QCS-03-TAX-TERMS_import.xlsx from the new Excel template with tools/build_package_03_tax_terms.py | Done; same records as trial run 1, without timestamp columns. The build now clears records the package owns before adding them, so it gives the same result on any export (fresh template or post-run) |

## Phase 1: New company and setup

| Step | Action | Check |
|---|---|---|
| 1.1 | Create company "Queen City Supply Co.", Production – Setup data only, modules per D-002 | Record any differences from the 28.3 template (number of accounts, posting setup rows, payment terms) |
| 1.2 | Company information (address, phone, email; bank fields blank) | |
| 1.3 | Work Date 10/1/2026 | Dates in October can be entered online |
| 1.4 | QCS-01-COA, then Indent Chart of Accounts | 40330 category Income; 25900 exists; nothing blocked yet |
| 1.5 | QCS-02-POSTING | 9 active General Posting Setup rows; template rows blocked |
| 1.6 | QCS-03-TAX-TERMS | 37 inserted, 1 modified (I-001 fixed) |
| 1.7 | Inventory Setup: Location Mandatory, Prevent Negative Inventory; G/L Setup: Payment Tolerance Warning (D-013) | |
| 1.8 | QCS-04-CUSTOMERS, then No. Series CUST Last No. Used = C00400 | 40 customers |
| 1.9 | QCS-05-VENDORS, then No. Series VEND Last No. Used = V00220 | 22 vendors |
| 1.10 | QCS-06-ITEMS | 61 items; Item Units of Measure created |
| 1.11 | IRS Forms: period 2026, IRS Forms Guide, NEC-01 and MISC-01 minimum 2,000.00, Vendor Setup for V00010, V00060, V00100, V00190 (D-019, I-017) | |
| 1.12 | Reason Code MIGRATION; journal batches OB-AR, OB-AP, OB-BANK, OB-GL (GENERAL) and OB-STOCK (ITEM), opening-batch settings | |
| 1.13 | QCS-10-BANK-ACCOUNTS | 4 bank accounts |

## Phase 2: Opening balances

After posting each batch, delete the empty line BC leaves in it.

| Step | Action | Check |
|---|---|---|
| 2.1 | QCS-07-OPEN-AR, Preview Posting, post OB-AR | Aged AR at 9/30 = 169,777.55; 25900 = -169,777.55 |
| 2.2 | QCS-08-OPEN-AP, post OB-AP | Aged AP at 9/30 = 81,160.02; 25900 = -88,617.53 |
| 2.3 | QCS-09-OPEN-STOCK (corrected file), post OB-STOCK | 107 lines; Inventory Valuation = 164,831.46 exactly; 25900 = -253,448.99 |
| 2.4 | QCS-11-OPEN-BANK, post; QCS-12-OPEN-BANK-REC (or create the reconciliations by hand, since dates can be typed online), match, post | Opening entries closed; 25900 = -393,169.17 |
| 2.5 | QCS-13-OPEN-GL, post | **25900 = 0.00** |
| 2.6 | Final reconciliation: `tools/reconcile_trial_balance.py <export> trial-run-2` | 55 of 55 accounts match |

## Phase 3: Go-live configuration and tests

| Step | Action | Check |
|---|---|---|
| 3.1 | QCS-14-BLOCK-ACCOUNTS | 176 modified |
| 3.2 | G/L Setup: Allow Posting From 10/1/2026 (period lock) | A posting dated 9/30/2026 is refused |
| 3.3 | Day-one tests dated in October: 3 invoices (NC, SC, exempt), purchase order, sales order, payment applied to opening invoice 4410 | Same results as trial run 1 |
| 3.4 | 1099 check: enter Jan–Sep amounts as IRS 1099 adjustments (I-011); pay Andre Coleman's opening bill | BC's 2026 1099 amount for V00010 = Jan–Sep + Q4 payment |
| 3.5 | Check Tax Details for automatically created zero-rate rows (I-020) | Explained or prevented |
| 3.6 | After sign-off: block 25900 and the MIGRATION posting setup rows | |
