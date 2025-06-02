#!/usr/bin/env python3
"""
Data Extractor - Simple direct processing of all JSON files
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FacilityDataExtractor:
    """Extract from all JSON files in directory"""

    def __init__(self, data_dir: Optional[str] = None):
        """Initialize data directory"""
        if data_dir is None:
            current_dir = Path(__file__).resolve().parent
            project_root = current_dir.parent.parent.parent
            data_dir = project_root / "data" / "facility_data"
        else:
            data_dir = Path(data_dir)

        self.data_dir = data_dir
        logger.info(f"Data directory: {self.data_dir}")

    def get_available_facilities(self) -> List[str]:
        """Get ALL JSON files in directory"""
        if not self.data_dir.exists():
            logger.warning(f"Data directory not found: {self.data_dir}")
            return []

        json_files = list(self.data_dir.glob("*.json"))
        facilities = [f.stem for f in json_files]

        logger.info(f"Found {len(facilities)} files: {facilities}")
        return facilities

    def extract_facility_data(self, facility_id: str) -> Dict[str, Any]:
        """Extract data from any JSON file"""
        file_path = self.data_dir / f"{facility_id}.json"

        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return {}

        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            records = self._extract_records(data)
            logger.info(f"Extracted {len(records)} records from {facility_id}")

            return {"facility_id": facility_id, "records": records}

        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return {}

    def _extract_records(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract records from data structure"""
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

        return records


def extract_all_facilities(data_dir: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """Extract data from all available facilities"""
    extractor = FacilityDataExtractor(data_dir)

    facilities = extractor.get_available_facilities()
    result = {}

    for facility_id in facilities:
        facility_data = extractor.extract_facility_data(facility_id)
        if facility_data:
            result[facility_id] = facility_data

    logger.info(f"Successfully extracted data from {len(result)} facilities")
    return result
