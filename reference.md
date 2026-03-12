# Reference Guide

## Schedule E → Rental Income Worksheet: Cell Mapping

### Column Assignment

Each property maps to one column in the Excel worksheet, starting from column F:

| Property Order | Column |
| :------------- | :----- |
| Property 1     | F      |
| Property 2     | G      |
| Property 3     | H      |
| Property 4     | I      |
| ...            | ...    |

### Row Mapping

| JSON Field              | Excel Row | Worksheet Label                      | Notes                                 |
| :---------------------- | :-------- | :----------------------------------- | :------------------------------------ |
| `address`               | 6         | Rental Unit (address header)         | Text value                            |
| `months_in_service`     | 9         | Step 1 Result — months in service    | Numeric, 1 decimal place              |
| `rents_received`        | 12        | A1 — Enter total rents received      | From Schedule E Line 3                |
| `total_expenses`        | 13        | A2 — Subtract total expenses         | From Schedule E Line 20               |
| `insurance`             | 14        | A3 — Add back insurance expense      | From Schedule E Line 9                |
| `mortgage_interest`     | 15        | A4 — Add back mortgage interest paid | From Schedule E Line 12               |
| `taxes`                 | 16        | A5 — Add back tax expense            | From Schedule E Line 16               |
| `hoa_dues`              | 17        | A6 — Add back HOA dues               | From Schedule E Line 17 (conditional) |
| `depreciation`          | 18        | A7 — Add back depreciation           | From Schedule E Line 18               |
| `extraordinary_expense` | 19        | A8 — Add back extraordinary expense  | From Schedule E Line 8 (conditional)  |

### Formula Cells — DO NOT OVERWRITE

| Row | Label                                                |
| :-- | :--------------------------------------------------- |
| 20  | Equals adjusted rental income (formula)              |
| 21  | A9 — Divide by months (formula)                      |
| 22  | Step 2A Result — Monthly qualifying income (formula) |

---

## Edge Cases

### A6 — HOA Dues

- **Only fill** if Schedule E explicitly identifies the expense as "HOA", "homeowners association dues", or "condominium association fees".
- If Line 17 contains other utilities or miscellaneous expenses, leave A6 as `null`.
- Reason: Fannie Mae guidelines require HOA dues to be specifically identified on Schedule E.

### A8 — Extraordinary Expense

- **Only fill** if there is documented evidence of a one-time extraordinary expense (e.g., casualty loss, major one-time repair).
- Must be clearly distinguishable from recurring operating expenses.
- Reason: Fannie Mae requires evidence of the one-time nature before adding back.

### Fair Rental Days

- 365 or 366 → 12 months (full year)
- Blank / not reported → 12 months (per Fannie Mae guidelines)
- Any other value → round(days / 30, 1)

### Multiple Schedule E Pages

- Schedule E supports 3 properties (A/B/C) per page.
- If taxpayer has more than 3 properties, there will be additional Schedule E pages.
- Process all pages; assign `property_index` sequentially across pages.
- Map to columns F, G, H, I, J, ... in order.

### Negative Values

- Negative values on Schedule E appear in parentheses, e.g., `(500)`.
- Write as negative numbers in Excel: `-500`.
- This can occur for Line 21 (net income/loss) but should not occur for the fields we extract.
