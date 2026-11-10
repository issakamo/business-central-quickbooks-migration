# Cutover Checklist: Queen City Supply Co.

**Go-live:** Thursday, October 1, 2026 (balances as of Wednesday, September 30, 2026)
**Users start in Business Central:** Monday, October 5, 2026
**Procedure:** `docs/runbook.md`, rehearsed in two trial runs (`docs/reconciliation-trial-run-1.md`, `docs/reconciliation-trial-run-2.md`)

> Portfolio project: the client, people and dates are fictional. The checklist shows how the cutover of a QuickBooks-to-Business Central migration is planned.

## Roles

| Role | Responsibility |
|---|---|
| **Owner (client)** | Go/no-go decision |
| **Accountant (client)** | Closes Q3 in QuickBooks, delivers the final extract, reviews and signs the reconciliation |
| **Warehouse lead (client)** | Stock count at 9/30, receiving and shipping during the blackout |
| **Migration consultant** | Runs the runbook, the reconciliation and the day-one tests; keeps the issues log |

## Why the cutover takes a weekend

Go-live is a Thursday, but loading a company the accountant has not yet closed would mean loading balances that still change. So QuickBooks stops taking transactions on Wednesday evening, the accountant closes the quarter on Thursday and Friday, and the load runs over the weekend. During those two business days the company keeps trading on paper (the **blackout**), and everything is entered in Business Central on Monday with its real date. This works because the period lock allows posting from 10/1/2026 (runbook step 3.2).

## T-4 to T-1 weeks: prerequisites

| Done | When | Item | Owner |
|---|---|---|---|
| ☐ | T-4 weeks | Trial run 2 signed off; open issues reviewed (issues log) | Accountant, consultant |
| ☐ | T-4 weeks | Business Central licenses assigned to the 6 users; permission sets per role; User Setup has no posting date overrides | Consultant |
| ☐ | T-3 weeks | User training: sales orders and invoices, purchase orders and receipts, cash receipts and payments, item journals | Consultant |
| ☐ | T-3 weeks | Decide payment methods for vendor payments (open item from trial run 2) | Accountant |
| ☐ | T-2 weeks | Tax advisor confirms: sourcing rules, SC 2026 rates, taxability of delivery charges (D-011, D-015) | Accountant |
| ☐ | T-2 weeks | Accountant reviews the 1099 setup: MISC thresholds (D-019), W-9 status of the I-007 vendors | Accountant |
| ☐ | T-1 week | Blackout procedure agreed with sales, purchasing and the warehouse (hold log, numbered paper forms) | Owner |
| ☐ | T-1 week | Go/no-go criteria and rollback plan confirmed (below) | Owner, consultant |

## Wednesday 9/30: QuickBooks freeze

| Done | Time | Item | Owner |
|---|---|---|---|
| ☐ | 5:00 PM | Last QuickBooks transactions entered; users stop entering | Accountant |
| ☐ | 5:00 PM | Blackout starts: orders, receipts and payments go on the hold log with their real dates | All |
| ☐ | after close | Stock count of all items at MAIN | Warehouse lead |

## Thursday 10/1 – Friday 10/2: Q3 close in QuickBooks

| Done | Item | Why | Owner |
|---|---|---|---|
| ☐ | Bank and credit card accounts reconciled at 9/30; outstanding items listed | Opening bank reconciliation (D-021) | Accountant |
| ☐ | Undeposited Funds deposited, balance 0.00 | I-013 | Accountant |
| ☐ | Opening Balance Equity and Uncategorized Expense 0.00 | Not migrated; must be zero | Accountant |
| ☐ | Count adjustments posted; no item with negative quantity | I-015, D-013 | Accountant, warehouse lead |
| ☐ | Duplicate or unapplied bills and payments cleared | I-014 | Accountant |
| ☐ | Q3 depreciation and accruals booked | YTD P&L is loaded (D-005) | Accountant |
| ☐ | **Friday 3:00 PM:** QuickBooks closing date set to 9/30/2026 with a password | Nothing can change after the extract | Accountant |
| ☐ | **Friday 3:00 PM:** final extract: trial balance, A/R and A/P aging detail, inventory valuation, 1099 contractor summary (Jan 1 – Sep 30) | Source for the load | Accountant |
| ☐ | Friday evening: runbook Phase 0: compare extracts, rebuild all import files | Differences only from approved corrections | Consultant |

## Saturday 10/3: load (runbook Phases 1 and 2)

| Done | Item | Check |
|---|---|---|
| ☐ | Phase 1: company, setup, master data, IRS forms, batches, bank accounts (steps 1.1–1.16) | Every predicted count matches |
| ☐ | Phase 2: opening AR, AP, stock, bank, G/L (steps 2.1–2.5) | **25900 Opening Balance Clearing = 0.00** |
| ☐ | Step 2.6: final reconciliation; reconciliation report drafted | Every account matches |

## Sunday 10/4: sign-off and go/no-go

| Done | Time | Item | Owner |
|---|---|---|---|
| ☐ | 9:00 AM | Accountant reviews the reconciliation report and the subledger reports in BC | Accountant |
| ☐ | 11:00 AM | Phase 3: blocking, period lock, day-one tests (steps 3.1–3.3, 3.5) | Consultant |
| ☐ | 1:00 PM | Reconciliation report signed | Accountant, consultant |
| ☐ | 2:00 PM | **Go/no-go decision** | Owner |
| ☐ | after go | Step 3.6: block 25900 and the MIGRATION posting setup | Consultant |

### Go/no-go criteria (all must be met)

- 25900 Opening Balance Clearing = 0.00
- Every account in the reconciliation matches QuickBooks to the cent
- Aged AR, aged AP and inventory valuation at 9/30 equal the QuickBooks reports
- Day-one tests pass (sales, purchase, payment)
- Reconciliation report signed by the accountant

### Rollback plan (if no-go)

- QuickBooks is unchanged: the accountant removes the closing date and the company continues in QuickBooks
- Hold-log transactions are entered in QuickBooks
- The Business Central company is not used; the cause goes in the issues log, is fixed, and is proven in a new trial run
- A new cutover date is set at the next month-end; it needs a new extract that includes October's transactions

## Monday 10/5: users start

| Done | Item | Owner |
|---|---|---|
| ☐ | Users sign in; consultant on site for questions | Consultant |
| ☐ | Hold-log transactions from 10/1–10/2 entered with their real dates | Sales, purchasing |
| ☐ | First cash receipts applied to opening invoices (QuickBooks invoice numbers) | Accountant |

## Hypercare: October 5–30

| Done | Item | Owner |
|---|---|---|
| ☐ | Daily check that 25900 stays at 0.00 and no MIGRATION postings exist | Consultant |
| ☐ | IRS 1099 adjustments for Jan–Sep entered from the confirmed contractor summary (I-011) | Accountant |
| ☐ | Contractors' TINs entered from W-9s by an authorized client user (I-006) | Accountant |
| ☐ | First bank reconciliation in BC (statement 1) | Accountant |
| ☐ | First sales tax return prepared from BC (NC and SC) | Accountant |
| ☐ | Month-end close for October in BC; P&L shows Jan–Oct | Accountant |
| ☐ | QuickBooks subscription switched to read-only for history and audit | Owner |
