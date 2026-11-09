"""
Item units of measure, loaded explicitly (I-021).

BC 28.3 created an Item Unit of Measure record when Base Unit of Measure was validated; BC 29.0 does not
(through RapidStart). These two packages make the load independent of that side effect:
  QCS-06B-ITEM-UOM       table 5404: one record per item for its base unit, Qty. per Unit of Measure = 1
  QCS-06C-ITEM-S-P-UOM   table 27:   Sales and Purch. Unit of Measure = base unit (cases are never split, I-010)
Apply 06B before importing 06C (06C's values refer to 06B's records, I-012).
Source: mapping/item-xref.csv (Base UOM per item, from D-016).
Usage:
  python tools/transform_item_uom.py 06B <QCS-06B-ITEM-UOM_export-template.xlsx>
  python tools/transform_item_uom.py 06C <QCS-06C-ITEM-S-P-UOM_export-template.xlsx>
"""
import csv, sys
from pathlib import Path
from rapidstart_excel import read, write

ROOT = Path(__file__).resolve().parent.parent
uom = {r["BC No."]: r["Base UOM"] for r in csv.DictReader(open(ROOT / "mapping/item-xref.csv", encoding="utf-8"))}
part, template = sys.argv[1], sys.argv[2]
D = read(template); s = next(iter(D)); h = D[s]["hdr"]

if part == "06B":
    D[s]["rows"] = [[{"Item No.": no, "Code": u, "Qty. per Unit of Measure": "1"}[x] for x in h] for no, u in sorted(uom.items())]
    out = ROOT / "packages/QCS-06B-ITEM-UOM_import.xlsx"
elif part == "06C":
    exported = {r[h.index("No.")] for r in D[s]["rows"]}
    if exported != set(uom):   # the export lists the company's items: they must be exactly ours
        sys.exit(f"Stopped: items differ from the cross-reference: missing {sorted(set(uom) - exported)}, extra {sorted(exported - set(uom))}")
    D[s]["rows"] = [[{"No.": no, "Sales Unit of Measure": u, "Purch. Unit of Measure": u}[x] for x in h] for no, u in sorted(uom.items())]
    out = ROOT / "packages/QCS-06C-ITEM-S-P-UOM_import.xlsx"
else:
    sys.exit("first argument must be 06B or 06C")
write(template, out, D)
print(f"{out.name}: {len(D[s]['rows'])} records")
