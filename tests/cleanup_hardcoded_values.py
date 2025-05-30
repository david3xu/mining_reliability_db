#!/usr/bin/env python3
"""
Cleanup script to remove hardcoded values and setup schema-driven architecture
"""

import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    """Main cleanup function"""

    # Get project root
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    logger.info("Starting cleanup of hardcoded values...")
    logger.info(f"Project root: {project_root}")

    # Files to remove
    files_to_remove = [
        project_root / "data" / "facility_data" / "sample.json",
        project_root / "configs" / "settings.py"
    ]

    # Remove files
    for file_path in files_to_remove:
        if file_path.exists():
            try:
                file_path.unlink()
                logger.info(f"✅ Removed: {file_path}")
            except Exception as e:
                logger.error(f"❌ Failed to remove {file_path}: {e}")
        else:
            logger.info(f"⚠️  File not found (already removed?): {file_path}")

    # Check that required config files exist
    required_config_files = [
        project_root / "configs" / "model_schema.json",
        project_root / "configs" / "field_mappings.json",
        project_root / "configs" / "environment.py"
    ]

    logger.info("\nVerifying required configuration files...")
    all_configs_exist = True

    for config_file in required_config_files:
        if config_file.exists():
            logger.info(f"✅ Found: {config_file}")
        else:
            logger.error(f"❌ Missing: {config_file}")
            all_configs_exist = False

    # Create data directory if it doesn't exist
    data_dir = project_root / "data" / "facility_data"
    if not data_dir.exists():
        try:
            data_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"✅ Created data directory: {data_dir}")
        except Exception as e:
            logger.error(f"❌ Failed to create data directory: {e}")

    # Summary
    logger.info("\n" + "="*50)
    logger.info("CLEANUP SUMMARY")
    logger.info("="*50)

    if all_configs_exist:
        logger.info("✅ All required configuration files present")
        logger.info("✅ Schema-driven architecture ready")
        logger.info("\nNext steps:")
        logger.info("1. Place your real facility JSON files in: data/facility_data/")
        logger.info("2. Run: python scripts/import_data.py")
        return 0
    else:
        logger.error("❌ Missing required configuration files")
        logger.error("Cannot proceed with schema-driven setup")
        return 1

if __name__ == "__main__":
    exit(main())