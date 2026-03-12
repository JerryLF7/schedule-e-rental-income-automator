# Role
You are an expert Python developer. Please write a Python script named `write_excel.py` that reads data from a JSON file and writes it into specific cells of an existing Excel template without breaking any formulas.

# CLI Usage
The script should accept 3 arguments:
`python write_excel.py <input_json_path> <template_excel_path> <output_excel_path>`

# Input JSON Structure
```json
{
  "properties": [
    {
      "address": "String", "months_in_service": 12, "rents_received": 1000.0,
      "total_expenses": 500.0, "insurance": 100.0, "mortgage_interest": 200.0,
      "taxes": 50.0, "hoa_dues": null, "depreciation": 50.0, "extraordinary_expense": null,
      "confidence": 0.95
    }
  ],
  "validation": { "passed": true, "notes": "" }
}
```

# Requirements & Logic
1. Dependency: Use openpyxl.
2. Validation Check:
   - Before modifying the Excel file, check if validation["passed"] is true. If false, print the notes and exit with code 1.
   - Check if any property has a confidence score < 0.85. If so, print a warning but allow the user to continue via a y/n CLI prompt.
3. Excel Mapping:
   - Properties correspond to columns starting from F.
     - Property 1 -> Col F, Property 2 -> Col G, Property 3 -> Col H, etc. (Support up to Column O).
   - Map the JSON keys to rows:
     - address -> Row 6
     - months_in_service -> Row 9
     - rents_received -> Row 12
     - total_expenses -> Row 13
     - insurance -> Row 14
     - mortgage_interest -> Row 15
     - taxes -> Row 16
     - hoa_dues -> Row 17
     - depreciation -> Row 18
     - extraordinary_expense -> Row 19
4. Strict Constraint (Formula Protection):
 - Only write to the cells if the JSON value is NOT null.
 - DO NOT write anything to Rows 20, 21, or 22 (these contain Excel formulas).
 - Save the workbook to the <output_excel_path>. Do not overwrite the original template.

Please provide the complete, robust Python code with basic error handling (e.g., FileNotFoundError).