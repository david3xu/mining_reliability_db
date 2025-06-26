#!/usr/bin/env python3
"""
Data Adapters Package - Search-Focused Adapter Pattern Implementation
Clean data adapters for search functionality.
"""

from dashboard.adapters.config_adapter import (
    get_config_adapter,
    reset_config_adapter,
)
from dashboard.adapters.data_adapter import get_data_adapter

__all__ = [
    "get_data_adapter",
    "get_config_adapter",
    "reset_config_adapter",
]
