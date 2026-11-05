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

