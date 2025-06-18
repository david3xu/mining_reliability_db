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


def create_safe_filename(record: Dict[str, Any], index: int) -> str:
    """
    Create a safe filename for the record JSON file.

    Args:
        record: The record dictionary
        index: Index of the record in the original file

    Returns:
        Safe filename string
    """
    # Try to use meaningful identifiers from the record
    potential_ids = [
        record.get("Action Request Number:", ""),
        record.get("Title", ""),
        record.get("Asset Number(s)", ""),
        record.get("_facility_name", "")
    ]

    # Find the first non-empty identifier
    record_id = None
    for id_val in potential_ids:
        if id_val and str(id_val).strip():
            record_id = str(id_val).strip()
            break

    if record_id:
        # Clean the ID to make it filesystem-safe
        safe_id = "".join(c for c in record_id if c.isalnum() or c in ('-', '_', ' ')).strip()
        safe_id = safe_id.replace(' ', '_')[:50]  # Limit length
        filename = f"{index:04d}_{safe_id}.json"
    else:
        # Fallback to just the index
        filename = f"{index:04d}_record.json"

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
            # Create filename
            filename = create_safe_filename(record, index)
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
