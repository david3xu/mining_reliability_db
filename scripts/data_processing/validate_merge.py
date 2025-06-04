#!/usr/bin/env python3
"""
Simple validation script to verify merge results.
"""

import json
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))


def validate_merge_results():
    """Validate the merge results by comparing original and merged data."""

    original_file = project_root / "data/facility_data/mining_maintenance_nested.json"
    merged_file = project_root / "data/exports/mining_maintenance_merged.json"

    print("🔍 Validating merge results...")
    print("=" * 50)

    # Load original data
    with open(original_file, "r", encoding="utf-8") as f:
        original_data = json.load(f)
        original_records = original_data["sheets"]["Mining_Maintenance_Records"]["records"]

    # Load merged data
    with open(merged_file, "r", encoding="utf-8") as f:
        merged_records = json.load(f)

    print(f"📊 Original records: {len(original_records)}")
    print(f"📊 Merged records: {len(merged_records)}")
    print(f"📉 Records reduced: {len(original_records) - len(merged_records)}")

    # Check for Action Request Numbers
    original_action_nums = [
        r.get("Action Request Number:") for r in original_records if r.get("Action Request Number:")
    ]
    merged_action_nums = [
        r.get("Action Request Number:") for r in merged_records if r.get("Action Request Number:")
    ]

    original_unique = set(original_action_nums)
    merged_unique = set(merged_action_nums)

    print(f"📋 Original unique Action Request Numbers: {len(original_unique)}")
    print(f"📋 Merged unique Action Request Numbers: {len(merged_unique)}")

    # Find records with merge metadata
    merged_count = 0
    for record in merged_records:
        if "_merged_from_count" in record:
            merged_count += 1
            print(
                f"✅ Merged record found: {record.get('Action Request Number:', 'Unknown')} "
                f"(from {record['_merged_from_count']} records, "
                f"complexity: {record.get('_merge_complexity', 'unknown')}, "
                f"differing fields: {len(record.get('_differing_fields', []))})"
            )

    print(f"\n📈 Records with merge metadata: {merged_count}")

    # Validate that no data was lost
    if len(merged_unique) == len(original_unique):
        print("✅ All unique Action Request Numbers preserved")
    else:
        print("❌ Some Action Request Numbers were lost!")
        missing = original_unique - merged_unique
        if missing:
            print(f"Missing: {missing}")

    # Check specific merge examples
    duplicate_examples = ["2021-06400", "2023-02031", "2023-05713"]
    print(f"\n🔍 Checking specific duplicate examples:")

    for action_num in duplicate_examples:
        # Count in original
        original_count = original_action_nums.count(action_num)
        merged_count = merged_action_nums.count(action_num)

        print(f"  {action_num}: {original_count} → {merged_count} records")

        if merged_count == 1:
            # Find the merged record
            merged_record = next(
                (r for r in merged_records if r.get("Action Request Number:") == action_num), None
            )
            if merged_record and "_merged_from_count" in merged_record:
                expected_merged = merged_record["_merged_from_count"]
                if expected_merged == original_count:
                    print(f"    ✅ Correctly merged from {expected_merged} records")
                else:
                    print(f"    ❌ Expected to merge {original_count}, but shows {expected_merged}")
            else:
                print(f"    ❌ No merge metadata found")
        else:
            print(f"    ❌ Expected 1 merged record, found {merged_count}")

    print("\n" + "=" * 50)
    print("✅ Merge validation completed!")


if __name__ == "__main__":
    validate_merge_results()
