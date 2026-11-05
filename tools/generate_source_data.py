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


# ---------------------------------------------------------------------------
# Master data: QuickBooks Online list exports
# ---------------------------------------------------------------------------
import random

RNG = random.Random(2026)  # fixed seed: same output every run

# (city, state, ZIP) -> used for billing and shipping addresses
CITIES = {
    "Charlotte": ("NC", "28203"), "Matthews": ("NC", "28105"), "Huntersville": ("NC", "28078"),
    "Concord": ("NC", "28025"), "Kannapolis": ("NC", "28081"),
    "Gastonia": ("NC", "28052"), "Belmont": ("NC", "28012"),
    "Monroe": ("NC", "28110"), "Indian Trail": ("NC", "28079"),
    "Rock Hill": ("SC", "29730"), "Fort Mill": ("SC", "29715"),
    "Lancaster": ("SC", "29720"), "Indian Land": ("SC", "29707"),
}

CUSTOMERS = [
    # display name, city, terms, tax exempt (resale certificate), status
    ("Ballantyne Office Park Association", "Charlotte", "Net 30", "", "Active"),
    ("Belmont Abbey Facilities", "Belmont", "Net 30", "", "Active"),
    ("Brightside Learning Academy", "Matthews", "Net 30", "", "Active"),
    ("Cabarrus Family Medicine", "Concord", "Net 30", "", "Active"),
    ("Carolina Office Partners", "Charlotte", "2% 10 Net 30", "", "Active"),
    ("Catawba Ridge Apartments", "Rock Hill", "Net 30", "", "Active"),
    ("CleanPro Janitorial Services", "Charlotte", "Net 15", "Resale", "Active"),
    ("Concord Mills Dental", "Concord", "Net 30", "", "Active"),
    ("Crown Point Restaurant Group", "Charlotte", "Net 15", "", "Active"),
    ("Dilworth Dental Group", "Charlotte", "Net 30", "", "Active"),
    ("Dilworth Dental Group, PLLC", "Charlotte", "Net 30", "", "Active"),   # duplicate of the line above
    ("Eastover Property Management", "Charlotte", "2% 10 Net 30", "", "Active"),
    ("Fort Mill Fitness Center", "Fort Mill", "Due on receipt", "", "Active"),
    ("Freedom Drive Auto Spa", "Charlotte", "Due on receipt", "", "Active"),
    ("Gaston Valley Hospital Services", "Gastonia", "Net 30", "", "Active"),
    ("Gastonia Grill & Taproom", "Gastonia", "Net 15", "", "Active"),
    ("Harrisburg Hardware Co.", "Concord", "Net 30", "", "Inactive"),       # no activity since 2024
    ("Huntersville Ice Arena", "Huntersville", "Net 30", "", "Active"),
    ("Indian Land Medical Plaza", "Indian Land", "Net 30", "", "Active"),
    ("Indian Trail Elementary PTA", "Indian Trail", "Due on receipt", "", "Active"),
    ("Kannapolis Logistics Hub", "Kannapolis", "Net 30", "", "Active"),
    ("Lake Norman Event Center", "Huntersville", "Net 15", "", "Active"),
    ("Lancaster Senior Living", "Lancaster", "Net 30", "", "Active"),
    ("Matthews Medical Arts Building", "Matthews", "Net 30", "", "Active"),
    ("Midtown Coworking Suites", "Charlotte", "2% 10 Net 30", "", "Active"),
    ("Monroe Manufacturing Supply", "Monroe", "Net 30", "Resale", "Active"),
    ("NoDa Brewing Collective", "Charlotte", "Net 15", "", "Active"),
    ("Piedmont Pediatrics", "Charlotte", "Net 30", "", "Active"),
    ("Plaza Midwood Bakery", "Charlotte", "Due on receipt", "", "Active"),
    ("Queens Road Animal Hospital", "Charlotte", "Net 30", "", "Active"),
    ("Riverwalk Hotel Rock Hill", "Rock Hill", "Net 30", "", "Active"),
    ("Sharon Square Shopping Center", "Charlotte", "2% 10 Net 30", "", "Active"),
    ("SouthPark Law Offices", "Charlotte", "Net 30", "", "Active"),
    ("Sparkle Commercial Cleaning", "Rock Hill", "Net 15", "Resale", "Active"),
    ("Steele Creek Distribution Center", "Charlotte", "Net 30", "", "Active"),
    ("Union County Racquet Club", "Monroe", "Net 30", "", "Active"),
    ("University City Labs", "Charlotte", "Net 30", "", "Active"),
    ("Uptown Tower Management", "Charlotte", "2% 10 Net 30", "", "Active"),
    ("Waxhaw Veterinary Clinic", "Wingate", "Net 30", "", "Active"),          # city not in the tax-area list
    ("Wesley Heights Daycare", "Charlotte", "Due on receipt", "", "Active"),
    ("York Technical Training Center", "Rock Hill", "Net 30", "", "Active"),
    ("Zeta Data Center Services", "Charlotte", "Net 30", "", "Active"),
]

STREETS = ["Commerce Dr", "Trade St", "Tryon St", "Park Rd", "Main St", "Industrial Blvd",
           "Market St", "Church St", "Providence Rd", "Center Pkwy", "Gateway Blvd", "Lakeview Dr"]


def email_for(name):
    slug = "".join(ch for ch in name.lower() if ch.isalnum())[:18]
    return f"ap@{slug}.example"


def customer_rows():
    rows = []
    for i, (name, city, terms, exempt, status) in enumerate(CUSTOMERS):
        state, zipc = CITIES.get(city, ("NC", "28173"))
        street = f"{100 + 37 * i} {STREETS[i % len(STREETS)]}"
        if name == "Matthews Medical Arts Building":
            zipc = ""                                   # missing ZIP code in QuickBooks
        phone = f"(704) 555-{1000 + i * 7:04d}" if state == "NC" else f"(803) 555-{1000 + i * 7:04d}"
        cert = f"QCS-EX-{i + 1:03d}" if exempt else ""
        rows.append([name, name, phone, email_for(name), street, city, state, zipc,
                     street, city, state, zipc, terms, "Yes" if exempt else "No", exempt, cert, status])
    return rows


VENDORS = [
    # name, city, state, terms, 1099, category
    ("Atlantic Paper Converters", "Greensboro", "NC", "Net 30", "No", "Paper"),
    ("Blue Ridge Chemical Supply", "Hickory", "NC", "Net 30", "No", "Chemicals"),
    ("Carolina Can Liner Co.", "Charlotte", "NC", "Net 30", "No", "Paper"),
    ("CleanTech Equipment Distributors", "Atlanta", "GA", "Net 60", "No", "Equipment"),
    ("Freight Way Properties LLC", "Charlotte", "NC", "Due on receipt", "No", "Rent"),
    ("GreenLeaf Eco Chemicals", "Raleigh", "NC", "2% 10 Net 30", "No", "Chemicals"),
    ("Industrial Mop & Broom Works", "Spartanburg", "SC", "Net 30", "No", "Equipment"),
    ("Metro Fleet Fuel Services", "Charlotte", "NC", "Net 15", "No", "Fuel"),
    ("Piedmont Power Co.", "Charlotte", "NC", "Due on receipt", "No", "Utilities"),
    ("Precision Floor Machines", "Columbia", "SC", "Net 60", "No", "Equipment"),
    ("ProSan Disinfectants Inc.", "Charlotte", "NC", "Net 30", "No", "Chemicals"),
    ("Queen City Mutual Insurance", "Charlotte", "NC", "Due on receipt", "No", "Insurance"),
    ("Southern Tissue Mills", "Rock Hill", "SC", "Net 30", "No", "Paper"),
    ("Summit Safety Products", "Charlotte", "NC", "Net 30", "No", "Equipment"),
    ("TeleCarolina Communications", "Charlotte", "NC", "Due on receipt", "No", "Telephone"),
    ("Triad Truck & Van Repair", "Gastonia", "NC", "Net 15", "No", "Vehicle repairs"),
    ("Uptown Office Supply", "Charlotte", "NC", "Net 30", "No", "Office supplies"),
    ("Wilkes & Partners CPA", "Charlotte", "NC", "Net 15", "No", "Accounting"),
    # independent contractors (Form 1099-NEC)
    ("Andre Coleman", "Charlotte", "NC", "Net 15", "Yes", "Delivery contractor"),
    ("Danielle Ruiz", "Concord", "NC", "Net 15", "Yes", "Delivery contractor"),
    ("Marcus Bell Equipment Repair", "Matthews", "NC", "Net 15", "Yes", "Repair contractor"),
    ("Tomas Nguyen", "Fort Mill", "SC", "Net 15", "Yes", "Delivery contractor"),
]


def vendor_rows():
    rows = []
    for i, (name, city, state, terms, t1099, cat) in enumerate(VENDORS):
        street = f"{200 + 53 * i} {STREETS[(i + 3) % len(STREETS)]}"
        zipc = {"NC": f"28{200 + i:03d}", "SC": f"29{300 + i:03d}", "GA": f"30{300 + i:03d}"}[state]
        area = {"NC": "704", "SC": "803", "GA": "404"}[state]
        tax_id = f"XX-XXX{1000 + i:04d}" if t1099 == "Yes" else ""   # masked, as QuickBooks shows it
        rows.append([name, name, f"({area}) 555-{2000 + i * 11:04d}", email_for(name), street, city, state, zipc,
                     terms, t1099, tax_id, cat])
    return rows


ITEMS_SPEC = [
    # (prefix, category, income account, preferred vendor, [(name, cost)])
    ("CH", "Cleaning Chemicals", "Sales:Cleaning Chemicals", ["Blue Ridge Chemical Supply", "GreenLeaf Eco Chemicals", "ProSan Disinfectants Inc."], [
        ("All-Purpose Cleaner, 1 gal (case of 4)", 28.40), ("Glass Cleaner, 1 gal (case of 4)", 24.10),
        ("Neutral Floor Cleaner, 1 gal (case of 4)", 31.75), ("Heavy-Duty Degreaser, 1 gal (case of 4)", 38.20),
        ("Disinfectant Cleaner, 1 gal (case of 4)", 42.60), ("Bathroom Cleaner, 32 oz (case of 12)", 33.90),
        ("Toilet Bowl Cleaner, 32 oz (case of 12)", 29.50), ("Floor Finish, 5 gal pail", 89.00),
        ("Floor Stripper, 5 gal pail", 76.50), ("Carpet Extraction Cleaner, 1 gal (case of 4)", 44.80),
        ("Hand Soap, foaming, 1000 ml (case of 6)", 37.25), ("Hand Sanitizer, 1000 ml (case of 6)", 41.00),
        ("Stainless Steel Polish, 17 oz (case of 12)", 46.30), ("Odor Eliminator, 1 gal (case of 4)", 35.60),
        ("Laundry Detergent, 5 gal pail", 64.00), ("Dish Detergent, 1 gal (case of 4)", 27.90),
        ("Oven & Grill Cleaner, 1 gal (case of 4)", 39.40), ("Quat Sanitizer, 1 gal (case of 4)", 36.70),
        ("Eco All-Purpose Concentrate, 2 L (case of 4)", 52.00), ("Graffiti Remover, 1 gal (case of 4)", 58.30),
        ("Ice Melt, 50 lb bag", 18.60), ("Drain Maintenance Enzyme, 1 gal (case of 4)", 47.50),
    ]),
    ("PP", "Paper & Can Liners", "Sales:Paper & Can Liners", ["Atlantic Paper Converters", "Southern Tissue Mills", "Carolina Can Liner Co."], [
        ("Toilet Tissue, 2-ply (case of 96)", 48.90), ("Jumbo Roll Tissue, 9 in (case of 12)", 39.60),
        ("Multifold Towels, white (case of 4000)", 32.80), ("C-Fold Towels, white (case of 2400)", 30.40),
        ("Hardwound Roll Towels, 800 ft (case of 6)", 41.20), ("Center-Pull Towels (case of 6)", 37.90),
        ("Facial Tissue, flat box (case of 30)", 34.50), ("Toilet Seat Covers (case of 5000)", 29.70),
        ("Kitchen Roll Towels (case of 30)", 36.10), ("Dispenser Napkins (case of 6000)", 33.40),
        ("Can Liners, 33 gal, clear (case of 250)", 27.60), ("Can Liners, 45 gal, black (case of 250)", 31.90),
        ("Can Liners, 56 gal, black (case of 200)", 34.80), ("Can Liners, 10 gal, clear (case of 1000)", 25.30),
        ("Contractor Bags, 42 gal (case of 50)", 28.20), ("Recycling Liners, 45 gal, blue (case of 250)", 33.70),
        ("Compostable Liners, 13 gal (case of 200)", 39.90), ("Sanitary Napkin Disposal Bags (case of 500)", 22.40),
        ("Paper Hand Towel Rolls, kraft (case of 6)", 35.50), ("Wiping Rags, white, 25 lb box", 44.00),
    ]),
    ("EQ", "Equipment & Tools", "Sales:Equipment & Tools", ["CleanTech Equipment Distributors", "Industrial Mop & Broom Works", "Precision Floor Machines", "Summit Safety Products"], [
        ("Wet Mop Head, 24 oz", 6.80), ("Microfiber Flat Mop Kit", 42.50), ("Mop Bucket & Wringer, 35 qt", 68.00),
        ("Push Broom, 24 in", 21.40), ("Upright Lobby Dust Pan", 14.90), ("Microfiber Cloths (pack of 24)", 18.70),
        ("Squeegee, window, 14 in", 9.60), ("Extension Pole, 8 ft", 24.30), ("Toilet Bowl Brush & Caddy", 7.20),
        ("Janitor Cart with Bag", 189.00), ("Wet Floor Sign", 11.80), ("Backpack Vacuum, 10 qt", 329.00),
        ("Upright Vacuum, 14 in", 249.00), ("Auto Scrubber, 20 in", 3150.00), ("Floor Burnisher, 20 in", 1475.00),
        ("Paper Towel Dispenser, roll", 38.50), ("Soap Dispenser, foam", 24.90), ("Nitrile Gloves, L (case of 1000)", 64.50),
    ]),
]


def item_rows():
    rows = []
    for prefix, cat, income, vendors, items in ITEMS_SPEC:
        start = {"CH": 1001, "PP": 2001, "EQ": 3001}[prefix]
        for j, (name, cost) in enumerate(items):
            sku = f"{prefix}-{start + j}"
            price = round(cost * RNG.uniform(1.28, 1.42), 2)
            inc = income
            if sku == "PP-2006":
                inc = "Sales:Cleaning Chemicals"          # miscoded income account in QuickBooks
            if name == "Wet Floor Sign":
                sku = ""                                  # missing SKU in QuickBooks
            rows.append([name, sku, "Inventory", cat, name, f"{price:.2f}", inc, name, f"{cost:.2f}",
                         "Cost of Goods Sold", "Inventory Asset", vendors[j % len(vendors)], "Yes"])
    # service item used on invoices
    rows.append(["Delivery Charge", "", "Service", "Services", "Delivery charge", "25.00", "Delivery Income",
                 "", "", "", "", "", "Yes"])
    return rows


if __name__ == "__main__":
    write_csv("qbo_customers.csv",
              ["Customer", "Company", "Phone", "Email", "Billing Street", "Billing City", "Billing State", "Billing ZIP",
               "Shipping Street", "Shipping City", "Shipping State", "Shipping ZIP", "Terms", "Tax Exempt",
               "Exemption Reason", "Exemption Certificate No.", "Status"], customer_rows())
    write_csv("qbo_vendors.csv",
              ["Vendor", "Company", "Phone", "Email", "Street", "City", "State", "ZIP", "Terms",
               "Track Payments for 1099", "Tax ID", "Category"], vendor_rows())
    write_csv("qbo_products_services.csv",
              ["Product/Service Name", "SKU", "Type", "Category", "Sales Description", "Sales Price/Rate",
               "Income Account", "Purchase Description", "Purchase Cost", "Expense Account",
               "Inventory Asset Account", "Preferred Vendor", "Taxable"], item_rows())
