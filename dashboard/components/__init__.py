"""
Dashboard Components Package
Visual components for Mining Reliability Database multi-tab dashboard.
"""

# FIXED: Updated imports to match actual function names in portfolio_overview.py
from dashboard.components.portfolio_overview import (
    create_metrics_cards,
    create_field_distribution_chart,
    create_facility_pie_chart,
    create_historical_table,
    create_enhanced_dashboard_layout,
    create_complete_dashboard
)

# Multi-tab components
from dashboard.components.data_quality import (
    create_data_quality_layout,
    create_quality_metrics_cards,
    create_field_completeness_chart,
    create_facility_quality_comparison,
    create_quality_summary_table
)

from dashboard.components.workflow_analysis import (
    create_workflow_analysis_layout,
    create_workflow_metrics_cards,
    create_process_flow_diagram,
    create_entity_field_distribution,
    create_field_mapping_table
)

from dashboard.components.tab_navigation import (
    create_tab_navigation,
    create_tab_container,
    create_tab_header,
    get_tab_metadata
)

from dashboard.components.layout_template import (
    create_standard_layout,
    create_metric_card,
    create_metrics_row,
    create_main_grid,
    create_summary_section
)

# Facility detail
from dashboard.components.facility_detail import (
    create_facility_detail_layout,
    create_facility_metrics_cards,
    create_facility_category_chart,
    create_recurring_issues_analysis
)

# Graph visualization (placeholder)
from dashboard.components.graph_visualizer import (
    create_causal_network_graph,
    create_correlation_heatmap,
    create_root_cause_flow_diagram,
    create_network_analysis_dashboard
)

__all__ = [
    # Portfolio Overview (Fixed function names)
    'create_interactive_metrics_cards',
    'create_enhanced_field_distribution_chart',
    'create_enhanced_facility_pie_chart',
    'create_enhanced_historical_table',
    'create_enhanced_dashboard_layout',
    'create_complete_dashboard',

    # Data Quality Foundation
    'create_data_quality_layout',
    'create_quality_metrics_cards',
    'create_field_completeness_chart',
    'create_facility_quality_comparison',
    'create_quality_summary_table',

    # Workflow Understanding
    'create_workflow_analysis_layout',
    'create_workflow_metrics_cards',
    'create_process_flow_diagram',
    'create_stage_field_distribution',
    'create_workflow_mapping_table',

    # Tab Navigation System
    'create_tab_navigation',
    'create_tab_container',
    'create_tab_header',
    'get_tab_metadata',

    # Layout Template System
    'create_standard_layout',
    'create_metric_card',
    'create_metrics_row',
    'create_main_grid',
    'create_summary_section',

    # Facility Detail
    'create_facility_detail_layout',
    'create_facility_overview_card',
    'create_incident_timeline_chart',
    'create_workflow_analysis_table',

    # Graph Visualization (Placeholder)
    'create_causal_network_graph',
    'create_correlation_heatmap',
    'create_root_cause_flow_diagram',
    'create_network_analysis_dashboard'
]