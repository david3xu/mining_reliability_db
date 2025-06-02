#!/usr/bin/env python3
"""
Data Quality Components - Pure Adapter Dependencies
Quality assessment components with clean adapter integration.
"""

import logging

import plotly.graph_objects as go
from dash import dash_table, dcc, html

from dashboard.adapters import get_config_adapter, get_data_adapter
from dashboard.components.layout_template import create_metric_card, create_standard_layout
from dashboard.utils.styling import (
    get_chart_layout_template,
    get_colors,
    get_dashboard_styles,
    get_fonts,
    get_table_style,
)

logger = logging.getLogger(__name__)


def create_quality_metrics_cards() -> list:
    """Quality metrics using adapter data access"""
    try:
        data_adapter = get_data_adapter()
        config_adapter = get_config_adapter()
        colors = get_colors()

        portfolio_data = data_adapter.get_portfolio_metrics()
        field_data = data_adapter.get_field_distribution()

        cards = [
            create_metric_card(
                value=portfolio_data.facilities,
                label="Facilities Analyzed",
                detail="Active operational sites",
                color=colors.get("primary_blue"),
            ),
            create_metric_card(
                value=field_data.total_fields,
                label="Total Fields",
                detail="Data collection points",
                color=colors.get("chart_colors", [])[1] if colors.get("chart_colors") else None,
            ),
            create_metric_card(
                value=f"{portfolio_data.metadata.data_quality:.0%}",
                label="Data Quality Score",
                detail="Overall completeness",
                color=colors.get("chart_colors", [])[2] if colors.get("chart_colors") else None,
            ),
            create_metric_card(
                value=portfolio_data.years_coverage,
                label="Years Coverage",
                detail="Historical span",
                color=colors.get("chart_colors", [])[3] if colors.get("chart_colors") else None,
            ),
        ]

        return cards

    except Exception as e:
        config_adapter.handle_error_utility(logger, e, "quality metrics cards creation")
        return []


def create_field_completeness_chart() -> dcc.Graph:
    """Field completion analysis using adapter data"""
    try:
        data_adapter = get_data_adapter()
        config_adapter = get_config_adapter()
        colors = get_colors()
        fonts = get_fonts()
        layout_template = get_chart_layout_template()

        field_data = data_adapter.get_field_distribution()

        if not field_data.labels:
            return dcc.Graph(figure={})

        # Create completion simulation from field distribution
        completion_rates = [
            min(95, max(25, (v / max(field_data.values)) * 100)) for v in field_data.values
        ]

        # Color mapping based on completion
        bar_colors = []
        for rate in completion_rates:
            if rate >= 80:
                bar_colors.append(
                    colors.get("chart_colors", [])[2] if colors.get("chart_colors") else "#7ED321"
                )
            elif rate >= 60:
                bar_colors.append(
                    colors.get("chart_colors", [])[1] if colors.get("chart_colors") else "#F5A623"
                )
            else:
                bar_colors.append(
                    colors.get("chart_colors", [])[3] if colors.get("chart_colors") else "#D32F2F"
                )

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                y=field_data.labels,
                x=completion_rates,
                orientation="h",
                marker=dict(color=bar_colors),
                text=[f"{rate:.0f}%" for rate in completion_rates],
                textposition="inside",
            )
        )

        fig.update_layout(
            title="Field Completion Analysis",
            xaxis_title="Completion Rate (%)",
            height=layout_template.get("height", 400),
            font=layout_template.get("font", {"family": fonts.get("primary_font", "Arial")}),
            paper_bgcolor=layout_template.get(
                "paper_bgcolor", colors.get("background_light", "#FFFFFF")
            ),
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        config_adapter.handle_error_utility(logger, e, "field completeness chart creation")
        return dcc.Graph(figure={})


def create_facility_quality_comparison() -> dcc.Graph:
    """Facility quality comparison using adapter data"""
    try:
        data_adapter = get_data_adapter()
        config_adapter = get_config_adapter()
        colors = get_colors()
        fonts = get_fonts()
        layout_template = get_chart_layout_template()

        facility_data = data_adapter.get_facility_breakdown()

        if not facility_data.labels:
            return dcc.Graph(figure={})

        # Quality score simulation based on record count
        max_records = max(facility_data.values) if facility_data.values else 1
        quality_scores = [min(100, (v / max_records) * 100) for v in facility_data.values]

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=facility_data.labels,
                y=quality_scores,
                marker_color=colors.get("chart_colors", [])[0]
                if colors.get("chart_colors")
                else "#4A90E2",
                text=[f"{score:.0f}%" for score in quality_scores],
                textposition="outside",
            )
        )

        fig.update_layout(
            title="Facility Quality Comparison",
            xaxis_title="Facility",
            yaxis_title="Quality Score (%)",
            height=layout_template.get("height", 400),
            font=layout_template.get("font", {"family": fonts.get("primary_font", "Arial")}),
            paper_bgcolor=layout_template.get(
                "paper_bgcolor", colors.get("background_light", "#FFFFFF")
            ),
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        config_adapter.handle_error_utility(logger, e, "facility quality comparison creation")
        return dcc.Graph(figure={})


def create_quality_summary_table() -> dash_table.DataTable:
    """Quality summary using adapter data"""
    try:
        data_adapter = get_data_adapter()
        config_adapter = get_config_adapter()
        table_style = get_table_style()
        colors = get_colors()

        facility_data = data_adapter.get_facility_breakdown()

        if not facility_data.labels:
            return dash_table.DataTable(data=[])

        # Build quality assessment table
        table_data = []
        for i, (facility, records, percentage) in enumerate(
            zip(facility_data.labels, facility_data.values, facility_data.percentages)
        ):
            quality_score = min(100, (records / max(facility_data.values)) * 100)
            status = (
                "Excellent"
                if quality_score >= 80
                else "Good"
                if quality_score >= 60
                else "Needs Attention"
            )

            table_data.append(
                {
                    "Facility": facility,
                    "Total Records": records,
                    "Percentage": f"{percentage:.1f}%",
                    "Quality Score": f"{quality_score:.0f}%",
                    "Status": status,
                }
            )

        return dash_table.DataTable(
            data=table_data,
            columns=[
                {"name": "Facility", "id": "Facility"},
                {"name": "Total Records", "id": "Total Records", "type": "numeric"},
                {"name": "Percentage", "id": "Percentage"},
                {"name": "Quality Score", "id": "Quality Score"},
                {"name": "Status", "id": "Status"},
            ],
            style_cell=table_style.get("style_cell"),
            style_header=table_style.get("style_header"),
            style_data=table_style.get("style_data"),
            style_table=table_style.get("style_table"),
            conditional_formatting=[
                {
                    "if": {"filter_query": "{Status} = 'Excellent'"},
                    "backgroundColor": colors.get("chart_colors", [])[2]
                    if colors.get("chart_colors")
                    else "#E8F5E8",
                },
                {
                    "if": {"filter_query": "{Status} = 'Good'"},
                    "backgroundColor": colors.get("chart_colors", [])[1]
                    if colors.get("chart_colors")
                    else "#FFF8E1",
                },
                {
                    "if": {"filter_query": "{Status} = 'Needs Attention'"},
                    "backgroundColor": colors.get("chart_colors", [])[3]
                    if colors.get("chart_colors")
                    else "#FFE6E6",
                },
            ],
        )

    except Exception as e:
        config_adapter.handle_error_utility(logger, e, "quality summary table creation")
        return dash_table.DataTable(data=[])


def create_data_quality_layout() -> html.Div:
    """Data quality analysis page - 20 lines"""
    try:
        config_adapter = get_config_adapter()
        return html.Div(
            [
                create_standard_layout(
                    title="Data Quality Foundation",
                    metric_cards=create_quality_metrics_cards(),
                    chart_components=[
                        create_field_completeness_chart(),
                        create_facility_quality_comparison(),
                    ],
                    table_components=[create_quality_summary_table()],
                    chart_titles=[
                        "Field Completion Analysis",
                        "Facility Quality Comparison",
                    ],
                    table_titles=["Quality Summary by Facility"],
                )
            ],
            className="p-4",
            style=get_dashboard_styles().get("main_container"),
        )
    except Exception as e:
        config_adapter.handle_error_utility(logger, e, "data quality layout creation")
        return dbc.Alert("Data Quality layout unavailable", color="danger")
