#!/usr/bin/env python3
"""
Consolidated Environment Configuration Loader
Single source for all configuration access.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from mine_core.shared.constants import (
    DEFAULT_NEO4J_URI, DEFAULT_NEO4J_USER, DEFAULT_NEO4J_PASSWORD,
    DEFAULT_LOG_LEVEL, DEFAULT_DATA_DIR
)

# Load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Cache for loaded configurations
_schema_cache: Optional[Dict[str, Any]] = None
_mappings_cache: Optional[Dict[str, Any]] = None

def get_env(key: str, default: str = None) -> str:
    """Load environment variable with default"""
    return os.environ.get(key, default)

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

def _load_json_config(filename: str) -> Dict[str, Any]:
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

def get_schema() -> Dict[str, Any]:
    """Load schema configuration with caching"""
    global _schema_cache
    if _schema_cache is None:
        _schema_cache = _load_json_config("model_schema.json")
    return _schema_cache

def get_mappings() -> Dict[str, Any]:
    """Load field mappings configuration with caching"""
    global _mappings_cache
    if _mappings_cache is None:
        _mappings_cache = _load_json_config("field_mappings.json")
    return _mappings_cache

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

def get_entity_names() -> list:
    """Get all entity names from schema"""
    return list(get_entities_from_schema().keys())

def clear_cache():
    """Clear configuration cache (useful for testing)"""
    global _schema_cache, _mappings_cache
    _schema_cache = None
    _mappings_cache = None
