---
name: schedule-e-rental-income
description: Use this skill when the user wants to extract rental-property figures from IRS Schedule E and fill a rental income Excel worksheet while preserving the worksheet's existing formulas.
---

# Schedule E Rental Income

Use this skill to move data from Schedule E into a rental income worksheet and return the completed Excel file to the user in chat.

When this skill is active, follow this workflow:

1. Read the Schedule E tax document and identify each rental property in order.

2. Extract the property address, fair rental days, rents received, total expenses, insurance, mortgage interest, taxes, depreciation, and any explicitly identified HOA dues or one-time extraordinary expense.

3. Convert fair rental days into months in service using these rules:
   - `365` -> `12`
   - `366` -> `12`
   - any other value -> `fair_rental_days / 30`

4. Build a structured JSON payload for all properties in worksheet order.

5. If any required value is uncertain, missing, contradictory, or low-confidence, ask the user for confirmation before writing the workbook.

6. Otherwise, use `scripts/write_excel.py` to write values into `template.xlsx` without overwriting formulas in calculated cells.

7. After the workbook is generated, attach the generated `.xlsx` file directly in the chat response and present that file as the final deliverable.

8. Do not stop after printing JSON or after reporting an output path. The task is not complete until the completed Excel file has been returned to the user in chat, unless file attachment is impossible in the current environment.

Read `extraction_prompt.md` before asking a model to extract data.
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

JSON is an intermediate artifact. The normal final output is the completed Excel file.

## Output Requirements

The default final deliverable for this skill is:
- a completed `.xlsx` file
- attached in the assistant's chat response to the user

A filesystem path such as `out/property_1_filled.xlsx` is not sufficient by itself when the environment supports sending files in chat.

If the workbook is successfully created and chat file attachment is available, attach the file immediately without waiting for an additional user message.

Only return a path instead of a file if:
- the environment cannot attach files in chat
- file generation failed
- the user explicitly asked for the path only

## Guidelines

- Preserve property order across extraction and worksheet fill.
- Do not infer HOA dues from generic "other" expenses unless the document clearly identifies them.
- Do not infer extraordinary expense unless there is explicit evidence.
- Treat worksheet formulas as read-only; only write into user-input cells.
- If confidence is low, ask for review before writing the workbook.
- Treat `template.xlsx` bundled with the skill as the default worksheet template unless the user explicitly provides another one.
- After generating the workbook, return the actual `.xlsx` file in chat instead of only describing it.
- Do not ask the user whether they want the generated Excel file after it has already been created; send it automatically.
- Do not consider the task complete merely because the file exists on disk.

## Examples

- User uploads a Schedule E PDF and wants the worksheet populated; return the completed Excel file in chat.
- User asks to extract Schedule E rental-property numbers into JSON first, then write them into Excel; after writing, send the Excel file in chat.
- User provides a multi-property Schedule E and wants each property mapped to a separate rental-unit column in the returned workbook.