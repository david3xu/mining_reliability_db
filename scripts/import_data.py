#!/usr/bin/env python3
"""
Data Import Script for Mining Reliability Database
Extracts, transforms, and loads facility data into Neo4j.
"""

import sys
import os
import logging
import argparse

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from mine_core.pipelines.extractor import FacilityDataExtractor
from mine_core.pipelines.transformer import DataTransformer
from mine_core.pipelines.loader import Neo4jLoader
from mine_core.database.db import get_database
from configs.environment import get_data_dir

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def import_facility(facility_id, data_dir=None, db_config=None):
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
        uri, user, password = db_config if db_config else (None, None, None)
        loader = Neo4jLoader(uri, user, password)
        result = loader.load_data(transformed_data)

        if result:
            logger.info(f"Successfully imported data for facility {facility_id}")
        else:
            logger.error(f"Failed to import data for facility {facility_id}")

        return result

    except Exception as e:
        logger.error(f"Error importing facility {facility_id}: {e}")
        return False

def import_all_facilities(data_dir=None, db_config=None):
    """Import data for all available facilities"""
    extractor = FacilityDataExtractor(data_dir)
    facilities = extractor.get_available_facilities()

    if not facilities:
        logger.error("No facility data found")
        return False

    success = True
    for facility_id in facilities:
        result = import_facility(facility_id, data_dir, db_config)
        if not result:
            success = False

    return success

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Import facility data into Mining Reliability Database"
    )
    parser.add_argument("--facility", type=str, help="Facility ID to import (default: all)")
    parser.add_argument("--data-dir", type=str, help="Data directory path")
    parser.add_argument("--uri", type=str, help="Neo4j URI")
    parser.add_argument("--user", type=str, help="Neo4j username")
    parser.add_argument("--password", type=str, help="Neo4j password")

    args = parser.parse_args()

    try:
        # Setup database connection for queries
        get_database(args.uri, args.user, args.password)

        # Prepare configuration
        data_dir = args.data_dir or get_data_dir()
        db_config = (args.uri, args.user, args.password) if any([args.uri, args.user, args.password]) else None

        # Import data
        if args.facility:
            success = import_facility(args.facility, data_dir, db_config)
        else:
            success = import_all_facilities(data_dir, db_config)

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
        try:
            db = get_database()
            db.close()
        except:
            pass

if __name__ == "__main__":
    exit(main())
