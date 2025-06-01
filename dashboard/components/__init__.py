"""
Dashboard Components Package
Visual components for Mining Reliability Database - Interactive Navigation Hub.
"""

# Portfolio Overview (Updated with navigation pages)
from dashboard.components.portfolio_overview import (
    create_complete_dashboard,
    create_clean_metrics_section,
    create_enhanced_field_distribution_chart,
    create_enhanced_facility_pie_chart,
    create_enhanced_historical_table,
    create_historical_trends_chart,
    create_historical_records_page,
    create_facilities_distribution_page,
    create_data_types_distribution_page,
    # Legacy compatibility
    create_metrics_cards,
    create_field_distribution_chart,
    create_facility_pie_chart,
    create_historical_table,
    create_portfolio_layout
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
    create_stage_field_distribution,
    create_workflow_mapping_table
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
    create_recurring_issues_analysis,
    create_operating_centre_table
)

# Graph visualization (placeholder)
from dashboard.components.graph_visualizer import (
    create_causal_network_graph,
    create_correlation_heatmap,
    create_root_cause_flow_diagram,
    create_network_analysis_dashboard
)

# Interactive elements
from dashboard.components.interactive_elements import (
    create_interactive_metric_card,
    create_interactive_pie_chart,
    create_interactive_bar_chart,
    create_interactive_timeline_table
)

__all__ = [
    # Portfolio Overview (Navigation Hub)
    'create_complete_dashboard',
    'create_clean_metrics_section',
    'create_enhanced_field_distribution_chart',
    'create_enhanced_facility_pie_chart',
    'create_enhanced_historical_table',

    # Dedicated Analysis Pages
    'create_historical_records_page',
    'create_facilities_distribution_page',
    'create_data_types_distribution_page',

    # Legacy Compatibility
    'create_metrics_cards',
    'create_field_distribution_chart',
    'create_facility_pie_chart',
    'create_historical_table',
    'create_portfolio_layout',

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
    'create_facility_metrics_cards',
    'create_facility_category_chart',
    'create_recurring_issues_analysis',
    'create_operating_centre_table',

    # Graph Visualization (Placeholder)
    'create_causal_network_graph',
    'create_correlation_heatmap',
    'create_root_cause_flow_diagram',
    'create_network_analysis_dashboard',

    # Interactive Elements
    'create_interactive_metric_card',
    'create_interactive_pie_chart',
    'create_interactive_bar_chart',
    'create_interactive_timeline_table'
]