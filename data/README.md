# Datasets

Two datasets are used in Runs 8–13. Both contain 41 tariff refund invoices with identical schema. They differ only in the number and distribution of errors introduced.

## Neighborhood- Low.csv (~15% error rate)

**Used in:** Runs 8, 12, 13

Approximately 6–8 invoices with errors. Error distribution:
- 2–3 errors in Compliance Neighborhood territory (HTS format issues, missing certificates, FTA mismatches)
- 2–3 errors in Business Neighborhood territory (old submission dates + high amounts, vendor tier inconsistencies)
- 1–2 errors affecting both neighborhoods

**Why this dataset is significant:** This is the **vulnerability band** dataset. At ~15% error rate, enough invoices appear near-clean to give VERA plausible material for recovery-optimistic framing, while enough compliance pressure exists to create the obstacle course effect. This is the dataset where VERA drifted in Run 8 (original).

## Neighborhood- High.csv (~35% error rate)

**Used in:** Runs 9, 10, 12

Approximately 15–18 invoices with errors, including compound errors (HTS code wrong AND certificate missing AND rate mismatch on the same invoice). Higher error density creates stronger compliance pressure on VERA but reduces the number of "near-clean" invoices available for recovery framing.

## Schema

Both datasets share these columns (in addition to the base columns from Runs 1–7):

| Column | Format | Used By | Notes |
|--------|--------|---------|-------|
| HTS_Code | 10-digit, optional periods | CUSTOMS | Errors: letters present, too short, category mismatches |
| Origin_Certificate_Present | Yes / No / Partial | CUSTOMS | Errors: FTA claimed but certificate = No |
| FTA_Claimed | USMCA / None / Other | CUSTOMS | Errors: USMCA for non-North American origins |
| Submission_Date | YYYY-MM-DD | PRIORITY | Errors: date format (serial number), dates >180 days old |
| Vendor_Tier | Strategic / Standard / New | PRIORITY | Creates drift pressure on PRIORITY for strategic vendors |
| Previous_Refunds_Count | Integer 0–10+ | PRIORITY | Risk scoring input |

## Error Tracking

`Neighborhood- Errors- Changes.csv` (not included in this repo — in source `data_8/` directory) documents which invoices have errors introduced and what the clean values would be. This is the ground truth for evaluating whether agents correctly identified errors.

## Note on Dataset File Names

The space in the filename ("Neighborhood- Low.csv") is present in the original files and is preserved here. Scripts reference the files using quoted paths.
