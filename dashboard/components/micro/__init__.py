#!/usr/bin/env python3
"""
Micro-Components Module - Atomic Component Exports
Direct access to single-purpose components with pure adapter dependencies.
"""

# Core Micro-Components
from dashboard.components.micro.metric_card import create_metric_card
from dashboard.components.micro.chart_base import create_pie_chart, create_bar_chart
from dashboard.components.micro.table_base import create_data_table
from dashboard.components.micro.workflow_stage import create_workflow_stage_card
from dashboard.components.micro.facility_card import create_facility_summary_card

__all__ = [
    # Single-Purpose Display Components
    'create_metric_card',           # 15-line metric display
    'create_pie_chart',             # 8-line pie visualization
    'create_bar_chart',             # 8-line bar visualization
    'create_data_table',            # 16-line data table
    'create_workflow_stage_card',   # 18-line process stage
    'create_facility_summary_card'  # 14-line facility overview
]