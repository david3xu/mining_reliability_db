#!/usr/bin/env python3
"""
Facility Detail Components - Pure Adapter Dependencies
Facility-specific analysis components with clean adapter integration.
"""

import logging

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dash_table, dcc, html

from dashboard.adapters import get_config_adapter, get_facility_adapter
from dashboard.components.micro.chart_base import create_pie_chart
from dashboard.components.micro.metric_card import create_metric_card

logger = logging.getLogger(__name__)


def create_facility_metrics_cards(facility_id: str) -> list:
    """Facility-specific metrics using adapter data"""
    try:
        facility_adapter = get_facility_adapter()
        config_adapter = get_config_adapter()

        facility_analysis = facility_adapter.get_facility_performance_analysis(facility_id)
        comparison_metrics = facility_adapter.get_facility_comparison_metrics(facility_id)

        if not facility_analysis:
            return []

        cards = [
            create_metric_card(
                value=facility_analysis.get("total_records", 0),
                label="Total Records",
                clickable=False,
            ),
            create_metric_card(
                value=facility_analysis.get("categories_count", 0),
                label="Issue Categories",
                clickable=False,
            ),
            create_metric_card(
                value=f"#{comparison_metrics.get('performance_rank', 0)}",
                label="Performance Rank",
                clickable=False,
            ),
            create_metric_card(
                value=f"{comparison_metrics.get('vs_average', 0):+.1f}%",
                label="vs Average",
                clickable=False,
            ),
        ]

        return cards

    except Exception as e:
        config_adapter.handle_error_utility(
            logger, e, f"facility metrics cards creation for {facility_id}"
        )
        return []


def create_facility_category_chart(facility_id: str) -> dcc.Graph:
    """Category distribution chart for facility"""
    try:
        facility_adapter = get_facility_adapter()
        config_adapter = get_config_adapter()

        facility_analysis = facility_adapter.get_facility_performance_analysis(facility_id)

        if not facility_analysis or not facility_analysis.get("category_distribution"):
            return dcc.Graph(figure={})

        category_dist = facility_analysis["category_distribution"]
        labels = list(category_dist.keys())
        values = list(category_dist.values())

        return create_pie_chart(labels, values, f"{facility_id} Issue Categories")

    except Exception as e:
        config_adapter.handle_error_utility(
            logger, e, f"facility category chart creation for {facility_id}"
        )
        return dcc.Graph(figure={})


def create_recurring_issues_analysis(facility_id: str) -> dcc.Graph:
    """Recurring issues analysis chart"""
    try:
        facility_adapter = get_facility_adapter()
        config_adapter = get_config_adapter()

        causal_data = facility_adapter.get_facility_causal_intelligence(facility_id)
        chart_config = config_adapter.get_chart_styling_template()

        if not causal_data or not causal_data.get("causal_patterns"):
            return dcc.Graph(figure={})

        patterns = causal_data["causal_patterns"][:10]  # Top 10

        causes = [p.get("primary_cause", "Unknown") for p in patterns]
        frequencies = [p.get("frequency", 0) for p in patterns]

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=frequencies,
                y=causes,
                orientation="h",
                marker_color=chart_config.get("colors", ["#4A90E2"])[0],
            )
        )

        fig.update_layout(
            title=f"{facility_id} - Top Recurring Issues",
            xaxis_title="Frequency",
            yaxis_title="Root Cause",
            height=chart_config.get("height", 400),
            font={"family": chart_config.get("font_family", "Arial")},
            paper_bgcolor=chart_config.get("background", "#FFFFFF"),
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        config_adapter.handle_error_utility(
            logger, e, f"recurring issues analysis for {facility_id}"
        )
        return dcc.Graph(figure={})


def create_operating_centre_table(facility_id: str) -> dash_table.DataTable:
    """Operating centre performance table"""
    try:
        facility_adapter = get_facility_adapter()
        config_adapter = get_config_adapter()

        causal_data = facility_adapter.get_facility_causal_intelligence(facility_id)
        styling = config_adapter.get_styling_config()

        if not causal_data or not causal_data.get("causal_patterns"):
            return dash_table.DataTable(data=[])

        # Process causal patterns for table display
        patterns = causal_data["causal_patterns"]
        table_data = []

        for pattern in patterns[:20]:  # Top 20
            table_data.append(
                {
                    "Primary Cause": pattern.get("primary_cause", "Unknown"),
                    "Secondary Cause": pattern.get("secondary_cause", "N/A"),
                    "Category": pattern.get("category", "General"),
                    "Frequency": pattern.get("frequency", 0),
                    "Impact": "High"
                    if pattern.get("frequency", 0) > 5
                    else "Medium"
                    if pattern.get("frequency", 0) > 2
                    else "Low",
                }
            )

        return dash_table.DataTable(
            data=table_data,
            columns=[
                {"name": "Primary Cause", "id": "Primary Cause"},
                {"name": "Secondary Cause", "id": "Secondary Cause"},
                {"name": "Category", "id": "Category"},
                {"name": "Frequency", "id": "Frequency", "type": "numeric"},
                {"name": "Impact", "id": "Impact"},
            ],
            style_cell={"textAlign": "left", "padding": "12px"},
            style_header={
                "backgroundColor": styling.get("primary_color", "#4A90E2"),
                "color": "white",
                "fontWeight": "bold",
            },
            style_data={"backgroundColor": "white"},
            style_data_conditional=[
                {"if": {"filter_query": "{Impact} = High"}, "backgroundColor": "#FFE6E6"},
                {"if": {"filter_query": "{Impact} = Low"}, "backgroundColor": "#E6F7FF"},
            ],
            sort_action="native",
            page_size=10,
        )

    except Exception as e:
        config_adapter.handle_error_utility(
            logger, e, f"operating centre table creation for {facility_id}"
        )
        return dash_table.DataTable(data=[])


def create_facility_detail_layout(facility_id: str) -> html.Div:
    """Complete facility detail layout"""
    try:
        facility_adapter = get_facility_adapter()
        config_adapter = get_config_adapter()

        # Validate facility exists
        validation = facility_adapter.validate_facility_data(facility_id)
        if not validation.get("facility_exists", False):
            return dbc.Container(
                [
                    dbc.Alert(
                        [
                            html.H4("Facility Not Found"),
                            html.P(f"Facility '{facility_id}' does not exist or has no data"),
                            dbc.Button("Return to Portfolio", href="/", color="primary"),
                        ],
                        color="warning",
                    )
                ]
            )

        # Get facility info
        facility_analysis = facility_adapter.get_facility_performance_analysis(facility_id)
        facility_name = facility_analysis.get("facility_name", facility_id)

        return html.Div(
            [
                # Header with back navigation
                dbc.Container(
                    [
                        dbc.Button(
                            "← Back to Portfolio",
                            href="/",
                            color="secondary",
                            size="sm",
                            className="mb-3",
                        ),
                        html.H2(
                            f"{facility_name} - Detailed Analysis", className="text-primary mb-4"
                        ),
                    ],
                    fluid=True,
                ),
                # Metrics cards
                html.Div(
                    [
                        html.H4("Performance Metrics", className="mb-3"),
                        html.Div(
                            create_facility_metrics_cards(facility_id),
                            className="d-flex justify-content-around flex-wrap gap-3 mb-4",
                        ),
                    ],
                    className="mb-5",
                ),
                # Analysis charts
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H5("Category Distribution", className="mb-3"),
                                create_facility_category_chart(facility_id),
                            ],
                            md=6,
                        ),
                        dbc.Col(
                            [
                                html.H5("Recurring Issues", className="mb-3"),
                                create_recurring_issues_analysis(facility_id),
                            ],
                            md=6,
                        ),
                    ],
                    className="mb-5",
                ),
                # Detailed analysis table
                html.Div(
                    [
                        html.H5("Root Cause Analysis", className="mb-3"),
                        create_operating_centre_table(facility_id),
                    ],
                    className="mb-4",
                ),
            ],
            className="container-fluid p-4",
        )

    except Exception as e:
        config_adapter.handle_error_utility(
            logger, e, f"facility detail layout creation for {facility_id}"
        )
        return dbc.Container(
            [
                dbc.Alert(
                    [
                        html.H4("Analysis Error"),
                        html.P(f"Failed to load analysis for facility: {facility_id}"),
                        dbc.Button("Return to Portfolio", href="/", color="secondary"),
                    ],
                    color="danger",
                )
            ]
        )
