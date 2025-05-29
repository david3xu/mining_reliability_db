#!/usr/bin/env python3
"""
Configuration Settings Manager
Loads and provides access to application settings.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def load_configuration(config_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from environment, files, and defaults

    Priority order:
    1. Environment variables
    2. Configuration file (if provided)
    3. Default values
    """
    # Load defaults
    config = {
        "database": {
            "uri": "bolt://localhost:7687",
            "user": "neo4j",
            "password": "password",
            "batch_size": 5000
        },
        "paths": {
            "data_dir": str(Path(__file__).parent.parent / "data" / "facility_data"),
            "schema_file": str(Path(__file__).parent / "model_schema.json"),
            "mappings_file": str(Path(__file__).parent / "field_mappings.json")
        }
    }

    # Load configuration file if provided
    if config_file:
        config_path = Path(config_file)
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    file_config = json.load(f)

                # Merge configuration
                for section, values in file_config.items():
                    if section in config and isinstance(config[section], dict):
                        config[section].update(values)
                    else:
                        config[section] = values

                logger.info(f"Loaded configuration from {config_file}")
            except Exception as e:
                logger.error(f"Error loading configuration from {config_file}: {e}")

    # Override with environment variables
    if "NEO4J_URI" in os.environ:
        config["database"]["uri"] = os.environ["NEO4J_URI"]

    if "NEO4J_USER" in os.environ:
        config["database"]["user"] = os.environ["NEO4J_USER"]

    if "NEO4J_PASSWORD" in os.environ:
        config["database"]["password"] = os.environ["NEO4J_PASSWORD"]

    if "NEO4J_BATCH_SIZE" in os.environ:
        try:
            config["database"]["batch_size"] = int(os.environ["NEO4J_BATCH_SIZE"])
        except ValueError:
            logger.warning(f"Invalid NEO4J_BATCH_SIZE: {os.environ['NEO4J_BATCH_SIZE']}")

    if "DATA_DIR" in os.environ:
        config["paths"]["data_dir"] = os.environ["DATA_DIR"]

    if "SCHEMA_FILE" in os.environ:
        config["paths"]["schema_file"] = os.environ["SCHEMA_FILE"]

    if "MAPPINGS_FILE" in os.environ:
        config["paths"]["mappings_file"] = os.environ["MAPPINGS_FILE"]

    # Load schema
    schema_path = Path(config["paths"]["schema_file"])
    if schema_path.exists():
        try:
            with open(schema_path, 'r') as f:
                config["schema"] = json.load(f)
            logger.info(f"Loaded schema from {schema_path}")
        except Exception as e:
            logger.error(f"Error loading schema: {e}")

    # Load field mappings
    mappings_path = Path(config["paths"]["mappings_file"])
    if mappings_path.exists():
        try:
            with open(mappings_path, 'r') as f:
                config["mappings"] = json.load(f)
            logger.info(f"Loaded field mappings from {mappings_path}")
        except Exception as e:
            logger.error(f"Error loading field mappings: {e}")

    return config

# Load configuration on module import
CONFIG = load_configuration()

def get_config(section: Optional[str] = None, key: Optional[str] = None, default: Any = None) -> Any:
    """Get configuration value"""
    if section is None:
        return CONFIG

    if section not in CONFIG:
        return default

    if key is None:
        return CONFIG[section]

    return CONFIG[section].get(key, default)

def reload_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """Reload configuration"""
    global CONFIG
    CONFIG = load_configuration(config_file)
    return CONFIG
