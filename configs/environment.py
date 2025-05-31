#!/usr/bin/env python3
"""
Optimized Configuration Gateway - Clean State Management
Single source for all system configuration with optimized caching strategy.
"""

import os
import json
import threading
from pathlib import Path
from typing import Dict, Any, Optional, List
from mine_core.shared.constants import (
    DEFAULT_NEO4J_URI, DEFAULT_NEO4J_USER, DEFAULT_NEO4J_PASSWORD,
    DEFAULT_LOG_LEVEL, DEFAULT_DATA_DIR, DEFAULT_BATCH_SIZE, CONNECTION_TIMEOUT, MAX_RETRIES
)

# Load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class ConfigurationManager:
    """Thread-safe configuration manager with optimized caching"""

    def __init__(self):
        self._schema_cache: Optional[Dict[str, Any]] = None
        self._mappings_cache: Optional[Dict[str, Any]] = None
        self._lock = threading.Lock()

    def get_schema(self) -> Dict[str, Any]:
        """Load schema configuration with thread-safe caching"""
        if self._schema_cache is None:
            with self._lock:
                if self._schema_cache is None:  # Double-check locking
                    self._schema_cache = self._load_json_config("model_schema.json")
        return self._schema_cache

    def get_mappings(self) -> Dict[str, Any]:
        """Load field mappings configuration with thread-safe caching"""
        if self._mappings_cache is None:
            with self._lock:
                if self._mappings_cache is None:  # Double-check locking
                    self._mappings_cache = self._load_json_config("field_mappings.json")
        return self._mappings_cache

    def clear_cache(self):
        """Clear configuration cache (useful for testing)"""
        with self._lock:
            self._schema_cache = None
            self._mappings_cache = None

    def _load_json_config(self, filename: str) -> Dict[str, Any]:
        """Load JSON configuration file with error handling"""
        config_dir = Path(__file__).parent
        config_path = config_dir / filename

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Error loading {filename}: {e}")

# Singleton configuration manager
_config_manager = ConfigurationManager()

def get_env(key: str, default: str = None) -> str:
    """Load environment variable with default - primary access method"""
    return os.environ.get(key, default)

def get_env_required(key: str) -> str:
    """Load required environment variable, raise if missing"""
    value = os.environ.get(key)
    if value is None:
        raise ValueError(f"Required environment variable missing: {key}")
    return value

def validate_required_env(required_vars: List[str]) -> bool:
    """Validate required environment variables exist"""
    missing = [var for var in required_vars if not os.environ.get(var)]
    if missing:
        raise ValueError(f"Missing required environment variables: {missing}")
    return True

def get_db_config() -> Dict[str, str]:
    """Get database configuration from environment"""
    return {
        "uri": get_env("NEO4J_URI", DEFAULT_NEO4J_URI),
        "user": get_env("NEO4J_USER", DEFAULT_NEO4J_USER),
        "password": get_env("NEO4J_PASSWORD", DEFAULT_NEO4J_PASSWORD)
    }

def get_data_dir() -> str:
    """Get data directory path"""
    return get_env("DATA_DIR", DEFAULT_DATA_DIR)

def get_log_level() -> str:
    """Get logging level"""
    return get_env("LOG_LEVEL", DEFAULT_LOG_LEVEL)

def get_batch_size() -> int:
    """Get processing batch size"""
    try:
        return int(get_env("BATCH_SIZE", str(DEFAULT_BATCH_SIZE)))
    except ValueError:
        return DEFAULT_BATCH_SIZE

def get_connection_timeout() -> int:
    """Get database connection timeout"""
    try:
        return int(get_env("CONNECTION_TIMEOUT", str(CONNECTION_TIMEOUT)))
    except ValueError:
        return CONNECTION_TIMEOUT

def get_max_retries() -> int:
    """Get maximum retry attempts"""
    try:
        return int(get_env("MAX_RETRIES", str(MAX_RETRIES)))
    except ValueError:
        return MAX_RETRIES

def get_root_cause_delimiters() -> List[str]:
    """Get configurable root cause extraction delimiters"""
    delimiters_str = get_env("ROOT_CAUSE_DELIMITERS", ";,|,\n, - , / , and , & ")
    return [d.strip() for d in delimiters_str.split(",")]

def get_log_file() -> Optional[str]:
    """Get log file path if configured"""
    return get_env("LOG_FILE")

def get_schema() -> Dict[str, Any]:
    """Load schema configuration with optimized caching"""
    return _config_manager.get_schema()

def get_mappings() -> Dict[str, Any]:
    """Load field mappings configuration with optimized caching"""
    return _config_manager.get_mappings()

def get_entities_from_schema() -> Dict[str, Dict[str, Any]]:
    """Get entities dictionary from schema"""
    schema = get_schema()
    return {e["name"]: e for e in schema.get("entities", [])}

def get_entity_primary_key(entity_name: str) -> Optional[str]:
    """Get primary key for entity from schema"""
    entities = get_entities_from_schema()
    entity = entities.get(entity_name, {})
    properties = entity.get("properties", {})

    for prop_name, prop_info in properties.items():
        if prop_info.get("primary_key", False):
            return prop_name
    return None

def get_entity_names() -> List[str]:
    """Get all entity names from schema"""
    return list(get_entities_from_schema().keys())

def get_project_root() -> Path:
    """Get project root directory"""
    return Path(__file__).resolve().parent.parent

def get_data_directory() -> Path:
    """Get full data directory path"""
    return get_project_root() / "data" / "facility_data"

def ensure_directory(path: Path) -> Path:
    """Ensure directory exists, create if necessary"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def clear_cache():
    """Clear configuration cache (useful for testing)"""
    _config_manager.clear_cache()

def get_all_config() -> Dict[str, Any]:
    """Get comprehensive configuration summary for debugging"""
    return {
        "database": get_db_config(),
        "directories": {
            "data_dir": get_data_dir(),
            "project_root": str(get_project_root()),
            "data_directory": str(get_data_directory())
        },
        "processing": {
            "batch_size": get_batch_size(),
            "connection_timeout": get_connection_timeout(),
            "max_retries": get_max_retries(),
            "log_level": get_log_level()
        },
        "feature_config": {
            "root_cause_delimiters": get_root_cause_delimiters(),
            "log_file": get_log_file()
        },
        "cache_status": {
            "schema_loaded": _config_manager._schema_cache is not None,
            "mappings_loaded": _config_manager._mappings_cache is not None
        }
    }
