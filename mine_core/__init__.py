"""
Mining Reliability Database Core Package
Graph-based system for analyzing mining incident data.
"""

__version__ = "0.1.0"

from mine_core.database import (
    get_database,
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
from mine_core.pipelines import FacilityDataExtractor, DataTransformer, Neo4jLoader
from mine_core.shared import field_utils, common
from mine_core.entities import get_entity_definitions, create_entity_from_dict, get_schema_manager
from mine_core.helpers import setup_logging, get_logger
from mine_core.analytics import WorkflowAnalyzer, PatternDiscovery, QualityAnalyzer

__all__ = [
    # Database functions
    'get_database', 'get_facilities', 'get_facility', 'get_action_requests',
    'get_incident_chain', 'get_department', 'get_assets',
    'get_incident_counts_by_category', 'get_root_cause_frequency',
    'get_effectiveness_stats', 'get_root_cause_intelligence_summary',
    'get_operational_performance_dashboard', 'get_predictive_intelligence_indicators',
    'get_missing_data_quality_intelligence', 'get_causal_correlation_matrix',

    # Pipeline classes
    'FacilityDataExtractor', 'DataTransformer', 'Neo4jLoader',

    # Entity functions
    'get_entity_definitions', 'create_entity_from_dict', 'get_schema_manager',

    # Helper functions
    'setup_logging', 'get_logger',

    # Analytics classes
    'WorkflowAnalyzer', 'PatternDiscovery', 'QualityAnalyzer'
]
