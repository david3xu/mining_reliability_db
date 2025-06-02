#!/usr/bin/env python3
"""
Interactive Elements - Enhanced Component Interactions
Clickable components with adapter-driven configuration.
"""

from typing import Any, Dict, List

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dash_table, dcc, html

from dashboard.adapters import get_config_adapter
from mine_core.shared.common import handle_error


def create_interactive_metric_card(
    value: Any, label: str, href: str = None, card_id: str = None
) -> html.A:
    """Interactive metric card with click navigation"""
    config_adapter = get_config_adapter()
    styling = config_adapter.get_metric_card_styling()

    display_value = f"{value:,}" if isinstance(value, int) and value > 999 else str(value)

    card_content = [
        html.H2(
            display_value,
            style={"fontSize": "32px", "fontWeight": "bold", "margin": "0", "color": "#FFFFFF"},
        ),
        html.P(
            label,
            style={"fontSize": "14px", "margin": "5px 0 0 0", "color": "#FFFFFF", "opacity": "0.9"},
        ),
    ]

    card_style = {
        "backgroundColor": styling.get("primary_color", "#4A90E2"),
        "padding": "20px",
        "borderRadius": "8px",
        "textAlign": "center",
        "height": f"{styling.get('card_height', 120)}px",
        "width": f"{styling.get('card_width', 220)}px",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
        "textDecoration": "none",
        "cursor": "pointer",
        "transition": "transform 0.2s ease, box-shadow 0.2s ease",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
    }

    return html.A(
        card_content, href=href, style=card_style, id=card_id, className="metric-card-hover"
    )


def create_interactive_pie_chart(
    data: Dict[str, Any], chart_id: str = "interactive-pie"
) -> dcc.Graph:
    """Clickable pie chart with hover effects"""
    try:
        config_adapter = get_config_adapter()
        chart_config = config_adapter.get_chart_styling_template()

        fig = go.Figure()

        fig.add_trace(
            go.Pie(
                labels=data.get("labels", []),
                values=data.get("values", []),
                textinfo="label+percent",
                textposition="auto",
                marker=dict(
                    colors=chart_config.get("colors", ["#4A90E2", "#F5A623", "#7ED321", "#B57EDC"]),
                    line=dict(color="#FFFFFF", width=2),
                ),
                hovertemplate="<b>%{label}</b><br>Records: %{value}<br>Click to explore<extra></extra>",
            )
        )

        fig.update_layout(
            title="Facility Distribution (Click to Navigate)",
            height=chart_config.get("height", 400),
            font={"family": chart_config.get("font_family", "Arial"), "size": 14},
            paper_bgcolor=chart_config.get("background", "#FFFFFF"),
            showlegend=True,
        )

        return dcc.Graph(
            id=chart_id,
            figure=fig,
            config={
                "displayModeBar": True,
                "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
                "displaylogo": False,
            },
        )

    except Exception as e:
        handle_error("interactive_elements", e, "interactive pie chart creation")
        return dcc.Graph(figure={})


def create_interactive_bar_chart(
    data: Dict[str, Any], chart_id: str = "interactive-bar"
) -> dcc.Graph:
    """Clickable bar chart with analysis navigation"""
    try:
        config_adapter = get_config_adapter()
        chart_config = config_adapter.get_chart_styling_template()

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=data.get("labels", []),
                y=data.get("values", []),
                text=[f"{p}%" for p in data.get("percentages", [])],
                textposition="outside",
                marker=dict(
                    color=chart_config.get("colors", ["#4A90E2"])[0],
                    line=dict(color="#CCCCCC", width=1),
                ),
                hovertemplate="<b>%{x}</b><br>Count: %{y}<br>Click for analysis<extra></extra>",
            )
        )

        fig.update_layout(
            title="Data Types Distribution (Click to Analyze)",
            xaxis_title="Field Type",
            yaxis_title="Count",
            height=chart_config.get("height", 400),
            font={"family": chart_config.get("font_family", "Arial"), "size": 14},
            paper_bgcolor=chart_config.get("background", "#FFFFFF"),
        )

        return dcc.Graph(
            id=chart_id,
            figure=fig,
            config={
                "displayModeBar": True,
                "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
                "displaylogo": False,
            },
        )

    except Exception as e:
        handle_error("interactive_elements", e, "interactive bar chart creation")
        return dcc.Graph(figure={})


def create_interactive_data_table(
    data: List[Dict], columns: List[str], table_id: str = "interactive-table"
) -> dash_table.DataTable:
    """Clickable data table with facility navigation"""
    try:
        config_adapter = get_config_adapter()
        styling = config_adapter.get_styling_config()

        table_columns = [{"name": col, "id": col} for col in columns]

        return dash_table.DataTable(
            id=table_id,
            data=data,
            columns=table_columns,
            style_cell={
                "textAlign": "center",
                "padding": "12px",
                "fontFamily": "Arial, sans-serif",
                "fontSize": "14px",
                "border": f"1px solid {styling.get('border_color', '#CCCCCC')}",
                "cursor": "pointer",
            },
            style_header={
                "backgroundColor": styling.get("primary_color", "#4A90E2"),
                "color": "#FFFFFF",
                "fontWeight": "bold",
            },
            style_data={
                "backgroundColor": "#FFFFFF",
                "color": styling.get("text_primary", "#333333"),
            },
            style_data_conditional=[
                {
                    "if": {"state": "active"},
                    "backgroundColor": "#E3F2FD",
                    "border": f"2px solid {styling.get('primary_color', '#4A90E2')}",
                }
            ],
            sort_action="native",
            cell_selectable=True,
            row_selectable="single",
            page_size=10,
        )

    except Exception as e:
        handle_error("interactive_elements", e, "interactive data table creation")
        return dash_table.DataTable(data=[])


def create_navigation_toast() -> dbc.Toast:
    """Navigation feedback toast"""
    return dbc.Toast(
        id="navigation-toast",
        header="Navigation",
        is_open=False,
        dismissable=True,
        icon="info",
        duration=2000,
        style={"position": "fixed", "top": 10, "right": 10, "width": 300, "zIndex": 9999},
    )


def create_loading_overlay(loading_id: str = "page-loading") -> dcc.Loading:
    """Interactive loading overlay"""
    config_adapter = get_config_adapter()
    styling = config_adapter.get_styling_config()

    return dcc.Loading(
        id=loading_id,
        type="default",
        color=styling.get("primary_color", "#4A90E2"),
        children=[html.Div(id=f"{loading_id}-output")],
        style={"minHeight": "200px"},
    )
