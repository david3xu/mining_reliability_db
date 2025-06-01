"""
Dashboard Components Package
Visual components for Mining Reliability Database dashboard.
"""

from dashboard.components.portfolio_overview import (
    create_interactive_metrics_cards,
    create_enhanced_field_distribution_chart,
    create_enhanced_facility_pie_chart,
    create_enhanced_historical_table,
    create_enhanced_dashboard_layout,
    create_complete_dashboard
)

# Phase 5: Facility Detail Components (Placeholder Implementation)
from dashboard.components.facility_detail import (
    create_facility_overview_card,
    create_incident_timeline_chart,
    create_workflow_analysis_table,
    create_facility_detail_layout
)

# Phase 6: Graph Visualization Components (Placeholder Implementation)
from dashboard.components.graph_visualizer import (
    create_causal_network_graph,
    create_correlation_heatmap,
    create_root_cause_flow_diagram,
    create_network_analysis_dashboard
)

__all__ = [
    # Phase 4: Portfolio Overview (Implemented)
    'create_interactive_metrics_cards',
    'create_enhanced_field_distribution_chart',
    'create_enhanced_facility_pie_chart',
    'create_enhanced_historical_table',
    'create_enhanced_dashboard_layout',
    'create_complete_dashboard',

    # Phase 5: Facility Detail (Placeholder)
    'create_facility_overview_card',
    'create_incident_timeline_chart',
    'create_workflow_analysis_table',
    'create_facility_detail_layout',

    # Phase 6: Graph Visualization (Placeholder)
    'create_causal_network_graph',
    'create_correlation_heatmap',
    'create_root_cause_flow_diagram',
    'create_network_analysis_dashboard'
]
