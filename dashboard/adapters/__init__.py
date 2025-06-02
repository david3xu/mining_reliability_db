#!/usr/bin/env python3
"""
Dashboard Adapters Module - Phase 2 Purified Architecture
Clean separation between core business logic and component data access.
"""

from dashboard.adapters.config_adapter import ConfigAdapter, get_config_adapter

# Purified Data Adapters - Pure data access, zero business logic
from dashboard.adapters.data_adapter import PurifiedDataAdapter, get_data_adapter
from dashboard.adapters.facility_adapter import FacilityAdapter, get_facility_adapter

# Data Interface Contracts
from dashboard.adapters.interfaces import (
    ChartConfig,
    ComponentMetadata,
    ComponentResult,
    DashboardConfig,
    FacilityData,
    FieldData,
    PlotlyData,
    PortfolioData,
    StyleConfig,
    TimelineData,
    ValidationResult,
)
from dashboard.adapters.workflow_adapter import WorkflowAdapter, get_workflow_adapter

__all__ = [
    # Phase 2 Purified Adapters
    "PurifiedDataAdapter",
    "WorkflowAdapter",
    "FacilityAdapter",
    "ConfigAdapter",
    # Singleton Access Functions
    "get_data_adapter",
    "get_workflow_adapter",
    "get_facility_adapter",
    "get_config_adapter",
    # Data Interface Contracts
    "PortfolioData",
    "FacilityData",
    "FieldData",
    "TimelineData",
    # Support Interfaces
    "ComponentMetadata",
    "ValidationResult",
    "DashboardConfig",
    "ChartConfig",
    # Type Aliases
    "PlotlyData",
    "ComponentResult",
    "StyleConfig",
]

# Backward Compatibility Aliases
DashboardDataAdapter = PurifiedDataAdapter  # Legacy compatibility
