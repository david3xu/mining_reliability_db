#!/usr/bin/env python3
"""
Simple Environment Configuration Loader
Basic, direct environment variable access.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

def get_env(key: str, default: str = None) -> str:
    """Load environment variable with optional default"""
    return os.environ.get(key, default)

def load_json_config(filename: str) -> Dict[str, Any]:
    """Load JSON configuration file"""
    config_dir = Path(__file__).parent
    config_path = config_dir / filename

    if not config_path.exists():
        return {}

    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

# Database configuration
def get_db_config() -> Dict[str, str]:
    """Get database configuration from environment"""
    return {
        "uri": get_env("NEO4J_URI", "bolt://localhost:7687"),
        "user": get_env("NEO4J_USER", "neo4j"),
        "password": get_env("NEO4J_PASSWORD", "password")
    }

# Data paths
def get_data_dir() -> str:
    """Get data directory path"""
    return get_env("DATA_DIR", str(Path(__file__).parent.parent / "data" / "facility_data"))

# Schema and mappings
def get_schema() -> Dict[str, Any]:
    """Load schema configuration"""
    return load_json_config("model_schema.json")

def get_mappings() -> Dict[str, Any]:
    """Load field mappings configuration"""
    return load_json_config("field_mappings.json")
