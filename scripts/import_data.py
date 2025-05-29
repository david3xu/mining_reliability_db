#!/usr/bin/env python3
"""
Data Import Script for Mining Reliability Database
Extracts, transforms, and loads facility data into Neo4j.
"""

import os
import argparse
import logging
from typing import List, Optional

from mine_core.database.connection import get_connection
from mine_core.pipelines.extractor import FacilityDataExtractor
from mine_core.pipelines.transformer import DataTransformer
from mine_core.pipelines.loader import Neo4jLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def import_facility(facility_id: str, data_dir: Optional[str] = None) -> bool:
    """Import data for a specific facility"""
    try:
        # Extract data
        extractor = FacilityDataExtractor(data_dir)
        facility_data = extractor.extract_facility_data(facility_id)

        if not facility_data or not facility_data.get("records"):
            logger.error(f"No data found for facility {facility_id}")
            return False

        # Transform data
        transformer = DataTransformer()
        transformed_data = transformer.transform_facility_data(facility_data)

        # Load data
        loader = Neo4jLoader()
        result = loader.load_data(transformed_data)

        if result:
            logger.info(f"Successfully imported data for facility {facility_id}")
        else:
            logger.error(f"Failed to import data for facility {facility_id}")

        return result

    except Exception as e:
        logger.error(f"Error importing facility {facility_id}: {e}")
        return False

def import_all_facilities(data_dir: Optional[str] = None) -> bool:
    """Import data for all available facilities"""
    extractor = FacilityDataExtractor(data_dir)
    facilities = extractor.get_available_facilities()

    if not facilities:
        logger.error("No facility data found")
        return False

    success = True
    for facility_id in facilities:
        result = import_facility(facility_id, data_dir)
        if not result:
            success = False

    return success

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Import facility data into Mining Reliability Database"
    )
    parser.add_argument("--facility", type=str, default=None,
                        help="Facility ID to import (default: all facilities)")
    parser.add_argument("--data-dir", type=str, default=None,
                        help="Data directory (default: data/facility_data)")
    parser.add_argument("--uri", type=str, default=None,
                        help="Neo4j URI (default: environment variable or bolt://localhost:7687)")
    parser.add_argument("--user", type=str, default=None,
                        help="Neo4j username (default: environment variable or neo4j)")
    parser.add_argument("--password", type=str, default=None,
                        help="Neo4j password (default: environment variable or password)")

    args = parser.parse_args()

    try:
        # Setup connection (for queries.py)
        get_connection(args.uri, args.user, args.password)

        # Import data
        if args.facility:
            success = import_facility(args.facility, args.data_dir)
        else:
            success = import_all_facilities(args.data_dir)

        if success:
            print("Data import successful!")
            return 0
        else:
            print("Data import failed for some facilities")
            return 1

    except Exception as e:
        logger.error(f"Error importing data: {e}")
        print(f"Data import failed: {e}")
        return 1

    finally:
        # Close connection
        connection = get_connection()
        connection.close()

if __name__ == "__main__":
    exit(main())
