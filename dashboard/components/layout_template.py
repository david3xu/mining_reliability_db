#!/usr/bin/env python3
"""
Standardized Layout Template
Uniform grid layout for all dashboard tabs.
"""

from dash import html
import dash_bootstrap_components as dbc
from typing import List, Any, Optional
from dashboard.utils.style_constants import PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, INFO_COLOR

def create_metrics_row(metric_cards: List[Any]) -> dbc.Row:
    """Create standardized metrics row with 4 cards"""

    return dbc.Row([
        dbc.Col([
            html.Div(
                metric_cards,
                className="d-flex justify-content-around flex-wrap gap-3"
            )
        ], width=12)
    ], className="mb-4")

def create_main_grid(left_component: Any, right_component: Any) -> dbc.Row:
    """Create standardized 2-column main content grid"""

    return dbc.Row([
        dbc.Col([
            left_component
        ], md=6, className="mb-3"),
        dbc.Col([
            right_component
        ], md=6, className="mb-3")
    ], className="mb-4")

def create_summary_section(summary_component: Any, title: str = "Summary Analysis") -> html.Div:
    """Create standardized bottom summary section"""

    return html.Div([
        html.H3(title, className="mb-3 text-secondary"),
        summary_component
    ], className="bg-light rounded p-4")

def create_standard_layout(
    tab_id: str,
    metric_cards: List[Any],
    left_component: Any,
    right_component: Any,
    summary_component: Any,
    summary_title: str = "Summary Analysis"
) -> html.Div:
    """
    Create complete standardized layout for any tab.

    Layout Pattern:
    - Header (title + subtitle)
    - Metrics Row (4 cards)
    - Main Grid (left | right components)
    - Summary Section (bottom component)
    """

    from dashboard.components.tab_navigation import create_tab_header

    return html.Div([
        # Header Section
        create_tab_header(tab_id),

        # Metrics Cards Row
        create_metrics_row(metric_cards),

        # Main Content Grid
        create_main_grid(left_component, right_component),

        # Summary Section
        create_summary_section(summary_component, summary_title)

    ], className="container-fluid")

def create_metric_card(
    value: Any,
    label: str,
    detail: str = "",
    color: str = None
) -> dbc.Card:
    """Create standardized metric card with config-driven colors"""

    # Get color from configuration if not provided
    if color is None:
        try:
            from configs.environment import get_dashboard_styling_config
            styling_config = get_dashboard_styling_config()
            color = styling_config.get("primary_color", PRIMARY_COLOR)
        except Exception:
            color = PRIMARY_COLOR  # Fallback

    display_value = f"{value:,}" if isinstance(value, int) and value > 999 else str(value)

    card_content = [
        html.H2(
            display_value,
            className="text-white mb-1",
            style={"fontSize": "32px", "fontWeight": "bold"}
        ),
        html.P(
            label,
            className="text-white-50 mb-0",
            style={"fontSize": "14px"}
        )
    ]

    if detail:
        card_content.append(
            html.Small(
                detail,
                className="text-white-50",
                style={"fontSize": "12px"}
            )
        )

    return dbc.Card(
        dbc.CardBody(card_content),
        style={
            "backgroundColor": color,
            "height": "120px",
            "width": "220px",
            "borderRadius": "8px",
            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
        },
        className="text-center d-flex align-items-center justify-content-center"
    )

def create_chart_container(chart_component: Any, title: str) -> html.Div:
    """Create standardized chart container with title"""

    return html.Div([
        html.H5(title, className="mb-3 text-secondary"),
        chart_component
    ], className="bg-white rounded p-3 shadow-sm")

def create_empty_state(message: str = "No data available") -> html.Div:
    """Create standardized empty state component"""

    return html.Div([
        html.I(className="fas fa-chart-bar fa-3x text-muted mb-3"),
        html.H5(message, className="text-muted"),
        html.P("Check data source and try again", className="text-muted small")
    ], className="text-center p-5 bg-light rounded")

def create_loading_state(message: str = "Loading analysis...") -> html.Div:
    """Create standardized loading state"""

    return html.Div([
        dbc.Spinner(size="lg", color="primary"),
        html.P(message, className="mt-3 text-muted")
    ], className="text-center p-5")

def get_layout_config() -> dict:
    """Get standardized layout configuration from centralized config"""
    try:
        from configs.environment import get_dashboard_styling_config, get_dashboard_chart_config
        styling_config = get_dashboard_styling_config()
        chart_config = get_dashboard_chart_config()

        return {
            "colors": {
                "primary": styling_config.get("primary_color", PRIMARY_COLOR),
                "secondary": styling_config.get("chart_colors", [PRIMARY_COLOR, SECONDARY_COLOR])[1] if len(styling_config.get("chart_colors", [])) > 1 else SECONDARY_COLOR,
                "success": styling_config.get("chart_colors", [PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR])[2] if len(styling_config.get("chart_colors", [])) > 2 else SUCCESS_COLOR,
                "info": styling_config.get("chart_colors", [PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, INFO_COLOR])[3] if len(styling_config.get("chart_colors", [])) > 3 else INFO_COLOR
            },
            "spacing": {
                "card_gap": "15px",
                "section_margin": "30px",
                "container_padding": "20px"
            },
            "dimensions": {
                "metric_card_height": f"{chart_config.get('metric_card_height', 120)}px",
                "metric_card_width": f"{chart_config.get('metric_card_width', 220)}px",
                "chart_height": f"{chart_config.get('default_height', 400)}px"
            }
        }
    except Exception as e:
        # Fallback to prevent breaking if config unavailable
        return {
            "colors": {
                "primary": PRIMARY_COLOR,
                "secondary": SECONDARY_COLOR,
                "success": SUCCESS_COLOR,
                "info": INFO_COLOR
            },
            "spacing": {
                "card_gap": "15px",
                "section_margin": "30px",
                "container_padding": "20px"
            },
            "dimensions": {
                "metric_card_height": "120px",
                "metric_card_width": "220px",
                "chart_height": "400px"
            }
        }