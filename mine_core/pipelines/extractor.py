#!/usr/bin/env python3
"""
Data Extractor for Mining Reliability Database
Extracts data from JSON facility files.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class FacilityDataExtractor:
    """Extracts data from facility JSON files"""

    def __init__(self, data_dir: Optional[str] = None):
        """Initialize with data directory path"""
        # Find the data directory
        if data_dir is None:
            # Try to find it relative to the current file
            current_dir = Path(__file__).resolve().parent
            project_root = current_dir.parent.parent.parent
            data_dir = project_root / "data" / "facility_data"
        else:
            data_dir = Path(data_dir)

        self.data_dir = data_dir
        logger.info(f"Data directory set to: {self.data_dir}")

    def get_available_facilities(self) -> List[str]:
        """Get list of available facility data files"""
        if not self.data_dir.exists():
            logger.warning(f"Data directory not found: {self.data_dir}")
            return []

        # Find all JSON files in the data directory
        json_files = list(self.data_dir.glob("*.json"))

        # Extract facility IDs from filenames
        facilities = [f.stem for f in json_files]

        logger.info(f"Found {len(facilities)} facility data files")
        return facilities

    def extract_facility_data(self, facility_id: str) -> Dict[str, Any]:
        """Extract data for a specific facility"""
        file_path = self.data_dir / f"{facility_id}.json"

        if not file_path.exists():
            logger.error(f"Facility data file not found: {file_path}")
            return {}

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Extract records from the nested structure
            records = self._extract_records(data)

            logger.info(f"Extracted {len(records)} records from {facility_id}")
            return {
                "facility_id": facility_id,
                "records": records
            }

        except Exception as e:
            logger.error(f"Error extracting data from {file_path}: {e}")
            return {}

    def _extract_records(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract records from nested data structure"""
        records = []

        # Handle nested structure (sheets.{sheet_name}.records)
        if isinstance(data, dict):
            if "sheets" in data:
                for sheet_name, sheet_data in data["sheets"].items():
                    if isinstance(sheet_data, dict) and "records" in sheet_data:
                        records.extend(sheet_data["records"])
            elif "records" in data:
                records.extend(data["records"])
            else:
                # If it's a dict but not nested, treat it as a single record
                records.append(data)
        elif isinstance(data, list):
            records.extend(data)

        return records

# Convenience function
def extract_all_facilities(data_dir: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """Extract data from all available facilities"""
    extractor = FacilityDataExtractor(data_dir)

    facilities = extractor.get_available_facilities()
    result = {}

    for facility_id in facilities:
        facility_data = extractor.extract_facility_data(facility_id)
        if facility_data:
            result[facility_id] = facility_data

    return result
