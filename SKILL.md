---
name: schedule-e-rental-income
description: Use this skill when the user wants to extract rental-property figures from IRS Schedule E and fill a rental income Excel worksheet while preserving the worksheet's existing formulas.
---
# Schedule E Rental Income

Use this skill to move data from Schedule E into a rental income worksheet.

When this skill is active, follow this workflow:

1. Read the Schedule E tax document and identify each rental property in order.

2. Extract the property address, fair rental days, rents received, total expenses, insurance, mortgage interest, taxes, depreciation, and any explicitly identified HOA dues or one-time extraordinary expense.

3. Convert fair rental days into months in service using these rules:
   - `365` -> `12`
   - `366` -> `12`
   - any other value -> `fair_rental_days / 30`

4. Build a structured JSON payload for all properties in worksheet order.

5. Show the extracted values to the user for confirmation if accuracy is important or any value is uncertain.

6. After confirmation, use `scripts/write_excel.py` to write values into the Excel template without overwriting formulas in calculated cells.

Read `extraction_prompt.txt` before asking a model to extract data.
Read `reference.md` before writing to Excel so the field mapping and edge-case rules are applied correctly.

## Data To Extract

For each Schedule E property, extract:

- property address
- fair rental days
- months in service
- rents received
- total expenses
- insurance
- mortgage interest paid to banks or others
- taxes
- depreciation expense or depletion
- HOA dues, only if explicitly identifiable
- one-time extraordinary expense, only if explicitly supported by the form or accompanying evidence

If multiple properties are present, keep the A, B, C order from Schedule E and fill worksheet rental-unit columns left to right in the same order.

## Output Shape

Create a JSON object with a `properties` array. Each property should contain the extracted source values plus the derived `months_in_service` value.

If a field is missing or not clearly supported by the document, set it to `null` instead of guessing.

## Guidelines

- Preserve property order across extraction and worksheet fill.
- Do not infer HOA dues from generic "other" expenses unless the document clearly identifies them.
- Do not infer extraordinary expense unless there is explicit evidence.
- Treat worksheet formulas as read-only; only write into user-input cells.
- If confidence is low, ask for review before writing the workbook.

## Examples

- User uploads a Schedule E PDF and a rental income worksheet and asks to populate the worksheet.
- User asks to extract Schedule E rental-property numbers into JSON first, then write them into Excel.
- User provides a multi-property Schedule E and wants each property mapped to a separate rental-unit column.
