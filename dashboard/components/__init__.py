#!/usr/bin/env python3
"""
Dashboard Components Module - Phase 3 Atomized Architecture
Clean exports for micro-component composition with adapter dependencies.
"""

# Atomized Portfolio Components
from dashboard.components.portfolio_overview import (
    create_complete_dashboard,
    create_metrics_section,
    create_facility_chart,
    create_field_chart,
    create_timeline_table,
    create_historical_records_page,
    create_facilities_distribution_page,
    create_data_types_distribution_page
)

# Atomized Workflow Components
from dashboard.components.workflow_analysis import (
    create_workflow_analysis_layout,
    create_workflow_metrics,
    create_process_flow,
    create_entity_distribution_chart,
    create_mapping_table,
    create_workflow_process_page
)

# Data Quality Components
from dashboard.components.data_quality import (
    create_data_quality_layout,
    create_quality_metrics_cards,
    create_field_completeness_chart,
    create_facility_quality_comparison,
    create_quality_summary_table
)

# Facility Detail Components
from dashboard.components.facility_detail import (
    create_facility_detail_layout,
    create_facility_metrics_cards,
    create_facility_category_chart,
    create_recurring_issues_analysis,
    create_operating_centre_table
)

# Layout Infrastructure
from dashboard.components.layout_template import (
    create_standard_layout,
    create_metric_card,
    create_metrics_row,
    create_main_grid,
    create_summary_section,
    create_tab_header,
    get_tab_metadata
)

# Micro-Components (Direct Import)
from dashboard.components.micro.metric_card import create_metric_card as create_micro_metric_card
from dashboard.components.micro.chart_base import create_pie_chart, create_bar_chart
from dashboard.components.micro.table_base import create_data_table
from dashboard.components.micro.workflow_stage import create_workflow_stage_card
from dashboard.components.micro.facility_card import create_facility_summary_card

__all__ = [
    # Atomized Portfolio Components
    'create_complete_dashboard',
    'create_metrics_section',
    'create_facility_chart',
    'create_field_chart',
    'create_timeline_table',
    'create_historical_records_page',
    'create_facilities_distribution_page',
    'create_data_types_distribution_page',

    # Atomized Workflow Components
    'create_workflow_analysis_layout',
    'create_workflow_metrics',
    'create_process_flow',
    'create_entity_distribution_chart',
    'create_mapping_table',
    'create_workflow_process_page',

    # Data Quality Components
    'create_data_quality_layout',
    'create_quality_metrics_cards',
    'create_field_completeness_chart',
    'create_facility_quality_comparison',
    'create_quality_summary_table',

    # Facility Detail Components
    'create_facility_detail_layout',
    'create_facility_metrics_cards',
    'create_facility_category_chart',
    'create_recurring_issues_analysis',
    'create_operating_centre_table',

    # Layout Infrastructure
    'create_standard_layout',
    'create_metric_card',
    'create_metrics_row',
    'create_main_grid',
    'create_summary_section',
    'create_tab_header',
    'get_tab_metadata',

    # Micro-Components
    'create_micro_metric_card',
    'create_pie_chart',
    'create_bar_chart',
    'create_data_table',
    'create_workflow_stage_card',
    'create_facility_summary_card'
]

# Legacy Compatibility Aliases
create_enhanced_field_distribution_chart = create_field_chart
create_enhanced_facility_pie_chart = create_facility_chart
create_enhanced_historical_table = create_timeline_table
create_metrics_cards = create_metrics_section
create_field_distribution_chart = create_field_chart
create_facility_pie_chart = create_facility_chart
create_historical_table = create_timeline_table
create_portfolio_layout = create_complete_dashboard
create_workflow_metrics_cards = create_workflow_metrics
create_process_flow_diagram = create_process_flow
create_stage_field_distribution = create_entity_distribution_chart
create_workflow_mapping_table = create_mapping_table