#!/usr/bin/env python3
"""
Simplified Merge Process for Mining Maintenance Records
Groups records by Action Request Number and merges differing field values with pipe delimiter.
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class SimpleMerger:
    """Simple record merger that groups by Action Request Number and merges differing values with '|'."""

    def get_action_numbers_in_original_order(
        self, records: List[Dict[str, Any]], grouped_records: Dict[str, List[Dict[str, Any]]]
    ) -> List[str]:
        """
        Get Action Request Numbers in the order they first appear in the original dataset.
        This preserves the original input order rather than sorting alphabetically.
        """
        action_field = self.find_action_request_field(records)
        if not action_field:
            return list(grouped_records.keys())

        seen_action_numbers = set()
        ordered_action_numbers = []

        # Go through original records in order and track first occurrence of each Action Request Number
        for record in records:
            action_number = record.get(action_field)
            if action_number:
                action_key = str(action_number).strip()
                if action_key not in seen_action_numbers and action_key in grouped_records:
                    seen_action_numbers.add(action_key)
                    ordered_action_numbers.append(action_key)

        return ordered_action_numbers

    def merge_field_values(self, values: List[Any]) -> Any:
        """
        Core merge logic: identical values = keep one, different values = join with ' | '
        """
        # Filter out None and empty string values
        valid_values = []
        for value in values:
            if value is not None and str(value).strip():
                valid_values.append(str(value).strip())

        if not valid_values:
            return None

        # Get unique values while preserving order
        unique_values = []
        for value in valid_values:
            if value not in unique_values:
                unique_values.append(value)

        # If only one unique value, return it
        if len(unique_values) == 1:
            return unique_values[0]

        # Multiple different values: join with pipe
        return " | ".join(unique_values)

    def merge_record_group(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge a group of records with the same Action Request Number."""
        if not records:
            return {}

        if len(records) == 1:
            return records[0]

        # Preserve order from first record
        field_order = list(records[0].keys())
        for record in records[1:]:
            for field in record.keys():
                if field not in field_order:
                    field_order.append(field)

        # Merge in correct order
        merged_record = {}
        for field_name in field_order:
            values = [record.get(field_name) for record in records]
            merged_record[field_name] = self.merge_field_values(values)

        return merged_record

    def find_action_request_field(self, records: List[Dict[str, Any]]) -> Optional[str]:
        """Find the correct Action Request Number field name in the data."""
        if not records:
            return None

        # Check first record for possible field names
        sample_record = records[0]
        possible_names = [
            "Action Request Number:",
            "Action Request Number",
            "action_request_number",
            "ActionRequestNumber",
        ]

        for name in possible_names:
            if name in sample_record:
                logger.info(f"Found Action Request field: '{name}'")
                return name

        # Log available fields for debugging
        logger.warning(
            f"Action Request field not found. Available fields: {list(sample_record.keys())[:10]}"
        )
        return None

    def group_records_by_action_number(
        self, records: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Group records by Action Request Number field."""
        action_field = self.find_action_request_field(records)
        if not action_field:
            logger.error("Cannot find Action Request Number field")
            return {}

        grouped = {}
        for record in records:
            action_number = record.get(action_field)
            if action_number:
                action_key = str(action_number).strip()
                if action_key not in grouped:
                    grouped[action_key] = []
                grouped[action_key].append(record)

        logger.info(
            f"Grouped {len(records)} records into {len(grouped)} unique Action Request Numbers"
        )
        return grouped

    def load_json_data(self, file_path: Path) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Load JSON data and extract records, preserving structure info."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        structure_info = {"type": "unknown"}
        records = []

        if isinstance(data, list):
            # Direct array of records
            records = data
            structure_info = {"type": "array"}
        elif isinstance(data, dict):
            if "records" in data:
                # {'records': [...]} structure
                records = data["records"]
                structure_info = {"type": "records_wrapper"}
            elif "sheets" in data and isinstance(data["sheets"], dict):
                # Multi-sheet structure - take first sheet
                sheet_name = next(iter(data["sheets"]))
                sheet_data = data["sheets"][sheet_name]
                if isinstance(sheet_data, dict) and "records" in sheet_data:
                    records = sheet_data["records"]
                    structure_info = {
                        "type": "sheets",
                        "sheet_name": sheet_name,
                        "has_records": True,
                    }
                elif isinstance(sheet_data, list):
                    records = sheet_data
                    structure_info = {
                        "type": "sheets",
                        "sheet_name": sheet_name,
                        "has_records": False,
                    }
                else:
                    logger.error(f"Unrecognized sheet structure in {file_path}")
                    return [], structure_info
            else:
                logger.error(f"Unrecognized JSON structure in {file_path}")
                return [], structure_info
        else:
            logger.error(f"Invalid JSON data type in {file_path}: {type(data)}")
            return [], structure_info

        logger.info(f"Loaded {len(records)} records from {file_path}")
        return records, structure_info

    def save_json_data(
        self, records: List[Dict[str, Any]], structure_info: Dict[str, Any], output_file: Path
    ) -> None:
        """Save records in the same structure format as input."""
        if structure_info["type"] == "array":
            output_data = records
        elif structure_info["type"] == "records_wrapper":
            output_data = {"records": records}
        elif structure_info["type"] == "sheets":
            if structure_info.get("has_records", False):
                sheet_data = {"records": records}
            else:
                sheet_data = records
            output_data = {"sheets": {structure_info["sheet_name"]: sheet_data}}
        else:
            # Default to records wrapper
            output_data = {"records": records}

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved {len(records)} records to {output_file}")

    def process_facility_file(self, input_file: Path, output_file: Path) -> Dict[str, Any]:
        """Process a single facility file: load, merge, save."""
        logger.info(f"Processing {input_file.name}")

        try:
            # Load data
            records, structure_info = self.load_json_data(input_file)
            if not records:
                logger.warning(f"No records in {input_file.name}")
                return {
                    "input_file": input_file.name,
                    "input_records": 0,
                    "output_records": 0,
                    "merge_groups": 0,
                    "status": "empty",
                }

            # Group by Action Request Number
            grouped_records = self.group_records_by_action_number(records)
            if not grouped_records:
                logger.warning(f"Grouping failed for {input_file.name}")
                return {
                    "input_file": input_file.name,
                    "input_records": len(records),
                    "output_records": 0,
                    "merge_groups": 0,
                    "status": "grouping_failed",
                }

            # Merge each group - preserve original order from input dataset
            merged_records = []
            merge_count = 0
            # Get Action Request Numbers in the order they first appeared in the original dataset
            ordered_action_numbers = self.get_action_numbers_in_original_order(records, grouped_records)

            logger.info(
                f"Processing {len(ordered_action_numbers)} Action Request Numbers in original input order"
            )

            for action_number in ordered_action_numbers:
                record_group = grouped_records[action_number]
                merged_record = self.merge_record_group(record_group)
                merged_records.append(merged_record)
                if len(record_group) > 1:
                    merge_count += 1
                    logger.info(
                        f"Merged {len(record_group)} records for Action Request: {action_number}"
                    )

            # Save merged data
            self.save_json_data(merged_records, structure_info, output_file)

            return {
                "input_file": input_file.name,
                "input_records": len(records),
                "output_records": len(merged_records),
                "merge_groups": merge_count,
                "unique_actions": len(grouped_records),
                "status": "success",
            }

        except Exception as e:
            logger.error(f"Processing failed for {input_file.name}: {e}")
            return {
                "input_file": input_file.name,
                "input_records": 0,
                "output_records": 0,
                "merge_groups": 0,
                "status": "failed",
                "error": str(e),
            }


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="Simple record merger by Action Request Number")
    parser.add_argument("--input-dir", default="data/inter_data", help="Input directory")
    parser.add_argument("--output-dir", default="data/facility_data", help="Output directory")
    parser.add_argument("--input-file", help="Process single file")

    args = parser.parse_args()

    # Setup paths
    project_root = Path(__file__).parent.parent.parent
    input_dir = project_root / args.input_dir
    output_dir = project_root / args.output_dir

    # Find input files
    if args.input_file:
        input_files = [project_root / args.input_file]
    else:
        input_files = list(input_dir.glob("*.json"))

    if not input_files:
        logger.error(f"No JSON files found in {input_dir}")
        return 1

    logger.info(f"Found {len(input_files)} files to process")

    # Process files
    merger = SimpleMerger()
    all_stats = []

    for input_file in input_files:
        output_file = output_dir / input_file.name
        stats = merger.process_facility_file(input_file, output_file)
        all_stats.append(stats)

        logger.info(
            f"Completed {input_file.name}: {stats['input_records']} → {stats['output_records']} records"
        )

    # Print summary
    total_input = sum(s["input_records"] for s in all_stats)
    total_output = sum(s["output_records"] for s in all_stats)
    total_groups = sum(s["merge_groups"] for s in all_stats)

    logger.info("=" * 50)
    logger.info("PROCESSING SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Files processed: {len(all_stats)}")
    logger.info(f"Total input records: {total_input}")
    logger.info(f"Total output records: {total_output}")
    logger.info(f"Total merge groups: {total_groups}")
    logger.info(f"Records reduced: {total_input - total_output}")
    logger.info("=" * 50)

    return 0


if __name__ == "__main__":
    exit(main())
