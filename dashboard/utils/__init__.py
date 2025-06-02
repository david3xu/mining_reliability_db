"""
Dashboard Utilities Package
Data transformation and formatting utilities for dashboard components.
"""

from dashboard.utils.data_transformers import (
    format_for_plotly_bar,
    format_for_plotly_pie,
    format_for_plotly_table,
    get_facility_breakdown_data,
    get_field_distribution_data,
    get_historical_timeline_data,
    get_portfolio_metrics,
    validate_dashboard_data,
)
from dashboard.utils.styling import (
    COLORS,
    DASHBOARD_STYLES,
    FONTS,
    LAYOUT,
    apply_theme_mode,
    get_bar_chart_style,
    get_chart_layout_template,
    get_metric_card_style,
    get_pie_chart_style,
    get_responsive_style,
    get_table_style,
)
from dashboard.utils.url_builders import (
    build_analysis_url,
    build_detail_url,
    build_facility_url,
    build_filter_url,
    create_breadcrumb_data,
    get_navigation_context,
    get_page_title,
    is_dashboard_url,
    is_valid_facility_url,
    parse_detail_url,
    parse_facility_url,
    sanitize_url_component,
)

__all__ = [
    # Data transformers
    "get_portfolio_metrics",
    "get_field_distribution_data",
    "get_facility_breakdown_data",
    "get_historical_timeline_data",
    "validate_dashboard_data",
    "format_for_plotly_bar",
    "format_for_plotly_pie",
    "format_for_plotly_table",
    # Styling constants and functions
    "COLORS",
    "FONTS",
    "LAYOUT",
    "DASHBOARD_STYLES",
    "get_metric_card_style",
    "get_chart_layout_template",
    "get_bar_chart_style",
    "get_pie_chart_style",
    "get_table_style",
    "apply_theme_mode",
    "get_responsive_style",
    # URL builders
    "sanitize_url_component",
    "build_facility_url",
    "build_analysis_url",
    "build_detail_url",
    "build_filter_url",
    "parse_facility_url",
    "parse_detail_url",
    "create_breadcrumb_data",
    "get_navigation_context",
    "is_valid_facility_url",
    "is_dashboard_url",
    "get_page_title",
]
