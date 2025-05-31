#!/usr/bin/env python3
"""
Dashboard Adapters Module
Provides clean data access layer for dashboard components.
"""

from dashboard.adapters.data_adapter import DashboardDataAdapter, get_data_adapter
from dashboard.adapters.interfaces import (
    PortfolioData, FacilityData, FieldData, TimelineData,
    ComponentMetadata, ValidationResult, DashboardConfig,
    ChartConfig, PlotlyData, ComponentResult, StyleConfig
)

__all__ = [
    # Core adapter
    'DashboardDataAdapter',
    'get_data_adapter',

    # Data interfaces
    'PortfolioData',
    'FacilityData',
    'FieldData',
    'TimelineData',

    # Support interfaces
    'ComponentMetadata',
    'ValidationResult',
    'DashboardConfig',
    'ChartConfig',

    # Type aliases
    'PlotlyData',
    'ComponentResult',
    'StyleConfig'
]
