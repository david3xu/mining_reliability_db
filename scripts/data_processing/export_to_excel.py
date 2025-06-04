#!/usr/bin/env python3
"""
Export Merged Mining Maintenance Records to Excel
Reads merged JSON data and exports it to Excel format (.xlsx)
Each record becomes one row in the Excel sheet
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ExcelExporter:
    """Exports JSON records to Excel format."""

    def load_json_data(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load JSON data and extract records."""
        logger.info(f"Loading data from {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        records = []

        if isinstance(data, list):
            # Direct array of records
            records = data
        elif isinstance(data, dict):
            if "records" in data:
                # {'records': [...]} structure
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
                    logger.error(f"Unrecognized sheet structure in {file_path}")
                    return []
            else:
                logger.error(f"Unrecognized JSON structure in {file_path}")
                return []
        else:
            logger.error(f"Invalid JSON data type in {file_path}: {type(data)}")
            return []

        logger.info(f"Loaded {len(records)} records from {file_path}")
        return records

    def export_to_excel(self, records: List[Dict[str, Any]], output_file: Path) -> bool:
        """Export records to Excel file."""
        try:
            # Convert to pandas DataFrame
            df = pd.DataFrame(records)

            # Create output directory if it doesn't exist
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # Export to Excel
            with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Mining Records', index=False)

                # Auto-adjust column widths
                worksheet = writer.sheets['Mining Records']
                for i, col in enumerate(df.columns):
                    # Find the maximum length in the column
                    max_len = max(
                        df[col].astype(str).apply(len).max(),  # max length of values
                        len(str(col))  # length of column name
                    ) + 2  # add a little extra space

                    # Set column width (limited to reasonable size)
                    worksheet.set_column(i, i, min(max_len, 50))

            logger.info(f"Successfully exported {len(records)} records to {output_file}")
            return True

        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}")
            return False

    def process_file(self, input_file: Path, output_file: Path) -> Dict[str, Any]:
        """Process a single JSON file to Excel."""
        logger.info(f"Processing {input_file.name}")

        # Load data
        records = self.load_json_data(input_file)
        if not records:
            return {
                "input_file": input_file.name,
                "records": 0,
                "status": "no_records"
            }

        # Export to Excel
        success = self.export_to_excel(records, output_file)

        return {
            "input_file": input_file.name,
            "records": len(records),
            "status": "success" if success else "failed"
        }


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="Export merged JSON records to Excel")
    parser.add_argument("--input-dir", default="data/facility_data", help="Input directory with JSON files")
    parser.add_argument("--output-dir", default="data/excel_output", help="Output directory for Excel files")
    parser.add_argument("--input-file", help="Process single file")
    parser.add_argument("--output-file", help="Output Excel filename (when processing a single file)")

    args = parser.parse_args()

    # Setup paths
    project_root = Path(__file__).parent.parent.parent
    input_dir = project_root / args.input_dir
    output_dir = project_root / args.output_dir

    # Find input files
    if args.input_file:
        input_files = [project_root / args.input_file]

        # Set default output filename if not provided
        if args.output_file:
            output_files = [project_root / args.output_file]
        else:
            input_path = Path(args.input_file)
            output_files = [output_dir / f"{input_path.stem}.xlsx"]
    else:
        input_files = list(input_dir.glob("*.json"))
        # Generate output filenames
        output_files = [output_dir / f"{input_file.stem}.xlsx" for input_file in input_files]

    if not input_files:
        logger.error(f"No JSON files found in {input_dir}")
        return 1

    logger.info(f"Found {len(input_files)} files to process")

    # Process files
    exporter = ExcelExporter()
    all_stats = []

    for input_file, output_file in zip(input_files, output_files):
        stats = exporter.process_file(input_file, output_file)
        all_stats.append(stats)

        logger.info(f"Completed {input_file.name} → {output_file.name}: {stats['records']} records")

    # Print summary
    total_records = sum(s["records"] for s in all_stats)
    success_count = sum(1 for s in all_stats if s["status"] == "success")

    logger.info("=" * 50)
    logger.info("PROCESSING SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Files processed: {len(all_stats)}")
    logger.info(f"Files succeeded: {success_count}")
    logger.info(f"Files failed: {len(all_stats) - success_count}")
    logger.info(f"Total records exported: {total_records}")
    logger.info("=" * 50)

    return 0


if __name__ == "__main__":
    exit(main())
