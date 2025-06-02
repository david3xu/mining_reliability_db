#!/usr/bin/env python3
"""
Data Adapters Package - Clean Adapter Pattern Implementation
Unified data adapters for dashboard-core integration.
"""

from dashboard.adapters.config_adapter import (
    get_config_adapter,
    handle_error_utility,
    reset_config_adapter,
)
from dashboard.adapters.data_adapter import PurifiedDataAdapter, get_data_adapter, reset_adapter
from dashboard.adapters.facility_adapter import get_facility_adapter, reset_facility_adapter
from dashboard.adapters.workflow_adapter import get_workflow_adapter, reset_workflow_adapter

__all__ = [
    "get_data_adapter",
    "reset_adapter",
    "PurifiedDataAdapter",
    "get_facility_adapter",
    "reset_facility_adapter",
    "get_config_adapter",
    "reset_config_adapter",
    "handle_error_utility",
    "get_workflow_adapter",
    "reset_workflow_adapter",
]
