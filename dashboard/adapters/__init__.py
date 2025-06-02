#!/usr/bin/env python3
"""
Data Adapters Package - Clean Adapter Pattern Implementation
Unified data adapters for dashboard-core integration.
"""

from dashboard.adapters.config_adapter import (
    ConfigAdapter,
    get_config_adapter,
    reset_config_adapter,
)
from dashboard.adapters.data_adapter import PurifiedDataAdapter, get_data_adapter, reset_adapter
from dashboard.adapters.facility_adapter import (
    FacilityAdapter,
    get_facility_adapter,
    reset_facility_adapter,
)
from dashboard.adapters.workflow_adapter import (
    WorkflowAdapter,
    get_workflow_adapter,
    reset_workflow_adapter,
)

__all__ = [
    # Base adapters
    "PurifiedDataAdapter",
    "get_data_adapter",
    "reset_adapter",
    "FacilityAdapter",
    "get_facility_adapter",
    "reset_facility_adapter",
    "ConfigAdapter",
    "get_config_adapter",
    "reset_config_adapter",
    "WorkflowAdapter",
    "get_workflow_adapter",
    "reset_workflow_adapter",
]
