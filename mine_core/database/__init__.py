#!/usr/bin/env python3
"""
Core Database Package
Centralized data access and query management.
"""

from mine_core.database.query_manager import QueryManager, get_query_manager
from mine_core.database.db import get_database

# Legacy compatibility
from mine_core.database.queries import (
    get_facilities,
    get_action_requests,
    get_operational_performance_dashboard,
    get_root_cause_intelligence_summary,
    get_field_completion_statistics,
    get_entity_completion_rates,
    get_facility_action_statistics,
    get_missing_data_quality_intelligence
)

__all__ = [
    # Core Query Management
    'QueryManager',
    'get_query_manager',
    'get_database',

    # Legacy Query Functions
    'get_facilities',
    'get_action_requests',
    'get_operational_performance_dashboard',
    'get_root_cause_intelligence_summary',
    'get_field_completion_statistics',
    'get_entity_completion_rates',
    'get_facility_action_statistics',
    'get_missing_data_quality_intelligence'
]