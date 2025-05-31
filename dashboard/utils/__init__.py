"""
Dashboard Utilities Package
Data transformation and formatting utilities for dashboard components.
"""

from dashboard.utils.data_transformers import (
    get_portfolio_metrics,
    get_field_distribution_data,
    get_facility_breakdown_data,
    get_historical_timeline_data,
    validate_dashboard_data,
    format_for_plotly_bar,
    format_for_plotly_pie,
    format_for_plotly_table
)

from dashboard.utils.styling import (
    COLORS, FONTS, LAYOUT, DASHBOARD_STYLES,
    get_metric_card_style, get_chart_layout_template,
    get_bar_chart_style, get_pie_chart_style, get_table_style,
    apply_theme_mode, get_responsive_style
)

__all__ = [
    # Data transformers
    'get_portfolio_metrics',
    'get_field_distribution_data',
    'get_facility_breakdown_data',
    'get_historical_timeline_data',
    'validate_dashboard_data',
    'format_for_plotly_bar',
    'format_for_plotly_pie',
    'format_for_plotly_table',

    # Styling constants and functions
    'COLORS', 'FONTS', 'LAYOUT', 'DASHBOARD_STYLES',
    'get_metric_card_style', 'get_chart_layout_template',
    'get_bar_chart_style', 'get_pie_chart_style', 'get_table_style',
    'apply_theme_mode', 'get_responsive_style'
]
