#!/usr/bin/env python3
"""
Facility Detail Components - Pure Adapter Dependencies
Facility-specific analysis components with clean adapter integration.
"""

import logging

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dash_table, dcc, html

from dashboard.adapters import get_config_adapter, get_facility_adapter, handle_error_utility
from dashboard.components.layout_template import create_standard_layout
from dashboard.components.micro.chart_base import create_pie_chart
from dashboard.components.micro.metric_card import create_metric_card
from dashboard.utils.styling import (
    get_chart_layout_template,
    get_colors,
    get_fonts,
    get_table_style,
)

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
        handle_error_utility(logger, e, f"facility metrics cards creation for {facility_id}")
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
        handle_error_utility(logger, e, f"facility category chart creation for {facility_id}")
        return dcc.Graph(figure={})


def create_recurring_issues_analysis(facility_id: str) -> dcc.Graph:
    """Recurring issues analysis chart"""
    try:
        facility_adapter = get_facility_adapter()
        config_adapter = get_config_adapter()
        colors = get_colors()

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
                marker_color=colors.get("primary_color"),
            )
        )

        fig.update_layout(
            title=f"{facility_id} - Top Recurring Issues",
            xaxis_title="Frequency",
            yaxis_title="Root Cause",
            height=chart_config.get("height", 400),
            font={
                "family": chart_config.get("font_family", "Arial"),
                "color": colors.get("text_light"),
            },
            paper_bgcolor=colors.get("background_dark"),
            plot_bgcolor=colors.get("background_dark"),
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        handle_error_utility(logger, e, f"recurring issues analysis for {facility_id}")
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
            style_cell={
                "textAlign": "left",
                "padding": "12px",
                "backgroundColor": styling.get("background_light"),
                "color": styling.get("text_primary"),
                "border": f"1px solid {styling.get('border_color')}",
            },
            style_header={
                "backgroundColor": styling.get("primary_color"),
                "color": styling.get("text_light"),
                "fontWeight": "bold",
                "border": f"1px solid {styling.get('primary_color')}",
            },
            style_data={
                "backgroundColor": styling.get("background_light"),
                "color": styling.get("text_primary"),
            },
            style_data_conditional=[
                {
                    "if": {"filter_query": "{Impact} = High"},
                    "backgroundColor": styling.get("error_color"),
                    "color": styling.get("text_light"),
                },
                {
                    "if": {"filter_query": "{Impact} = Low"},
                    "backgroundColor": styling.get("info_color"),
                    "color": styling.get("text_light"),
                },
                {
                    "if": {"filter_query": "{Impact} = Medium"},
                    "backgroundColor": styling.get("warning_color"),
                    "color": styling.get("text_primary"),
                },
            ],
            sort_action="native",
            page_size=10,
        )

    except Exception as e:
        handle_error_utility(logger, e, f"operating centre table creation for {facility_id}")
        return dash_table.DataTable(data=[])


def create_facility_detail_layout(facility_name: str) -> html.Div:
    """Layout for a single facility detail page"""
    try:
        facility_adapter = get_facility_adapter()
        config_adapter = get_config_adapter()
        colors = get_colors()

        # Fetch facility data
        facility_data = facility_adapter.get_facility_statistics_analysis(facility_name)
        if not facility_data or facility_data.get("error"):
            return html.Div(
                html.P(
                    f'Could not load data for facility: {facility_name}. {facility_data.get("error", "")}'
                ),
                className="alert alert-warning",
            )

        # Data quality metrics for the facility
        quality_metrics = facility_data.get("completeness_metrics", {})
        entity_completeness = quality_metrics.get("entity_completeness", {})
        incident_summary = facility_data.get(
            "total_action_requests", 0
        )  # This is a placeholder as incident_summary is not directly available
        action_summary = {}  # This is a placeholder as action_summary is not directly available

        # Extract relevant metrics for cards
        overall_score = quality_metrics.get("overall_score", 0.0)
        total_incidents = incident_summary
        open_actions = 0  # This is a placeholder

        metrics = [
            create_metric_card(f"{overall_score:.1f}%", "Overall Quality Score"),
            create_metric_card(total_incidents, "Total Incidents"),
            create_metric_card(open_actions, "Open Actions"),
        ]

        # Chart for entity completeness
        # The entity_completeness structure from _analyze_entity_completeness is different.
        # Need to adapt it or query it separately if a detailed chart is required.
        # For now, I'll use a dummy data if entity_completeness is not directly available in expected format.
        if not entity_completeness:
            entity_names = []
            completeness_scores = []
        else:
            entity_names = list(entity_completeness.keys())
            completeness_scores = [
                entity_completeness[e].get("completeness_percentage", 0.0) for e in entity_names
            ]

        entity_completeness_chart = go.Figure(
            data=[
                go.Bar(
                    x=entity_names,
                    y=completeness_scores,
                    marker_color=colors.get("primary_color"),
                )
            ]
        )
        entity_completeness_chart.update_layout(
            **get_chart_layout_template(),
            title_text="Entity Completeness",
            xaxis_title="Entity",
            yaxis_title="Completeness (%)",
            font=get_fonts(),
            paper_bgcolor=colors.get("background_dark"),
            plot_bgcolor=colors.get("background_dark"),
        )

        # Incident status table - adapting to available data
        incident_table_data = [
            {
                "Category": "Total Incidents",
                "Count": total_incidents,
                "Color": colors.get("primary_color"),
            }
        ]
        incident_table = dash_table.DataTable(
            id="incident-status-table",
            columns=[{"name": i, "id": i} for i in incident_table_data[0].keys()],
            data=incident_table_data,
            style_header={
                "backgroundColor": colors.get("primary_color"),
                "color": colors.get("text_light"),
                "fontWeight": "bold",
            },
            style_data={
                "backgroundColor": colors.get("background_light"),
                "color": colors.get("text_primary"),
            },
            style_table={
                "overflowX": "auto",
                "border": f"1px solid {colors.get('border_color')}",
                "borderRadius": "8px",
            },
        )

        # Action status table - currently no direct equivalent in facility_statistics_analysis
        action_table = dash_table.DataTable(
            id="action-status-table",
            columns=[{"name": "Category", "id": "Category"}, {"name": "Count", "id": "Count"}],
            data=[{"Category": "Open Actions", "Count": open_actions}],
            style_header={
                "backgroundColor": colors.get("primary_color"),
                "color": colors.get("text_light"),
                "fontWeight": "bold",
            },
            style_data={
                "backgroundColor": colors.get("background_light"),
                "color": colors.get("text_primary"),
            },
            style_table={
                "overflowX": "auto",
                "border": f"1px solid {colors.get('border_color')}",
                "borderRadius": "8px",
            },
        )

        return create_standard_layout(
            title=f"{facility_name} Detail Analysis",
            content_cards=[
                html.Div(
                    metrics,
                    className="d-flex justify-content-around mb-4",
                    style={
                        "backgroundColor": colors.get("background_dark"),
                        "padding": "20px",
                        "borderRadius": "8px",
                        "color": colors.get("text_light"),
                    },
                ),
                html.Div(
                    [
                        dcc.Graph(id="entity-completeness-chart", figure=entity_completeness_chart),
                        html.Div(
                            [
                                html.H4(
                                    "Incident Status",
                                    className="text-center",
                                    style={"color": colors.get("text_primary")},
                                ),
                                incident_table,
                                html.H4(
                                    "Action Status",
                                    className="text-center mt-4",
                                    style={"color": colors.get("text_primary")},
                                ),
                                action_table,
                            ],
                            className="p-4",
                            style={
                                "backgroundColor": colors.get("background_secondary"),
                                "padding": "20px",
                                "borderRadius": "8px",
                                "color": colors.get("text_primary"),
                            },
                        ),
                    ],
                    className="row",  # This is hardcoded to be row
                    style={
                        "backgroundColor": colors.get("background_dark"),
                        "color": colors.get("text_light"),
                    },
                ),
            ],
        )

    except Exception as e:
        logging.error(f"Error creating facility detail layout for {facility_name}: {e}")
        handle_error_utility(logger, e, f"facility detail layout creation for {facility_name}")
        return html.Div(
            html.P(f"Error loading facility detail for {facility_name}: {e}"),
            className="alert alert-danger",
        )
