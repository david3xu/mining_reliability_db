#!/usr/bin/env python3
"""
Random Record Sampler for Mining Maintenance Records
Loads merged records from facility_data and randomly selects 5 records for sampling.
"""

import argparse
import json
import logging
import random
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class RecordSampler:
    """Random sampler for merged maintenance records."""

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

        logger.info(f"Saved {len(records)} sampled records to {output_file}")

    def sample_records(self, records: List[Dict[str, Any]], sample_size: int = 5) -> List[Dict[str, Any]]:
        """Randomly sample records from the input list."""
        if len(records) <= sample_size:
            logger.warning(f"Dataset has only {len(records)} records, returning all records")
            return records.copy()

        # Set seed for reproducible results (optional)
        # random.seed(42)

        sampled_records = random.sample(records, sample_size)
        logger.info(f"Randomly sampled {len(sampled_records)} records from {len(records)} total records")
        return sampled_records

    def process_facility_file(self, input_file: Path, output_file: Path, sample_size: int = 5) -> Dict[str, Any]:
        """Process a single facility file: load, sample, save."""
        logger.info(f"Processing {input_file.name}")

        try:
            # Load data
            records, structure_info = self.load_json_data(input_file)
            if not records:
                logger.warning(f"No records in {input_file.name}")
                return {
                    "input_file": input_file.name,
                    "input_records": 0,
                    "sampled_records": 0,
                    "status": "empty",
                }

            # Sample records
            sampled_records = self.sample_records(records, sample_size)

            # Save sampled data
            self.save_json_data(sampled_records, structure_info, output_file)

            return {
                "input_file": input_file.name,
                "input_records": len(records),
                "sampled_records": len(sampled_records),
                "status": "success",
            }

        except Exception as e:
            logger.error(f"Processing failed for {input_file.name}: {e}")
            return {
                "input_file": input_file.name,
                "input_records": 0,
                "sampled_records": 0,
                "status": "failed",
                "error": str(e),
            }


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="Random record sampler for merged maintenance records")
    parser.add_argument("--input-dir", default="data/facility_data", help="Input directory (merged records)")
    parser.add_argument("--output-dir", default="data/sample_data", help="Output directory")
    parser.add_argument("--input-file", help="Process single file")
    parser.add_argument("--sample-size", type=int, default=5, help="Number of records to sample (default: 5)")
    parser.add_argument("--seed", type=int, help="Random seed for reproducible sampling")

    args = parser.parse_args()

    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)
        logger.info(f"Random seed set to {args.seed}")

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
    sampler = RecordSampler()
    all_stats = []

    for input_file in input_files:
        # Create output filename with _sample suffix
        output_filename = input_file.stem + "_sample.json"
        output_file = output_dir / output_filename

        stats = sampler.process_facility_file(input_file, output_file, args.sample_size)
        all_stats.append(stats)

        logger.info(
            f"Completed {input_file.name}: {stats['input_records']} → {stats['sampled_records']} records"
        )

    # Print summary
    total_input = sum(s["input_records"] for s in all_stats)
    total_sampled = sum(s["sampled_records"] for s in all_stats)

    logger.info("=" * 50)
    logger.info("SAMPLING SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Files processed: {len(all_stats)}")
    logger.info(f"Total input records: {total_input}")
    logger.info(f"Total sampled records: {total_sampled}")
    logger.info(f"Sample size per file: {args.sample_size}")
    if args.seed is not None:
        logger.info(f"Random seed used: {args.seed}")
    logger.info("=" * 50)

    return 0


if __name__ == "__main__":
    exit(main())
