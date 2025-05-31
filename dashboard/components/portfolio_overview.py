#!/usr/bin/env python3
"""
Portfolio Overview Component - Adapter Integration
Clean component implementation using data adapter pattern.
"""

import logging
from typing import Dict, List, Any

# Dash components
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Use adapter instead of direct mine_core access
from dashboard.utils.data_transformers import (
    get_portfolio_metrics,
    get_field_distribution_data,
    get_facility_breakdown_data,
    get_historical_timeline_data,
    validate_dashboard_data
)

# Configuration-driven styling
from configs.environment import get_dashboard_styling_config, get_dashboard_chart_config
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)

def create_metrics_cards() -> List[dbc.Card]:
    """Create 4 metric cards using adapter data"""
    try:
        logger.info("Creating portfolio metrics cards...")

        # Get styling configuration
        styling_config = get_dashboard_styling_config()
        chart_config = get_dashboard_chart_config()

        # Get data via adapter
        metrics_data = get_portfolio_metrics()

        if not metrics_data:
            logger.warning("No metrics data available")
            return []

        cards = []
        card_order = ["total_records", "data_fields", "facilities", "years_coverage"]

        for metric_key in card_order:
            metric_info = metrics_data.get(metric_key, {})
            value = metric_info.get("value", 0)
            label = metric_info.get("label", "Unknown")
            detail = metric_info.get("detail", "")

            # Format display value
            display_value = f"{value:,}" if isinstance(value, int) and value > 999 else str(value)

            # Create card content
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

            # Create card with configuration-driven styling
            card = dbc.Card(
                dbc.CardBody(card_content),
                style={
                    "backgroundColor": styling_config.get("primary_color", "#4A90E2"),
                    "color": styling_config.get("text_light", "#FFFFFF"),
                    "padding": "20px",
                    "borderRadius": "8px",
                    "textAlign": "center",
                    "height": chart_config.get("metric_card_height", 120),
                    "width": chart_config.get("metric_card_width", 220),
                    "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                    "margin": "15px"
                },
                className="text-center shadow-sm"
            )

            cards.append(card)

        logger.info(f"Created {len(cards)} metric cards")
        return cards

    except Exception as e:
        handle_error(logger, e, "metrics cards creation")
        return []

def create_field_distribution_chart() -> dcc.Graph:
    """Create field distribution bar chart using adapter data"""
    try:
        logger.info("Creating field distribution chart...")

        # Get configuration
        styling_config = get_dashboard_styling_config()
        chart_config = get_dashboard_chart_config()

        # Get data via adapter
        field_data = get_field_distribution_data()

        if not field_data:
            logger.warning("No field distribution data available")
            return dcc.Graph(figure={})

        # Create bar chart
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=field_data.get("labels", []),
            y=field_data.get("values", []),
            text=[f"{v} ({p}%)" for v, p in zip(
                field_data.get("values", []),
                field_data.get("percentages", [])
            )],
            textposition="outside",
            marker=dict(
                color=styling_config.get("chart_colors", ["#4A90E2"])[0],
                line=dict(color="#CCCCCC", width=1)
            ),
            hovertemplate="<b>%{x}</b><br>Count: %{y}<br>Percentage: %{text}<extra></extra>"
        ))

        # Apply configuration-driven layout
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
            font={
                "family": chart_config.get("font_family", "Arial, sans-serif"),
                "size": chart_config.get("body_font_size", 14),
                "color": styling_config.get("text_primary", "#333333")
            },
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
            showlegend=False
        )

        return dcc.Graph(
            figure=fig,
            config={"displayModeBar": False},
            style={"height": f"{chart_config.get('default_height', 400)}px"}
        )

    except Exception as e:
        handle_error(logger, e, "field distribution chart creation")
        return dcc.Graph(figure={})

def create_facility_pie_chart() -> dcc.Graph:
    """Create facility pie chart using adapter data"""
    try:
        logger.info("Creating facility pie chart...")

        # Get configuration
        styling_config = get_dashboard_styling_config()
        chart_config = get_dashboard_chart_config()

        # Get data via adapter
        facility_data = get_facility_breakdown_data()

        if not facility_data:
            logger.warning("No facility breakdown data available")
            return dcc.Graph(figure={})

        # Create pie chart
        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=facility_data.get("labels", []),
            values=facility_data.get("values", []),
            marker=dict(
                colors=styling_config.get("chart_colors", ["#4A90E2", "#F5A623", "#7ED321", "#B57EDC"]),
                line=dict(color=styling_config.get("background_light", "#FFFFFF"), width=2)
            ),
            textfont=dict(
                size=chart_config.get("body_font_size", 14),
                color=styling_config.get("text_light", "#FFFFFF")
            ),
            textposition="inside",
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>Records: %{value}<br>Percentage: %{percent}<extra></extra>"
        ))

        # Apply configuration-driven layout
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
            font={
                "family": chart_config.get("font_family", "Arial, sans-serif"),
                "size": chart_config.get("body_font_size", 14),
                "color": styling_config.get("text_primary", "#333333")
            },
            height=chart_config.get("default_height", 400),
            showlegend=True,
            legend={
                "orientation": "v",
                "yanchor": "middle",
                "y": 0.5,
                "xanchor": "left",
                "x": 1.05
            }
        )

        return dcc.Graph(
            figure=fig,
            config={"displayModeBar": False},
            style={"height": f"{chart_config.get('default_height', 400)}px"}
        )

    except Exception as e:
        handle_error(logger, e, "facility pie chart creation")
        return dcc.Graph(figure={})

def create_historical_table() -> dash_table.DataTable:
    """Create historical timeline table using adapter data"""
    try:
        logger.info("Creating historical timeline table...")

        # Get configuration
        styling_config = get_dashboard_styling_config()
        chart_config = get_dashboard_chart_config()

        # Get data via adapter
        timeline_data = get_historical_timeline_data()

        if not timeline_data:
            logger.warning("No timeline data available")
            return dash_table.DataTable(data=[])

        columns = timeline_data.get("columns", [])
        rows = timeline_data.get("rows", [])

        # Create column definitions
        table_columns = []
        for col in columns:
            column_def = {
                "name": col.title(),
                "id": col,
                "type": "numeric" if col != "facility" else "text"
            }

            if col == "facility":
                column_def.update({
                    "presentation": "markdown",
                    "type": "text"
                })

            table_columns.append(column_def)

        # Create DataTable with configuration-driven styling
        data_table = dash_table.DataTable(
            id="historical-timeline-table",
            columns=table_columns,
            data=rows,
            style_cell={
                "textAlign": "center",
                "padding": "12px",
                "fontFamily": chart_config.get("font_family", "Arial, sans-serif"),
                "fontSize": chart_config.get("body_font_size", 14),
                "border": f"1px solid {styling_config.get('border_color', '#CCCCCC')}"
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
                    "if": {"row_index": len(rows) - 1},
                    "backgroundColor": styling_config.get("light_blue", "#7BB3F0"),
                    "color": styling_config.get("text_light", "#FFFFFF"),
                    "fontWeight": "bold"
                },
                {
                    "if": {"column_id": "facility"},
                    "textAlign": "left",
                    "fontWeight": "bold"
                }
            ],
            sort_action="native",
            filter_action="native",
            page_action="none",
            fixed_rows={"headers": True},
            style_table={
                "height": f"{chart_config.get('table_height', 300)}px",
                "overflowY": "auto",
                "border": f"1px solid {styling_config.get('border_color', '#CCCCCC')}",
                "borderRadius": "8px"
            }
        )

        logger.info("Historical table created successfully")
        return data_table

    except Exception as e:
        handle_error(logger, e, "historical table creation")
        return dash_table.DataTable(data=[])

def create_complete_dashboard() -> html.Div:
    """Create complete dashboard using adapter pattern"""
    try:
        logger.info("Creating complete portfolio dashboard...")

        # Get configuration
        styling_config = get_dashboard_styling_config()
        chart_config = get_dashboard_chart_config()

        # Validate data before rendering
        validation_results = validate_dashboard_data()

        if not validation_results.get("phase2_complete", False):
            logger.warning("Data validation failed - showing error state")
            return html.Div([
                dbc.Alert([
                    html.H4("Data Validation Error", className="alert-heading"),
                    html.P("Dashboard data pipeline validation failed. Please check system status."),
                    html.Hr(),
                    html.P("Run system diagnostics to resolve issues.", className="mb-0")
                ], color="warning", dismissable=True)
            ], style={"padding": "50px"})

        # Create components
        metric_cards = create_metrics_cards()
        field_chart = create_field_distribution_chart()
        facility_chart = create_facility_pie_chart()
        timeline_table = create_historical_table()

        # Main layout with configuration-driven styling
        dashboard = html.Div([
            # Header section
            html.Div([
                html.H1(
                    "Portfolio Overview - What data do we have?",
                    style={
                        "fontSize": chart_config.get("title_font_size", 24),
                        "fontWeight": "bold",
                        "marginBottom": "10px",
                        "color": styling_config.get("text_light", "#FFFFFF")
                    }
                ),
                html.H4(
                    "Comprehensive Analysis Across 4 Operational Facilities",
                    style={
                        "fontSize": chart_config.get("subtitle_font_size", 18),
                        "fontWeight": "normal",
                        "margin": "0",
                        "color": styling_config.get("text_light", "#FFFFFF"),
                        "opacity": "0.9"
                    }
                )
            ], style={
                "textAlign": "center",
                "marginBottom": "30px",
                "padding": "20px",
                "backgroundColor": styling_config.get("background_dark", "#1E1E1E"),
                "color": styling_config.get("text_light", "#FFFFFF"),
                "borderRadius": "10px"
            }),

            # Metrics cards
            html.Div([
                html.H3(
                    "Key Portfolio Metrics",
                    style={
                        "textAlign": "center",
                        "marginBottom": "20px",
                        "color": styling_config.get("text_primary", "#333333"),
                        "fontSize": chart_config.get("subtitle_font_size", 18)
                    }
                ),
                html.Div(
                    metric_cards,
                    style={
                        "display": "flex",
                        "justifyContent": "space-around",
                        "flexWrap": "wrap",
                        "marginBottom": "30px",
                        "gap": "15px"
                    }
                )
            ], style={"marginBottom": "40px"}),

            # Charts section
            html.Div([
                html.Div([field_chart], style={"width": "48%", "display": "inline-block"}),
                html.Div([facility_chart], style={"width": "48%", "display": "inline-block", "marginLeft": "4%"})
            ], style={"marginBottom": "40px"}),

            # Timeline table
            html.Div([
                html.H3(
                    "Historical Records by Year",
                    style={
                        "marginBottom": "20px",
                        "color": styling_config.get("text_primary", "#333333"),
                        "fontSize": chart_config.get("subtitle_font_size", 18)
                    }
                ),
                timeline_table,
                html.P(
                    "Data spans multiple years with consistent field structure",
                    style={
                        "marginTop": "15px",
                        "fontSize": chart_config.get("caption_font_size", 12),
                        "color": styling_config.get("text_secondary", "#666666"),
                        "fontStyle": "italic",
                        "textAlign": "center"
                    }
                )
            ], style={
                "marginTop": "30px",
                "backgroundColor": styling_config.get("background_light", "#FFFFFF"),
                "borderRadius": "8px",
                "padding": "20px",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)"
            })

        ], style={
            "backgroundColor": styling_config.get("background_light", "#FFFFFF"),
            "padding": "20px",
            "fontFamily": chart_config.get("font_family", "Arial, sans-serif")
        })

        logger.info("Complete dashboard created successfully")
        return dashboard

    except Exception as e:
        handle_error(logger, e, "complete dashboard creation")
        return html.Div([
            dbc.Alert([
                html.H2("Dashboard Error", className="alert-heading"),
                html.P(f"Failed to initialize dashboard: {str(e)}"),
                html.P("Please contact system administrator.", className="mb-0")
            ], color="danger")
        ], style={"padding": "50px"})

def create_portfolio_layout() -> html.Div:
    """Legacy compatibility function that maps to create_complete_dashboard"""
    return create_complete_dashboard()
