#!/usr/bin/env python3
"""
Dashboard Components Module - Phase 3 Atomized Architecture
Clean exports for micro-component composition with adapter dependencies.
"""

# Data Quality Components
from dashboard.components.data_quality import create_data_quality_layout

# Facility Detail Components
from dashboard.components.facility_detail import (
    create_facility_category_chart,
    create_facility_detail_layout,
    create_facility_metrics_cards,
    create_operating_centre_table,
    create_recurring_issues_analysis,
)

# Incident Search Components
from dashboard.components.incident_search import create_incident_search_layout

# Interactive Elements
from dashboard.components.interactive_elements import (
    create_interactive_bar_chart,
    create_interactive_data_table,
    create_interactive_metric_card,
    create_interactive_pie_chart,
    create_loading_overlay,
    create_navigation_toast,
)

# Layout Infrastructure
from dashboard.components.layout_template import (
    create_main_grid,
    create_metric_card,
    create_metrics_row,
    create_standard_layout,
    create_summary_section,
    create_tab_header,
    get_tab_metadata,
)
from dashboard.components.micro.chart_base import create_bar_chart, create_pie_chart
from dashboard.components.micro.facility_card import create_facility_summary_card

# Micro-Components (Direct Import)
from dashboard.components.micro.metric_card import create_metric_card as create_micro_metric_card
from dashboard.components.micro.table_base import create_data_table
from dashboard.components.micro.workflow_stage import create_workflow_stage_card

# Atomized Portfolio Components
from dashboard.components.portfolio_overview import (
    create_complete_dashboard,
    create_data_types_distribution_page,
    create_facilities_distribution_page,
    create_facility_chart,
    create_field_chart,
    create_historical_records_page,
    create_metrics_section,
    create_timeline_table,
)
from dashboard.components.solution_sequence_case_study import (
    create_solution_sequence_case_study_layout,
)

# Stakeholder Questions Components
from dashboard.components.stakeholder_questions import (
    create_question_category_card,
    create_question_detail_view,
    create_stakeholder_questions_overview,
    get_question_category_metrics,
)

# Navigation Components
from dashboard.components.tab_navigation import (
    create_breadcrumb_navigation,
    create_page_header,
    create_tab_container,
    create_tab_navigation,
    get_tab_content_id,
)

# Atomized Workflow Components
from dashboard.components.workflow_analysis import (
    create_workflow_analysis_layout,
    create_workflow_metrics,
)

__all__ = [
    # Atomized Portfolio Components
    "create_complete_dashboard",
    "create_metrics_section",
    "create_facility_chart",
    "create_field_chart",
    "create_timeline_table",
    "create_historical_records_page",
    "create_facilities_distribution_page",
    "create_data_types_distribution_page",
    # Atomized Workflow Components
    "create_workflow_analysis_layout",
    "create_workflow_metrics",
    # Data Quality Components
    "create_data_quality_layout",
    # Incident Search Components
    "create_incident_search_layout",
    # Facility Detail Components
    "create_facility_detail_layout",
    "create_facility_metrics_cards",
    "create_facility_category_chart",
    "create_recurring_issues_analysis",
    "create_operating_centre_table",
    # Interactive Elements
    "create_interactive_metric_card",
    "create_interactive_pie_chart",
    "create_interactive_bar_chart",
    "create_interactive_data_table",
    "create_navigation_toast",
    "create_loading_overlay",
    # Navigation Components
    "create_tab_navigation",
    "create_tab_container",
    "create_breadcrumb_navigation",
    "get_tab_content_id",
    "create_page_header",
    # Layout Infrastructure
    "create_standard_layout",
    "create_metric_card",
    "create_metrics_row",
    "create_main_grid",
    "create_summary_section",
    "create_tab_header",
    "get_tab_metadata",
    # Micro-Components
    "create_micro_metric_card",
    "create_pie_chart",
    "create_bar_chart",
    "create_data_table",
    "create_workflow_stage_card",
    "create_facility_summary_card",
    "create_solution_sequence_case_study_layout",
    # Stakeholder Questions Components
    "create_stakeholder_questions_overview",
    "create_question_category_card",
    "create_question_detail_view",
    "get_question_category_metrics",
]
