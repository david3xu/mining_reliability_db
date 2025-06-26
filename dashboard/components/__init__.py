#!/usr/bin/env python3
"""
Search Components Module - Search-Algorithms-Only Architecture
Clean exports for core search functionality with focused dependencies.
"""

# Core Search Components
from dashboard.components.graph_search import create_graph_search_layout
from dashboard.components.cypher_search import create_cypher_search_layout

# Layout Infrastructure
from dashboard.components.layout_template import (
    create_main_grid,
    create_metric_card,
    create_metrics_row,
    create_standard_layout,
    create_summary_section,
    create_tab_header,
    get_tab_metadata,
    create_chart_container,
    create_empty_state,
    get_layout_config,
)

__all__ = [
    # Core Search Components
    "create_graph_search_layout",
    "create_cypher_search_layout",
    # Layout Infrastructure
    "create_standard_layout",
    "create_metric_card",
    "create_metrics_row",
    "create_main_grid",
    "create_summary_section",
    "create_tab_header",
    "get_tab_metadata",
    "create_chart_container",
    "create_empty_state",
    "get_layout_config",
]
