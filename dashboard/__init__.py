"""
Dashboard Package
Mining Reliability Database dashboard components and utilities.
"""

# FIXED: Updated imports to match new portfolio_overview.py implementation
from dashboard.components.portfolio_overview import (
    create_complete_dashboard,
    create_historical_records_page,
    create_facilities_distribution_page,
    create_data_types_distribution_page,
    create_historical_trends_chart,
    # Legacy compatibility maintained
    create_metrics_cards,
    create_field_distribution_chart,
    create_facility_pie_chart,
    create_historical_table,
    create_portfolio_layout
)

# Data processing
from dashboard.utils.data_transformers import (
    get_portfolio_metrics,
    get_field_distribution_data,
    get_facility_breakdown_data,
    get_historical_timeline_data,
    validate_dashboard_data
)

# Layouts
from dashboard.layouts.main_layout import (
    create_main_layout,
    create_navigation_bar,
    create_footer
)

# REMOVED: create_enhanced_dashboard_layout (doesn't exist in new implementation)

__all__ = [
    # Portfolio components
    'create_complete_dashboard',
    'create_historical_records_page',
    'create_facilities_distribution_page',
    'create_data_types_distribution_page',
    'create_historical_trends_chart',
    'create_metrics_cards',
    'create_field_distribution_chart',
    'create_facility_pie_chart',
    'create_historical_table',
    'create_portfolio_layout',

    # Data transformers
    'get_portfolio_metrics',
    'get_field_distribution_data',
    'get_facility_breakdown_data',
    'get_historical_timeline_data',
    'validate_dashboard_data',

    # Layouts
    'create_main_layout',
    'create_navigation_bar',
    'create_footer'
]