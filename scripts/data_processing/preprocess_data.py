#!/usr/bin/env python3
"""
Data Preprocessing Script for Mining Reliability Database
Converts list fields to strings, enhances root cause intelligence, and applies schema-aware type conversion.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from configs.environment import (
    get_data_dir,
    get_field_mappings,
    get_project_root,
    get_root_cause_delimiters,
)
from mine_core.shared.common import handle_error, setup_project_environment
from mine_core.shared.field_utils import extract_root_cause_tail_extraction, has_real_value

# Initialize logger
logger = None


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
        record["Root Cause Tail Extraction"] = extract_root_cause_tail_extraction(root_cause_str)
    else:
        record["Root Cause Tail Extraction"] = "NOT_SPECIFIED"

    return record


def load_schema_definitions() -> Optional[Dict[str, Any]]:
    """Load model schema definitions from config file"""
    try:
        config_dir = Path(__file__).resolve().parent.parent / "configs"
        schema_file = config_dir / "model_schema.json"

        if schema_file.exists():
            with open(schema_file, "r") as f:
                return json.load(f)
        else:
            logger.warning(f"Schema file not found: {schema_file}")
            return None
    except Exception as e:
        logger.warning(f"Failed to load schema definitions: {e}")
        return None


def convert_to_schema_type(value: Any, field_type: str) -> Any:
    """Convert value to the specified schema type"""
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return None

    try:
        if field_type == "string":
            return str(value).strip() if value else None
        elif field_type == "text":
            return str(value).strip() if value else None
        elif field_type == "integer":
            if isinstance(value, str):
                # Handle common integer-like strings
                value = value.strip()
                if value.lower() in ["", "null", "none", "n/a"]:
                    return None
                # Remove any non-numeric characters except negative sign
                cleaned = "".join(c for c in value if c.isdigit() or c == "-")
                return int(cleaned) if cleaned and cleaned != "-" else None
            return int(value) if value is not None else None
        elif field_type == "boolean":
            if isinstance(value, str):
                value = value.strip().lower()
                if value in ["true", "yes", "1", "y", "t"]:
                    return True
                elif value in ["false", "no", "0", "n", "f"]:
                    return False
                else:
                    return None
            return bool(value) if value is not None else None
        elif field_type == "date":
            if isinstance(value, str):
                value = value.strip()
                if value.lower() in ["", "null", "none", "n/a"]:
                    return None
                # Try to parse common date formats including ISO format
                for fmt in [
                    "%Y-%m-%d",
                    "%Y-%m-%dT%H:%M:%S",
                    "%d/%m/%Y",
                    "%m/%d/%Y",
                    "%Y-%m-%d %H:%M:%S",
                ]:
                    try:
                        parsed_date = datetime.strptime(value, fmt)
                        return parsed_date.strftime("%Y-%m-%d")
                    except ValueError:
                        continue
                return value  # Return as-is if can't parse
            return str(value) if value is not None else None
        else:
            # Unknown type, return as string
            return str(value) if value is not None else None
    except (ValueError, TypeError) as e:
        logger.debug(f"Type conversion failed for value '{value}' to type '{field_type}': {e}")
        return str(value) if value is not None else None


def apply_schema_type_conversion(
    record: Dict[str, Any], field_mappings: Dict[str, Any], schema_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Apply schema-aware type conversion to a record using configuration files"""
    if not field_mappings or not schema_data:
        return record

    converted_record = record.copy()
    entity_mappings = field_mappings.get("entity_mappings", {})
    entities = {entity["name"]: entity for entity in schema_data.get("entities", [])}

    conversion_stats = {"converted": 0, "skipped": 0, "errors": 0}

    # Process each entity type
    for entity_name, entity_fields in entity_mappings.items():
        if entity_name not in entities:
            continue

        entity_schema = entities[entity_name]
        entity_properties = entity_schema.get("properties", {})

        # Convert fields for this entity
        for schema_field, data_field in entity_fields.items():
            if data_field in converted_record and schema_field in entity_properties:
                field_def = entity_properties[schema_field]
                field_type = field_def.get("type", "string")

                try:
                    original_value = converted_record[data_field]
                    converted_value = convert_to_schema_type(original_value, field_type)

                    if converted_value != original_value:
                        converted_record[data_field] = converted_value
                        conversion_stats["converted"] += 1
                        logger.debug(
                            f"Converted field '{data_field}' from '{original_value}' to '{converted_value}' (type: {field_type})"
                        )
                    else:
                        conversion_stats["skipped"] += 1

                except Exception as e:
                    logger.warning(f"Failed to convert field '{data_field}': {e}")
                    conversion_stats["errors"] += 1

    if conversion_stats["converted"] > 0:
        logger.debug(f"Schema conversion stats: {conversion_stats}")

    return converted_record


def analyze_all_field_types(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """Comprehensive analysis of ALL field types across records"""
    field_analysis = {}

    for record in records:
        for field_name, value in record.items():
            if field_name not in field_analysis:
                field_analysis[field_name] = {
                    "list_count": 0,
                    "string_count": 0,
                    "total_count": 0,
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


def preprocess_record(
    record: Dict[str, Any],
    list_fields: List[str],
    field_mappings: Dict[str, Any] = None,
    schema_data: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Preprocess single record: convert lists, enhance intelligence, and apply schema type conversion"""
    processed_record = record.copy()

    # Remove 'Column 42' field if it exists
    if "Column 42" in processed_record:
        del processed_record["Column 42"]
        logger.debug("Removed 'Column 42' field from record")

    # Convert identified list fields to strings
    for field_name in list_fields:
        if field_name in processed_record:
            processed_record[field_name] = convert_list_to_string(processed_record[field_name])

    # Enhance root cause intelligence
    processed_record = enhance_root_cause_intelligence(processed_record)

    # Apply schema-aware type conversion if configuration data provided
    if field_mappings and schema_data:
        try:
            processed_record = apply_schema_type_conversion(
                processed_record, field_mappings, schema_data
            )
            logger.debug("Applied schema-aware type conversion")
        except Exception as e:
            logger.warning(
                f"Schema type conversion failed: {e}, proceeding without type conversion"
            )

    return processed_record


def preprocess_facility_data(
    input_file: Path, output_file: Path, enable_schema_conversion: bool = True
) -> Dict[str, Any]:
    """Preprocess facility data file with comprehensive field analysis and schema-aware type conversion"""
    logger.info(f"Preprocessing {input_file}")

    try:
        # Load configuration files for schema-aware type conversion
        field_mappings = None
        schema_data = None

        if enable_schema_conversion:
            try:
                field_mappings = get_field_mappings()
                schema_data = load_schema_definitions()

                if field_mappings and schema_data:
                    logger.info("Schema type conversion initialized successfully")
                else:
                    logger.warning(
                        "Failed to load configuration files, proceeding without type conversion"
                    )
                    enable_schema_conversion = False
            except Exception as e:
                logger.warning(
                    f"Failed to initialize schema conversion: {e}, proceeding without type conversion"
                )
                enable_schema_conversion = False

        # Load raw data
        with open(input_file, "r") as f:
            data = json.load(f)

        # Extract records from data structure
        records = []
        if isinstance(data, dict):
            if "sheets" in data:
                # Ensure 'sheets' is a dictionary before iterating over it
                if isinstance(data["sheets"], dict):
                    for sheet_name, sheet_data in data["sheets"].items():
                        if isinstance(sheet_data, dict) and "records" in sheet_data:
                            records.extend(sheet_data["records"])
                else:
                    logger.warning(
                        f"Skipping sheets in {input_file.name}: Expected 'sheets' to be a dictionary, got {type(data.get('sheets', 'N/A'))}"
                    )
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
        if enable_schema_conversion:
            logger.info("Schema-aware type conversion enabled")

        # Log field analysis summary
        for field_name, stats in field_analysis.items():
            if stats["list_count"] > 0:
                logger.info(
                    f"Field '{field_name}': {stats['list_count']}/{stats['total_count']} are lists"
                )

        # Preprocess all records
        processed_records = []
        conversion_stats = {"converted_records": 0, "conversion_errors": 0, "column_42_removed": 0}

        for record in records:
            try:
                # Check if 'Column 42' exists before preprocessing
                had_column_42 = "Column 42" in record

                processed_record = preprocess_record(
                    record,
                    list_fields,
                    field_mappings if enable_schema_conversion else None,
                    schema_data if enable_schema_conversion else None,
                )
                processed_records.append(processed_record)
                conversion_stats["converted_records"] += 1

                # Count removals
                if had_column_42:
                    conversion_stats["column_42_removed"] += 1

            except Exception as e:
                logger.error(f"Failed to preprocess record: {e}")
                # Add original record to maintain data integrity
                processed_records.append(record)
                conversion_stats["conversion_errors"] += 1

        # Create output directory if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Reconstruct data structure
        if isinstance(data, dict) and "sheets" in data:
            # Multi-sheet structure
            processed_data = {"sheets": {}}
            for sheet_name, sheet_data in data["sheets"].items():
                processed_data["sheets"][sheet_name] = {"records": processed_records}
        elif isinstance(data, dict) and "records" in data:
            # Single records structure
            processed_data = {"records": processed_records}
        else:
            # Direct list
            processed_data = processed_records

        # Save processed data
        with open(output_file, "w") as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Preprocessed {len(processed_records)} records")
        logger.info(
            f"Schema type conversion: {conversion_stats['converted_records']} successful, {conversion_stats['conversion_errors']} errors"
        )
        if conversion_stats["column_42_removed"] > 0:
            logger.info(f"Removed 'Column 42' field from {conversion_stats['column_42_removed']} records")
        else:
            logger.info("No 'Column 42' fields found to remove")
        logger.info(f"Output saved to {output_file}")

        return {
            "processed": len(processed_records),
            "field_analysis": field_analysis,
            "list_fields": list_fields,
            "schema_conversion_enabled": enable_schema_conversion,
            "conversion_stats": conversion_stats,
            "column_42_removed": conversion_stats["column_42_removed"],
            "root_cause_enhanced": sum(
                1 for r in processed_records if has_real_value(r.get("Root Cause Tail Extraction"))
            ),
        }

    except Exception as e:
        handle_error(logger, e, f"preprocessing {input_file}")
        return {"processed": 0, "field_analysis": {}, "error": str(e)}


def preprocess_all_facilities(
    raw_data_dir: str = None,
    output_data_dir: str = None,
    enable_schema_conversion: bool = True,
) -> Dict[str, Any]:
    """Preprocess all facility data files, handling directory path resolution and error reporting"""
    project_root = (
        Path(__file__).resolve().parents[2]
    )  # Go up two levels from script to project root

    # Resolve data directories
    actual_raw_data_dir = Path(raw_data_dir) if raw_data_dir else (project_root / "data/raw_data")
    actual_output_data_dir = (
        Path(output_data_dir) if output_data_dir else (project_root / "data/facility_data")
    )

    # Initialize summary with all expected keys, including defaults for potential errors
    summary = {
        "files_processed": 0,
        "total_records": 0,
        "schema_conversion_enabled": enable_schema_conversion,
        "facilities_data": [],
        "error": None,
        "all_field_analysis": {},
        "list_fields_found": [],
        "root_cause_enhancements": 0,
        "total_column_42_removed": 0,
    }

    # Validate raw data directory
    if not actual_raw_data_dir.is_dir():
        error_message = f"Raw data directory not found: {actual_raw_data_dir}"
        logger.error(error_message)
        summary["error"] = error_message
        return summary  # Return initialized summary on early exit

    # Create output directory if it doesn't exist
    actual_output_data_dir.mkdir(parents=True, exist_ok=True)

    # Find all JSON files in the raw data directory
    json_files = list(actual_raw_data_dir.glob("*.json"))
    if not json_files:
        summary["error"] = f"No JSON files found in raw data directory: {actual_raw_data_dir}"
        logger.warning(summary["error"])
        return summary  # Return initialized summary on early exit

    logger.info(f"Found {len(json_files)} raw files to preprocess")
    logger.info(f"Schema type conversion: {'enabled' if enable_schema_conversion else 'disabled'}")

    all_records = []
    for input_file in json_files:
        try:
            with open(input_file, "r") as f:
                file_content = json.load(f)
                if isinstance(file_content, dict):
                    # If it's a dictionary, assume it's a single record or has a 'records' key
                    if "records" in file_content and isinstance(file_content["records"], list):
                        all_records.extend(file_content["records"])
                    elif "sheets" in file_content:
                        # Handle multi-sheet structure similar to preprocess_facility_data
                        # Ensure 'sheets' is a dictionary before iterating over it
                        if isinstance(file_content["sheets"], dict):
                            for sheet_name, sheet_data in file_content["sheets"].items():
                                if isinstance(sheet_data, dict) and "records" in sheet_data:
                                    all_records.extend(sheet_data["records"])
                                else:
                                    logger.warning(
                                        f"Skipping sheet '{sheet_name}' in {input_file.name}: Expected dict with 'records' key, got {type(sheet_data)}"
                                    )
                        else:
                            logger.warning(
                                f"Skipping sheets in {input_file.name}: Expected 'sheets' to be a dictionary, got {type(file_content['sheets'])}"
                            )
                    else:
                        # Assume it's a single record dictionary
                        all_records.append(file_content)
                elif isinstance(file_content, list):
                    # If it's a list, assume it's a list of records
                    all_records.extend(file_content)
                else:
                    logger.warning(
                        f"Skipping {input_file.name}: Expected JSON object or array, got {type(file_content)}"
                    )
        except Exception as e:
            logger.warning(f"Could not load records from {input_file.name}: {e}")
            # Do not return, try to process other files, but log the error
            if not summary["error"]:
                summary[
                    "error"
                ] = f"Error loading records from {input_file.name}: {e}"  # Store first loading error

    if not all_records:
        summary["error"] = "No valid records found across all raw data files."
        logger.error(summary["error"])
        return summary  # Return initialized summary on early exit

    # Perform comprehensive field analysis on all records
    total_field_analysis = analyze_all_field_types(all_records)
    list_fields_to_convert = identify_list_fields(total_field_analysis)

    summary["all_field_analysis"] = total_field_analysis
    summary["list_fields_found"] = list_fields_to_convert

    logger.info(f"Identified {len(list_fields_to_convert)} fields for list-to-string conversion")

    # Process each facility file
    for input_file in json_files:
        try:
            # Preprocess facility data
            output_file = (
                actual_output_data_dir / input_file.name
            )  # Same filename in output directory
            result = preprocess_facility_data(input_file, output_file, enable_schema_conversion)

            if result.get("processed", 0) > 0:
                summary["files_processed"] += 1
                summary["total_records"] += result["processed"]
                summary["facilities_data"].append(result)
                summary["root_cause_enhancements"] += result.get("root_cause_enhanced", 0)
                summary["total_column_42_removed"] += result.get("column_42_removed", 0)

        except Exception as e:
            error_message = f"Error processing file {input_file.name}: {e}"
            logger.error(error_message)
            if not summary["error"]:
                summary["error"] = error_message

    logger.info("Data preprocessing complete.")
    if summary["total_column_42_removed"] > 0:
        logger.info(f"Total 'Column 42' fields removed across all files: {summary['total_column_42_removed']}")
    else:
        logger.info("No 'Column 42' fields found in any files")
    return summary


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Preprocess mining reliability data: convert lists to strings, enhance root cause intelligence, and apply schema-aware type conversion"
    )
    parser.add_argument("--facility", type=str, help="Process specific facility file")
    parser.add_argument(
        "--raw-data-dir",
        type=str,
        help="Raw data directory path (default: data/raw_data)",
    )
    parser.add_argument(
        "--output-data-dir",
        type=str,
        help="Output data directory path (default: data/facility_data)",
    )
    parser.add_argument(
        "--no-schema-conversion",
        action="store_true",
        help="Disable schema-aware type conversion",
    )
    parser.add_argument("--log-level", type=str, help="Logging level")

    args = parser.parse_args()

    # Standardized project initialization
    global logger
    logger = setup_project_environment("preprocess_data", args.log_level)

    # Determine schema conversion setting
    enable_schema_conversion = not args.no_schema_conversion

    try:
        # Set up directories, relative to project root using get_project_root
        project_root = get_project_root()

        # Convert paths to absolute strings before passing to preprocess_all_facilities
        raw_data_dir_abs = str(project_root / (args.raw_data_dir or "data/raw_data"))
        output_data_dir_abs = str(project_root / (args.output_data_dir or "data/facility_data"))

        if args.facility:
            # Process specific facility
            input_file = Path(raw_data_dir_abs) / f"{args.facility}.json"
            output_file = Path(output_data_dir_abs) / f"{args.facility}.json"

            if not input_file.exists():
                logger.error(f"Facility file not found: {input_file}")
                return 1

            # Create output directory
            output_file.parent.mkdir(parents=True, exist_ok=True)

            result = preprocess_facility_data(input_file, output_file, enable_schema_conversion)

            if result.get("processed", 0) > 0:
                print(f"Successfully preprocessed {args.facility}")
                print(f"Records processed: {result['processed']}")
                # Ensure 'list_fields' and 'root_cause_enhanced' are always present
                print(f"List fields converted: {result.get('list_fields', [])}")
                print(
                    f"Schema conversion: {'enabled' if result.get('schema_conversion_enabled') else 'disabled'}"
                )
                print(
                    f"Root cause intelligence enhanced: {result.get('root_cause_enhanced', 0)} records"
                )
                return 0
            else:
                print(f"Preprocessing failed for {args.facility}")
                return 1
        else:
            # Process all facilities, passing absolute paths
            summary = preprocess_all_facilities(
                raw_data_dir_abs, output_data_dir_abs, enable_schema_conversion
            )

            # Ensure summary keys exist before printing
            files_processed = summary.get("files_processed", 0)
            total_records = summary.get("total_records", 0)
            schema_conversion_enabled = summary.get("schema_conversion_enabled", False)
            list_fields_found = summary.get("list_fields_found", [])
            root_cause_enhancements = summary.get("root_cause_enhancements", 0)
            all_field_analysis = summary.get("all_field_analysis", {})

            print("Preprocessing Summary:")
            print(f"Files processed: {files_processed}")
            print(f"Total records: {total_records}")
            print(f"Schema conversion: {'enabled' if schema_conversion_enabled else 'disabled'}")
            print(f"List fields found: {list_fields_found}")
            print(f"Root cause enhancements: {root_cause_enhancements}")
            if summary["error"]:
                print(f"Error: {summary['error']}")

            # Print field analysis summary
            if all_field_analysis:
                print("\nField Analysis Summary:")
                for field_name, stats in all_field_analysis.items():
                    if stats["list_count"] > 0:
                        print(
                            f"  {field_name}: {stats['list_count']}/{stats['total_count']} were lists"
                        )

            return 0 if files_processed > 0 else 1

    except Exception as e:
        handle_error(logger, e, "data preprocessing")
        print(f"Preprocessing failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
