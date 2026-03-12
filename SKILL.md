---
name: schedule-e-rental-income
description: Use this skill to extract rental-property figures from IRS Schedule E forms and produce a filled rental income Excel worksheet using the bundled template while preserving existing formulas.
---

# Schedule E Rental Income

Use this skill when the user wants a completed rental income worksheet, not just extracted numbers.

Your default goal is to produce and return a filled Excel file.

If the skill package includes `template.xlsx`, treat it as the default worksheet template automatically. Do not ask the user to upload a separate worksheet unless:
- `template.xlsx` is missing
- the user explicitly wants a different worksheet
- the bundled template cannot be used

When this skill is active, follow these steps in order:

1. Read the Schedule E document and identify each rental property in source order.
2. Extract the required values for each property.
3. Convert fair rental days into months in service:
   - `365` -> `12`
   - `366` -> `12`
   - any other numeric value -> `fair_rental_days / 30`
4. Build the worksheet JSON payload for all properties.
5. If required values are missing, unclear, contradictory, or confidence is low, ask the user for review before writing.
6. Otherwise, immediately use `scripts/write_excel.py` with `template.xlsx` to generate the completed workbook.
7. Return the completed Excel file to the user as the final output.

Read `extraction_prompt.md` before extracting data.
Read `reference.md` before writing values into the worksheet.

## Default Execution Rule

Do not stop after producing JSON if the extracted data is sufficient to fill the worksheet.

If all required values are available and there is no material ambiguity, continue automatically to workbook generation and return the filled Excel file.

JSON is an intermediate artifact, not the final deliverable, unless the user explicitly asks for JSON only.

## Required Data

For each property, extract:

- property address
- fair rental days
- months in service
- rents received
- total expenses
- insurance
- mortgage interest
- taxes
- depreciation
- HOA dues, only if explicitly identified
- extraordinary expense, only if explicitly supported

If multiple properties are present, preserve A/B/C order from Schedule E and fill worksheet rental-unit columns from left to right in that same order.

## Template Rule

Assume `template.xlsx` inside the skill package is the default workbook to use.

Do not ask the user for a worksheet/template if `template.xlsx` is available and the user did not request a different workbook.

## Output Rule

The normal output of this skill is:
1. a filled Excel workbook based on `template.xlsx`
2. returned to the user as a downloadable file

Do not treat a filesystem path alone as the final user-facing result when the environment supports returning the actual file.

## Guidelines

- Preserve worksheet formulas, formatting, labels, and existing structure.
- Write only to user-input cells defined in `reference.md`.
- Do not infer HOA dues from generic "other" expenses.
- Do not infer extraordinary expense without explicit support.
- Use `null` for unsupported or unreadable fields instead of guessing.
- If the number of properties exceeds the available worksheet columns, stop and report the issue.
- If the workbook is successfully generated, return it immediately to the user.
- Only ask a follow-up question when ambiguity prevents a reliable worksheet output.
- Do not ask whether to proceed to Excel generation if the extracted values are already sufficient.

## Examples

- User uploads a Schedule E PDF and wants the worksheet completed.
- User provides a scanned Schedule E and expects a finished Excel file as output.
- User provides a multi-property Schedule E and wants each property filled into separate rental-unit columns.
- User asks for JSON only; in that case, return JSON and do not generate Excel unless requested.