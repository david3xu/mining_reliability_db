#!/usr/bin/env python3
"""
Interactive Elements - Reusable Interactive Components
Clean interactive components for dashboard enhancement.
"""

import logging
from typing import Dict, List, Any, Optional
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from dashboard.utils.data_transformers import get_styling_config, get_chart_config
from dashboard.utils.url_builders import build_facility_url, build_detail_url
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)

def create_interactive_metric_card(metric_data: Dict[str, Any], card_id: str) -> dbc.Card:
    """Create clickable metric card with hover effects"""
    try:
        styling_config = get_styling_config()
        chart_config = get_chart_config()

        value = metric_data.get("value", 0)
        label = metric_data.get("label", "Unknown")
        detail = metric_data.get("detail", "")

        # Format display value
        display_value = f"{value:,}" if isinstance(value, int) and value > 999 else str(value)

        # Card content with click interaction
        card_content = [
            html.H2(
                display_value,
                style={
                    "fontSize": "32px",
                    "fontWeight": "bold",
                    "margin": "0",
                    "color": styling_config.get("text_light", "#FFFFFF")
                }
            ),
            html.P(
                label,
                style={
                    "fontSize": "14px",
                    "margin": "5px 0 0 0",
                    "color": styling_config.get("text_light", "#FFFFFF"),
                    "opacity": "0.9"
                }
            )
        ]

        # Add detail if available
        if detail:
            card_content.append(
                html.Small(
                    detail,
                    style={
                        "fontSize": "12px",
                        "color": styling_config.get("text_light", "#FFFFFF"),
                        "opacity": "0.8"
                    }
                )
            )

        # Interactive card with hover effects
        return dbc.Card(
            dbc.CardBody(card_content),
            id=card_id,
            style={
                "backgroundColor": styling_config.get("primary_color", "#4A90E2"),
                "color": styling_config.get("text_light", "#FFFFFF"),
                "padding": "20px",
                "borderRadius": "8px",
                "textAlign": "center",
                "height": "140px",  # Slightly taller for click hint
                "width": chart_config.get("metric_card_width", 220),
                "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                "margin": "15px",
                "cursor": "pointer",
                "transition": "all 0.3s ease",
                "border": "2px solid transparent"
            },
            className="metric-card-interactive"
        )

    except Exception as e:
        handle_error(logger, e, "interactive metric card creation")
        return dbc.Card([html.P("Error loading metric")])

def create_interactive_pie_chart(facility_data: Dict[str, Any]) -> dcc.Graph:
    """Create clickable pie chart with enhanced interactivity"""
    try:
        styling_config = get_styling_config()
        chart_config = get_chart_config()

        if not facility_data:
            return dcc.Graph(figure={})

        # Enhanced pie chart with click interactions
        fig = go.Figure()

        # Add hover and click enhancements
        hover_template = (
            "<b>%{label}</b><br>"
            "Records: %{value}<br>"
            "Percentage: %{percent}"
            "<extra></extra>"
        )

        fig.add_trace(go.Pie(
            labels=facility_data.get("labels", []),
            values=facility_data.get("values", []),
            marker=dict(
                colors=styling_config.get("chart_colors", ["#4A90E2", "#F5A623", "#7ED321", "#B57EDC"]),
                line=dict(color=styling_config.get("background_light", "#FFFFFF"), width=3)
            ),
            textfont=dict(
                size=chart_config.get("body_font_size", 14),
                color=styling_config.get("text_light", "#FFFFFF")
            ),
            textposition="inside",
            textinfo="label+percent",
            hovertemplate=hover_template,
            # Enable click interactions
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.8)",
                font_size=12,
                font_family=chart_config.get("font_family", "Arial, sans-serif")
            )
        ))

        # Enhanced layout with interaction hints
        fig.update_layout(
            title={
                "text": "Records Distribution by Site",
                "font": {
                    "family": chart_config.get("font_family", "Arial, sans-serif"),
                    "size": chart_config.get("title_font_size", 18),
                    "color": styling_config.get("text_primary", "#333333")
                },
                "x": 0.5,
                "xanchor": "center"
            },
            paper_bgcolor=styling_config.get("background_light", "#FFFFFF"),
            plot_bgcolor=styling_config.get("background_light", "#FFFFFF"),
            height=chart_config.get("default_height", 400),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            ),
            # Add subtle animation
            transition_duration=500
        )

        return dcc.Graph(
            id="facility-pie-chart",
            figure=fig,
            config={
                'displayModeBar': True,
                'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                'displaylogo': False,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'facility_distribution',
                    'height': 500,
                    'width': 700,
                    'scale': 1
                }
            },
            style={"height": f"{chart_config.get('default_height', 400)}px"}
        )

    except Exception as e:
        handle_error(logger, e, "interactive pie chart creation")
        return dcc.Graph(figure={})

def create_interactive_bar_chart(field_data: Dict[str, Any]) -> dcc.Graph:
    """Create clickable bar chart with enhanced interactivity"""
    try:
        styling_config = get_styling_config()
        chart_config = get_chart_config()

        if not field_data:
            return dcc.Graph(figure={})

        fig = go.Figure()

        # Enhanced hover template
        hover_template = (
            "<b>%{x}</b><br>"
            "Count: %{y}<br>"
            "Percentage: %{text}<br>"
            "<i>Click to analyze field type</i>"
            "<extra></extra>"
        )

        fig.add_trace(go.Bar(
            x=field_data.get("labels", []),
            y=field_data.get("values", []),
            text=[f"{p}%" for p in field_data.get("percentages", [])],
            textposition="outside",
            marker=dict(
                color=styling_config.get("chart_colors", ["#4A90E2"])[0],
                line=dict(color=styling_config.get("border_color", "#CCCCCC"), width=1),
                # Add hover highlighting
                opacity=0.8
            ),
            hovertemplate=hover_template,
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.8)",
                font_size=12,
                font_family=chart_config.get("font_family", "Arial, sans-serif")
            )
        ))

        # Enhanced layout
        fig.update_layout(
            title={
                "text": "Data Types Distribution",
                "font": {
                    "family": chart_config.get("font_family", "Arial, sans-serif"),
                    "size": chart_config.get("title_font_size", 18),
                    "color": styling_config.get("text_primary", "#333333")
                },
                "x": 0.5,
                "xanchor": "center"
            },
            paper_bgcolor=styling_config.get("background_light", "#FFFFFF"),
            plot_bgcolor=styling_config.get("background_light", "#FFFFFF"),
            xaxis={
                "title": "Field Type Category",
                "tickangle": -45,
                "tickfont": {"size": chart_config.get("caption_font_size", 12)}
            },
            yaxis={
                "title": "Number of Fields",
                "tickfont": {"size": chart_config.get("caption_font_size", 12)}
            },
            height=chart_config.get("default_height", 400),
            showlegend=False,
            transition_duration=500
        )

        return dcc.Graph(
            id="field-bar-chart",
            figure=fig,
            config={
                'displayModeBar': True,
                'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                'displaylogo': False,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'field_distribution',
                    'height': 500,
                    'width': 700,
                    'scale': 1
                }
            },
            style={"height": f"{chart_config.get('default_height', 400)}px"}
        )

    except Exception as e:
        handle_error(logger, e, "interactive bar chart creation")
        return dcc.Graph(figure={})

def create_interactive_timeline_table(timeline_data: Dict[str, Any]) -> dash_table.DataTable:
    """Create clickable timeline table with enhanced interactivity"""
    try:
        styling_config = get_styling_config()
        chart_config = get_chart_config()

        if not timeline_data:
            return dash_table.DataTable(data=[])

        columns = timeline_data.get("columns", [])
        rows = timeline_data.get("rows", [])

        # Create enhanced column definitions
        table_columns = []
        for col in columns:
            column_def = {
                "name": col.title(),
                "id": col,
                "type": "numeric" if col != "facility" else "text"
            }

            # Special formatting for facility column
            if col == "facility":
                column_def.update({
                    "presentation": "markdown",
                    "type": "text"
                })

            table_columns.append(column_def)

        # Enhanced table with interaction support
        return dash_table.DataTable(
            id="historical-timeline-table",
            columns=table_columns,
            data=rows,
            style_cell={
                "textAlign": "center",
                "padding": "12px",
                "fontFamily": chart_config.get("font_family", "Arial, sans-serif"),
                "fontSize": chart_config.get("body_font_size", 14),
                "border": f"1px solid {styling_config.get('border_color', '#CCCCCC')}",
                "cursor": "pointer"  # Indicate clickability
            },
            style_header={
                "backgroundColor": styling_config.get("primary_color", "#4A90E2"),
                "color": styling_config.get("text_light", "#FFFFFF"),
                "fontWeight": "bold",
                "border": f"1px solid {styling_config.get('primary_color', '#4A90E2')}"
            },
            style_data={
                "backgroundColor": styling_config.get("background_light", "#FFFFFF"),
                "color": styling_config.get("text_primary", "#333333")
            },
            style_data_conditional=[
                {
                    "if": {"row_index": len(rows) - 1},  # Totals row
                    "backgroundColor": styling_config.get("light_blue", "#7BB3F0"),
                    "color": styling_config.get("text_light", "#FFFFFF"),
                    "fontWeight": "bold"
                },
                {
                    "if": {"column_id": "facility"},
                    "textAlign": "left",
                    "fontWeight": "bold"
                },
                # Hover effect for data rows
                {
                    "if": {"state": "active"},
                    "backgroundColor": styling_config.get("light_blue", "#7BB3F0"),
                    "border": f"2px solid {styling_config.get('primary_color', '#4A90E2')}"
                }
            ],
            # Enhanced interaction settings
            sort_action="native",
            filter_action="native",
            page_action="none",
            fixed_rows={"headers": True},
            cell_selectable=True,
            row_selectable="single",
            selected_cells=[],
            active_cell=None,
            style_table={
                "height": f"{chart_config.get('table_height', 300)}px",
                "overflowY": "auto",
                "border": f"1px solid {styling_config.get('border_color', '#CCCCCC')}",
                "borderRadius": "8px"
            }
        )

    except Exception as e:
        handle_error(logger, e, "interactive timeline table creation")
        return dash_table.DataTable(data=[])

def create_interaction_feedback_toast():
    """Create toast notifications for user feedback"""
    return dbc.Toast(
        id="interaction-toast",
        header="Navigation",
        is_open=False,
        dismissable=True,
        icon="info",
        duration=3000,
        style={"position": "fixed", "top": 10, "right": 10, "width": 350, "zIndex": 9999}
    )

def create_loading_overlay():
    """Create loading overlay for interactions"""
    return dcc.Loading(
        id="interaction-loading",
        type="default",
        children=[html.Div(id="interaction-loading-output")],
        style={"position": "absolute", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)"}
    )
