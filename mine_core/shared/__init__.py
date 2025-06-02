#!/usr/bin/env python3
"""
Core Shared Utilities Package
Common infrastructure for error handling and system utilities.
"""

from mine_core.shared.common import (
    handle_error,
    setup_project_environment,
    get_logger
)

__all__ = [
    'handle_error',
    'setup_project_environment',
    'get_logger'
]