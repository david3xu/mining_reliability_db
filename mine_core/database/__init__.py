#!/usr/bin/env python3
"""
Core Database Package
Centralized data access and query management.
"""

from mine_core.database.db import (
    get_database,
)

# Legacy compatibility
from mine_core.database.queries import (  # Legacy function aliases
    get_action_requests,
    get_assets,
    get_causal_correlation_matrix,
    get_department,
    get_effectiveness_stats,
    get_entity_completion_rates,
    get_facilities,
    get_facility,
    get_facility_action_statistics,
    get_field_completion_statistics,
    get_incident_chain,
    get_incident_counts_by_category,
    get_missing_data_quality_intelligence,
    get_operational_performance_dashboard,
    get_predictive_intelligence_indicators,
    get_root_cause_frequency,
    get_root_cause_intelligence_summary,
)
from mine_core.database.query_manager import (
    QueryManager,
    get_entities_by_type,
    get_query_manager,
    get_relationship_data,
)

__all__ = [
    # Core Query Management
    "QueryManager",
    "get_query_manager",
    "get_database",
    # Core Query Functions
    "get_facilities",
    "get_facility",
    "get_action_requests",
    "get_incident_chain",
    "get_operational_performance_dashboard",
    "get_root_cause_intelligence_summary",
    "get_predictive_intelligence_indicators",
    "get_missing_data_quality_intelligence",
    "get_causal_correlation_matrix",
    "get_field_completion_statistics",
    "get_entity_completion_rates",
    "get_facility_action_statistics",
    # DB operations
    # Query manager functions
    "get_entities_by_type",
    "get_relationship_data",
    # Legacy function aliases for backward compatibility
    "get_assets",
    "get_department",
    "get_effectiveness_stats",
    "get_incident_counts_by_category",
    "get_root_cause_frequency",
]
