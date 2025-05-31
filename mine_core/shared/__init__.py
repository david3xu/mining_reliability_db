"""
Mining Reliability Database - Shared Utilities
Core utilities for field processing, constants, and common functionality.
"""

# Field processing utilities
from .field_utils import (
    has_real_value,
    is_missing_data_indicator,
    clean_label,
    normalize_field_value,
    validate_field_for_entity,
    get_field_category,
    MISSING_DATA_INDICATORS,
    MISSING_DATA_CONTEXT
)

# Core constants
from .constants import (
    DEFAULT_BATCH_SIZE,
    MAX_RETRIES,
    CONNECTION_TIMEOUT,
    DEFAULT_NEO4J_URI,
    DEFAULT_NEO4J_USER,
    DEFAULT_NEO4J_PASSWORD,
    DEFAULT_LOG_LEVEL,
    DEFAULT_DATA_DIR,
    ENTITY_LOAD_ORDER,
    RELATIONSHIP_CONFIGS,
    FIELD_PRIORITY_CATEGORIES,
    ROOT_CAUSE_PROCESSING,
    LABEL_PATTERNS,
    FIELD_NORMALIZATION,
    ENTITY_CREATION_THRESHOLDS,
    ANALYTICS_CATEGORIES,
    LOG_FORMAT,
    QUERY_OPTIMIZATION,
    VALIDATION_RULES,
    PROCESSING_CONFIG
)

# Common utilities
from .common import (
    setup_project_path,
    setup_logging,
    setup_project_environment,
    handle_error,
    ensure_directory
)

__all__ = [
    # Field utils
    'has_real_value',
    'is_missing_data_indicator',
    'clean_label',
    'normalize_field_value',
    'validate_field_for_entity',
    'get_field_category',
    'MISSING_DATA_INDICATORS',
    'MISSING_DATA_CONTEXT',

    # Constants
    'DEFAULT_BATCH_SIZE',
    'MAX_RETRIES',
    'CONNECTION_TIMEOUT',
    'DEFAULT_NEO4J_URI',
    'DEFAULT_NEO4J_USER',
    'DEFAULT_NEO4J_PASSWORD',
    'DEFAULT_LOG_LEVEL',
    'DEFAULT_DATA_DIR',
    'ENTITY_LOAD_ORDER',
    'RELATIONSHIP_CONFIGS',
    'FIELD_PRIORITY_CATEGORIES',
    'ROOT_CAUSE_PROCESSING',
    'LABEL_PATTERNS',
    'FIELD_NORMALIZATION',
    'ENTITY_CREATION_THRESHOLDS',
    'ANALYTICS_CATEGORIES',
    'LOG_FORMAT',
    'QUERY_OPTIMIZATION',
    'VALIDATION_RULES',
    'PROCESSING_CONFIG',

    # Common utils
    'setup_project_path',
    'setup_logging',
    'setup_project_environment',
    'handle_error',
    'ensure_directory'
]
