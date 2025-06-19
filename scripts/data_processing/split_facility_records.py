#!/usr/bin/env python3
"""
Script to split facility data files into individual JSON files for each record.

This script:
1. Reads all JSON files from the facility_data folder
2. For each input file, extracts individual records
3. Creates a subfolder for each input file
4. Saves each record as a separate JSON file in the corresponding subfolder
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Union
import argparse


def load_records_from_file(file_path: Path) -> List[Dict[str, Any]]:
    """
    Load records from a JSON file, handling different structures.

    Args:
        file_path: Path to the JSON file

    Returns:
        List of record dictionaries
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle different JSON structures
        if isinstance(data, list):
            # Direct array of records
            return data
        elif isinstance(data, dict):
            if 'records' in data:
                # Records nested under 'records' key
                return data['records']
            elif len(data) == 1 and isinstance(list(data.values())[0], list):
                # Single key with array value
                return list(data.values())[0]
            else:
                # Single record as object
                return [data]
        else:
            print(f"Warning: Unexpected data structure in {file_path}")
            return []

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Error: Could not read {file_path}: {e}")
        return []


def create_safe_filename(record: Dict[str, Any], index: int, source_filename: str = "") -> str:
    """
    Create a safe filename for the record JSON file using action request number + facility name.

    Args:
        record: The record dictionary
        index: Index of the record in the original file
        source_filename: Name of the source file (used as fallback for facility name)

    Returns:
        Safe filename string in format: ActionRequestNumber_FacilityName.json
    """
    # Get action request number
    action_request = record.get("Action Request Number:", "")
    if not action_request:
        action_request = record.get("Action Request Number", "")

    # Get facility name
    facility_name = record.get("_facility_name", "")
    if not facility_name and source_filename:
        # Use source filename without extension as facility name
        facility_name = Path(source_filename).stem

    # Clean values to make them filesystem-safe
    if action_request:
        safe_action = "".join(c for c in str(action_request).strip() if c.isalnum() or c in ('-', '_')).strip()
    else:
        safe_action = f"Record{index:04d}"

    if facility_name:
        safe_facility = "".join(c for c in str(facility_name).strip() if c.isalnum() or c in ('-', '_')).strip()
    else:
        safe_facility = "UnknownFacility"

    # Create filename: ActionRequestNumber_FacilityName.json
    filename = f"{safe_action}_{safe_facility}.json"

    # Ensure filename is not too long (max 255 characters for most filesystems)
    if len(filename) > 200:
        safe_action = safe_action[:100]
        safe_facility = safe_facility[:90]
        filename = f"{safe_action}_{safe_facility}.json"

    return filename


def split_facility_file(input_file: Path, output_base_dir: Path) -> int:
    """
    Split a single facility file into individual record files.

    Args:
        input_file: Path to the input JSON file
        output_base_dir: Base directory for output

    Returns:
        Number of records processed
    """
    print(f"Processing {input_file.name}...")

    # Load records from the file
    records = load_records_from_file(input_file)

    if not records:
        print(f"  No records found in {input_file.name}")
        return 0

    # Create output subfolder
    subfolder_name = input_file.stem  # Filename without extension
    output_dir = output_base_dir / subfolder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each record
    processed_count = 0
    for index, record in enumerate(records):
        try:
            # Create filename using action request number + facility name
            filename = create_safe_filename(record, index, input_file.name)
            output_file = output_dir / filename

            # Add metadata to the record
            record_with_meta = record.copy()
            record_with_meta['_split_metadata'] = {
                'source_file': input_file.name,
                'record_index': index,
                'split_timestamp': None  # Will be filled at runtime if needed
            }

            # Write the individual record file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(record_with_meta, f, indent=2, ensure_ascii=False)

            processed_count += 1

        except Exception as e:
            print(f"  Error processing record {index}: {e}")
            continue

    print(f"  Created {processed_count} individual files in {output_dir}")
    return processed_count


def main():
    """Main function to process all facility data files."""
    parser = argparse.ArgumentParser(description="Split facility data files into individual JSON records")
    parser.add_argument("--input-dir",
                       default="data/facility_data",
                       help="Input directory containing facility data files (default: data/facility_data)")
    parser.add_argument("--output-dir",
                       default="data/facility_data/split_records",
                       help="Output directory for split records (default: data/facility_data/split_records)")
    parser.add_argument("--file-pattern",
                       default="*.json",
                       help="File pattern to match (default: *.json)")

    args = parser.parse_args()

    # Get the workspace root (assumes script is run from project root or scripts folder)
    if Path.cwd().name == "scripts":
        workspace_root = Path.cwd().parent
    else:
        workspace_root = Path.cwd()

    # Set up paths
    input_dir = workspace_root / args.input_dir
    output_dir = workspace_root / args.output_dir

    # Validate input directory
    if not input_dir.exists():
        print(f"Error: Input directory {input_dir} does not exist")
        sys.exit(1)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all JSON files in the input directory
    json_files = list(input_dir.glob(args.file_pattern))

    # Filter out hidden files and .keep files
    json_files = [f for f in json_files if not f.name.startswith('.') and f.name != '.keep']

    if not json_files:
        print(f"No JSON files found in {input_dir}")
        sys.exit(1)

    print(f"Found {len(json_files)} JSON files to process")
    print(f"Output directory: {output_dir}")
    print("-" * 50)

    # Process each file
    total_records = 0
    for json_file in json_files:
        record_count = split_facility_file(json_file, output_dir)
        total_records += record_count

    print("-" * 50)
    print(f"Processing complete!")
    print(f"Total files processed: {len(json_files)}")
    print(f"Total records created: {total_records}")
    print(f"Output location: {output_dir}")


if __name__ == "__main__":
    main()
