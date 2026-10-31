# Client Brief: Queen City Supply Co.

> Fictional client, created for a Business Central portfolio project. Names, figures, and data are invented.

## The business

| | |
|---|---|
| **Company** | Queen City Supply Co. |
| **Location** | Charlotte, North Carolina (one warehouse and office) |
| **What it does** | Distributes janitorial, cleaning, and facility supplies to businesses: offices, schools, restaurants, property managers |
| **Customers** | About 40 active business customers in North Carolina and South Carolina |
| **Vendors** | About 20 suppliers, plus independent contractors (delivery and equipment repair) who receive Form 1099-NEC |
| **Items** | About 60 stocked items, valued at FIFO cost |
| **Size** | About 25 employees; 6 people will use Business Central |
| **Fiscal year** | Calendar year |

## Why they are moving

- QuickBooks Online no longer fits: no proper warehouse handling, weak inventory costing visibility, and sales tax reporting is done partly in spreadsheets.
- They want one system for finance, inventory, purchasing and sales, with room to grow into a second location.

## Current system

- **QuickBooks Online Plus.** Data is exported as standard QuickBooks reports and lists (CSV/Excel): Chart of Accounts, Customer and Vendor contact lists, Product/Service list, Open Invoices (A/R Aging Detail), Unpaid Bills (A/P Aging Detail), Inventory Valuation Summary, and Trial Balance.

## Go-live

- **Go-live date:** October 1, 2026 (start of Q4).
- **Cutover balances:** as of September 30, 2026, after the Q3 close in QuickBooks.
- **Why a quarter-end:** the client did not want to wait until year-end, and a closed, reconciled quarter gives a clean starting point. Q4 transactions are entered directly in Business Central.

## In scope

1. **Setup:** chart of accounts, posting groups, payment terms, sales tax (North Carolina and South Carolina jurisdictions), 1099 vendor setup, number series.
2. **Master data:** customers, vendors, items.
3. **Open balances at 9/30/2026:**
   - Open customer invoices and credits (AR)
   - Unpaid vendor bills and credits (AP)
   - Inventory on hand, by item, quantity and cost
   - G/L opening trial balance for all other accounts
4. **Reconciliation:** Business Central totals must match the QuickBooks source totals for the trial balance, AR aging, AP aging, and inventory valuation, before sign-off.

## Out of scope

| Item | Reason |
|---|---|
| Transaction history before 10/1/2026 | Stays available in QuickBooks (read-only subscription) for lookups and audit. Migrating history adds cost and risk for little benefit. |
| Payroll | Remains with the external payroll provider; payroll totals post to Business Central through a journal. |
| Fixed asset register | Fixed assets come across as G/L balances only; a fixed asset module can be a later phase. |
| Bank reconciliation history | The first Business Central bank reconciliation starts from the 9/30/2026 statement balance. |

## Success criteria

- Every source total reconciles to Business Central to the cent, with differences explained in the issues log.
- Users can create a sales order, purchase order, and invoice on day one without manual workarounds.
- Sales tax on a test invoice to a North Carolina and a South Carolina customer matches the expected rate.
