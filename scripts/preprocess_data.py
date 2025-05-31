#!/usr/bin/env python3
"""
Data Preprocessing Script for Mining Reliability Database
Converts list fields to strings and enhances root cause intelligence.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Union
from mine_core.shared.common import setup_project_environment, handle_error
from mine_core.shared.field_utils import extract_root_cause_tail, has_real_value
from configs.environment import get_data_dir, get_root_cause_delimiters

def convert_list_to_string(value: Union[List, Any], delimiter: str = "; ") -> str:
    """Convert list field to string using consistent delimiter"""
    if isinstance(value, list):
        # Filter out empty/null values and convert to strings
        valid_items = [str(item).strip() for item in value if has_real_value(item)]
        return delimiter.join(valid_items) if valid_items else "DATA_NOT_AVAILABLE"

    # If not a list, return as string
    return str(value) if has_real_value(value) else "DATA_NOT_AVAILABLE"

def enhance_root_cause_intelligence(record: Dict[str, Any]) -> Dict[str, Any]:
    """Add root cause tail field for enhanced causal intelligence"""
    root_cause = record.get("Root Cause")

    if has_real_value(root_cause):
        # Convert to string if it's a list
        if isinstance(root_cause, list):
            root_cause_str = convert_list_to_string(root_cause)
            record["Root Cause"] = root_cause_str
        else:
            root_cause_str = str(root_cause)

        # Extract tail for secondary causal analysis - use default delimiters to avoid empty separator issue
        record["Root Cause Tail"] = extract_root_cause_tail(root_cause_str)
    else:
        record["Root Cause Tail"] = "NOT_SPECIFIED"

    return record

def analyze_all_field_types(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """Comprehensive analysis of ALL field types across records"""
    field_analysis = {}

    for record in records:
        for field_name, value in record.items():
            if field_name not in field_analysis:
                field_analysis[field_name] = {
                    "list_count": 0,
                    "string_count": 0,
                    "total_count": 0
                }

            field_analysis[field_name]["total_count"] += 1

            if isinstance(value, list):
                field_analysis[field_name]["list_count"] += 1
            elif isinstance(value, (str, int, float, bool)) or value is None:
                field_analysis[field_name]["string_count"] += 1

    return field_analysis

def identify_list_fields(field_analysis: Dict[str, Dict[str, int]]) -> List[str]:
    """Identify fields that should be converted from lists to strings"""
    list_fields = []

    for field_name, stats in field_analysis.items():
        # Convert if ANY occurrence is a list
        if stats["list_count"] > 0:
            list_fields.append(field_name)

    return list_fields

def preprocess_record(record: Dict[str, Any], list_fields: List[str]) -> Dict[str, Any]:
    """Preprocess single record: convert lists and enhance intelligence"""
    processed_record = record.copy()

    # Convert identified list fields to strings
    for field_name in list_fields:
        if field_name in processed_record:
            processed_record[field_name] = convert_list_to_string(
                processed_record[field_name]
            )

    # Enhance root cause intelligence
    processed_record = enhance_root_cause_intelligence(processed_record)

    return processed_record

def preprocess_facility_data(input_file: Path, output_file: Path) -> Dict[str, Any]:
    """Preprocess facility data file with comprehensive field analysis and conversion"""
    logger.info(f"Preprocessing {input_file}")

    try:
        # Load raw data
        with open(input_file, 'r') as f:
            data = json.load(f)

        # Extract records from data structure
        records = []
        if isinstance(data, dict):
            if "sheets" in data:
                for sheet_name, sheet_data in data["sheets"].items():
                    if isinstance(sheet_data, dict) and "records" in sheet_data:
                        records.extend(sheet_data["records"])
            elif "records" in data:
                records.extend(data["records"])
            else:
                records.append(data)
        elif isinstance(data, list):
            records.extend(data)

        if not records:
            logger.warning(f"No records found in {input_file}")
            return {"processed": 0, "field_analysis": {}}

        # Comprehensive field analysis
        field_analysis = analyze_all_field_types(records)
        list_fields = identify_list_fields(field_analysis)

        logger.info(f"Analyzed {len(field_analysis)} fields across {len(records)} records")
        logger.info(f"Fields requiring list conversion: {list_fields}")

        # Log field analysis summary
        for field_name, stats in field_analysis.items():
            if stats["list_count"] > 0:
                logger.info(f"Field '{field_name}': {stats['list_count']}/{stats['total_count']} are lists")

        # Preprocess all records
        processed_records = []
        for record in records:
            processed_record = preprocess_record(record, list_fields)
            processed_records.append(processed_record)

        # Create output directory if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Reconstruct data structure
        if isinstance(data, dict) and "sheets" in data:
            # Multi-sheet structure
            processed_data = {"sheets": {}}
            for sheet_name, sheet_data in data["sheets"].items():
                processed_data["sheets"][sheet_name] = {
                    "records": processed_records
                }
        elif isinstance(data, dict) and "records" in data:
            # Single records structure
            processed_data = {
                "records": processed_records
            }
        else:
            # Direct list
            processed_data = processed_records

        # Save processed data
        with open(output_file, 'w') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Preprocessed {len(processed_records)} records")
        logger.info(f"Output saved to {output_file}")

        return {
            "processed": len(processed_records),
            "field_analysis": field_analysis,
            "list_fields": list_fields,
            "root_cause_enhanced": sum(1 for r in processed_records
                                     if has_real_value(r.get("Root Cause Tail")))
        }

    except Exception as e:
        handle_error(logger, e, f"preprocessing {input_file}")
        return {"processed": 0, "field_analysis": {}, "error": str(e)}

def preprocess_all_facilities(raw_data_dir: str = None, output_data_dir: str = None) -> Dict[str, Any]:
    """Preprocess all facility data files from raw_data to facility_data"""
    # Set up directories
    if raw_data_dir is None:
        project_root = Path(__file__).resolve().parent.parent
        raw_directory = project_root / "data" / "raw_data"
    else:
        raw_directory = Path(raw_data_dir)

    if output_data_dir is None:
        project_root = Path(__file__).resolve().parent.parent
        output_directory = project_root / "data" / "facility_data"
    else:
        output_directory = Path(output_data_dir)

    if not raw_directory.exists():
        logger.error(f"Raw data directory not found: {raw_directory}")
        return {"processed_files": 0, "total_records": 0}

    # Create output directory
    output_directory.mkdir(parents=True, exist_ok=True)

    json_files = list(raw_directory.glob("*.json"))
    logger.info(f"Found {len(json_files)} raw files to preprocess")

    summary = {
        "processed_files": 0,
        "total_records": 0,
        "all_field_analysis": {},
        "list_fields_found": set(),
        "root_cause_enhancements": 0
    }

    for json_file in json_files:
        output_file = output_directory / json_file.name  # Same filename in output directory

        result = preprocess_facility_data(json_file, output_file)

        if result.get("processed", 0) > 0:
            summary["processed_files"] += 1
            summary["total_records"] += result["processed"]
            summary["list_fields_found"].update(result.get("list_fields", []))
            summary["root_cause_enhancements"] += result.get("root_cause_enhanced", 0)

            # Aggregate field analysis
            for field_name, stats in result.get("field_analysis", {}).items():
                if field_name not in summary["all_field_analysis"]:
                    summary["all_field_analysis"][field_name] = {"list_count": 0, "total_count": 0}
                summary["all_field_analysis"][field_name]["list_count"] += stats["list_count"]
                summary["all_field_analysis"][field_name]["total_count"] += stats["total_count"]

    # Convert set to list for JSON serialization
    summary["list_fields_found"] = list(summary["list_fields_found"])

    logger.info(f"Preprocessing complete: {summary}")
    return summary

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Preprocess mining reliability data: convert lists to strings and enhance root cause intelligence"
    )
    parser.add_argument("--facility", type=str, help="Process specific facility file")
    parser.add_argument("--raw-data-dir", type=str, help="Raw data directory path (default: data/raw_data)")
    parser.add_argument("--output-data-dir", type=str, help="Output data directory path (default: data/facility_data)")
    parser.add_argument("--log-level", type=str, help="Logging level")

    args = parser.parse_args()

    # Standardized project initialization
    global logger
    logger = setup_project_environment("preprocess_data", args.log_level)

    try:
        # Set up directories
        if args.raw_data_dir:
            raw_data_dir = args.raw_data_dir
        else:
            project_root = Path(__file__).resolve().parent.parent
            raw_data_dir = str(project_root / "data" / "raw_data")

        if args.output_data_dir:
            output_data_dir = args.output_data_dir
        else:
            project_root = Path(__file__).resolve().parent.parent
            output_data_dir = str(project_root / "data" / "facility_data")

        if args.facility:
            # Process specific facility
            input_file = Path(raw_data_dir) / f"{args.facility}.json"
            output_file = Path(output_data_dir) / f"{args.facility}.json"

            if not input_file.exists():
                logger.error(f"Facility file not found: {input_file}")
                return 1

            # Create output directory
            output_file.parent.mkdir(parents=True, exist_ok=True)

            result = preprocess_facility_data(input_file, output_file)

            if result.get("processed", 0) > 0:
                print(f"Successfully preprocessed {args.facility}")
                print(f"Records processed: {result['processed']}")
                print(f"List fields converted: {result['list_fields']}")
                print(f"Root cause intelligence enhanced: {result.get('root_cause_enhanced', 0)} records")
                return 0
            else:
                print(f"Preprocessing failed for {args.facility}")
                return 1
        else:
            # Process all facilities
            summary = preprocess_all_facilities(raw_data_dir, output_data_dir)

            print("Preprocessing Summary:")
            print(f"Files processed: {summary['processed_files']}")
            print(f"Total records: {summary['total_records']}")
            print(f"List fields found: {summary['list_fields_found']}")
            print(f"Root cause enhancements: {summary['root_cause_enhancements']}")

            # Print field analysis summary
            if summary.get("all_field_analysis"):
                print("\nField Analysis Summary:")
                for field_name, stats in summary["all_field_analysis"].items():
                    if stats["list_count"] > 0:
                        print(f"  {field_name}: {stats['list_count']}/{stats['total_count']} were lists")

            return 0 if summary["processed_files"] > 0 else 1

    except Exception as e:
        handle_error(logger, e, "data preprocessing")
        print(f"Preprocessing failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
