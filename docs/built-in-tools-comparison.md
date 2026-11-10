# Built-in QuickBooks Migration vs This Project's Approach

Business Central includes a **QuickBooks Online Data Migration** extension (and a QuickBooks Desktop one), run from **Assisted Setup → Migrate business data**. This document compares it with the scripted, reconciled approach used in this project, for this client.

> **Basis and limits of this comparison.** The built-in tool's behavior is taken from Microsoft's documentation ("The QuickBooks Online Data Migration Extension", learn.microsoft.com, page dated 2021). The tool was **not run** in this project: it connects to a live QuickBooks Online company, and the client data here is a generated extract. A newer version of the tool may behave differently. The extension is confirmed available in BC 29.0 (Assisted Setup → Migrate business data offers QuickBooks Online as a source); its behavior was not tested.

## What the built-in tool does

- Imports customers, vendors, items, the chart of accounts and a beginning balance transaction in the general ledger
- Imports open customer and vendor documents (invoices, credit memos, payments)
- Creates them **unposted**, so they can be reviewed and adjusted before posting

## Documented limitations, against this client's data

| Built-in tool (documented) | This client | This project |
|---|---|---|
| Migrates **full** amounts on open documents; partially paid amounts must be corrected manually | Open AR includes partially paid invoices (e.g. #4437, half paid) | Loads each document's **open balance**; the description keeps the original amount (D-017) |
| Requires **account numbers** in QuickBooks Online | The QuickBooks chart has no account numbers (QuickBooks Online default) | Account mapping assigns BC numbers without changing the source (D-003, `mapping/account-mapping.csv`) |
| Markup and discount amounts must be added manually | 2% 10 Net 30 terms; discount account | Discount terms and accounts mapped; discount windows checked at load (D-012, D-018) |
| Beginning balances may need correcting (QuickBooks Online does not store current balances for all accounts) | — | Every account reconciled to the QuickBooks trial balance by script (`tools/reconcile_trial_balance.py`) |
| Purchase and sales orders not migrated | — | Same scope |
| Tax accounts must be set up for tax jurisdictions before posting | NC and SC, six counties, Mecklenburg rate change on 7/1/2026 | Jurisdictions, areas and dated rates loaded and tested on invoices (D-011) |

## What the built-in tool does not address (not covered by its documentation)

These are not claims that the tool fails at them, only that its documentation does not describe them, so they would need to be checked or done separately:

- **Data profiling and cleanup:** duplicate customer (I-002), missing and inconsistent addresses for tax (I-004, I-005), missing SKU (I-008), miscoded income account (I-009), undeposited funds, a duplicate bill, negative stock (I-013 to I-015)
- **Client-specific design:** posting groups per income account (D-007), the MIGRATION posting group that keeps opening stock out of the P&L (D-006), units of measure (D-016), delivery as a service item (D-015)
- **Subledgers beyond AR/AP:** opening stock at FIFO value (I-018), bank balances with an opening reconciliation (D-021)
- **US-specific year-end reporting:** 1099 tracking across a mid-year cutover (I-011, I-017)
- **Repeatability and evidence:** the same load rerun in a second trial run on a newer BC version, with predicted counts and a signed reconciliation

## When each approach fits

| Situation | Better fit |
|---|---|
| Small company, clean QuickBooks data, account numbers already in use, few partially paid documents, no inventory valuation concerns | **Built-in tool**: fast, no scripting, and its unposted documents can be reviewed before posting |
| Data needs cleaning or merging; mid-year cutover; inventory; multi-jurisdiction sales tax; an accountant who needs reconciliation evidence; more than one trial run | **Scripted, reconciled approach** (this project) |
| In between | **Combination**: use the built-in tool for master data, then load and reconcile balances with packages, keeping the reconciliation either way |

## The point that applies either way

The tool moves data; it does not prove the result. Whichever approach is used, the migration is finished when every balance in Business Central has been **reconciled to the source**, differences are **explained**, and the client's accountant has **signed** the result.
