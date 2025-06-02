#!/usr/bin/env python3
"""
Data Quality Components - Pure Adapter Dependencies
Quality assessment components with clean adapter integration.
"""

import logging
from typing import Dict, List, Tuple

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

from dashboard.adapters import get_data_adapter, get_workflow_adapter, handle_error_utility
from dashboard.components.layout_template import create_standard_layout
from dashboard.utils.styling import get_colors

logger = logging.getLogger(__name__)


def create_data_quality_layout() -> html.Div:
    """Simple 41-field completion focus"""
    try:
        return create_standard_layout(
            title="Data Quality Foundation", content_cards=[create_41_field_completion_analysis()]
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
                        style={"color": "#7ED321", "marginBottom": "10px"},
                    ),
                    html.P(
                        ", ".join(complete_fields),
                        style={
                            "backgroundColor": "#7ED321",
                            "color": "white",
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


def create_raw_field_completion_chart(incomplete_fields: List[Tuple[str, float]]) -> dcc.Graph:
    """Chart using exact raw field names from field_mappings.json"""
    if not incomplete_fields:
        return html.P("All fields are 100% complete!", style={"color": "#7ED321"})

    raw_field_names = [field[0] for field in incomplete_fields]
    completion_rates = [field[1] for field in incomplete_fields]

    # Color coding
    colors_list = []
    for rate in completion_rates:
        if rate >= 80:
            colors_list.append("#7ED321")  # Green
        elif rate >= 60:
            colors_list.append("#F5A623")  # Orange
        else:
            colors_list.append("#D32F2F")  # Red

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
        paper_bgcolor="#2F2F2F",
        plot_bgcolor="#2F2F2F",
        font_color="white",
    )

    return dcc.Graph(figure=fig)
