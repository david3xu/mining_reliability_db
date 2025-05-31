#!/usr/bin/env python3
"""
Data Import Script for Mining Reliability Database
Standardized configuration access and unified initialization pattern.
"""

import argparse
from mine_core.shared.common import setup_project_environment, handle_error
from mine_core.pipelines.extractor import FacilityDataExtractor
from mine_core.pipelines.transformer import DataTransformer
from mine_core.pipelines.loader import Neo4jLoader
from mine_core.database.db import get_database, close_database
from configs.environment import get_data_dir

def import_facility(facility_id, data_dir=None, db_config=None):
    """Import data for a specific facility"""
    try:
        logger.info(f"Starting import for facility: {facility_id}")

        # Extract data using unified configuration
        extractor = FacilityDataExtractor(data_dir)
        facility_data = extractor.extract_facility_data(facility_id)

        if not facility_data or not facility_data.get("records"):
            logger.error(f"No data found for facility {facility_id}")
            return False

        logger.info(f"Extracted {len(facility_data.get('records', []))} records for {facility_id}")

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
        handle_error(logger, e, f"importing facility {facility_id}")
        return False

def import_all_facilities(data_dir=None, db_config=None):
    """Import data for all available facilities"""
    logger.info("Starting import for all facilities")

    extractor = FacilityDataExtractor(data_dir)
    facilities = extractor.get_available_facilities()

    if not facilities:
        logger.error("No facility data found")
        return False

    logger.info(f"Found {len(facilities)} facilities to import: {facilities}")

    success_count = 0
    for facility_id in facilities:
        if import_facility(facility_id, data_dir, db_config):
            success_count += 1

    logger.info(f"Import completed: {success_count}/{len(facilities)} facilities successful")
    return success_count == len(facilities)

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
    parser.add_argument("--log-level", type=str, help="Logging level")

    args = parser.parse_args()

    # Standardized project initialization
    global logger
    logger = setup_project_environment("import_data", args.log_level)

    try:
        # Setup database connection for validation using unified configuration
        get_database(args.uri, args.user, args.password)

        # Use unified configuration gateway for data directory
        data_dir = args.data_dir or get_data_dir()
        db_config = (args.uri, args.user, args.password) if any([args.uri, args.user, args.password]) else None

        logger.info(f"Using data directory: {data_dir}")

        # Import data
        if args.facility:
            success = import_facility(args.facility, data_dir, db_config)
        else:
            success = import_all_facilities(data_dir, db_config)

        if success:
            print("Data import successful!")
            logger.info("Data import completed successfully")
            return 0
        else:
            print("Data import failed for some facilities")
            logger.error("Data import failed")
            return 1

    except Exception as e:
        handle_error(logger, e, "data import")
        print(f"Data import failed: {e}")
        return 1

    finally:
        close_database()

if __name__ == "__main__":
    exit(main())
