---
name: schedule-e-rental-income-automator
description: Extract rental-property values from IRS Schedule E forms and produce a filled rental income Excel worksheet using the bundled template while preserving formulas and formatting. Use when the user wants Schedule E figures converted into worksheet-ready JSON or directly written into the rental income workbook, including multi-property Schedule E pages.
---

# Schedule E Rental Income Automator

Use this skill to turn one or more IRS Schedule E pages into worksheet-ready JSON and, when the extracted values are reliable enough, a completed Excel workbook.

Default to returning a filled workbook, not just extracted numbers.

## Workflow

1. Read `references/extraction_prompt.md` and extract one property record per rental in source order.
2. Read `references/reference.md` and validate the worksheet mapping and business rules.
3. Compute `months_in_service` with these rules:
   - `365` or `366` -> `12`
   - blank or missing fair-rental days -> `12`
   - any other numeric value -> `round(days / 30, 1)`
4. Keep JSON numeric fields numeric.
5. Set unclear, missing, or unsupported fields to `null` instead of guessing.
6. If required values are missing, confidence is low, or the form is materially ambiguous, ask for confirmation before writing the workbook.
7. Otherwise, write the confirmed JSON into `assets/template.xlsx` with `scripts/write_excel.py` and return the completed workbook.

## Operating Rules

- Preserve property order exactly as shown across all Schedule E pages.
- Fill worksheet columns from left to right in that same order.
- Preserve formulas, formatting, labels, and untouched cells.
- Write only to the mapped input cells from `references/reference.md`.
- Do not infer HOA dues from generic expenses.
- Do not infer extraordinary expense without explicit support.
- If the worksheet does not have enough property columns, stop and report it.
- Treat JSON as an intermediate artifact unless the user explicitly asks for JSON only.

## Bundled Files

- `references/extraction_prompt.md` — extraction prompt and JSON schema
- `references/reference.md` — worksheet mapping and business rules
- `assets/template.xlsx` — default worksheet template
- `scripts/write_excel.py` — writes JSON into Excel without overwriting formulas

## Execution Rule

If the required values are readable and validation passes, continue straight to workbook generation. Do not stop after producing JSON unless the user asked for JSON only.

Run:

```bash
python scripts/write_excel.py <input_json> assets/template.xlsx <output.xlsx>
```

Use `--force` when the JSON was already reviewed and you want non-interactive execution despite low confidence or validation warnings.
