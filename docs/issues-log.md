# Issues Log: Queen City Supply Co. Migration

| ID | Date | Area | Issue | Impact | Resolution | Status |
|---|---|---|---|---|---|---|
| I-001 | 2026-11-01 | Package QCS-03 | Apply reported 16 records modified instead of the 1 expected. All 16 are pre-existing Payment Terms (11) and Tax Group (5) records; the package included their Last Modified Date Time field. | Data values unchanged (verified); only audit timestamps updated. | Exclude system and audit fields from all packages; untick Last Modified Date Time in QCS-03 before trial run 2. | Open |
