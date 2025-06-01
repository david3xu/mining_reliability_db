"""
Mining Reliability Database - Dashboard Package
Portfolio analytics and visualization layer.
"""

__version__ = "1.0.0"

# Phase 2: Data Pipeline
from dashboard.utils.data_transformers import (
    get_portfolio_metrics,
    get_field_distribution_data,
    get_facility_breakdown_data,
    get_historical_timeline_data,
    validate_dashboard_data
)

# Phase 3: Visual Components
from dashboard.components.portfolio_overview import (
    create_metrics_cards,
    create_field_distribution_chart,
    create_facility_pie_chart,
    create_historical_table,
    create_enhanced_dashboard_layout,
    create_complete_dashboard
)

# Phase 4: Application Integration
from dashboard.layouts.main_layout import (
    create_main_layout,
    create_navigation_bar,
    create_footer
)

from dashboard.app import (
    create_dashboard_app
)

__all__ = [
    # Data Pipeline (Phase 2)
    'get_portfolio_metrics',
    'get_field_distribution_data',
    'get_facility_breakdown_data',
    'get_historical_timeline_data',
    'validate_dashboard_data',

    # Visual Components (Phase 3)
    'create_metrics_cards',
    'create_field_distribution_chart',
    'create_facility_pie_chart',
    'create_historical_table',
    'create_enhanced_dashboard_layout',
    'create_complete_dashboard',

    # Application Layer (Phase 4)
    'create_main_layout',
    'create_navigation_bar',
    'create_footer',
    'create_dashboard_app'
]
