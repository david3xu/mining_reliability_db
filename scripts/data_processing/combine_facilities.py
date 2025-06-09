#!/usr/bin/env python3
"""
Combine Facility Records Script
Merges all facility outputs from merge_records.py into single dataset.
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class FacilityCombiner:
    """Combines processed facility records into unified dataset."""

    def load_facility_records(self, facility_file: Path) -> List[Dict[str, Any]]:
        """Load records from a single facility file."""
        try:
            with open(facility_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            records = []
            facility_name = facility_file.stem

            # Handle different JSON structures
            if isinstance(data, list):
                records = data
            elif isinstance(data, dict):
                if "records" in data:
                    records = data["records"]
                elif "sheets" in data and isinstance(data["sheets"], dict):
                    # Multi-sheet structure - take first sheet
                    sheet_name = next(iter(data["sheets"]))
                    sheet_data = data["sheets"][sheet_name]
                    if isinstance(sheet_data, dict) and "records" in sheet_data:
                        records = sheet_data["records"]
                    elif isinstance(sheet_data, list):
                        records = sheet_data
                else:
                    # Single record as dict
                    records = [data]

            # Ensure facility name is set
            for record in records:
                if isinstance(record, dict) and "_facility_name" not in record:
                    record["_facility_name"] = facility_name

            logger.info(f"Loaded {len(records)} records from {facility_name}")
            return records

        except Exception as e:
            logger.error(f"Failed to load {facility_file.name}: {e}")
            return []

    def combine_all_facilities(self, input_dir: Path, output_file: Path) -> Dict[str, Any]:
        """Combine all facility files into single dataset."""

        # Find all JSON files
        facility_files = list(input_dir.glob("*.json"))
        if not facility_files:
            logger.error(f"No JSON files found in {input_dir}")
            return {"status": "no_files", "combined_records": 0}

        logger.info(f"Found {len(facility_files)} facility files")

        # Combine all records
        all_records = []
        facility_stats = []

        for facility_file in sorted(facility_files):
            records = self.load_facility_records(facility_file)
            if records:
                all_records.extend(records)
                facility_stats.append({
                    "facility": facility_file.stem,
                    "records": len(records)
                })

        if not all_records:
            logger.error("No records found across all facilities")
            return {"status": "no_records", "combined_records": 0}

        # Create output structure
        combined_data = {
            "records": all_records,
            "metadata": {
                "total_facilities": len(facility_stats),
                "total_records": len(all_records),
                "facility_breakdown": facility_stats,
                "combined_timestamp": "2025-06-09T00:00:00"
            }
        }

        # Save combined dataset
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(combined_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Combined {len(all_records)} records from {len(facility_stats)} facilities")
        logger.info(f"Output saved to {output_file}")

        return {
            "status": "success",
            "combined_records": len(all_records),
            "facilities_processed": len(facility_stats),
            "facility_breakdown": facility_stats
        }


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Combine facility records into unified dataset")
    parser.add_argument("--input-dir", default="data/facility_data", help="Input directory with facility files")
    parser.add_argument("--output-file", default="data/combined/all_facilities.json", help="Output combined file")

    args = parser.parse_args()

    # Setup paths
    project_root = Path(__file__).parent.parent.parent
    input_dir = project_root / args.input_dir
    output_file = project_root / args.output_file

    # Combine facilities
    combiner = FacilityCombiner()
    result = combiner.combine_all_facilities(input_dir, output_file)

    # Print summary
    if result["status"] == "success":
        print("Combination Summary:")
        print(f"Facilities processed: {result['facilities_processed']}")
        print(f"Total records combined: {result['combined_records']}")
        print("\nFacility breakdown:")
        for facility_info in result["facility_breakdown"]:
            print(f"  {facility_info['facility']}: {facility_info['records']} records")
        return 0
    else:
        print(f"Combination failed: {result['status']}")
        return 1


if __name__ == "__main__":
    exit(main())