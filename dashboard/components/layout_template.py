#!/usr/bin/env python3
"""
Layout Template Infrastructure - Standardized Component Patterns
Direct template system with adapter-driven configuration.
"""

from typing import Any, List

import dash_bootstrap_components as dbc
from dash import html

from dashboard.adapters import get_config_adapter
from dashboard.utils.styling import get_colors, get_dashboard_styles

__all__ = [
    "create_metrics_row",
    "create_main_grid",
    "create_summary_section",
    "create_standard_layout",
    "create_metric_card",
    "create_tab_header",
    "get_tab_metadata",
    "create_chart_container",
    "create_empty_state",
    "get_layout_config",
]


def create_metrics_row(metric_cards: List[Any]) -> dbc.Row:
    """Standard metrics row layout"""
    return dbc.Row(
        [
            dbc.Col(
                [html.Div(metric_cards, className="d-flex justify-content-around flex-wrap gap-3")],
                width=12,
            )
        ],
        className="mb-4",
    )


def create_main_grid(left_component: Any, right_component: Any) -> dbc.Row:
    """Standard 2-column content grid"""
    return dbc.Row(
        [
            dbc.Col([left_component], md=6, className="mb-3"),
            dbc.Col([right_component], md=6, className="mb-3"),
        ],
        className="mb-4",
    )


def create_summary_section(summary_component: Any, title: str = "Analysis Summary") -> html.Div:
    """Standard bottom summary section"""
    colors = get_colors()
    return html.Div(
        [
            html.H3(title, className="mb-3", style={"color": colors.get("text_secondary")}),
            summary_component,
        ],
        className="rounded p-4",
        style={
            "backgroundColor": colors.get("background_secondary"),
            "boxShadow": colors.get("shadow_light"),
        },
    )


def create_standard_layout(
    title: str,
    content_cards: List[Any],
) -> html.Div:
    """Complete standardized layout template with dynamic content cards"""
    colors = get_colors()
    dashboard_styles = get_dashboard_styles()

    return html.Div(
        [
            html.H2(
                title,
                className="text-center mb-4",
                style={
                    "color": colors.get("text_primary"),
                    "fontSize": dashboard_styles.get("title_font_size", "2.5rem"),
                },
            ),
            html.Div(content_cards, className="d-flex flex-column gap-4"),
        ],
        className="container-fluid p-4",
        style={
            "backgroundColor": colors.get("background_dark"),
            "minHeight": "100vh",
        },
    )


def create_metric_card(value: Any, label: str, detail: str = "", color: str = None) -> dbc.Card:
    """Standard metric card with adapter styling"""
    config_adapter = get_config_adapter()
    styling = config_adapter.get_metric_card_styling()

    card_color = color or styling.get("primary_color", "#4A90E2")
    display_value = f"{value:,}" if isinstance(value, int) and value > 999 else str(value)

    content = [
        html.H2(
            display_value,
            className="text-white mb-1",
            style={"fontSize": "32px", "fontWeight": "bold"},
        ),
        html.P(label, className="text-white-50 mb-0", style={"fontSize": "14px"}),
    ]

    if detail:
        content.append(html.Small(detail, className="text-white-50", style={"fontSize": "12px"}))

    return dbc.Card(
        dbc.CardBody(content),
        style={
            "backgroundColor": card_color,
            "height": f"{styling.get('card_height', 120)}px",
            "width": f"{styling.get('card_width', 220)}px",
            "borderRadius": "8px",
            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
        },
        className="text-center d-flex align-items-center justify-content-center",
    )


def create_tab_header(tab_id: str) -> html.Div:
    """Standard tab header with metadata"""
    metadata = get_tab_metadata(tab_id)

    return html.Div(
        [
            html.H1(
                metadata.get("title", "Analysis Dashboard"),
                className="text-primary mb-2",
                style={"fontSize": "28px", "fontWeight": "bold"},
            ),
            html.H4(
                metadata.get("subtitle", "Data Analysis"),
                className="text-muted mb-4",
                style={"fontSize": "18px", "fontWeight": "normal"},
            ),
        ],
        className="text-center p-4 bg-dark text-white rounded mb-4",
    )


def get_tab_metadata(tab_id: str) -> dict:
    """Tab metadata definitions"""
    metadata = {
        "portfolio": {
            "title": "Portfolio Overview - Data Inventory",
            "subtitle": "Comprehensive Analysis Across Operational Facilities",
        },
        "quality": {
            "title": "Data Quality Foundation - Problem Identification",
            "subtitle": "Field Completeness and Categorical Value Analysis",
        },
        "workflow": {
            "title": "Workflow Understanding - Process Organization",
            "subtitle": "Field Mapping Across Core Process Stages",
        },
    }
    return metadata.get(tab_id, {"title": "Analysis Dashboard", "subtitle": "Data Analysis"})


def create_chart_container(chart_component: Any, title: str) -> html.Div:
    """Standard chart container with title"""
    return html.Div(
        [html.H5(title, className="mb-3 text-secondary"), chart_component],
        className="bg-white rounded p-3 shadow-sm",
    )


def create_empty_state(message: str = "No data available") -> html.Div:
    """Standard empty state component"""
    return html.Div(
        [
            html.I(className="fas fa-chart-bar fa-3x text-muted mb-3"),
            html.H5(message, className="text-muted"),
            html.P("Check data source and retry", className="text-muted small"),
        ],
        className="text-center p-5 bg-light rounded",
    )


def get_layout_config() -> dict:
    """Layout configuration from adapter"""
    config_adapter = get_config_adapter()
    styling = config_adapter.get_styling_config()
    chart = config_adapter.get_chart_config()

    return {
        "colors": {
            "primary": styling.get("primary_color", "#4A90E2"),
            "success": "#7ED321",
            "warning": "#F5A623",
            "info": "#B57EDC",
        },
        "dimensions": {
            "metric_card_height": chart.get("metric_card_height", 120),
            "metric_card_width": chart.get("metric_card_width", 220),
            "chart_height": chart.get("default_height", 400),
        },
    }
