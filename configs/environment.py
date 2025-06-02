#!/usr/bin/env python3
"""
Corrected Configuration Gateway - Complete Adapter Support
Single source for all system configuration with full adapter method support.
"""

import json
import logging
import os
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

# Load .env file if available
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

__all__ = [
    # Core config functions
    "get_config",
    "get_schema",
    "get_env",
    "get_env_required",
    "validate_required_env",
    "get_entity_names",
    "get_entity_primary_key",
    "get_field_category_display_mapping",
    "get_entity_connections",
    # Dashboard config
    "get_dashboard_config",
    "get_dashboard_server_config",
    "get_dashboard_performance_config",
    # Utility functions
    "ensure_directory",
    "get_project_root",
]

logger = logging.getLogger(__name__)


class ConfigurationManager:
    """Thread-safe configuration manager with complete adapter support"""

    def __init__(self):
        self._schema_cache: Optional[Dict[str, Any]] = None
        self._mappings_cache: Optional[Dict[str, Any]] = None
        self._dashboard_cache: Optional[Dict[str, Any]] = None
        self._system_constants_cache: Optional[Dict[str, Any]] = None
        self._workflow_stages_cache: Optional[Dict[str, Any]] = None
        self._entity_classification_cache: Optional[Dict[str, Any]] = None
        self._entity_connections_cache: Optional[Dict[str, Any]] = None
        self._field_analysis_cache: Optional[Dict[str, Any]] = None
        self._dashboard_styling_cache: Optional[Dict[str, Any]] = None
        self._dashboard_charts_cache: Optional[Dict[str, Any]] = None
        self._field_category_display_cache: Optional[Dict[str, Any]] = None
        self._lock = threading.Lock()

    def get_system_constants(self) -> Dict[str, Any]:
        """Load system constants configuration with thread-safe caching"""
        if self._system_constants_cache is None:
            with self._lock:
                if self._system_constants_cache is None:
                    self._system_constants_cache = self._load_json_config("system_constants.json")
        return self._system_constants_cache

    def get_schema(self) -> Dict[str, Any]:
        """Load schema configuration with thread-safe caching"""
        if self._schema_cache is None:
            with self._lock:
                if self._schema_cache is None:
                    self._schema_cache = self._load_json_config("model_schema.json")
        return self._schema_cache

    def get_mappings(self) -> Dict[str, Any]:
        """Load field mappings configuration with thread-safe caching"""
        if self._mappings_cache is None:
            with self._lock:
                if self._mappings_cache is None:
                    self._mappings_cache = self._load_json_config("field_mappings.json")
        return self._mappings_cache

    def get_dashboard_config(self) -> Dict[str, Any]:
        """Load dashboard configuration with thread-safe caching"""
        if self._dashboard_cache is None:
            with self._lock:
                if self._dashboard_cache is None:
                    self._dashboard_cache = self._load_json_config("dashboard_config.json")
        return self._dashboard_cache

    def get_dashboard_styling_config(self) -> Dict[str, Any]:
        """Load dashboard styling configuration with thread-safe caching"""
        if self._dashboard_styling_cache is None:
            with self._lock:
                if self._dashboard_styling_cache is None:
                    self._dashboard_styling_cache = self._load_json_config("dashboard_styling.json")
        return self._dashboard_styling_cache

    def get_dashboard_charts_config(self) -> Dict[str, Any]:
        """Load dashboard charts configuration with thread-safe caching"""
        if self._dashboard_charts_cache is None:
            with self._lock:
                if self._dashboard_charts_cache is None:
                    self._dashboard_charts_cache = self._load_json_config("dashboard_charts.json")
        return self._dashboard_charts_cache

    def get_workflow_stages_config(self) -> Dict[str, Any]:
        """Load workflow stages configuration with thread-safe caching"""
        if self._workflow_stages_cache is None:
            with self._lock:
                if self._workflow_stages_cache is None:
                    self._workflow_stages_cache = self._load_json_config("workflow_stages.json")
        return self._workflow_stages_cache

    def get_entity_classification(self) -> Dict[str, Any]:
        """Load entity classification with thread-safe caching"""
        if self._entity_classification_cache is None:
            with self._lock:
                if self._entity_classification_cache is None:
                    self._entity_classification_cache = self._load_json_config(
                        "entity_classification.json"
                    )
        return self._entity_classification_cache

    def get_entity_connections(self) -> Dict[str, Any]:
        """Load entity connections with thread-safe caching"""
        if self._entity_connections_cache is None:
            with self._lock:
                if self._entity_connections_cache is None:
                    self._entity_connections_cache = self._load_json_config(
                        "entity_connections.json"
                    )
        return self._entity_connections_cache

    def get_field_analysis_config(self) -> Dict[str, Any]:
        """Load field analysis configuration with thread-safe caching"""
        if self._field_analysis_cache is None:
            with self._lock:
                if self._field_analysis_cache is None:
                    self._field_analysis_cache = self._load_json_config("field_analysis.json")
        return self._field_analysis_cache

    def get_field_category_display_mapping(self) -> Dict[str, Any]:
        """Load field category display mapping with thread-safe caching"""
        if self._field_category_display_cache is None:
            with self._lock:
                if self._field_category_display_cache is None:
                    self._field_category_display_cache = self._load_json_config(
                        "field_category_display_mapping.json"
                    )
        return self._field_category_display_cache

    def clear_cache(self):
        """Clear configuration cache (useful for testing)"""
        with self._lock:
            self._schema_cache = None
            self._mappings_cache = None
            self._dashboard_cache = None
            self._system_constants_cache = None
            self._workflow_stages_cache = None
            self._entity_classification_cache = None
            self._entity_connections_cache = None
            self._field_analysis_cache = None
            self._dashboard_styling_cache = None
            self._dashboard_charts_cache = None
            self._field_category_display_cache = None

    def _load_json_config(self, filename: str) -> Dict[str, Any]:
        """Load JSON configuration file with error handling"""
        config_dir = Path(__file__).parent
        config_path = config_dir / filename

        if not config_path.exists():
            if filename == "dashboard_config.json":
                return self._get_default_dashboard_config()
            elif filename == "dashboard_styling.json":
                return self._get_default_styling_config()
            elif filename == "dashboard_charts.json":
                return self._get_default_charts_config()
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Error loading {filename}: {e}")

    def _get_default_dashboard_config(self) -> Dict[str, Any]:
        """Get default dashboard configuration"""
        return {
            "server": {"default_host": "127.0.0.1", "default_port": 8050},
            "styling": {"primary_color": "#4A90E2", "chart_height": 400},
            "performance": {"query_timeout_warning": 5.0, "cache_ttl_seconds": 300},
        }

    def _get_default_styling_config(self) -> Dict[str, Any]:
        """Get default styling configuration"""
        return {
            "primary_color": "#4A90E2",
            "chart_colors": ["#4A90E2", "#F5A623", "#7ED321", "#B57EDC"],
            "background_light": "#FFFFFF",
            "text_primary": "#333333",
        }

    def _get_default_charts_config(self) -> Dict[str, Any]:
        """Get default charts configuration"""
        return {
            "font_family": "Arial, sans-serif",
            "default_height": 400,
            "title_font_size": 18,
            "card_padding": "15px",
        }


# Singleton configuration manager
_config_manager = ConfigurationManager()


def get_system_constants() -> Dict[str, Any]:
    """Load system constants configuration with optimized caching"""
    return _config_manager.get_system_constants()


def _get_constant(path: str, default: Any = None) -> Any:
    """Get a value from system constants using dot notation (e.g., 'database.default_uri')"""
    constants = get_system_constants()
    keys = path.split(".")
    value = constants

    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default


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
        "uri": get_env("NEO4J_URI", _get_constant("database.default_uri", "bolt://localhost:7687")),
        "user": get_env("NEO4J_USER", _get_constant("database.default_user", "neo4j")),
        "password": get_env(
            "NEO4J_PASSWORD", _get_constant("database.default_password", "password")
        ),
    }


def get_data_dir() -> str:
    """Get data directory path"""
    return get_env("DATA_DIR", _get_constant("database.default_data_dir", "data"))


def get_log_level() -> str:
    """Get logging level"""
    return get_env("LOG_LEVEL", _get_constant("database.default_log_level", "INFO"))


def get_batch_size() -> int:
    """Get processing batch size"""
    try:
        return int(get_env("BATCH_SIZE", str(_get_constant("processing.batch_size", 1000))))
    except ValueError:
        return _get_constant("processing.batch_size", 1000)


def get_connection_timeout() -> int:
    """Get database connection timeout"""
    try:
        return int(
            get_env("CONNECTION_TIMEOUT", str(_get_constant("processing.connection_timeout", 30)))
        )
    except ValueError:
        return _get_constant("processing.connection_timeout", 30)


def get_max_retries() -> int:
    """Get maximum retry attempts"""
    try:
        return int(get_env("MAX_RETRIES", str(_get_constant("processing.max_retries", 3))))
    except ValueError:
        return _get_constant("processing.max_retries", 3)


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


def get_field_mappings() -> Dict[str, Any]:
    """Load field mappings configuration (alias for get_mappings)"""
    return get_mappings()


def get_dashboard_config() -> Dict[str, Any]:
    """Load dashboard configuration with optimized caching"""
    return _config_manager.get_dashboard_config()


def get_workflow_stages_config() -> Dict[str, Any]:
    """Load workflow stages configuration with optimized caching"""
    return _config_manager.get_workflow_stages_config()


def get_entity_classification() -> Dict[str, Any]:
    """Load entity classification configuration with optimized caching"""
    return _config_manager.get_entity_classification()


def get_entity_connections() -> Dict[str, Any]:
    """Load entity connections configuration with optimized caching"""
    return _config_manager.get_entity_connections()


def get_field_analysis_config() -> Dict[str, Any]:
    """Public function to access field analysis configuration"""
    return _config_manager.get_field_analysis_config()


def get_field_category_display_mapping() -> Dict[str, Any]:
    """Load field category display mapping with optimized caching"""
    return _config_manager.get_field_category_display_mapping()


def get_entity_names() -> List[str]:
    """Get list of all entity names from schema configuration"""
    schema = get_schema()
    entities = schema.get("entities", [])
    return [entity.get("name") for entity in entities if entity.get("name")]


def get_entity_primary_key(entity_name: str) -> Optional[str]:
    """Get the primary key field for a given entity from schema"""
    schema = get_schema()
    entities = schema.get("entities", [])
    for entity in entities:
        if entity.get("name") == entity_name:
            properties = entity.get("properties", {})
            for prop_name, prop_details in properties.items():
                if prop_details.get("primary_key"):
                    return prop_name
    return None


# Dashboard-specific configuration functions
def get_dashboard_server_config() -> Dict[str, Any]:
    """Get dashboard server configuration"""
    config = get_dashboard_config()
    return config.get("server", {"default_host": "127.0.0.1", "default_port": 8050})


def get_dashboard_styling_config() -> Dict[str, Any]:
    """Get dashboard styling configuration"""
    return _config_manager.get_dashboard_styling_config()


def get_dashboard_chart_config() -> Dict[str, Any]:
    """Get dashboard chart configuration"""
    return _config_manager.get_dashboard_charts_config()


def get_dashboard_performance_config() -> Dict[str, Any]:
    """Get dashboard performance configuration"""
    config = get_dashboard_config()
    return config.get("performance", {"query_timeout_warning": 5.0, "cache_ttl_seconds": 300})


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
            "data_directory": str(get_data_directory()),
        },
        "processing": {
            "batch_size": get_batch_size(),
            "connection_timeout": get_connection_timeout(),
            "max_retries": get_max_retries(),
            "log_level": get_log_level(),
        },
        "feature_config": {
            "root_cause_delimiters": get_root_cause_delimiters(),
            "log_file": get_log_file(),
        },
        "dashboard": get_dashboard_config(),
        "cache_status": {
            "schema_loaded": _config_manager._schema_cache is not None,
            "mappings_loaded": _config_manager._mappings_cache is not None,
            "dashboard_loaded": _config_manager._dashboard_cache is not None,
            "workflow_stages_loaded": _config_manager._workflow_stages_cache is not None,
            "styling_loaded": _config_manager._dashboard_styling_cache is not None,
            "charts_loaded": _config_manager._dashboard_charts_cache is not None,
        },
    }


def get_config() -> Dict[str, Any]:
    """Get all configuration settings - alias for get_all_config"""
    return get_all_config()
