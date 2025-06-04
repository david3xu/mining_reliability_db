#!/usr/bin/env python3
"""
Data Quality Components - Pure Adapter Dependencies
Quality assessment components with clean adapter integration.
"""

import logging
from typing import Dict, List, Tuple

import plotly.graph_objects as go
from dash import dash_table, dcc, html

from dashboard.adapters import get_data_adapter, get_workflow_adapter, handle_error_utility
from dashboard.components.layout_template import create_standard_layout
from dashboard.utils.styling import get_colors

logger = logging.getLogger(__name__)


def create_data_quality_layout() -> html.Div:
    """Simple 41-field completion focus with ActionRequest facility statistics"""
    try:
        # Get colors configuration
        colors = get_colors()

        return create_standard_layout(
            title="Data Quality Foundation",
            content_cards=[
                create_41_field_completion_analysis(),
                create_action_request_facility_table(),
            ],
        )
    except Exception as e:
        handle_error_utility(logger, e, "data quality layout creation")
        return html.Div("Data quality page unavailable")


def create_41_field_completion_analysis() -> html.Div:
    """Direct 41 raw field completion analysis"""
    try:
        data_adapter = get_data_adapter()
        colors = get_colors()

        # Get raw field completion rates
        field_completion_data = data_adapter.get_41_raw_field_completion_rates()

        logger.info(
            f"Field completion data received in component: {len(field_completion_data)} fields"
        )
        logger.info(f"Sample data in component: {list(field_completion_data.items())[:5]}")

        if not field_completion_data:
            return html.Div("No field completion data available")

        # Separate 100% complete from incomplete fields
        complete_fields = []
        incomplete_fields = []

        for raw_field_name, completion_rate in field_completion_data.items():
            if completion_rate >= 99.9:
                complete_fields.append(raw_field_name)
            else:
                incomplete_fields.append((raw_field_name, completion_rate))

        # Sort incomplete by completion rate (lowest first)
        incomplete_fields.sort(key=lambda x: x[1])

        # Create 100% complete fields display
        complete_section = (
            html.Div(
                [
                    html.H5(
                        f"100% Complete Fields ({len(complete_fields)} fields):",
                        style={"color": colors.get("success_color"), "marginBottom": "10px"},
                    ),
                    html.P(
                        ", ".join(complete_fields),
                        style={
                            "backgroundColor": colors.get("success_color"),
                            "color": colors.get("text_light"),
                            "padding": "10px",
                            "borderRadius": "5px",
                        },
                    ),
                ]
            )
            if complete_fields
            else html.Div()
        )

        # Create incomplete fields chart
        incomplete_chart = create_raw_field_completion_chart(incomplete_fields)

        return html.Div(
            [
                html.H3("Field Completeness Analysis (41 Fields)", className="mb-4"),
                complete_section,
                html.H5(
                    f"Field Completion Rates (Excluding 100% Complete Fields)",
                    className="mt-4 mb-3",
                ),
                incomplete_chart,
            ]
        )

    except Exception as e:
        handle_error_utility(logger, e, "41-field completion analysis")
        return html.Div("Field completion analysis unavailable")


def create_raw_field_completion_chart(
    incomplete_fields: List[Tuple[str, float]],
) -> dcc.Graph:
    """Chart using exact raw field names from field_mappings.json"""
    colors = get_colors()
    if not incomplete_fields:
        return html.P("All fields are 100% complete!", style={"color": colors.get("success_color")})

    raw_field_names = [field[0] for field in incomplete_fields]
    completion_rates = [field[1] for field in incomplete_fields]

    # Color coding
    colors_list = []
    for rate in completion_rates:
        if rate >= 80:
            colors_list.append(colors.get("success_color"))  # Green
        elif rate >= 60:
            colors_list.append(colors.get("warning_color"))  # Orange
        else:
            colors_list.append(colors.get("error_color"))  # Red

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=raw_field_names,
            x=completion_rates,
            orientation="h",
            marker=dict(color=colors_list),
            text=[f"{rate:.1f}%" for rate in completion_rates],
            textposition="inside",
        )
    )

    fig.update_layout(
        title="Raw Field Completion Rates from field_mappings.json",
        xaxis_title="Completion Rate (%)",
        height=max(400, len(raw_field_names) * 20),
        font={"family": "Arial", "size": 10},
        paper_bgcolor=colors.get("background_dark"),
        plot_bgcolor=colors.get("background_dark"),
        font_color=colors.get("text_light"),
    )

    return dcc.Graph(figure=fig)


def create_action_request_facility_table() -> html.Div:
    """ActionRequest facility statistics table component"""
    try:
        data_adapter = get_data_adapter()
        colors = get_colors()

        # Get ActionRequest facility summary data
        facility_summary = data_adapter.get_action_request_facility_summary()

        facility_statistics = facility_summary.get("facility_statistics", [])
        summary_totals = facility_summary.get("summary_totals", {})
        metadata = facility_summary.get("metadata", {})

        if not facility_statistics:
            return html.Div(
                [
                    html.H4("ActionRequest Facility Statistics", className="mb-3"),
                    html.P(
                        "No ActionRequest facility data available",
                        style={"color": colors.get("warning_color"), "fontStyle": "italic"},
                    ),
                ]
            )

        # Prepare table data
        table_data = []
        for facility in facility_statistics:
            table_data.append(
                {
                    "Facility ID": facility.get("facility_id", "Unknown"),
                    "Total Records": facility.get("total_records", 0),
                    "Unique Actions": facility.get("unique_actions", 0),
                    "Records/Action": facility.get("records_per_action", 0.0),
                    "Max Records/Action": facility.get("max_records_per_action", 0),
                }
            )

        # Create summary cards
        summary_cards = html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            "Total Records",
                            style={"color": colors.get("success_color"), "margin": "0"},
                        ),
                        html.H4(
                            f"{summary_totals.get('total_records', 0):,}",
                            style={"color": colors.get("text_light"), "margin": "5px 0"},
                        ),
                    ],
                    className="col-md-4",
                    style={
                        "textAlign": "center",
                        "padding": "15px",
                        "backgroundColor": colors.get("background_secondary"),
                        "borderRadius": "5px",
                        "margin": "5px",
                    },
                ),
                html.Div(
                    [
                        html.H6(
                            "Unique Actions",
                            style={"color": colors.get("warning_color"), "margin": "0"},
                        ),
                        html.H4(
                            f"{summary_totals.get('total_unique_actions', 0):,}",
                            style={"color": colors.get("text_light"), "margin": "5px 0"},
                        ),
                    ],
                    className="col-md-4",
                    style={
                        "textAlign": "center",
                        "padding": "15px",
                        "backgroundColor": colors.get("background_secondary"),
                        "borderRadius": "5px",
                        "margin": "5px",
                    },
                ),
                html.Div(
                    [
                        html.H6(
                            "Records/Action",
                            style={"color": colors.get("info_color"), "margin": "0"},
                        ),
                        html.H4(
                            f"{summary_totals.get('records_per_action', 0):.1f}",
                            style={"color": colors.get("text_light"), "margin": "5px 0"},
                        ),
                    ],
                    className="col-md-4",
                    style={
                        "textAlign": "center",
                        "padding": "15px",
                        "backgroundColor": colors.get("background_secondary"),
                        "borderRadius": "5px",
                        "margin": "5px",
                    },
                ),
                html.Div(
                    [
                        html.H6(
                            "Max Records/Action",
                            style={"color": colors.get("error_color"), "margin": "0"},
                        ),
                        html.H4(
                            f"{summary_totals.get('max_records_per_action', 0):,}",
                            style={"color": colors.get("text_light"), "margin": "5px 0"},
                        ),
                    ],
                    className="col-md-4",
                    style={
                        "textAlign": "center",
                        "padding": "15px",
                        "backgroundColor": colors.get("background_secondary"),
                        "borderRadius": "5px",
                        "margin": "5px",
                    },
                ),
            ],
            className="row justify-content-center mb-4",
        )

        # Prepare table columns with custom styling
        table_columns = [
            {
                "name": "Facility ID",
                "id": "Facility ID",
                "type": "text",
                "presentation": "markdown",
            },
            {"name": "Total Records", "id": "Total Records", "type": "numeric"},
            {"name": "Unique Actions", "id": "Unique Actions", "type": "numeric"},
            {
                "name": "Records/Action",
                "id": "Records/Action",
                "type": "numeric",
                "format": {"specifier": ".1f"},
            },
            {
                "name": "Max Records/Action",
                "id": "Max Records/Action",
                "type": "numeric",
            },
        ]

        # Conditional formatting for the table
        conditional_formatting = [
            {
                "if": {"column_id": "Records/Action", "filter_query": "{Records/Action} > 10"},
                "backgroundColor": colors.get("error_color"),
                "color": colors.get("text_light"),
            },
            {
                "if": {"column_id": "Records/Action", "filter_query": "{Records/Action} > 5"},
                "backgroundColor": colors.get("warning_color"),
                "color": colors.get("text_primary"),
            },
            {
                "if": {"column_id": "Records/Action", "filter_query": "{Records/Action} <= 5"},
                "backgroundColor": colors.get("success_color"),
                "color": colors.get("text_light"),
            },
        ]

        return html.Div(
            [
                html.H4(
                    "ActionRequest Facility Statistics (Click Facility ID for Detail)",
                    className="mb-3",
                    style={"color": colors.get("text_primary")},
                ),
                summary_cards,
                dash_table.DataTable(
                    id="facility-records-table",
                    columns=table_columns,
                    data=table_data,
                    sort_action="native",
                    page_action="native",
                    page_size=10,
                    style_header={
                        "backgroundColor": colors.get("background_dark"),
                        "color": colors.get("text_light"),
                        "fontWeight": "bold",
                        "border": f"1px solid {colors.get('border_color')}",
                    },
                    style_data_conditional=conditional_formatting
                    + [
                        {
                            "if": {"row_index": "odd"},
                            "backgroundColor": colors.get("background_secondary"),
                            "color": colors.get("text_primary"),
                        },
                        {
                            "if": {"row_index": "even"},
                            "backgroundColor": colors.get("background_light"),
                            "color": colors.get("text_primary"),
                        },
                    ],
                    style_cell={
                        "textAlign": "center",
                        "padding": "12px",
                        "fontSize": "14px",
                        "border": f"1px solid {colors.get('border_light')}",
                        "backgroundColor": colors.get("background_light"),
                        "color": colors.get("text_primary"),
                    },
                    style_table={
                        "overflowX": "auto",
                        "border": f"1px solid {colors.get('border_color')}",
                        "borderRadius": "8px",
                    },
                    cell_selectable=True,
                    active_cell=None,
                ),
            ]
        )

    except Exception as e:
        handle_error_utility(logger, e, "ActionRequest facility table")
        return html.Div("Facility statistics unavailable")
