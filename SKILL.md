---
name: schedule_e_rental_income_automator
description: Extract rental property numbers from IRS Schedule E tax forms and fill them into a rental income Excel worksheet while preserving existing formulas.
---

# Schedule E Rental Income

Use this skill when the user wants to read numbers from IRS Schedule E tax forms and enter them into a rental income Excel worksheet that already contains formulas.

When this skill is active, you should:

1. Read the Schedule E form from the provided PDF or image.
2. Extract the required fields for each rental property.
3. Convert fair rental days into months in service.
4. Build a clean JSON object for the worksheet input.
5. Ask for confirmation when any extracted value is unclear or confidence is low.
6. Write the confirmed values into the Excel worksheet without overwriting formulas.

Read `extraction_prompt.txt` for the exact extraction prompt and output schema.
Read `reference.md` for worksheet mapping rules and business logic.
Use `scripts/write_excel.py` to write confirmed JSON values into the worksheet.

Important rules:
- Treat fair rental days of 365 or 366 as 12 months.
- For any other fair rental days value, divide by 30.
- If multiple rental properties are present, fill them into the worksheet from left to right in the same order they appear on Schedule E.
- Do not guess values that are not clearly supported by the tax form.
- Preserve all formulas, formatting, and labels in the Excel file.

## Examples

- User uploads a Schedule E tax form and a rental income worksheet and asks to fill the worksheet automatically.
- User provides a scanned Schedule E image and wants the rental numbers transferred into the Excel template.
- User uploads a Schedule E form with multiple rental properties and wants each property filled into a separate rental unit column.

## Guidelines

- Extract values directly using the model's document understanding capability; do not rely on Python OCR logic in `write_excel.py`.
- Use structured JSON as the handoff format between extraction and Excel writing.
- Extract at least these fields for each property:
  - property_address
  - fair_rental_days
  - months_in_service
  - rents_received
  - total_expenses
  - insurance
  - mortgage_interest
  - taxes
  - depreciation
- If a field is missing, unclear, or not explicitly shown, set it to `null` and flag it for review.
- Only populate HOA dues if the expense is specifically identified as HOA or homeowners' association dues.
- Only populate extraordinary expense if there is explicit support in the tax form or supporting evidence.
- Keep numeric fields numeric in JSON and Excel output.
- If the number of properties exceeds the available rental-unit columns in the worksheet, stop and report the issue instead of truncating data.