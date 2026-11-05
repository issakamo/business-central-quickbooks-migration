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


# ---------------------------------------------------------------------------
# Cutover snapshot: QuickBooks reports as of 9/30/2026 (first extract, "v1")
# ---------------------------------------------------------------------------
from datetime import date, timedelta

CUTOFF = date(2026, 9, 30)
TERMS_DAYS = {"Net 15": 15, "Net 30": 30, "Net 60": 60, "Due on receipt": 0, "2% 10 Net 30": 30}
R2 = random.Random(930)   # separate fixed seed for balances


def ar_rows():
    """A/R Aging Detail: open invoices and credits at the cutoff."""
    cust = {c[0]: c for c in CUSTOMERS}
    picks = [c[0] for c in CUSTOMERS if c[4] == "Active" and c[0] != "Dilworth Dental Group, PLLC"]
    R2.shuffle(picks)
    docs, num = [], 4401
    for name in sorted(picks[:30]) + ["Dilworth Dental Group, PLLC", "Carolina Office Partners", "Uptown Tower Management",
                                      "Steele Creek Distribution Center", "Gaston Valley Hospital Services"]:
        d = CUTOFF - timedelta(days=R2.randint(3, 115))
        docs.append([d, "Invoice", name, round(R2.uniform(320, 8900), 2)])
    docs.append([date(2026, 9, 12), "Invoice", "Dilworth Dental Group", 1186.40])      # posted to the duplicate name
    docs.append([date(2026, 9, 18), "Credit Memo", "Crown Point Restaurant Group", -420.00])
    rows = []
    for d, typ, name, amt in sorted(docs, key=lambda x: (x[0], x[2])):
        terms = cust[name][2]
        due = d + timedelta(days=TERMS_DAYS[terms])
        open_bal = amt
        if typ == "Invoice" and R2.random() < 0.12:
            open_bal = round(amt * 0.5, 2)                    # partially paid
        days = (CUTOFF - due).days
        bucket = "Current" if days <= 0 else ("1 - 30" if days <= 30 else ("31 - 60" if days <= 60 else ("61 - 90" if days <= 90 else "91 and over")))
        rows.append([d.isoformat(), typ, str(num), name, due.isoformat(), f"{amt:.2f}", f"{open_bal:.2f}", bucket])
        num += 1
    return rows


def ap_rows(version=1):
    """A/P Aging Detail: unpaid bills and vendor credits at the cutoff. Num = the vendor's invoice number."""
    vend = {v[0]: v for v in VENDORS}
    plan = [("Atlantic Paper Converters", 3), ("Blue Ridge Chemical Supply", 3), ("Carolina Can Liner Co.", 2),
            ("CleanTech Equipment Distributors", 2), ("GreenLeaf Eco Chemicals", 2), ("Industrial Mop & Broom Works", 1),
            ("Metro Fleet Fuel Services", 1), ("Piedmont Power Co.", 1), ("Precision Floor Machines", 1),
            ("ProSan Disinfectants Inc.", 2), ("Southern Tissue Mills", 2), ("Summit Safety Products", 1),
            ("TeleCarolina Communications", 1), ("Uptown Office Supply", 1), ("Wilkes & Partners CPA", 1),
            ("Andre Coleman", 1), ("Tomas Nguyen", 1)]
    rows = []
    for name, n in plan:
        prefix = "".join(w[0] for w in name.split()[:3]).upper()
        for k in range(n):
            d = CUTOFF - timedelta(days=R2.randint(2, 75))
            amt = round(R2.uniform(180, 7400) if vend[name][5] in ("Paper", "Chemicals", "Equipment") else R2.uniform(150, 1900), 2)
            due = d + timedelta(days=TERMS_DAYS[vend[name][3]])
            rows.append([d.isoformat(), "Bill", f"{prefix}-{R2.randint(10000, 99999)}", name, due.isoformat(), f"{amt:.2f}", f"{amt:.2f}"])
    dup = next(r for r in rows if r[3] == "Southern Tissue Mills")
    if version == 1:   # v2: duplicate voided by the accountant (I-014)
        rows.append([(date.fromisoformat(dup[0]) + timedelta(days=6)).isoformat(), "Bill", dup[2], dup[3], dup[4], dup[5], dup[6]])  # entered twice
    rows.append(["2026-09-22", "Vendor Credit", "BRCS-CR-118", "Blue Ridge Chemical Supply", "2026-09-22", "-315.60", "-315.60"])
    return sorted(rows, key=lambda r: (r[0], r[3]))


def inventory_rows(version=1):
    """Inventory Valuation Summary: quantity on hand and FIFO value per item."""
    rows = []
    for name, sku, typ, *_rest in item_rows():
        if typ != "Inventory":
            continue
        cost = float(_rest[5])          # Purchase Cost column
        qty = R2.randint(1, 6) if cost > 1000 else (R2.randint(4, 25) if cost > 150 else R2.randint(12, 140))
        if name.startswith("Ice Melt"):
            qty = -4 if version == 1 else 0            # v1: sold before received; v2: counted and adjusted to 0 (I-015)
        factor = R2.uniform(0.985, 1.015)                # FIFO layers: value is not exactly qty x list cost
        value = round(qty * cost * factor, 2)
        avg = f"{value / qty:.4f}" if qty else "0.0000"
        rows.append([name, sku, str(qty), f"{value:.2f}", avg])
    return rows


def trial_balance(ar, ap, inv, version=1):
    ar_total = round(sum(float(r[6]) for r in ar), 2)
    ap_total = round(sum(float(r[6]) for r in ap), 2)
    inv_total = round(sum(float(r[3]) for r in inv), 2)
    debit = {  # natural debit balances
        "Operating Checking": 84312.55, "Payroll Checking": 6000.00, "Savings": 50000.00,
        "Accounts Receivable (A/R)": ar_total, "Inventory Asset": inv_total, "Undeposited Funds": 1250.00,
        "Prepaid Expenses": 4800.00, "Employee Advances": 500.00, "Delivery Vehicles": 112000.00,
        "Warehouse Equipment": 64500.00, "Office Furniture & Equipment": 18200.00, "Security Deposits": 7500.00,
        "Shareholder Distributions": 60000.00, "Discounts Given": 21406.80,
        "Cost of Goods Sold": 2679388.42, "Freight In": 21530.00, "Inventory Shrinkage": 3104.65,
        "Rent": 72000.00, "Utilities": 14388.12, "Insurance": 16200.00, "Payroll Expenses:Wages": 662000.00,
        "Payroll Expenses:Payroll Taxes": 50643.00, "Payroll Expenses:Employee Benefits": 58200.00,
        "Contract Labor": 46000.00, "Vehicle Expenses:Fuel": 21806.43, "Vehicle Expenses:Repairs": 9400.00,
        "Repairs & Maintenance": 6310.00, "Office Supplies": 3912.66, "Software Subscriptions": 5400.00,
        "Telephone & Internet": 4104.00, "Advertising & Marketing": 6700.00, "Bank Charges & Fees": 1096.20,
        "Merchant Account Fees": 7814.33, "Legal & Professional Fees": 9500.00, "Depreciation Expense": 15450.00,
        "Travel": 2311.80, "Meals": 1904.55, "Interest Expense": 4612.70,
    }
    credit = {  # natural credit balances
        "Accumulated Depreciation": 61850.00, "Accounts Payable (A/P)": ap_total, "Company Credit Card": 1842.37,
        "NC Department of Revenue Payable": 6412.18, "SC Department of Revenue Payable": 1123.40,
        "Payroll Liabilities": 9876.00, "Accrued Expenses": 3200.00, "Customer Deposits": 2500.00,
        "Equipment Loan": 38400.00, "Vehicle Loan": 46900.00, "Common Stock": 50000.00,
        "Sales:Cleaning Chemicals": 1681240.10, "Sales:Paper & Can Liners": 1428917.75, "Sales:Equipment & Tools": 790384.60,
        "Delivery Income": 18425.00, "Interest Earned": 918.44,
    }
    if version == 2:   # accountant's corrections posted in QuickBooks before the final extract
        debit["Operating Checking"] += 1250.00; debit["Undeposited Funds"] -= 1250.00          # I-013 deposit
        debit["Freight In"] = round(debit["Freight In"] - 281.98, 2)                              # I-014 void duplicate (AP side via ap_rows)
        debit["Inventory Shrinkage"] = round(debit["Inventory Shrinkage"] - 73.43, 2)             # I-015 count adjustment (inventory side via inventory_rows)
    plug = 265349.95   # prior years' profit (Retained Earnings), fixed so both extracts share it
    credit["Retained Earnings"] = plug
    order = [a[0] for a in CHART_OF_ACCOUNTS]
    rows = []
    for acct in order:
        if acct in debit and debit[acct]:
            rows.append([acct, f"{debit[acct]:.2f}", ""])
        elif acct in credit and credit[acct]:
            rows.append([acct, "", f"{credit[acct]:.2f}"])
    td = round(sum(debit.values()), 2); tc = round(sum(credit.values()), 2)
    assert abs(td - tc) < 0.005 and plug > 0, (td, tc, plug)
    rows.append(["TOTAL", f"{td:.2f}", f"{tc:.2f}"])
    return rows


def contractor_1099_rows():
    """1099 Contractor Summary, Jan 1 - Sep 30, 2026 (payments by check/ACH; card payments excluded)."""
    return [["Andre Coleman", "Nonemployee compensation", "14200.00"],
            ["Danielle Ruiz", "Nonemployee compensation", "11850.00"],
            ["Marcus Bell Equipment Repair", "Nonemployee compensation", "9400.00"],
            ["Tomas Nguyen", "Nonemployee compensation", "10550.00"]]


if __name__ == "__main__":
    # extract v1 (first export) and v2 (after the accountant's corrections) share the same random draws
    for version, folder in ((1, OUT), (2, OUT / "extract-v2")):
        state = R2.getstate()
        ar, ap, inv = ar_rows(), ap_rows(version), inventory_rows(version)
        R2.setstate(state) if version == 1 else None
        files = {
            "qbo_ar_aging_detail_2026-09-30.csv": (["Date", "Transaction Type", "Num", "Customer", "Due Date", "Amount", "Open Balance", "Aging"], ar),
            "qbo_ap_aging_detail_2026-09-30.csv": (["Date", "Transaction Type", "Num", "Vendor", "Due Date", "Amount", "Open Balance"], ap),
            "qbo_inventory_valuation_2026-09-30.csv": (["Product/Service", "SKU", "Qty On Hand", "Asset Value", "Avg Cost"], inv),
            "qbo_trial_balance_2026-09-30.csv": (["Account", "Debit", "Credit"], trial_balance(ar, ap, inv, version)),
            "qbo_1099_contractor_summary_2026-01-01_2026-09-30.csv": (["Vendor", "Box", "Total"], contractor_1099_rows()),
        }
        for name, (header, rows) in files.items():
            folder.mkdir(parents=True, exist_ok=True)
            with open(folder / name, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f); w.writerow(header); w.writerows(rows)
            print(f"v{version} {name}: {len(rows)} rows")
