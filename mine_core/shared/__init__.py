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

    # Common utils
    'setup_project_path',
    'setup_logging',
    'setup_project_environment',
    'handle_error',
    'ensure_directory'
]
