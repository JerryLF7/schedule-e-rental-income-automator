#!/usr/bin/env python3
"""
Write rental property data from JSON into a bundled Excel template.
Preserve existing formulas and formatting.

Usage:
    python write_excel.py <input_json_path> <template_excel_path> <output_excel_path> [--force]
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("Error: openpyxl is not installed. Please run: pip install openpyxl")
    sys.exit(1)


ROW_MAPPING = {
    "address": 6,
    "months_in_service": 9,
    "rents_received": 12,
    "total_expenses": 13,
    "insurance": 14,
    "mortgage_interest": 15,
    "taxes": 16,
    "hoa_dues": 17,
    "depreciation": 18,
    "extraordinary_expense": 19,
}

FORMULA_ROWS = {20, 21, 22}
MAX_PROPERTY_COUNT = 10  # Columns F:O


def get_column_letter(property_index: int) -> str:
    """Map property 1..10 to Excel columns F..O."""
    if property_index < 1:
        raise ValueError(f"Property index must be >= 1, got {property_index}.")
    if property_index > MAX_PROPERTY_COUNT:
        raise ValueError(
            f"Maximum of {MAX_PROPERTY_COUNT} properties supported (columns F-O). "
            f"Property {property_index} exceeds limit."
        )

    column_number = 5 + property_index  # F=6 in 1-indexed Excel numbering
    result = ""
    while column_number:
        column_number, remainder = divmod(column_number - 1, 26)
        result = chr(65 + remainder) + result
    return result


def prompt_yes_no(message: str) -> bool:
    while True:
        response = input(f"\n{message} (y/n): ").strip().lower()
        if response == "y":
            return True
        if response == "n":
            return False
        print("Please enter 'y' or 'n'.")


def validate_payload(data: dict) -> tuple[list, dict]:
    if "properties" not in data or not isinstance(data["properties"], list):
        raise ValueError("JSON must contain a 'properties' array.")
    if "validation" not in data or not isinstance(data["validation"], dict):
        raise ValueError("JSON must contain a 'validation' object.")

    properties = data["properties"]
    validation = data["validation"]
    if not properties:
        raise ValueError("JSON contains no properties to write.")

    return properties, validation


def confirm_warnings(properties: list, validation: dict, force: bool) -> None:
    warnings = []

    if not validation.get("passed", False):
        warnings.append(f"Validation failed: {validation.get('notes', 'Validation failed')}")

    low_conf = [
        f"{prop.get('address', 'Unknown')} ({prop.get('confidence', 0.0):.2f})"
        for prop in properties
        if prop.get("confidence", 1.0) < 0.85
    ]
    if low_conf:
        warnings.append("Low confidence properties: " + "; ".join(low_conf))

    if not warnings:
        return

    if force:
        for warning in warnings:
            print(f"⚠️  {warning}")
        print("--force supplied; continuing non-interactively.")
        return

    print("\n⚠️  Review required before workbook generation:")
    for warning in warnings:
        print(f"  - {warning}")

    if not prompt_yes_no("Do you want to continue"):
        print("Operation cancelled by user.")
        sys.exit(0)


def write_json_to_excel(json_path: str, template_path: str, output_path: str, force: bool = False) -> None:
    json_file = Path(json_path)
    template_file = Path(template_path)
    output_file = Path(output_path)

    if not json_file.exists():
        raise FileNotFoundError(f"Input JSON file not found: {json_path}")
    if not template_file.exists():
        raise FileNotFoundError(f"Template Excel file not found: {template_path}")

    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    properties, validation = validate_payload(data)
    confirm_warnings(properties, validation, force)

    print(f"Loading template: {template_path}")
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    print(f"Processing {len(properties)} property(ies)...")
    for prop in properties:
        property_index = prop.get("property_index", 1)
        column = get_column_letter(property_index)
        print(f"  Writing Property {property_index} ({prop.get('address', 'N/A')[:30]}...) to column {column}")

        for json_key, row in ROW_MAPPING.items():
            if row in FORMULA_ROWS:
                continue
            value = prop.get(json_key)
            if value is not None:
                ws[f"{column}{row}"].value = value

    output_file.parent.mkdir(parents=True, exist_ok=True)
    print(f"Saving output to: {output_path}")
    wb.save(output_file)
    print("✅ Successfully wrote data to Excel template!")
    print("\nSummary:")
    print(f"  - Properties processed: {len(properties)}")
    print(f"  - Output file: {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write Schedule E JSON into an Excel template.")
    parser.add_argument("input_json_path")
    parser.add_argument("template_excel_path")
    parser.add_argument("output_excel_path")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Continue non-interactively despite validation or low-confidence warnings.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        write_json_to_excel(
            args.input_json_path,
            args.template_excel_path,
            args.output_excel_path,
            force=args.force,
        )
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Value Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
