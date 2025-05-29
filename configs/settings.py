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

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class Settings:
    """Configuration settings manager"""

    def __init__(self, config_file: Optional[str] = None):
        """Initialize settings from environment and config file"""
        self._settings = {}

        # Load default settings
        self._load_defaults()

        # Override with config file if provided
        if config_file:
            self._load_from_file(config_file)

        # Override with environment variables
        self._load_from_env()

        logger.info("Settings initialized")

    def _load_defaults(self):
        """Load default settings"""
        self._settings = {
            "database": {
                "uri": "bolt://localhost:7687",
                "user": "neo4j",
                "password": "password",
                "batch_size": 5000
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": None  # No file logging by default
            },
            "paths": {
                "data_dir": str(Path(__file__).parent.parent / "data" / "facility_data"),
                "schema_file": str(Path(__file__).parent / "model_schema.json")
            }
        }

    def _load_from_file(self, config_file: str):
        """Load settings from config file"""
        path = Path(config_file)
        if not path.exists():
            logger.warning(f"Config file not found: {config_file}")
            return

        try:
            with open(path, 'r') as f:
                file_settings = json.load(f)

            # Merge settings
            self._merge_settings(file_settings)
            logger.info(f"Loaded settings from {config_file}")

        except Exception as e:
            logger.error(f"Error loading config file {config_file}: {e}")

    def _load_from_env(self):
        """Load settings from environment variables"""
        # Database settings
        if "NEO4J_URI" in os.environ:
            self._settings["database"]["uri"] = os.environ["NEO4J_URI"]

        if "NEO4J_USER" in os.environ:
            self._settings["database"]["user"] = os.environ["NEO4J_USER"]

        if "NEO4J_PASSWORD" in os.environ:
            self._settings["database"]["password"] = os.environ["NEO4J_PASSWORD"]

        if "NEO4J_BATCH_SIZE" in os.environ:
            try:
                self._settings["database"]["batch_size"] = int(os.environ["NEO4J_BATCH_SIZE"])
            except ValueError:
                logger.warning(f"Invalid NEO4J_BATCH_SIZE: {os.environ['NEO4J_BATCH_SIZE']}")

        # Logging settings
        if "LOG_LEVEL" in os.environ:
            self._settings["logging"]["level"] = os.environ["LOG_LEVEL"]

        if "LOG_FILE" in os.environ:
            self._settings["logging"]["file"] = os.environ["LOG_FILE"]

        # Path settings
        if "DATA_DIR" in os.environ:
            self._settings["paths"]["data_dir"] = os.environ["DATA_DIR"]

        if "SCHEMA_FILE" in os.environ:
            self._settings["paths"]["schema_file"] = os.environ["SCHEMA_FILE"]

    def _merge_settings(self, new_settings: Dict[str, Any]):
        """Merge new settings into existing settings"""
        for section, values in new_settings.items():
            if section in self._settings:
                if isinstance(self._settings[section], dict) and isinstance(values, dict):
                    # Update existing section
                    self._settings[section].update(values)
                else:
                    # Replace section
                    self._settings[section] = values
            else:
                # Add new section
                self._settings[section] = values

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get setting value"""
        if section in self._settings and key in self._settings[section]:
            return self._settings[section][key]
        return default

    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire section"""
        return self._settings.get(section, {})

    def get_all(self) -> Dict[str, Any]:
        """Get all settings"""
        return self._settings

# Singleton instance
_settings_instance = None

def get_settings(config_file: Optional[str] = None) -> Settings:
    """Get singleton settings instance"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings(config_file)
    return _settings_instance
