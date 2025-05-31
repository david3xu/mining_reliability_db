"""
Schema-driven database layer using model_schema.json
"""

from mine_core.database.db import get_database
from mine_core.database.queries import (
    get_facilities,
    get_facility,
    get_action_requests,
    get_incident_chain,
    get_department,
    get_assets,
    get_incident_counts_by_category,
    get_root_cause_frequency,
    get_effectiveness_stats,
    get_root_cause_intelligence_summary,
    get_operational_performance_dashboard,
    get_predictive_intelligence_indicators,
    get_missing_data_quality_intelligence,
    get_causal_correlation_matrix
)

__all__ = [
    'get_database',
    'get_facilities',
    'get_facility',
    'get_action_requests',
    'get_incident_chain',
    'get_department',
    'get_assets',
    'get_incident_counts_by_category',
    'get_root_cause_frequency',
    'get_effectiveness_stats',
    'get_root_cause_intelligence_summary',
    'get_operational_performance_dashboard',
    'get_predictive_intelligence_indicators',
    'get_missing_data_quality_intelligence',
    'get_causal_correlation_matrix'
]
