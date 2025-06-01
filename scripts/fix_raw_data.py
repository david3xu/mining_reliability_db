#!/usr/bin/env python3
"""
Fix Raw Data Script for Mining Reliability Database
Converts 'Requested Response Time' from text (e.g., "48 hours", "2 weeks") to integer days (1-90)
Ensures 'Days Past Due' is properly formatted as integer
"""

import json
import argparse
import re
from pathlib import Path
from typing import Dict, Any, Optional

def convert_response_time_to_days(response_time_text: Any) -> Optional[int]:
    """Convert response time text to integer days (1-90 range)"""
    if response_time_text is None or response_time_text == "None":
        return None

    if isinstance(response_time_text, int):
        # Already an integer, clamp to valid range
        return max(1, min(90, response_time_text))

    if not isinstance(response_time_text, str):
        return None

    text = response_time_text.strip().lower()

    # Extract number from text
    number_match = re.search(r'(\d+)', text)
    if not number_match:
        return None

    number = int(number_match.group(1))

    # Convert based on time unit
    if 'hour' in text:
        # Convert hours to days (24 hours = 1 day)
        days = max(1, round(number / 24))
    elif 'day' in text:
        days = number
    elif 'week' in text:
        # Convert weeks to days
        days = number * 7
    elif 'month' in text:
        # Convert months to days (30 days per month)
        days = number * 30
    else:
        # Default: assume it's days
        days = number

    # Clamp to valid range (1-90 days)
    return max(1, min(90, days))

def fix_days_past_due(days_past_due: Any) -> Optional[int]:
    """Ensure Days Past Due is properly formatted as integer"""
    if days_past_due is None:
        return None

    if isinstance(days_past_due, int):
        return days_past_due

    if isinstance(days_past_due, str):
        try:
            return int(days_past_due)
        except ValueError:
            return None

    return None

def fix_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Fix a single record's response time and days past due fields"""
    fixed_record = record.copy()

    # Fix Requested Response Time
    if "Requested Response Time" in fixed_record:
        original_value = fixed_record["Requested Response Time"]
        converted_value = convert_response_time_to_days(original_value)
        if converted_value is not None:
            fixed_record["Requested Response Time"] = converted_value
            print(f"  Converted 'Requested Response Time': '{original_value}' → {converted_value} days")
        else:
            # Set a default value for invalid entries
            fixed_record["Requested Response Time"] = 7  # 1 week default
            print(f"  Fixed invalid 'Requested Response Time': '{original_value}' → 7 days (default)")

    # Fix Days Past Due
    if "Days Past Due" in fixed_record:
        original_value = fixed_record["Days Past Due"]
        converted_value = fix_days_past_due(original_value)
        fixed_record["Days Past Due"] = converted_value
        if original_value != converted_value:
            print(f"  Fixed 'Days Past Due': {original_value} → {converted_value}")

    return fixed_record

def fix_raw_data_file(input_file: Path, output_file: Path = None) -> Dict[str, Any]:
    """Fix a single raw data file"""
    if output_file is None:
        output_file = input_file  # Overwrite original file

    print(f"Fixing {input_file.name}...")

    try:
        # Load data
        with open(input_file, 'r') as f:
            data = json.load(f)

        # Handle different data structures
        records = []
        if isinstance(data, list):
            records = data
            fixed_data = []
        elif isinstance(data, dict):
            if "sheets" in data:
                # Multi-sheet structure
                for sheet_name, sheet_data in data["sheets"].items():
                    if isinstance(sheet_data, dict) and "records" in sheet_data:
                        records.extend(sheet_data["records"])
                fixed_data = {"sheets": {}}
            elif "records" in data:
                records = data["records"]
                fixed_data = {"records": []}
            else:
                records = [data]
                fixed_data = []

        if not records:
            print(f"  No records found in {input_file.name}")
            return {"processed": 0, "conversions": 0}

        # Fix all records
        fixed_records = []
        conversion_count = 0

        for i, record in enumerate(records):
            original_response_time = record.get("Requested Response Time")
            original_days_due = record.get("Days Past Due")

            fixed_record = fix_record(record)
            fixed_records.append(fixed_record)

            # Count conversions
            if (record.get("Requested Response Time") != fixed_record.get("Requested Response Time") or
                record.get("Days Past Due") != fixed_record.get("Days Past Due")):
                conversion_count += 1

        # Reconstruct data structure
        if isinstance(data, list):
            final_data = fixed_records
        elif isinstance(data, dict):
            if "sheets" in data:
                final_data = {"sheets": {}}
                for sheet_name, sheet_data in data["sheets"].items():
                    final_data["sheets"][sheet_name] = {
                        "records": fixed_records
                    }
            elif "records" in data:
                final_data = {"records": fixed_records}
            else:
                final_data = fixed_records[0] if len(fixed_records) == 1 else fixed_records

        # Save fixed data
        with open(output_file, 'w') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)

        print(f"  ✅ Fixed {len(fixed_records)} records ({conversion_count} conversions)")
        print(f"  📁 Saved to {output_file}")

        return {
            "processed": len(fixed_records),
            "conversions": conversion_count
        }

    except Exception as e:
        print(f"  ❌ Error fixing {input_file.name}: {e}")
        return {"processed": 0, "conversions": 0, "error": str(e)}

def fix_all_raw_data(raw_data_dir: str = None, backup: bool = True) -> Dict[str, Any]:
    """Fix all raw data files in the directory"""
    # Set up directory
    if raw_data_dir is None:
        project_root = Path(__file__).resolve().parent.parent
        raw_directory = project_root / "data" / "raw_data"
    else:
        raw_directory = Path(raw_data_dir)

    if not raw_directory.exists():
        print(f"❌ Raw data directory not found: {raw_directory}")
        return {"processed_files": 0, "total_records": 0, "total_conversions": 0}

    # Create backup directory if requested
    if backup:
        backup_dir = raw_directory.parent / "raw_data_backup"
        backup_dir.mkdir(exist_ok=True)
        print(f"📂 Backup directory: {backup_dir}")

    json_files = list(raw_directory.glob("*.json"))
    print(f"🔍 Found {len(json_files)} raw data files to fix")
    print()

    summary = {
        "processed_files": 0,
        "total_records": 0,
        "total_conversions": 0,
        "files_with_errors": []
    }

    for json_file in json_files:
        # Create backup if requested
        if backup:
            backup_file = backup_dir / json_file.name
            import shutil
            shutil.copy2(json_file, backup_file)
            print(f"  💾 Backed up to {backup_file}")

        # Fix the file
        result = fix_raw_data_file(json_file)

        if result.get("processed", 0) > 0:
            summary["processed_files"] += 1
            summary["total_records"] += result["processed"]
            summary["total_conversions"] += result.get("conversions", 0)

        if "error" in result:
            summary["files_with_errors"].append(json_file.name)

        print()

    print("=" * 50)
    print("📊 SUMMARY:")
    print(f"Files processed: {summary['processed_files']}")
    print(f"Total records: {summary['total_records']}")
    print(f"Total conversions: {summary['total_conversions']}")
    if summary["files_with_errors"]:
        print(f"Files with errors: {summary['files_with_errors']}")
    print()

    return summary

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Fix raw data: convert 'Requested Response Time' to integer days (1-90) and ensure 'Days Past Due' is integer"
    )
    parser.add_argument("--file", type=str, help="Fix specific file instead of all files")
    parser.add_argument("--raw-data-dir", type=str, help="Raw data directory path (default: data/raw_data)")
    parser.add_argument("--no-backup", action="store_true", help="Skip creating backup files")

    args = parser.parse_args()

    try:
        if args.file:
            # Fix specific file
            if args.raw_data_dir:
                raw_dir = Path(args.raw_data_dir)
            else:
                project_root = Path(__file__).resolve().parent.parent
                raw_dir = project_root / "data" / "raw_data"

            input_file = raw_dir / args.file
            if not input_file.exists():
                print(f"❌ File not found: {input_file}")
                return 1

            # Create backup if requested
            if not args.no_backup:
                backup_dir = raw_dir.parent / "raw_data_backup"
                backup_dir.mkdir(exist_ok=True)
                backup_file = backup_dir / input_file.name
                import shutil
                shutil.copy2(input_file, backup_file)
                print(f"💾 Backed up to {backup_file}")

            result = fix_raw_data_file(input_file)

            if result.get("processed", 0) > 0:
                print(f"✅ Successfully fixed {args.file}")
                print(f"Records processed: {result['processed']}")
                print(f"Conversions made: {result.get('conversions', 0)}")
                return 0
            else:
                print(f"❌ Failed to fix {args.file}")
                return 1
        else:
            # Fix all files
            summary = fix_all_raw_data(args.raw_data_dir, not args.no_backup)

            if summary["processed_files"] > 0:
                print("✅ Successfully fixed raw data files!")
                return 0
            else:
                print("❌ No files were processed successfully")
                return 1

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
