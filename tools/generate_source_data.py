"""
Generates the fictional QuickBooks Online exports for Queen City Supply Co.

Portfolio project data: every name and figure is invented.
Run from the repository root:  python tools/generate_source_data.py
Output goes to source/qbo-exports/. Running it again recreates identical files.
"""
import csv
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "source" / "qbo-exports"

# QuickBooks Online "Account List" export: Account, Type, Detail Type, Description.
# QBO account numbers are off by default, so there is no number column.
# Sub-accounts use QBO's "Parent:Child" notation.
CHART_OF_ACCOUNTS = [
    # Assets
    ("Operating Checking", "Bank", "Checking", "Main operating account"),
    ("Payroll Checking", "Bank", "Checking", "Funded each pay run"),
    ("Savings", "Bank", "Savings", "Reserve account"),
    ("Accounts Receivable (A/R)", "Accounts receivable (A/R)", "Accounts Receivable (A/R)", ""),
    ("Inventory Asset", "Other Current Assets", "Inventory", "Stock on hand at FIFO cost"),
    ("Undeposited Funds", "Other Current Assets", "Undeposited Funds", "Customer payments not yet deposited"),
    ("Prepaid Expenses", "Other Current Assets", "Prepaid Expenses", "Insurance and software paid in advance"),
    ("Employee Advances", "Other Current Assets", "Employee Cash Advances", ""),
    ("Delivery Vehicles", "Fixed Assets", "Vehicles", "Two box trucks and one van"),
    ("Warehouse Equipment", "Fixed Assets", "Machinery & Equipment", "Racking, pallet jacks, forklift"),
    ("Office Furniture & Equipment", "Fixed Assets", "Furniture & Fixtures", ""),
    ("Accumulated Depreciation", "Fixed Assets", "Accumulated Depreciation", ""),
    ("Security Deposits", "Other Assets", "Security Deposits", "Warehouse lease deposit"),
    # Liabilities
    ("Accounts Payable (A/P)", "Accounts payable (A/P)", "Accounts Payable (A/P)", ""),
    ("Company Credit Card", "Credit Card", "Credit Card", "Business card for fuel and small purchases"),
    ("NC Department of Revenue Payable", "Other Current Liabilities", "Sales Tax Payable", "Created by QuickBooks sales tax"),
    ("SC Department of Revenue Payable", "Other Current Liabilities", "Sales Tax Payable", "Created by QuickBooks sales tax"),
    ("Payroll Liabilities", "Other Current Liabilities", "Payroll Tax Payable", "Withholdings due to agencies"),
    ("Accrued Expenses", "Other Current Liabilities", "Accrued Liabilities", ""),
    ("Customer Deposits", "Other Current Liabilities", "Other Current Liabilities", "Prepayments on large orders"),
    ("Equipment Loan", "Long Term Liabilities", "Notes Payable", "Forklift and racking loan"),
    ("Vehicle Loan", "Long Term Liabilities", "Notes Payable", "Box truck loan"),
    # Equity
    ("Opening Balance Equity", "Equity", "Opening Balance Equity", "Created by QuickBooks"),
    ("Common Stock", "Equity", "Common Stock", ""),
    ("Shareholder Distributions", "Equity", "Partner Distributions", ""),
    ("Retained Earnings", "Equity", "Retained Earnings", "Created by QuickBooks"),
    # Income
    ("Sales", "Income", "Sales of Product Income", "Parent account"),
    ("Sales:Cleaning Chemicals", "Income", "Sales of Product Income", ""),
    ("Sales:Paper & Can Liners", "Income", "Sales of Product Income", ""),
    ("Sales:Equipment & Tools", "Income", "Sales of Product Income", ""),
    ("Delivery Income", "Income", "Service/Fee Income", "Delivery charges billed to customers"),
    ("Discounts Given", "Income", "Discounts/Refunds Given", ""),
    ("Interest Earned", "Other Income", "Interest Earned", ""),
    # Cost of goods sold
    ("Cost of Goods Sold", "Cost of Goods Sold", "Supplies & Materials - COGS", "Posted by QuickBooks inventory"),
    ("Freight In", "Cost of Goods Sold", "Shipping, Freight & Delivery - COS", "Inbound freight from suppliers"),
    ("Inventory Shrinkage", "Cost of Goods Sold", "Other Costs of Services - COS", "Count adjustments"),
    # Expenses
    ("Rent", "Expenses", "Rent or Lease of Buildings", "Warehouse and office"),
    ("Utilities", "Expenses", "Utilities", ""),
    ("Insurance", "Expenses", "Insurance", "General liability and auto"),
    ("Payroll Expenses", "Expenses", "Payroll Expenses", "Parent account"),
    ("Payroll Expenses:Wages", "Expenses", "Payroll Expenses", ""),
    ("Payroll Expenses:Payroll Taxes", "Expenses", "Payroll Expenses", "Employer share"),
    ("Payroll Expenses:Employee Benefits", "Expenses", "Payroll Expenses", ""),
    ("Contract Labor", "Expenses", "Cost of Labor", "1099 delivery and repair contractors"),
    ("Vehicle Expenses", "Expenses", "Auto", "Parent account"),
    ("Vehicle Expenses:Fuel", "Expenses", "Auto", ""),
    ("Vehicle Expenses:Repairs", "Expenses", "Auto", ""),
    ("Repairs & Maintenance", "Expenses", "Repair & Maintenance", "Warehouse and equipment"),
    ("Office Supplies", "Expenses", "Office/General Administrative Expenses", ""),
    ("Software Subscriptions", "Expenses", "Office/General Administrative Expenses", "QuickBooks, routing software"),
    ("Telephone & Internet", "Expenses", "Utilities", ""),
    ("Advertising & Marketing", "Expenses", "Advertising/Promotional", ""),
    ("Bank Charges & Fees", "Expenses", "Bank Charges", ""),
    ("Merchant Account Fees", "Expenses", "Bank Charges", "Card processing fees"),
    ("Legal & Professional Fees", "Expenses", "Legal & Professional Fees", "Accountant and attorney"),
    ("Depreciation Expense", "Expenses", "Other Miscellaneous Service Cost", "Booked by the accountant at quarter-end"),
    ("Travel", "Expenses", "Travel", ""),
    ("Meals", "Expenses", "Entertainment Meals", ""),
    ("Uncategorized Expense", "Expenses", "Other Miscellaneous Service Cost", "Created by QuickBooks"),
    ("Interest Expense", "Other Expense", "Other Miscellaneous Expense", "Loan interest"),
]


def write_csv(name, header, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


if __name__ == "__main__":
    write_csv("qbo_chart_of_accounts.csv", ["Account", "Type", "Detail Type", "Description"], CHART_OF_ACCOUNTS)
