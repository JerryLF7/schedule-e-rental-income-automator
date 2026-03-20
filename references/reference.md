# Schedule E Rental Income Reference

This reference defines the worksheet mapping, calculation rules, and completion requirements for the Schedule E rental-income workflow.

Use this file only for durable, reusable **general rules**. Put narrow, example-driven, or document-specific learnings in `cases.md` instead.

The final deliverable for this skill is a completed Excel workbook returned to the user in chat as an attached file whenever the environment supports file attachment.

A generated local path alone is not considered complete output if the file can be attached in the chat interface.

## 1. Overall Goal

Convert extracted Schedule E rental-property values into worksheet inputs and produce a completed `.xlsx` file based on `Rental_Income_Worksheet_Template.xlsx`.

The workflow is complete only when:
1. the workbook has been generated successfully, and
2. the generated `.xlsx` file has been sent back to the user in chat as an attachment, unless attachment is unavailable in the current environment

## 2. Property Ordering

If Schedule E contains multiple rental properties:
- preserve the property order exactly as shown on the form
- map property A to the first worksheet rental-unit column
- map property B to the next worksheet rental-unit column
- map property C to the next worksheet rental-unit column
- continue left to right

Do not reorder properties.

## 3. Step 1 Rule: Months In Service

Use Fair Rental Days to compute months in service as follows:
- `365` -> `12`
- `366` -> `12`
- any other numeric value -> `fair_rental_days / 30`

If Fair Rental Days is missing and there is no contrary evidence, treat the property as `12` months in service.

## 4. Worksheet Mapping

Use the skill's bundled `Rental_Income_Worksheet_Template.xlsx` as the default workbook unless the user explicitly provides a different worksheet.

For each property, write values into one worksheet column.

Default rental-unit columns:
- property 1 -> column `F`
- property 2 -> column `G`
- property 3 -> column `H`
- continue left to right as needed within template capacity

### Field-to-row mapping

- `property_address` -> row `6`
- `months_in_service` -> row `9`
- `rents_received` -> row `12`
- `total_expenses` -> row `13`
- `insurance` -> row `14`
- `mortgage_interest` -> row `15`
- `taxes` -> row `16`
- `hoa_dues` -> row `17`
- `depreciation` -> row `18`
- `extraordinary_expense` -> row `19`

## 5. Formula Protection

Do not overwrite calculated cells or formula cells.

In particular, do not write into result rows that are already formula-driven in the worksheet, including:
- adjusted rental income result rows
- divide-by-month rows
- monthly qualifying income result rows

Only write into the designated user-input cells.

Preserve:
- formulas
- formatting
- borders
- merged cells
- labels
- workbook structure

## 6. Data Interpretation Rules

### Rents received
Map from Schedule E line 3.

### Total expenses
Map from Schedule E line 20.

### Insurance
Map from Schedule E line 9.

### Mortgage interest
Map from Schedule E line 12.

### Taxes
Map from Schedule E line 16.

### Depreciation
Map from Schedule E line 18.

### HOA dues
Populate only if the expense is explicitly identified as homeowners' association dues, HOA dues, or a clearly equivalent label.

Do not infer HOA dues from generic "other" expenses.

### Extraordinary expense
Populate only if the document explicitly supports a one-time extraordinary expense such as casualty loss or another clearly documented one-time add-back item.

Do not infer extraordinary expense when evidence is missing.

## 7. Missing Or Unclear Values

If a required field is unreadable, missing, or materially ambiguous:
- set the structured value to `null`
- request review before writing the workbook if the missing value prevents reliable completion

Do not guess unsupported values.

## 8. When To Pause

Pause and ask the user for confirmation only if:
- an important field is missing or unclear
- confidence is low
- the extracted values are contradictory
- the number of properties exceeds worksheet capacity
- the workbook cannot be generated successfully

Do not pause merely to ask whether the user wants the Excel file after the workbook has already been created.

## 9. Output Behavior

If extraction is sufficiently reliable and workbook generation succeeds:
- immediately return the completed `.xlsx` file to the user in chat
- do not stop at JSON
- do not stop at a local file path
- do not ask whether the user wants the generated file
- do not treat "saved to ..." as the final answer

If the environment supports chat attachments, the assistant should attach the file in the same completion turn.

A short confirmation message is fine, for example:
- "Done — attached is the completed Excel worksheet."
- "Done — I filled the worksheet and attached the `.xlsx` file."

Do not replace the file attachment with a text-only summary when the file is available.